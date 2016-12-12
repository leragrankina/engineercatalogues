import time

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from filebrowser.base import FileObject

from articles.models import Article, Comment


class NewVisitorTest(LiveServerTestCase):
    @property
    def comments_count(self):
        return len(self.browser.find_elements_by_class_name('comment'))

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        self.first_article = Article(text='First ever article', title='First Article')
        self.first_article.cover = FileObject('uploads/bush.jpg')
        self.first_article.save()
        self.second_article = Article(text='Second article', title='Second Article')
        self.second_article.save()

        self.user = User.objects.create(username='other')
        self.user.set_password('other')
        self.user.save()

        self.andrew = User(username='andrew')
        self.andrew.set_password('leralera')
        self.andrew.save()

        self.comment = Comment.objects.create(text='comment not owned by Andrew'
                                              , article=self.first_article
                                              , created_by=self.user)

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
        articles = self.browser.find_elements_by_class_name("thumbnail")
        self.assertEqual(len(articles), 2)
        self.assertIn('First Article', articles[0].text)
        img = articles[0].find_element_by_tag_name('img')
        self.browser.execute_script('return arguments[0].complete && \
        typeof arguments[0].naturalWidth != "undefined" && \
        arguments[0].naturalWidth > 0', img)

        #He wants to know when first article was written
        first_article = articles[0]
        cells = first_article.find_elements_by_tag_name('td')
        second_cell = articles[1].text
        self.assertRegex(second_cell, '\d{2} [A-zА-я]+, \d{4}')

        #He clicks the title of an article
        first_article.find_element_by_tag_name('a').click()
        time.sleep(1)

        #He reads the article's text
        self.assertIn(self.first_article.text, self.browser.find_element_by_tag_name('body').text)

        #He goes back to home page
        self.browser.find_element_by_partial_link_text('Главная').click()
        time.sleep(1)
        self.assertHomePage()

        self.browser.find_element_by_id("articles_list_link").click()
        self.browser.find_element_by_partial_link_text('First').click()
        try:
            self.browser.find_element_by_id('comment_input')
            self.fail('Unauthorized users can add comments')
        except NoSuchElementException:
            pass

        #Andrew wants to log in
        #self.browser.find_element_by_partial_link_text('login').click()
        #time.sleep(1)
        self.browser.find_element_by_id('id_username').send_keys('andrew')
        self.browser.find_element_by_id('id_password').send_keys('leralera' + Keys.ENTER)

        #He clicks article
        self.browser.find_element_by_id("articles_list_link").click()
        time.sleep(0.5)
        self.browser.find_element_by_partial_link_text('First').click()
        time.sleep(1)

        #He sees an inputbox for comment
        inputbox = self.browser.find_element_by_id('comment_input')

        #He enters a text Good article
        inputbox.send_keys('Good article')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        comment = self.browser.find_elements_by_class_name('comment')[-1].get_attribute('innerHTML')
        self.assertIn('Good article', comment)


        #He again enters text
        inputbox = self.browser.find_element_by_id('comment_input')
        inputbox.send_keys('Really good article')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        comments = self.browser.find_elements_by_class_name('comment')
        self.assertIn('Really good article', self.browser.find_element_by_tag_name('body').get_attribute('innerHTML'))
        self.assertIn('Good article', self.browser.find_element_by_tag_name('body').get_attribute('innerHTML'))

        #Andrew wants to delete a comment
        self.browser.find_element_by_partial_link_text('Articles').click()
        self.browser.find_element_by_partial_link_text('First').click()
        time.sleep(0.5)
        old_count = self.comments_count
        self.browser.find_element_by_css_selector('input[value="delete"]').click()
        time.sleep(1)
        new_count = self.comments_count
        self.assertEqual(new_count, old_count - 1)

        #He cannot delete a comment not posted by himself
        comment_div = self.browser.find_elements_by_class_name('comment')[0]
        try:
            comment_div.find_element_by_partial_link_text('delete')
            self.fail('Andrew can delete not his comment')
        except NoSuchElementException:
            pass

        #Andrew wants to update a comment
        comment = self.browser.find_elements_by_class_name('comment')[1]
        comment.find_element_by_id('comment_update').send_keys('\nUPD: updated' + Keys.ENTER)
        time.sleep(0.5)
        comment = self.browser.find_elements_by_class_name('comment')[1]
        self.assertIn('UPD', comment.get_attribute('innerHTML'))

        #Comments are displayed only for current article
        self.browser.find_element_by_partial_link_text('Статьи').click()
        self.browser.find_element_by_partial_link_text('Second').click()
        time.sleep(1)
        self.assertEqual(self.comments_count, 0)

        #Andrew wants to log out
        self.browser.find_element_by_partial_link_text('Выйти').click()
        time.sleep(1)
        try:
            self.browser.find_element_by_partial_link_text('Выйти')
            self.fail('User must be logged out')
        except NoSuchElementException:
            pass

        #Andrew wants to see a Book tab
        self.browser.find_element_by_partial_link_text('Книга').click()

        #He sees a book cover
        self.browser.find_element_by_tag_name('img')

        self.fail('Work harder, bitch')

