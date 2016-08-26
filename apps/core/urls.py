from django.conf.urls import url
from .views import redirect_to_anchor


app_name = 'core'
urlpatterns = [

    url(r'^(?P<parent>\w+)/anchor/(?P<anchor>\w+)$', redirect_to_anchor, name='redirect_to_anchor'),
]

