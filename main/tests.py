from django.test import TestCase
from django.core import urlresolvers
from django.http import HttpRequest
from django.template.loader import render_to_string
from main import views


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


