from django.conf.urls import url

from .views import articles_list, article_detail

urlpatterns = [
    url(r'^$', articles_list, name='list'),
    url(r'^(?P<article_id>[0-9]+)$', article_detail, name="detail"),
]