from django.test import TestCase
from selenium import webdriver
import time


class NewVisitorTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def assertHomePage(self):
        self.assertIn('Статьи и каталоги', self.browser.title)

    def clickHomePage(self):
        self.browser.find_element_by_id("home_link").click()

    def test_site_navigation(self):
        self.browser.get('http://localhost:8000')
        self.assertHomePage()

        #Andrew wants to see the 'Articles' page
        self.browser.find_element_by_id("articles_list_link").click()
        time.sleep(1)
        self.assertIn('Статьи "В помощь конструктору"', self.browser.title)

        #He sees a list of articles
        articles = self.browser.find_elements_by_tag_name("tr")
        self.assertEqual(len(articles), 2)


