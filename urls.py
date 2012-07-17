from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)/(?P<person_id>\d+)$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)/sort/(?P<num_groups>\d+)$', 'groupsort.views.groups_view', name="groups"),
)