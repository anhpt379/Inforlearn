from django.conf import settings
from django.conf.urls.defaults import patterns, include
from common import patterns as common_patterns


urlpatterns = patterns('',
)

# Export data from GAE
urlpatterns += patterns('export.views',
    (r'^export/channel_members$', 'channel_members'),
    (r'^export/user_contacts', 'user_contacts'),
    (r'^export/channel_admins$', 'channel_admins'),
    (r'^export/user_history$', 'user_history'),
    (r'^export/user_comments$', 'user_comments'),
)

#BOOKMARKLET
urlpatterns += patterns('bookmarklet.views',
    (r'^post', 'actor_post'),
)

# FRONT
urlpatterns += patterns('front.views',
    (r'^$', 'front_front'),
)

# XMPP
urlpatterns += patterns('',
    (r'_ah/xmpp/message', 'api.views.api_vendor_xmpp_receive'),
)

# EXPLORE
urlpatterns += patterns('explore.views',
    (r'^explore/(?P<format>json|xml|atom|rss)$', 'explore_recent'),
    (r'^explore$', 'explore_recent'),
    (r'^feed/(?P<format>json|xml|atom|rss)$', 'explore_recent'),
)

# JOIN
urlpatterns += patterns('join.views',
    (r'^join$', 'join_join'),
    (r'^welcome$', 'join_welcome'),
    (r'^welcome/1$', 'join_welcome_photo'),
    (r'^welcome/2$', 'join_welcome_design'),
    (r'^welcome/3$', 'join_welcome_contacts'),
    (r'^welcome/done$', 'join_welcome_done'),
)

# INVITE
urlpatterns += patterns('invite.views',
    (r'^invite/email/(?P<code>\w+)', 'invite_email'),
)

# CONFIRM
urlpatterns += patterns('confirm.views',
    (r'^confirm/email/(?P<code>\w+)$', 'confirm_email'),
)

# FLAT
urlpatterns += patterns('flat.views',
    (r'^tour$', 'flat_tour'),
    (r'^tour/1$', 'flat_tour', {'page': 'create'}),
    (r'^tour/2$', 'flat_tour', {'page': 'contacts'}),
    (r'^tour/3$', 'flat_tour', {'page': 'faqs'}),
    (r'^about$', 'flat_about'),
    (r'^privacy$', 'flat_privacy'),
    (r'^roadmap$', 'flat_roadmap'),
    (r'^sourcecode$', 'flat_sourcecode'),
    (r'^terms$', 'flat_terms'),
    (r'^terms$', 'flat_press'),
    (r'^help$', 'flat_help'),
    (r'^sms$', 'flat_help', {'page': 'sms'}),
    (r'^help/im$', 'flat_help', {'page': 'im'}),
    (r'^help/commands$', 'flat_help', {'page': 'commands'}),
    (r'^help/im_clients$', 'flat_help', {'page': 'im_clients'}),
)

# ACTOR
urlpatterns += patterns('',
    (r'^user/(?P<nick>\w+)', include('actor.urls')),
    (r'^user/(?P<nick>\w+)/', include('actor.urls')),
)

# CHANNEL
urlpatterns += patterns('channel.views',
    (r'^channel/browse', 'channel_browse'),
    (r'^channel/recommendation', 'channel_recommendation_list'),
    (r'^channel/create$', 'channel_create'),
    (r'^channel/(?P<nick>\w+)/presence/(?P<item>[\da-f]+)/(?P<format>json|xml|atom)$', 'channel_item'),
    (r'^channel/(?P<nick>\w+)/presence/(?P<item>[\da-f]+)$', 'channel_item'),
    (r'^channel/(?P<nick>\w+)/(?P<format>json|xml|atom|rss)$', 'channel_history'),
    (r'^channel/(?P<nick>\w+)$', 'channel_history', {'format': 'html'}),
    (r'^channel/(?P<nick>\w+)/members/(?P<format>json|xml|atom|rss)$', 'channel_members'),
    (r'^channel/(?P<nick>\w+)/members$', 'channel_members', {'format': 'html'}),
    (r'^channel$', 'channel_index'),
    (r'^channel/(?P<nick>\w+)/settings$', 'channel_settings'),
    (r'^channel/(?P<nick>\w+)/settings/(?P<page>\w+)$', 'channel_settings'),
)
urlpatterns += patterns('',
    (r'^c/(?P<the_rest>.*)$',
     'django.views.generic.simple.redirect_to',
     {'url': '/channel/%(the_rest)s'}),
)

# SETTINGS redirect
urlpatterns += patterns('actor.views',
    (r'^settings', 'actor_settings_redirect')
)


# LOGIN
urlpatterns += patterns('login.views',
    (r'^login$', 'login_login'),
    (r'^login/noreally$', 'login_noreally'),
    (r'^login/forgot$', 'login_forgot'),
    (r'^login/reset', 'login_reset'),
    (r'^logout$', 'login_logout'),
)

# API
urlpatterns += patterns('',
    (r'^api/', include('api.urls')),
    (r'^api', 'django.views.generic.simple.redirect_to', {'url': '/api/docs'}),
    (r'_ah/queue/default', 'api.views.api_task_queue'),
)


# BLOG
if settings.BLOG_ENABLED:
  urlpatterns += patterns('',
    (r'^blog/feed$',
     'django.views.generic.simple.redirect_to',
     {'url': settings.BLOG_FEED_URL}
     ),
    (r'^blog$',
     'django.views.generic.simple.redirect_to',
     {'url': settings.BLOG_URL}
     ),
  )

# BADGES
urlpatterns += patterns('',
    (r'^badge/(?P<format>images|js-small|js-medium|js-large|json|xml)/(?P<nick>\w+)$', 'badge.views.badge_badge'),
    (r'^user/(?P<nick>\w+)/feed/badge$', 'actor.views.actor_history', {'format': 'rss'}),
    (r'^channel/(?P<nick>\w+)/feed/badge$', 'channel.views.channel_history', {'format': 'rss'}),
)


# COMMON
urlpatterns += patterns('common.views',
    (r'^error$', 'common_error'),
    (r'^confirm$', 'common_confirm'),
    (r'^(?P<path>.*)/$', 'common_noslash'),
)

# BLOB
urlpatterns += patterns('blob.views',
    (common_patterns.AVATAR_PATH_RE, 'blob_image_jpg'),
    (r'^archive/.*', 'get_archive'),
    (r'^css/.*', 'css'),
    (r'^js/.*', 'js'),
)

# INSTALL
urlpatterns += patterns('install.views',
    ('install', 'install_rootuser'),
)

handler404 = 'common.views.common_404'
handler500 = 'common.views.common_500'
