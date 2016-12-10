from django.conf.urls import url

from .views import BookView, charge

urlpatterns = [
    url(r'^$', BookView.as_view(), name='index'),
    url(r'^charge$', charge, name='charge')
]
