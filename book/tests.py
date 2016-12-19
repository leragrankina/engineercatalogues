from django.test import TestCase
from django.core import urlresolvers
from django.urls import reverse, reverse_lazy

from .views import BookView


class TestBook(TestCase):
    def test_book_view(self):
        found_view = urlresolvers.resolve('/book/')
        self.assertEqual(found_view.func.__name__, BookView.as_view().__name__)

    def test_book_template(self):
        response = self.client.get(reverse_lazy('book:index'))
        self.assertTemplateUsed(response, 'book/index.html')

    def test_book_cover(self):
        response = self.client.get(reverse('book:index')).content.decode('UTF-8')
        self.assertIn('<img src="media/book_cover.jpg"', response)
