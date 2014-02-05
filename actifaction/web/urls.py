from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'web.views',
    url(r'^$', 'action.index', name='web.index'),
	url(r'^actions/$', 'action.view_all_actions', name='web.view_all_actions'),
    url(r'^action/add/$', 'action.add_action', name='web.add_action'),
    url(r'^action/edit/(?P<action_id>\d+)/edit/$', 'action.edit_action', name='web.edit_action'),
    url(r'^action/(?P<action_id>\d+)/$', 'action.view_action', name='web.view_action'),
    url(r'^action/join/(?P<action_id>\d+)/$', 'action.view_action', name='web.view_action'),
)
