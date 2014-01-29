from django.conf.urls import patterns, include, url
from django.contrib import admin
from web.views.user import register_user
from web.views.user import edit_profile
from web.views.user import profile

from web.forms.user_forms import LoginForm
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	# WEB
	(r'', include('web.urls')),

	# ADMIN
	url(r'^admin/', include(admin.site.urls)),

	# STATIC CONTENT
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)

urlpatterns += patterns(
	'',
	url(r'^accounts/login/$', 'django.contrib.auth.views.login',
	    {'template_name': 'user/login.html', 'authentication_form': LoginForm},
	    name='login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
	    {'next_page': '/'}, name='logout'),
	url(r'^accounts/register/$', register_user, name='register'),
    url(r'^accounts/user/(?P<user_id>\d+)/edit/$', edit_profile, name='edit_profile'),
    url(r'^accounts/user/(?P<user_id>\d+)/$', profile, name='profile'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
