import unittest2
from app import app


class TagListTestCase(unittest2.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.page = {'url': 'https://google.com'}

    def test_api_get_all_pages(self):
        res = self.client().post('/tags/', data=self.page)
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/tags/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('https://google.com', str(res.data))
