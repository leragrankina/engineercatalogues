from django.conf.urls import url

from .views import ArticleList, ArticleDetail, save_comment, CommentDelete, update_comment

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)$', ArticleDetail.as_view(), name="detail"),
    url(r'^(?P<pk>[0-9]+)/comment$', save_comment, name='add_comment'),
    url(r'^comment/(?P<pk>[0-9]+)/delete$', CommentDelete.as_view(), name='delete_comment'),
    url(r'^comment/(?P<pk>[0-9]+)/update', update_comment, name='update_comment')
]