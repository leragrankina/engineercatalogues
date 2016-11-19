from main.models import Article
from django.test import LiveServerTestCase
from selenium import webdriver
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.first_article = Article(text='First ever article', title='First Article', url='first-article')
        self.first_article.save()
        self.second_article = Article(text='Second article', title='Second Article', url='second-article')
        self.second_article.save()

    def tearDown(self):
        self.browser.quit()

    def assertHomePage(self):
        self.assertIn('Статьи и каталоги', self.browser.title)

    def clickHomePage(self):
        self.browser.find_element_by_id("home_link").click()

    def test_site_navigation(self):
        self.browser.get(self.live_server_url)
        self.assertHomePage()

        #Andrew wants to see the 'Articles' page
        self.browser.find_element_by_id("articles_list_link").click()
        time.sleep(1)
        self.assertIn('Статьи "В помощь конструктору"', self.browser.title)

        #He sees a list of titles
        articles = self.browser.find_elements_by_tag_name("tr")
        self.assertEqual(len(articles), 2)
        self.assertIn('First Article', articles[0].text)

        #He wants to know when first article was written
        first_article = articles[0]
        cells = first_article.find_elements_by_tag_name('td')
        second_cell = cells[1].text
        self.assertRegex(second_cell, '\d{2} [A-zА-я]+, \d{4}')

        #He clicks the title of an article and redirects to a page with url as title
        first_article.find_element_by_tag_name('a').click()
        time.sleep(1)
        self.assertRegex(self.browser.current_url, 'first-article')

        #He reads the article's text
        self.assertIn(self.first_article.text, self.browser.find_element_by_tag_name('body').text)
