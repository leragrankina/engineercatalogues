from datetime import datetime

from django.test import TestCase
from django.core import urlresolvers
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

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
        self.assertTemplateUsed(response, 'index.html')

    def test_articles_resolves_to_articles_list(self):
        self.compare_resolved_to_func('/articles/', views.ArticleList.as_view())

    def test_articles_page_returns_articles(self):
        response = self.client.get('/articles/')
        self.assertTemplateUsed(response, 'index_articles.html')


class ArticleDetailPage(TestCase):
    def setUp(self):
        self.article = Article(text='text', title='title')
        self.article.save()

    def test_article_resolves_to_html(self):
        found = urlresolvers.resolve('/articles/1')
        self.assertEqual(views.ArticleDetail.as_view().__name__, found.func.__name__)

    def test_article_name_maps_to_html(self):
        response = self.client.get('/articles/' + str(self.article.pk)).content.decode('UTF-8')
        self.assertIn(self.article.text, response)

    def test_can_save_comment(self):
        request = HttpRequest()
        request.POST['comment_text'] = 'Good article'
        views.save_comment(request, self.article.pk)
        response = self.client.get('/articles/%d'%self.article.id).content.decode('UTF-8')
        self.assertIn('Good article', response)

    def test_prints_all_comments_in_db(self):
        Comment(text='First comment', article=self.article).save()
        Comment(text='Second comment', article=self.article).save()
        response = self.client.get('/articles/' + str(self.article.pk)).content.decode('UTF-8')
        for text in map(lambda c: c.text, Comment.objects.all()):
            self.assertIn(text, response)


class ArticleListPage(TestCase):
    def setUp(self):
        self.first = Article.objects.create(text='Linear Ball Bearings', title='First Article')
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
        self.comment = Comment(text='Good article', article=Article.objects.first())
        self.comment.save()

    def test_comment_text(self):
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.all().first().text, 'Good article')

    def test_article_field(self):
        self.assertEqual(self.comment.article.text, self.article.text)


class TestAuthentification(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('pass')
        self.user.save()

        self.article = Article.objects.create(title='test', text='article text')
        self.article.save()

        self.comment = Comment.objects.create(text='comment', article=self.article)
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
        response = self.client.post(reverse_lazy('accounts:auth_login'), kwargs={'username': 'wrong', 'password': 'wrong'})\
            .content.decode('UTF-8')
        self.assertIn('User not found', response)
