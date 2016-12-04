import time

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from articles.models import Article


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.first_article = Article(text='First ever article', title='First Article')
        self.first_article.save()
        self.second_article = Article(text='Second article', title='Second Article')
        self.second_article.save()
        self.user = User.objects.create(username='andrew')
        self.user.set_password('leralera')
        self.user.save()

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

        #He clicks the title of an article
        first_article.find_element_by_tag_name('a').click()
        time.sleep(1)

        #He reads the article's text
        self.assertIn(self.first_article.text, self.browser.find_element_by_tag_name('body').text)

        #He goes back to home page
        self.browser.find_element_by_partial_link_text('Home').click()
        time.sleep(1)
        self.assertHomePage()

        self.browser.find_element_by_id("articles_list_link").click()
        self.browser.find_element_by_partial_link_text('First').click()
        try:
            self.browser.find_element_by_id('comment_input')
            self.fail('Unauthorized users can add comments')
        except NoSuchElementException:
            pass

        #Andrew wants to logg in
        self.browser.find_element_by_partial_link_text('login').click()
        time.sleep(1)
        self.browser.find_element_by_id('id_username').send_keys('andrew')
        self.browser.find_element_by_id('id_password').send_keys('leralera' + Keys.ENTER)

        #He clicks article
        self.browser.find_element_by_id("articles_list_link").click()
        self.browser.find_element_by_partial_link_text('First').click()
        time.sleep(1)

        #He sees an inputbox for comment
        inputbox = self.browser.find_element_by_id('comment_input')

        #He enters a text Good article
        inputbox.send_keys('Good article')
        inputbox.send_keys(Keys.ENTER)
        comments = self.browser.find_elements_by_class_name('comment')
        self.assertTrue('Good article' in list(map(lambda c: c.text, comments)))

        #He again enters text
        inputbox = self.browser.find_element_by_id('comment_input')
        inputbox.send_keys('Really good article')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        comments = self.browser.find_elements_by_class_name('comment')
        comments_texts = list(map(lambda c: c.text, comments))
        self.assertTrue('Really good article' in comments_texts)
        self.assertTrue('Good article' in comments_texts)

        #Comments are displayed only for current article
        self.browser.find_element_by_partial_link_text('Articles').click()
        time.sleep(1)
        self.browser.find_element_by_partial_link_text('Second').click()
        time.sleep(1)
        comments = self.browser.find_elements_by_class_name('comment')
        self.assertEqual(len(comments), 0)

        #Andrew wants to log out
        self.browser.find_element_by_partial_link_text('logout').click()
        time.sleep(1)
        try:
            self.browser.find_element_by_partial_link_text('logout')
            self.fail('User must be logged out')
        except NoSuchElementException:
            pass

        self.fail('Work harder, bitch')
