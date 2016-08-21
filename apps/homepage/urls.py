from django.conf.urls import url
from .views import homepage


app_name = 'homepage'
urlpatterns = [

    url(r'^$', homepage, name='index'),
    url(r'^homepage/$', homepage, name='index'),
]
