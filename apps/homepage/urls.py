from django.conf.urls import url
from .views import homepage, galleries


app_name = 'homepage'
urlpatterns = [

    url(r'^$', homepage, name='index'),
    url(r'^gallery/([0-9])/$', galleries, name='galleries'),
    url(r'^homepage/$', homepage, name='index'),
]
