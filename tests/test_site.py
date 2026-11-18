"""Focused acceptance checks for the static academic site."""
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.elements = []
        self.text = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class AcademicSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / 'build.py')], check=True)

    def test_terse_homepage_has_accessible_academic_navigation(self):
        page = Document(ROOT / 'index.html')
        self.assertTrue(any(tag == 'nav' and attrs.get('aria-label') == 'Primary'
                            for tag, attrs in page.elements))
        self.assertTrue(any(tag == 'link' and attrs.get('href') == 'styles/academic.css'
                            for tag, attrs in page.elements))
        self.assertTrue(any(tag == 'img' and attrs.get('width') == '150'
                            and attrs.get('alt') == 'Colin Henry'
                            for tag, attrs in page.elements))
        self.assertFalse(any(tag == 'script' for tag, _ in page.elements))
        self.assertLess(len(' '.join(page.text).split()), 150)
    def test_sections_preserve_existing_content_and_local_links(self):
        from urllib.parse import unquote, urlsplit
        import yaml

        pages = ['index.html', 'publications.html', 'projects.html',
                 'teaching.html', 'contact.html']
        for filename in pages:
            with self.subTest(page=filename):
                self.assertTrue((ROOT / filename).is_file(), filename)
                page = Document(ROOT / filename)
                current = [attrs for _, attrs in page.elements
                           if attrs.get('aria-current') == 'page']
                self.assertEqual(len(current), 1)
                self.assertEqual(current[0]['href'], filename)
                self.assertFalse(any(tag == 'script' for tag, _ in page.elements))
                for tag, attrs in page.elements:
                    for attr in ('href', 'src'):
                        value = attrs.get(attr)
                        if not value:
                            continue
                        url = urlsplit(value)
                        if url.scheme or url.netloc:
                            continue
                        target = ROOT / unquote(url.path or filename)
                        self.assertTrue(target.exists(), value)
                        if url.fragment and target.suffix == '.html':
                            doc = Document(target)
                            self.assertIn(url.fragment, [a.get('id') for _, a in doc.elements])

        publications = ' '.join(Document(ROOT / 'publications.html').text)
        for paper in yaml.safe_load((ROOT / 'data/papers.yaml').read_text()):
            self.assertIn(paper['title'], publications)
        projects = Document(ROOT / 'projects.html')
        for project in yaml.safe_load((ROOT / 'data/projects.yaml').read_text()):
            self.assertIn('proj-' + project['slug'], [a.get('id') for _, a in projects.elements])
        teaching = (ROOT / 'teaching.html').read_text()
        self.assertIn('course/ai-research-tool/', teaching)
        self.assertIn('workshop/', teaching)

    def test_build_is_reproducible(self):
        pages = ['index.html', 'publications.html', 'projects.html',
                 'teaching.html', 'contact.html']
        before = {name: (ROOT / name).read_bytes() for name in pages if (ROOT / name).exists()}
        subprocess.run([sys.executable, str(ROOT / 'build.py')], check=True)
        after = {name: (ROOT / name).read_bytes() for name in pages if (ROOT / name).exists()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
