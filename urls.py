from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)$', 'groupsort.views.home_view', name="home"),
)