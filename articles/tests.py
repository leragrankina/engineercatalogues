from datetime import datetime

from django.test import TestCase
from django.core import urlresolvers
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone

from filebrowser.base import FileObject

from . import views
from .models import Article, Comment


class IndexPage(TestCase):
    def compare_resolved_to_func(self, url, func):
        found = urlresolvers.resolve(url)
        self.assertEqual(func.__name__, found.func.__name__)

    def compare_response_to_html(self, function, file):
        request = HttpRequest()
        response = function(request)
        expected_html = render_to_string(file)
        self.assertEqual(response.content.decode('UTF-8'), expected_html)

    def test_home_page_returns_correct_view(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertTemplateUsed(response, 'articles/index.html')

    def test_articles_resolves_to_articles_list(self):
        self.compare_resolved_to_func('/articles/', views.ArticleList.as_view())

    def test_articles_page_returns_articles(self):
        response = self.client.get('/articles/')
        self.assertTemplateUsed(response, 'articles/index_articles.html')


class ArticleDetailPage(TestCase):
    def setUp(self):
        self.article = Article(text='text', title='title')
        self.article.save()

        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()

        Comment(text='First comment', article=self.article, created_by=self.user).save()
        self.comment = Comment(text='Second comment', article=self.article, created_by=self.user)
        self.comment.save()

        self.client.login(username='test', password='test')

    def test_article_resolves_to_html(self):
        found = urlresolvers.resolve('/articles/1')
        self.assertEqual(views.ArticleDetail.as_view().__name__, found.func.__name__)

    def test_article_name_maps_to_html(self):
        response = self.client.get('/articles/' + str(self.article.pk)).content.decode('UTF-8')
        self.assertIn(self.article.text, response)

    def test_prints_all_comments_in_db(self):
        response = self.client.get('/articles/' + str(self.article.pk)).content.decode('UTF-8')
        for text in map(lambda c: c.text, Comment.objects.all()):
            self.assertIn(text, response)

    def test_comment_contains_author_and_date(self):
        response = self.client.get(reverse('articles:detail', args=(self.article.pk,))).content.decode('UTF-8')
        self.assertIn('test', response)
        self.assertIn(self.comment.datetime_posted.astimezone().strftime("%d %B, %Y %H:%M"), response)


class ArticleListPage(TestCase):
    def setUp(self):
        self.first = Article.objects.create(text='Linear Ball Bearings', title='First Article')
        self.first.cover = FileObject('uploads/bush.jpg')
        self.first.save()
        self.second = Article.objects.create(text='Some second article', title='Second Article')
        self.second.save()

    def test_articles_list_page(self):
        response = self.client.get('/articles/').content.decode('UTF-8')

        self.assertNotIn('Linear Ball Bearings', response)
        self.assertNotIn('Some second article', response)

        self.assertIn(datetime.now().date().strftime("%d %B, %Y"), response)
        self.assertIn('First Article', response)
        self.assertIn('Second Article', response)

        article_detail_url = reverse('articles:detail', args=[self.first.pk])

        self.assertRegex(response, '<a href="%s"'%article_detail_url)

    def test_img_tag(self):
        response = self.client.get('/articles/').content.decode('UTF-8')
        self.assertRegex(response, '<img src=".*bush.*">')


class ArticleModelTests(TestCase):
   def test_saving_and_retrieving_articles(self):
        first_article = Article()
        first_article.text = 'First (ever) article'
        first_article.save()

        second_article = Article()
        second_article.text = 'Second article'
        second_article.save()

        saved_articles = Article.objects.all()
        self.assertEqual(saved_articles.count(), 2)

        first_saved_article = saved_articles[0]
        second_saved_article = saved_articles[1]
        self.assertEqual(first_saved_article.text, 'First (ever) article')
        self.assertEqual(second_saved_article.text, 'Second article')

        self.assertEqual(first_saved_article.date_written, datetime.now().date())
        self.assertEqual(second_saved_article.date_written, datetime.now().date())


class ArticleTest(TestCase):
    def check_article_field(self, field, value):
        Article.objects.create(**{field:value})
        self.assertEqual(getattr(Article.objects.first(), field), value)

    def test_article_title(self):
        self.check_article_field('title', 'First Article')


class CommentTest(TestCase):
    def setUp(self):
        self.article = Article(title='First', text='First article')
        self.article.save()

        self.me = User.objects.create(username='me')
        self.me.set_password('me')
        self.me.save()

        self.other = User.objects.create(username='other')
        self.other.set_password('other')
        self.other.save()

        self.comment = Comment(text='Good article', article=self.article, created_by=self.other)
        self.comment.save()

        self.client.login(username='other', password='other')

    def test_comment_text(self):
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.all().first().text, 'Good article')

    def test_article_field(self):
        self.assertEqual(self.comment.article.text, self.article.text)

    def test_can_delete_comment(self):
        self.client.post(reverse('articles:delete_comment', args=[self.comment.pk]))
        response = self.client.get(reverse('articles:detail', args=[self.article.pk])).content.decode('UTF-8')
        self.assertFalse(self.comment.text in response)

    def test_can_delete_only_my_comment(self):
        self.client.login(username='me', password='me')
        response = self.client.get(reverse('articles:detail', args=[self.article.pk])).content.decode('UTF-8')
        self.assertFalse('delete' in response)

    def test_can_delete_only_with_post(self):
        self.client.get(reverse('articles:delete_comment', args=[self.comment.pk]))
        response = self.client.get(reverse('articles:detail', args=[self.article.pk])).content.decode('UTF-8')
        self.assertTrue(self.comment.text in response)

    def test_can_update_comment(self):
        self.client.post(reverse('articles:update_comment', args=[self.comment.pk]), {'id_text': 'UPD'})
        response = self.client.get(reverse('articles:detail', args=[self.article.pk])).content.decode('UTF-8')
        self.assertTrue('UPD' in response)

    def test_can_update_with_get(self):
        self.client.get(reverse('articles:update_comment', args=[self.comment.pk]), {'id_text': 'UPD'})
        response = self.client.get(reverse('articles:detail', args=[self.article.pk])).content.decode('UTF-8')
        self.assertFalse('UPD' in response)

    def test_cannot_update_anothers_comment(self):
        self.client.login(username='me', password='me')
        self.client.post(reverse('articles:update_comment', args=[self.comment.pk]), {'id_text': 'UPD'})
        response = self.client.get(reverse('articles:detail', args=[self.article.pk])).content.decode('UTF-8')
        self.assertFalse('UPD' in response)

    def test_can_save_comment(self):
        self.client.post(reverse('articles:add_comment', args=[self.article.pk]), {'comment_text': 'Good article'})
        response = self.client.get('/articles/%d' % self.article.id).content.decode('UTF-8')
        self.assertIn('Good article', response)


