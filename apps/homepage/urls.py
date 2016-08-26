from django.conf.urls import url
from .views import homepage, gallery, service


app_name = 'homepage'
urlpatterns = [

    url(r'^$', homepage, name='index'),
    url(r'^homepage/$', homepage, name='index'),
    url(r'^gallery/(?P<pk>[0-9])/$', gallery, name='gallery'),
    url(r'^service/(?P<pk>[0-9])/$', service, name='service'),
]

