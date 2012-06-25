from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)$', 'groupsort.views.namelist_view', name="view_namelist"),
)