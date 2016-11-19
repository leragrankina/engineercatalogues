from django.test import TestCase
from django.core import urlresolvers
from django.http import HttpRequest
from django.template.loader import render_to_string
from main import views
from main.models import Article


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

    def test_article_resolves_to_html(self):
        self.compare_resolved_to_func('/articles/bushes', views.article_page)

    def test_article_name_maps_to_html(self):
        request = HttpRequest()
        response = views.article_page(request, 'bushes')
        expected_html = render_to_string('bushes.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_articles_list_page(self):
        Article.objects.create(text='Linear Ball Bearings')
        Article.objects.create(text='Some second article')

        request = HttpRequest()
        response = views.articles_list(request)

        self.assertIn('Linear Ball Bearings', response.content.decode('UTF-8'))
        self.assertIn('Some second article', response.content.decode('UTF-8'))


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


