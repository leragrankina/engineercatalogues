from django.test import TestCase
from django.core import urlresolvers
from django.http import HttpRequest
from django.template.loader import render_to_string
from articles import views
from articles.models import Article
from datetime import datetime


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
        self.article = Article(text='text', title='title', url='url')
        self.article.save()

    def test_article_resolves_to_html(self):
        found = urlresolvers.resolve('/articles/url')
        self.assertEqual(views.article_page, found.func)

    def test_article_name_maps_to_html(self):
        request = HttpRequest()
        response = views.article_page(request, self.article.url).content.decode()
        self.assertIn(self.article.text, response)


class ArticleListPage(TestCase):
    def test_articles_list_page(self):
        Article.objects.create(text='Linear Ball Bearings', title='First Article', url='first-article')
        Article.objects.create(text='Some second article', title='Second Article', url='second-article')

        request = HttpRequest()
        response = views.articles_list(request).content.decode('UTF-8')

        self.assertNotIn('Linear Ball Bearings', response)
        self.assertNotIn('Some second article', response)

        self.assertIn(datetime.now().date().strftime("%d %B, %Y"), response)
        self.assertIn('First Article', response)
        self.assertIn('Second Article', response)

        self.assertRegex(response, '<a href=".*first-article*"')


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

    def test_article_title(self):
        article = Article()
        article.title = 'First Article'
        article.save()
        saved_articles = Article.objects.all()
        self.assertEqual(saved_articles[0].title, 'First Article')

    def test_article_url(self):
        article = Article(url='bushes')
        article.save()
        saved_articles = Article.objects.all()
        self.assertEqual(saved_articles[0].url, 'bushes')


