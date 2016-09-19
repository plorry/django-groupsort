from django.conf.urls import include, url
from .views import (GroupSortView, AjaxAddNamelistView,
    AjaxGetNamelist, AjaxGetNamelists, AjaxAddPersonView, AjaxCreateGroups)

urlpatterns = [
    url(r'^$', GroupSortView.as_view(), name="home"),
    #url(r'^namelist/(?P<namelist_id>[0-9]+)/sort/(?P<num_groups>[0-9]+)/$', GroupsView.as_view(), name="groups"),
    url(r'^add_namelist/$', AjaxAddNamelistView.as_view(), name="add_namelist"),
    url(r'^get_namelist/$', AjaxGetNamelist.as_view(), name="get_namelist"),
    url(r'^get_namelists/$', AjaxGetNamelists.as_view(), name="get_namelists"),
    url(r'^add_person/$', AjaxAddPersonView.as_view(), name="add_person"),
    url(r'^create_groups/$', AjaxCreateGroups.as_view(), name="create_groups"),
]
"""
    url(r'^namelist/(?P<namelist_id>\d+)$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)/(?P<person_id>\d+)$', 'groupsort.views.home_view', name="home"),
    url(r'^namelist/(?P<namelist_id>\d+)/sort/(?P<num_groups>\d+)$', 'groupsort.views.groups_view', name="groups"),
    url(r'^person/save$', 'groupsort.views.save_person', name='save_person'),

]
"""