class TestAuthentification(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('pass')
        self.user.save()

        self.article = Article.objects.create(title='test', text='article text')
        self.article.save()

        self.comment = Comment.objects.create(text='comment', article=self.article, created_by=self.user)
        self.comment.save()

        self.client.login(username='test', password='pass')

    def test_authorized_can_add_comments(self):
        response = self.client.get(reverse('articles:detail', args=[self.article.pk, ])).content.decode('UTF-8')
        self.assertIn('comment_input', response)

    def test_unauthorized_cannot_add_comments(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('articles:detail', args=[self.article.pk, ])).content.decode('UTF-8')
        self.assertNotIn('comment_input', response)

    def test_logout_link(self):
        response = self.client.get(reverse_lazy('index')).content.decode('UTF-8')
        self.client.get()


class TestAuthentification(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('pass')
        self.user.save()

        self.article = Article.objects.create(title='test', text='article text')
        self.article.save()

        self.comment = Comment.objects.create(text='comment', article=self.article, created_by=self.user)
        self.comment.save()

        self.client.login(username='test', password='pass')

    def test_authorized_can_add_comments(self):
        response = self.client.get(reverse_lazy('articles:detail', args=[self.article.pk, ])).content.decode('UTF-8')
        self.assertIn('comment_input', response)

    def test_unauthorized_cannot_add_comments(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('articles:detail', args=[self.article.pk, ])).content.decode('UTF-8')
        self.assertNotIn('comment_input', response)

    def test_logout_link(self):
        response = self.client.get(reverse_lazy('index')).content.decode('UTF-8')
        self.assertIn('logout', response)

    def test_no_such_user(self):
        response = self.client.post(reverse_lazy('auth_login'), kwargs={'username': 'wrong', 'password': 'wrong'})\
            .content.decode('UTF-8')
        self.assertIn('User not found', response)


