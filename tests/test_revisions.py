"""Acceptance checks for the requested publication, project, and course revisions."""
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ContentRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / 'build.py')], check=True)

    def test_feezell_project_replaces_platform_abm(self):
        projects = yaml.safe_load((ROOT / 'data/projects.yaml').read_text())
        self.assertNotIn('platform-abm', [p['slug'] for p in projects])
        project = next((p for p in projects if p['slug'] == 'feezell-socialization'), None)
        self.assertIsNotNone(project, 'Feezell socialization project is missing')
        assert project is not None
        self.assertEqual(project['name'], 'Online War Exposure')
        self.assertEqual(project['role'], 'Principal investigator')
        self.assertIn('Jessica Feezell', project['collaborators'])
        for phrase in ['survey experiments', 'data-donation', 'SNSF Scientific Exchange',
                       'Institute of Political Science']:
            self.assertIn(phrase, project['summary'])
        rendered = (ROOT / 'projects.html').read_text()
        self.assertIn('Online War Exposure', rendered)
        self.assertNotIn('Platform ABM', rendered)

    def test_course_shared_design_preserves_each_page(self):
        import hashlib
        import json
        from urllib.parse import unquote, urlsplit
        from bs4 import BeautifulSoup

        inventory = json.loads((ROOT / 'tests/fixtures/course-inventory.json').read_text())
        course = ROOT / 'course/ai-research-tool'
        self.assertEqual(set(inventory), {p.name for p in course.glob('*.html')})
        for filename, expected in inventory.items():
            with self.subTest(page=filename):
                source = (course / filename).read_text()
                soup = BeautifulSoup(source, 'html.parser')
                self.assertIsNotNone(soup.select_one('link[href="../../styles/academic.css"]'))
                self.assertIsNotNone(soup.select_one('link[href="../../styles/course.css"]'))
                self.assertFalse(soup.select('script, [style], link[rel="preconnect"]'))
                body = soup.select_one('.course-content')
                self.assertIsNotNone(body)
                assert body is not None
                text = ' '.join(body.get_text(' ', strip=True).split())
                self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), expected['content_sha256'])
                self.assertEqual(len(body.select('details')), expected['details'])
                for details in body.select('details'):
                    self.assertIsNotNone(details.find('summary', recursive=False), filename)
                    self.assertGreater(len(details.get_text(' ', strip=True)), 30, filename)
                self.assertEqual([hashlib.sha256(t.get_text().encode()).hexdigest()
                                  for t in body.select('pre')], expected['code_sha256'])
                self.assertEqual(sorted(t['href'] for t in body.select('a[href]')), expected['links'])
                self.assertTrue(set(expected['ids']) <= {str(t['id']) for t in soup.select('[id]')})
                for link in soup.select('a[href]'):
                    url = urlsplit(str(link['href']))
                    if url.scheme or url.netloc:
                        continue
                    target = (course / unquote(url.path)).resolve() if url.path else course / filename
                    self.assertTrue(target.exists(), link['href'])
                    if target.is_dir():
                        target = target / 'index.html'
                    if url.fragment and target.suffix == '.html':
                        other = BeautifulSoup(target.read_text(), 'html.parser')
                        self.assertIsNotNone(other.find(id=unquote(url.fragment)), link['href'])

    def test_full_author_names_and_registered_report_status(self):
        papers = yaml.safe_load((ROOT / 'data/papers.yaml').read_text())
        for paper in papers:
            for author in paper['authors']:
                self.assertGreaterEqual(len(author.split()), 2, author)
                self.assertGreater(len(author.split()[0].rstrip('.')), 1, author)
        article = next(p for p in papers if p['title'].startswith('Indirect Effects'))
        self.assertEqual(article['status'], 'r-and-r')
        self.assertEqual(article['venue'], 'Journal of Politics')
        self.assertEqual(article['note'], 'Stage 1 Registered Report')
        self.assertEqual(article['authors'], ['Colin Henry', 'Giuliano Formisano',
                         'Adiba Mahbub Proma', 'Karsten Donnay', 'Fabrizio Gilardi'])
        # The separately documented Bystander paper is not substituted for this title.
        self.assertIn('A Chatroom Experiment with AI Agents', article['title'])
        self.assertFalse(any('Related' in p.get('note', '') for p in papers))
        rendered = (ROOT / 'publications.html').read_text()
        self.assertIn('Stage 1 Registered Report', rendered)
        self.assertNotIn('Related —', rendered)


if __name__ == '__main__':
    unittest.main()
