from datetime import datetime

from django.test import TestCase
from django.core import urlresolvers
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse

from . import views
from .models import Article, Comment


class IndexPage(TestCase):
    def compare_resolved_to_func(self, url, func):
        found = urlresolvers.resolve(url)
        self.assertEqual(func, found.func)

    def compare_response_to_html(self, function, file):
        request = HttpRequest()
        response = function(request)
        expected_html = render_to_string(file)
        self.assertEqual(response.content.decode('UTF-8'), expected_html)

    def test_root_resolves_to_index(self):
        self.compare_resolved_to_func('/', views.index)

    def test_home_page_returns_correct_view(self):
        self.compare_response_to_html(views.index, 'index.html')

    def test_articles_resolves_to_articles_list(self):
        self.compare_resolved_to_func('/articles', views.articles_list)

    def test_artciles_page_returns_articles(self):
        self.compare_response_to_html(views.articles_list, 'index_articles.html')

    def test_catalogues_resolves_to_catalogues_list(self):
        self.compare_resolved_to_func("/catalogues", views.catalogues_list)

    def test_catalogues_page_returns_catalogues(self):
        self.compare_response_to_html(views.catalogues_list, 'catalog.html')


class ArticleDetailPage(TestCase):
    def setUp(self):
        self.article = Article(text='text', title='title')
        self.article.save()

    def test_article_resolves_to_html(self):
        found = urlresolvers.resolve('/articles/1')
        self.assertEqual(views.article_detail, found.func)

    def test_article_name_maps_to_html(self):
        request = HttpRequest()
        response = views.article_detail(request, self.article.pk).content.decode('UTF-8')
        self.assertIn(self.article.text, response)

    def test_can_save_comment(self):
        request = HttpRequest()
        request.POST['comment_text'] = 'Good article'
        response = views.article_detail(request, self.article.pk).content.decode('UTF-8')
        self.assertIn('Good article', response)

    def test_prints_all_comments_in_db(self):
        request = HttpRequest()
        Comment(text='First comment', article=self.article).save()
        Comment(text='Second comment', article=self.article).save()
        response = views.article_detail(request, self.article.pk).content.decode('UTF-8')
        for text in map(lambda c: c.text, Comment.objects.all()):
            self.assertIn(text, response)


class ArticleListPage(TestCase):
    def setUp(self):
        self.first = Article.objects.create(text='Linear Ball Bearings', title='First Article')
        self.first.save()
        self.second = Article.objects.create(text='Some second article', title='Second Article')
        self.second.save()

    def test_articles_list_page(self):
       request = HttpRequest()
       response = views.articles_list(request).content.decode('UTF-8')

       self.assertNotIn('Linear Ball Bearings', response)
       self.assertNotIn('Some second article', response)

       self.assertIn(datetime.now().date().strftime("%d %B, %Y"), response)
       self.assertIn('First Article', response)
       self.assertIn('Second Article', response)

       article_detail_url = reverse('article', args=[self.first.pk])

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
