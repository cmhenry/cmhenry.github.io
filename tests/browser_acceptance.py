"""Real-Chromium checks via a task-owned loopback CDP endpoint.

Run after build.py, with websockets installed in the test interpreter:
    python tests/browser_acceptance.py --port 9234 --include-course --base-url http://127.0.0.1:8766/
The script does not launch a browser, expose a server, or modify the site.
"""
import argparse
import asyncio
import base64
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

import websockets

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'publications.html', 'projects.html', 'teaching.html', 'contact.html']
COURSE = 'course/ai-research-tool/'


async def verify(port, pages, base_url=None):
    def page_url(page):
        return urljoin(base_url, page) if base_url else (ROOT / page).as_uri()
    out = ROOT / '.hermes' / 'verification'
    out.mkdir(parents=True, exist_ok=True)
    with urlopen(f'http://127.0.0.1:{port}/json/version', timeout=5) as response:
        endpoint = json.load(response)['webSocketDebuggerUrl']
    async with websockets.connect(endpoint, max_size=20_000_000) as ws:
        sequence = 0
        errors = []

        async def call(method, params=None, session=None):
            nonlocal sequence
            sequence += 1
            request_id = sequence
            request = {'id': request_id, 'method': method, 'params': params or {}}
            if session:
                request['sessionId'] = session
            await ws.send(json.dumps(request))
            while True:
                message = json.loads(await asyncio.wait_for(ws.recv(), timeout=20))
                if message.get('method') == 'Runtime.exceptionThrown':
                    errors.append(message['params'])
                if message.get('id') == request_id:
                    if 'error' in message:
                        raise RuntimeError(message['error'])
                    return message.get('result', {})

        context = (await call('Target.createBrowserContext', {'disposeOnDetach': True}))['browserContextId']
        try:
            target = (await call('Target.createTarget', {'url': 'about:blank', 'browserContextId': context}))['targetId']
            session = (await call('Target.attachToTarget', {'targetId': target, 'flatten': True}))['sessionId']
            await call('Page.enable', session=session)
            await call('Runtime.enable', session=session)

            async def evaluate(expression):
                result = await call('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True, 'userGesture': True}, session)
                if 'exceptionDetails' in result:
                    raise RuntimeError(result['exceptionDetails'])
                return result['result'].get('value')

            async def loaded(url):
                for _ in range(100):
                    if await evaluate(f'location.href === {json.dumps(url)} && document.readyState === "complete"'):
                        await evaluate('document.fonts.ready.then(() => true)')
                        return
                    await asyncio.sleep(0.05)
                raise RuntimeError(f'Navigation did not complete: {url}')

            async def mobile_menu(open_menu):
                await evaluate('''(() => {
                    const menu = document.querySelector('.course-mobile');
                    if (menu && getComputedStyle(menu).display !== 'none' && menu.open !== OPEN) menu.querySelector('summary').click();
                })()'''.replace('OPEN', 'true' if open_menu else 'false'))
                await evaluate('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')

            results = []
            for width, height in [(1280, 900), (768, 1024), (390, 844), (320, 800)]:
                await call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height, 'deviceScaleFactor': 1, 'mobile': False}, session)
                for page in pages:
                    url = page_url(page)
                    await call('Page.navigate', {'url': url}, session)
                    await loaded(url)
                    await mobile_menu(True)
                    state = await evaluate('''(() => {
                        const visible = e => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
                        return {
                            width: innerWidth,
                            scrollWidth: document.documentElement.scrollWidth,
                            current: [...document.querySelectorAll('[aria-current="page"]')].filter(visible).map(a => a.getAttribute('href')),
                            imagesLoaded: [...document.images].every(i => i.complete && i.naturalWidth > 0),
                            stylesheetLoaded: [...document.styleSheets].some(s => s.href && s.href.endsWith('academic.css')),
                            navMinHeight: Math.min(...[...document.querySelectorAll('nav a')].filter(visible).map(a => a.getBoundingClientRect().height)),
                            scripts: document.scripts.length
                        };
                    })()''')
                    assert state['scrollWidth'] <= width, (page, state)
                    assert state['current'] == [Path(page).name], (page, state)
                    assert state['imagesLoaded'] and state['stylesheetLoaded'], (page, state)
                    assert state['scripts'] == 0, (page, state)
                    if width <= 600:
                        assert state['navMinHeight'] >= 44, (page, state)
                    await mobile_menu(False)
                    answer = await evaluate('''(() => {
                        const keys = [...document.querySelectorAll('.course-content details')];
                        if (!keys.length) return null;
                        const passed = keys.every(details => {
                            details.querySelector('summary').click();
                            const opened = details.open;
                            details.querySelector('summary').click();
                            return opened && !details.open;
                        });
                        return {passed, count: keys.length};
                    })()''')
                    if answer is not None:
                        assert answer['passed'], page
                        state['answer_key_toggles'] = answer['count']
                    if page == 'index.html' or (width in (1280, 390) and (page == 'publications.html' or page in [COURSE + p for p in ['index.html', 'module-01.html', 'module-07.html', 'module-09.html', 'shared.html']])):
                        await evaluate('scrollTo(0, 0)')
                        screenshot = await call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': False}, session)
                        name = page.removesuffix('.html').replace('/', '_')
                        (out / f'{name}-{width}.png').write_bytes(base64.b64decode(screenshot['data']))
                    results.append({'page': page, **state})

            # Click the actual personal-site navigation.
            await call('Page.navigate', {'url': page_url('index.html')}, session)
            await loaded(page_url('index.html'))
            navigation = []
            for page in PAGES:
                await evaluate(f'document.querySelector("nav[aria-label=Primary] a[href=\\"{page}\\"]").click()')
                await loaded(page_url(page))
                navigation.append(page)
            # Enter through Teaching, then exercise every rendered course-menu destination.
            course_pages = [p for p in pages if p.startswith(COURSE)]
            if course_pages:
                await call('Page.navigate', {'url': page_url('teaching.html')}, session)
                await loaded(page_url('teaching.html'))
                await evaluate('document.querySelector("a[href=\\"course/ai-research-tool/\\"]").click()')
                await loaded(page_url(COURSE))
                for page in course_pages:
                    await mobile_menu(True)
                    href = json.dumps(Path(page).name)
                    await evaluate(f'[...document.querySelectorAll("nav[aria-label=Course] a")].find(a => a.getAttribute("href") === {href} && a.getClientRects().length).click()')
                    await loaded(page_url(page))
                    navigation.append(page)
            await call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9}, session)
            await call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9}, session)
            focus = await evaluate('document.activeElement.className')
            assert focus == 'skip-link', focus
            assert not errors, errors
            report = {'checks': results, 'navigation_clicks': navigation, 'keyboard_skip_link': True, 'runtime_errors': errors}
            (out / 'browser-results.json').write_text(json.dumps(report, indent=2))
            print(f"Passed {len(results)} page/viewport checks and {len(navigation)} navigation destinations; no runtime errors.")
            print(f'Screenshots and complete JSON: {out}')
        finally:
            await call('Target.disposeBrowserContext', {'browserContextId': context})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=9234)
    parser.add_argument('--pages', nargs='+', default=PAGES)
    parser.add_argument('--include-course', action='store_true')
    parser.add_argument('--base-url', help='HTTP origin for real directory-index navigation')
    args = parser.parse_args()
    if args.include_course and not args.base_url:
        parser.error('--include-course requires --base-url pointing to a local HTTP server')
    selected = list(args.pages)
    if args.include_course:
        selected += [str(p.relative_to(ROOT)) for p in sorted((ROOT / COURSE).glob('*.html'))]
    asyncio.run(verify(args.port, selected, args.base_url))
