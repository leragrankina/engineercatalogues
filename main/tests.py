from django.test import TestCase
from django.core import urlresolvers
from main import views


class IndexPage(TestCase):
    def test_root_resolves_to_index(self):
        found = urlresolvers.resolve('/')
        self.assertEqual(views.index, found.func)

