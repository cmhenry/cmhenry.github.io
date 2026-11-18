"""Optional real-Chromium checks via a task-owned loopback CDP endpoint.

Run after build.py, with websockets installed in the test interpreter:
    python tests/browser_acceptance.py --port 9234
The script does not launch a browser, expose a server, or modify the site.
"""
import argparse
import asyncio
import base64
import json
from pathlib import Path
from urllib.request import urlopen

import websockets

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'publications.html', 'projects.html', 'teaching.html', 'contact.html']


async def verify(port, pages):
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
                result = await call('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True}, session)
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

            results = []
            for width, height in [(1280, 900), (768, 1024), (390, 844), (320, 800)]:
                await call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height, 'deviceScaleFactor': 1, 'mobile': False}, session)
                for page in pages:
                    url = (ROOT / page).as_uri()
                    await call('Page.navigate', {'url': url}, session)
                    await loaded(url)
                    state = await evaluate('''(() => ({
                        width: innerWidth,
                        scrollWidth: document.documentElement.scrollWidth,
                        current: [...document.querySelectorAll('[aria-current="page"]')].map(a => a.getAttribute('href')),
                        imagesLoaded: [...document.images].every(i => i.complete && i.naturalWidth > 0),
                        stylesheetLoaded: [...document.styleSheets].some(s => s.href && s.href.endsWith('academic.css')),
                        navMinHeight: Math.min(...[...document.querySelectorAll('nav a')].map(a => a.getBoundingClientRect().height)),
                        scripts: document.scripts.length
                    }))()''')
                    assert state['scrollWidth'] <= width, (page, state)
                    assert state['current'] == [page], (page, state)
                    assert state['imagesLoaded'] and state['stylesheetLoaded'], (page, state)
                    assert state['scripts'] == 0, (page, state)
                    if width <= 600:
                        assert state['navMinHeight'] >= 44, (page, state)
                    if page == 'index.html' or (page == 'publications.html' and width in (1280, 390)):
                        screenshot = await call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': False}, session)
                        (out / f'{Path(page).stem}-{width}.png').write_bytes(base64.b64decode(screenshot['data']))
                    results.append({'page': page, **state})

            # Exercise the actual rendered navigation, not just direct page loads.
            for page in PAGES:
                url = (ROOT / page).as_uri()
                await evaluate(f'document.querySelector("nav[aria-label=Primary] a[href=\\"{page}\\"]").click()')
                await loaded(url)
                assert await evaluate('document.querySelector("[aria-current=page]").getAttribute("href")') == page
            await call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9}, session)
            await call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9}, session)
            focus = await evaluate('document.activeElement.className')
            assert focus == 'skip-link', focus
            assert not errors, errors
            report = {'checks': results, 'navigation_clicks': PAGES, 'keyboard_skip_link': True, 'runtime_errors': errors}
            (out / 'browser-results.json').write_text(json.dumps(report, indent=2))
            print(json.dumps(report, indent=2))
            print(f'Screenshots: {out}')
        finally:
            await call('Target.disposeBrowserContext', {'browserContextId': context})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=9234)
    parser.add_argument('--pages', nargs='+', default=PAGES)
    args = parser.parse_args()
    asyncio.run(verify(args.port, args.pages))
