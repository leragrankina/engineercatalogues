from django.test import TestCase
from selenium import webdriver


class NewVisitorTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_main_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Статьи и каталоги', self.browser.title)

