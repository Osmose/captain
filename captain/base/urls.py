from django.conf.urls.defaults import patterns, url

from captain.base import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='base.home'),
)
