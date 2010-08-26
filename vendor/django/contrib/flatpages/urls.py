from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.contrib.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
