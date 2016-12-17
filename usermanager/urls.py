from django.conf.urls import url

from .views import signin

urlpatterns = [
    url(r'^signin$', signin, name='signin')
]
