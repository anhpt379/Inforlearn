# These URLs are normally mapped to /admin/urls.py. This URLs file is 
# provided as a convenience to those who want to deploy these URLs elsewhere.
# This file is also used to provide a reliable view deployment for test purposes.

from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)

