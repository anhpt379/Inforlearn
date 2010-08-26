from django.conf.urls.defaults import patterns


urlpatterns = patterns('actor.views',
    (r'^invite$', 'actor_invite'),
    (r'^contacts$', 'actor_contacts'),
    (r'^contacts/(?P<format>json|xml|atom)$', 'actor_contacts'),
    (r'^followers$', 'actor_followers'),
    (r'^recommended_users', 'recommended_users'),
    (r'^followers/(?P<format>json|xml|atom)$', 'actor_followers'),
    (r'^presence/(?P<item>[\da-f]+|last)/(?P<format>json|xml|atom)$', 'actor_item'),
    (r'^presence/(?P<item>[\da-f]+|last)$', 'actor_item'),
    #(r'^presence/(?P<format>json|xml|atom)$', 'presence_current'),
    #(r'^presence$', 'presence_current'),
    (r'^(?P<format>json|xml|atom|rss)$', 'actor_history'),
    (r'^feed/(?P<format>json|xml|atom|rss)$', 'actor_history'),
    (r'^contacts/feed/(?P<format>json|xml|atom|rss)$', 'actor_overview'),
    (r'^overview/(?P<format>json|xml|atom|rss)$', 'actor_overview'),
    (r'^overview$', 'actor_overview', {"format": "html"}),
    (r'^$', 'actor_history', {'format': 'html'}),
    (r'^settings$', 'actor_settings'),
    (r'^settings/(?P<page>\w+)$', 'actor_settings'),
)


handler404 = 'common.views.common_404'
handler500 = 'common.views.common_500'
