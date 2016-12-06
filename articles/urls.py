from django.conf.urls import url

from .views import ArticleList, ArticleDetail, save_comment, delete_comment

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)$', ArticleDetail.as_view(), name="detail"),
    url(r'^(?P<pk>[0-9]+)/comment$', save_comment, name='add_comment'),
    url(r'^comment/(?P<pk>[0-9]+)/delete$', delete_comment, name='delete_comment')
]