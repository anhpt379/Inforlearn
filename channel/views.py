#! coding: utf-8
from django import http
from django import template
from django.conf import settings
from django.template import loader

from common import api
from common import clean
from common import decorator
from common import display
from common import exception
from common import util
from common import views as common_views
from operator import itemgetter
from settings import DEFAULT_OURPICKS_CHANNELS
#from cachepy import cachepy as cache
from common.memcache import client as cache
from common.slimmer import html_slimmer


CHANNEL_HISTORY_PER_PAGE = 20
CHANNELS_PER_INDEX_PAGE = 12
CHANNELS_PER_PAGE = 24
CONTACTS_PER_PAGE = 24


@decorator.login_required
def channel_create(request, format='html'):
  key_name = "html:channel_create"
  green_top = True
  channel = request.REQUEST.get('channel', '')

  handled = common_views.handle_view_action(
      request,
      {'channel_create': '/channel/%s' % channel,}
      )
  if handled:
    cache.delete(key_name)
    
    s = str(request.COOKIES.get('user')) + ":" + "/channel"
    key_name = "html:%s" % s
    cache.delete(key_name)
    return handled
  
#  cached_data = cache.get(key_name)
#  if cached_data:
#    return http.HttpResponse(cached_data)

  # for template sidebar
  sidebar_green_top = True

  area = 'channel'
  c = template.RequestContext(request, locals())

  if format == 'html':
    t = loader.get_template('channel/templates/create.html')
    html = html_slimmer(t.render(c))
    cache.set(key_name, html, 120)
    return http.HttpResponse(html)


def channel_index(request, format='html'):
  """ the index page for channels, /channel

  should list the channels you administer, the channels you belong to
  and let you create new channels

  if you are not logged in, it should suggest that you log in to create or
  join channels and give a list of public channels
  """
  if not request.user:
    return channel_index_signedout(request, format='html')

  if request.META.get("QUERY_STRING").startswith("offset"):
    s = str(request.COOKIES.get('user')) + ":"      \
      + request.META.get("PATH_INFO") + "?"  \
      + request.META.get("QUERY_STRING")
  else:
    s = str(request.COOKIES.get('user')) + ":"      \
      + request.META.get("PATH_INFO")
  key_name = "html:%s" % s.strip()
  
  cached_data = cache.get(key_name)
  if cached_data and format == "html":
#    print "has cache"
    return http.HttpResponse(cached_data)
  
  view = api.actor_lookup_nick(request.user, request.user.nick)
  
  owned_nicks = api.actor_get_channels_admin(
      request.user,
      request.user.nick,
      limit=(CHANNELS_PER_INDEX_PAGE + 1))
  owned_more = len(owned_nicks) > CHANNELS_PER_INDEX_PAGE

  followed_nicks = api.actor_get_channels_member(
      request.user,
      request.user.nick,
      limit=(CHANNELS_PER_INDEX_PAGE + 1))
  followed_more = len(owned_nicks) > CHANNELS_PER_INDEX_PAGE

  channel_nicks = owned_nicks + followed_nicks
  channels = api.channel_get_channels(request.user, channel_nicks)
  
  owned_channels = [channels[x] for x in owned_nicks if channels[x]]

  for c in owned_channels:
    c.i_am_admin = True

  followed_channels = [
      channels[x] for x in followed_nicks
          if channels[x] and x not in owned_nicks
  ]
  for c in followed_channels:
    c.i_am_member = True
  
  current_channels = api.actor_get_channels_member(request.user, request.user.nick, limit=1000)
  
#  user_nick = request.user.nick.split("@")[0] + "@inforlearn.appspot.com"
  users = api.get_recommended_items(request.user.nick, "user:users")  
  recommended_channels = []
  for user in users:
    _channels = api._actor_get_channels(user[1])
    for channel in _channels:
      if channel not in current_channels:
        channel_details = api.get_actor_details(channel)
        if not channel_details:
          continue
        recommended_channels.append({"rank": channel_details.rank, 
                                     "details": channel_details})
        
  # TODO: find other way to sort for more clear and simple
  # TODO: "Xem thêm" sẽ hiển thị toàn bộ danh sách gợi ý này, còn toàn bộ 
  # nhóm sẽ chuyển sang mục "Khám phá"
  # TODO: "Nhóm" nên sử dụng ảnh nền cá nhân
  recommended_channels.sort(key=itemgetter("rank"), reverse=True)
  ourpicks_channels = [x["details"] for x in recommended_channels[:3]]
  
  area = 'channel'
  c = template.RequestContext(request, locals())

  if format == 'html':
    t = loader.get_template('channel/templates/index.html')
    html = html_slimmer(t.render(c))
    cache.set(key_name, html, 120)
    return http.HttpResponse(html)


def channel_recommendation_list(request, format="html"):
  current_channels = api.actor_get_channels_member(request.user, request.user.nick, limit=1000)
  users = api.get_recommended_items(request.user.nick, "user:users")  
  recommended_channels = []
  for user in users:
    _channels = api._actor_get_channels(user[1])
    for channel in _channels:
      if channel not in current_channels:
        channel_details = api.get_actor_details(channel)
        if not channel_details:
          continue
        recommended_channels.append({"rank": channel_details.rank, 
                                     "details": channel_details})
        
  # TODO: find other way to sort for more clear and simple
  # TODO: "Xem thêm" sẽ hiển thị toàn bộ danh sách gợi ý này, còn toàn bộ 
  recommended_channels.sort(key=itemgetter("rank"), reverse=True)
  actors = [x["details"] for x in recommended_channels[:20]]
  
  channels = api.channel_browse(request.user, 5) # top channels
  
  area = 'channel'
  c = template.RequestContext(request, locals())
  

  # TODO(tyler): Other output formats.
  if format == 'html':
    t = loader.get_template('channel/templates/recommendation.html')
    return http.HttpResponse(t.render(c))

def channel_index_signedout(request, format='html'):
  # for the Our Picks section of the sidebar
  if request.META.get("QUERY_STRING").startswith("offset"):
    s = str(request.COOKIES.get('user')) + ":"      \
      + request.META.get("PATH_INFO") + "?"  \
      + request.META.get("QUERY_STRING")
  else:
    s = str(request.COOKIES.get('user')) + ":"      \
      + request.META.get("PATH_INFO")
  key_name = "html:%s" % s.strip()
  
  cached_data = cache.get(key_name)
  if cached_data and format == "html":
#    print "has cache"
    return http.HttpResponse(cached_data)
  
  ourpicks_channels = [] 
  for channel in DEFAULT_OURPICKS_CHANNELS:
    try:
      ourpicks_channels.append(api.get_actor_details(channel))
    except AttributeError:
      pass

  area = 'channel'
  c = template.RequestContext(request, locals())

  if format == 'html':
    t = loader.get_template('channel/templates/index_signedout.html')
    html = html_slimmer(t.render(c))
    cache.set(key_name, html, 20)
    return http.HttpResponse(html)


def channel_history(request, nick, format='html'):
  """ the page for a channel

  if the channel does not exist we go to create channel instead

  should let you join a channel or post to it if you already are a member
  also leave it if you are a member,
  display the posts to this channel and the member list if you are allowed
  to see them

  if you are an admin you should have the options to modify the channel
  """
  nick = clean.channel(nick)
  
  view = api.actor_lookup_nick(request.user, nick)
  if not view:
    return http.HttpResponseRedirect('/channel/create?channel=%s' % nick)

  if request.META.get("QUERY_STRING").startswith("offset"):
    s = str(request.COOKIES.get('user')) + ":"      \
      + request.META.get("PATH_INFO") + "?"  \
      + request.META.get("QUERY_STRING")
  else:
    s = str(request.COOKIES.get('user')) + ":"      \
      + request.META.get("PATH_INFO")
  key_name = "html:%s" % s.strip()

  admins = api.channel_get_admins(request.user, channel=view.nick)
  members = api.channel_get_members(request.user, channel=view.nick)
  
  handled = common_views.handle_view_action(
      request,
      {'channel_join': request.path,
       'channel_part': request.path,
       'channel_post': request.path,
       'entry_remove': request.path,
       'entry_remove_comment': request.path,
       'entry_mark_as_spam': request.path,
       'subscription_remove': request.path,
       'subscription_request': request.path,
       }
      )
  if handled:
    cache.delete(key_name)    
    s = str(None) + ":"      \
      + "/explore"
    key_name = "html:%s" % s
    cache.delete(key_name)
    
    s = str(request.COOKIES.get('user')) + ":"      \
      + "/explore"
    key_name = "html:%s" % s
    cache.delete(key_name)
    return handled

  cached_data = cache.get(key_name)
  if cached_data and format == "html":
#    print "has cache"
    return http.HttpResponse(cached_data)

  privacy = 'public'

  user_can_post = False
  user_is_admin = False
  if not request.user:
    pass
  elif api.channel_has_admin(request.user, view.nick, request.user.nick):
    privacy = 'private'
    user_can_post = True
    user_is_admin = True
  elif api.channel_has_member(request.user, view.nick, request.user.nick):
    privacy = 'contacts'
    user_can_post = True

  per_page = CHANNEL_HISTORY_PER_PAGE
  offset, prev = util.page_offset(request)

  if privacy == 'public':
    inbox = api.inbox_get_actor_public(
        request.user,
        view.nick,
        limit=(per_page + 1),
        offset=offset)
  elif privacy == 'contacts':
    inbox = api.inbox_get_actor_contacts(
        request.user,
        view.nick,
        limit=(per_page + 1),
        offset=offset)
  elif privacy == 'private':
    inbox = api.inbox_get_actor_private(
        api.ROOT,
        view.nick,
        limit=(per_page + 1),
        offset=offset)

  # START inbox generation chaos
  # TODO(termie): refacccttttooorrrrr

  entries = api.entry_get_entries(request.user, inbox)
  # clear out deleted entries
  per_page = per_page - (len(inbox) - len(entries))
  entries, more = util.page_entries(request, entries, per_page)

  stream_keys = [e.stream for e in entries]
  actor_streams = api.stream_get_actor(request.user, view.nick)
  stream_keys += [s.key().name() for s in actor_streams]
  streams = api.stream_get_streams(request.user, stream_keys)

  contact_nicks = api.actor_get_contacts(request.user, view.nick)
  actor_nicks = (contact_nicks +
                 admins +
                 members +
                 [view.nick] +
                 [s.owner for s in streams.values()] +
                 [e.actor for e in entries])
  actors = api.actor_get_actors(request.user, actor_nicks)

  # here comes lots of munging data into shape
  contacts = [actors[x] for x in contact_nicks if actors[x]]
  streams = display.prep_stream_dict(streams, actors)
  entries = display.prep_entry_list(entries, streams, actors)
  admins = [actors[x] for x in admins if actors[x]]
  members = [actors[x] for x in members if actors[x]]

#  transform_nick = view.nick.split('@')[0] + "@inforlearn.appspot.com"
  _items = api.get_recommended_items(view.nick, "channel:channels")  
  items = []
  for item in _items:
    details = api.get_actor_details(item[1])
    if details:
      items.append(details)
    if len(items) > 10:
      break

  # END inbox generation chaos

  presence = api.presence_get(request.user, view.nick)

  # for sidebar_members
  members_count = view.extra['member_count']
  members_more = members_count > CONTACTS_PER_PAGE

#  # for sidebar_admins
#  admins_count = view.extra['admin_count']
#  admins_more = admins_count > CONTACTS_PER_PAGE

  # config for templates
  green_top = True
  sidebar_green_top = True
  selectable_icons = display.SELECTABLE_ICONS


  # for sidebar streams (copied from actor/views.py.  refactor)
  view_streams = dict([(x.key().name(), streams[x.key().name()])
                       for x in actor_streams])
  if request.user:
    # un/subscribe buttons are possible only, when logged in

    # TODO(termie): what if there are quite a lot of streams?
    for stream in view_streams.values():
      stream.subscribed = api.subscription_exists(
          request.user,
          stream.key().name(),
          'inbox/%s/overview' % request.user.nick
          )

  area = 'channel'
  c = template.RequestContext(request, locals())

  if format == 'html':
    t = loader.get_template('channel/templates/history.html')
    html = html_slimmer(t.render(c))
    cache.set(key_name, html, 120)
    return http.HttpResponse(html)
  elif format == 'json':
    t = loader.get_template('channel/templates/history.json')
    return util.HttpJsonResponse(t.render(c), request)
  elif format == 'atom':
    t = loader.get_template('channel/templates/history.atom')
    return util.HttpAtomResponse(t.render(c), request)
  elif format == 'rss':
    t = loader.get_template('channel/templates/history.rss')
    return util.HttpRssResponse(t.render(c), request)


def channel_item(request, nick, item=None, format='html'):
  nick = clean.channel(nick)
  view = api.actor_lookup_nick(request.user, nick)

  if not view:
    raise http.Http404()

  if request.META.get("QUERY_STRING").startswith("offset"):
    s = request.META.get("PATH_INFO") + "?"  \
      + request.META.get("QUERY_STRING")
  else:
    s = request.META.get("PATH_INFO")
  key_name = "html:%s" % s.strip()

  
  stream_ref = api.stream_get_presence(request.user, view.nick)

  entry = '%s/%s' % (stream_ref.key().name(), item)
  
  entry_ref = api.entry_get(request.user, entry)
  if not entry_ref:
    raise http.Http404()

  handled = common_views.handle_view_action(
      request,
      {'entry_add_comment': entry_ref.url(request=request),
       'entry_remove': view.url(request=request),
       'entry_remove_comment': entry_ref.url(request=request),
       'entry_mark_as_spam': entry_ref.url(request=request)
       }
      )
  if handled:
    cache.delete(key_name)
    return handled
  
  cached_data = cache.get(key_name)
  if cached_data and format == "html":
#    print "has cache"
    return http.HttpResponse(cached_data)

  admins = api.channel_get_admins(request.user, channel=view.nick)
  user_is_admin = request.user and request.user.nick in admins

  comments = api.entry_get_comments(request.user, entry)

  actor_nicks = [entry_ref.owner, entry_ref.actor] + [c.actor for c in comments]
  actors = api.actor_get_actors(request.user, actor_nicks)

  # Creates a copy of actors with lowercase keys (Django #6904: template filter
  # dictsort sorts case sensitive), excluding channels and the currently
  # logged in user.
  participants = {}
  for k, v in actors.iteritems():
    if (v and
        not v.is_channel() and
        not (hasattr(request.user, 'nick') and request.user.nick == v.nick)):
      participants[k.lower()] = v

  # display munge
  entry = display.prep_entry(entry_ref,
                             { stream_ref.key().name(): stream_ref },
                             actors)
  comments = display.prep_comment_list(comments, actors)

  # config for template
  green_top = True
  sidebar_green_top = True

  # rendering
  c = template.RequestContext(request, locals())
  if format == 'html':
    t = loader.get_template('channel/templates/item.html')
    html = html_slimmer(t.render(c))
    cache.set(key_name, html, 120)
    return http.HttpResponse(html)
  elif format == 'json':
    t = loader.get_template('actor/templates/item.json')
    return util.HttpJsonResponse(t.render(c), request)

def channel_browse(request, format='html'):
  per_page = CHANNELS_PER_PAGE
  prev_offset, _ = util.page_offset_nick(request)

  # Use +1 to identify if there are more that need to be displayed.
  channel_list = api.channel_browse(request.user, (per_page + 1), prev_offset)

  actors, more = util.page_actors(request, channel_list, per_page)
  offset_text = 'More'

  # for the Our Picks section of the sidebar
  ourpicks_channels = api.actor_get_channels_member(request.user, api.ROOT.nick)
  ourpicks_channels = api.channel_get_channels(request.user, ourpicks_channels)
  ourpicks_channels = [x for x in ourpicks_channels.values() if x]

# TODO:
#  current_channels = api.actor_get_channels_member(request.user, request.user.nick, limit=1000)
#  users = api.get_recommended_items(request.user, "user:users")  
#  recommended_channels = []
#  for user in users:
#    _channels = api.actor_get_channels_member(request.user, request.user.nick, limit=1000)
#    if len(recommended_channels) > 10:
#      break
#    for channel in _channels:
#      if channel not in current_channels:
#        recommended_channels.append(api.get_actor_details(channel))



  area = 'channel'
  c = template.RequestContext(request, locals())

  # TODO(tyler): Other output formats.
  if format == 'html':
    t = loader.get_template('channel/templates/browse.html')
    return http.HttpResponse(t.render(c))

def channel_members(request, nick=None, format='html'):
  nick = clean.channel(nick)

  view = api.actor_lookup_nick(request.user, nick)

  if not view:
    raise exception.UserDoesNotExistError(nick, request.user)

  handled = common_views.handle_view_action(
      request,
      { 'actor_add_contact': request.path,
        'actor_remove_contact': request.path, })
  if handled:
    return handled

  per_page = CONTACTS_PER_PAGE
  offset, prev = util.page_offset_nick(request)

  follower_nicks = api.channel_get_members(request.user,
                                           view.nick,
                                           limit=(per_page + 1),
                                           offset=offset)
  actor_nicks = follower_nicks
  actors = api.actor_get_actors(request.user, actor_nicks)
  # clear deleted actors
  actors = dict([(k, v) for k, v in actors.iteritems() if v])
  per_page = per_page - (len(follower_nicks) - len(actors))

  whose = view.display_nick()

  # here comes lots of munging data into shape
  actor_tiles = [actors[x] for x in follower_nicks if x in actors]

  actor_tiles_count = view.extra.get('member_count', 0)
  actor_tiles, actor_tiles_more = util.page_actors(request,
                                                   actor_tiles,
                                                   per_page)

  area = 'channels'

  c = template.RequestContext(request, locals())

  # TODO: Other output formats.
  if format == 'html':
    t = loader.get_template('channel/templates/members.html')
    return http.HttpResponse(t.render(c))


@decorator.login_required
def channel_settings(request, nick, page='index'):
  nick = clean.channel(nick)
  view = api.actor_lookup_nick(request.user, nick)

  if not view:
    # Channel doesn't exist, bounce the user back so they can create it.
    # If the channel was just deleted, don't.  This unfortunately, misses the
    # case where a user is attempting to delete a channel that doesn't
    # exist.
    return http.HttpResponseRedirect('/channel/%s' % nick)

  handled = common_views.handle_view_action(
      request,
      {
        'channel_update': request.path,
        'actor_remove' : '/channel',
      }
  )
  if page == 'photo' and not handled:
    handled = common_views.common_photo_upload(request, request.path, nick)
  if page == 'design' and not handled:
    handled = common_views.common_design_update(request=request, nick=nick)

  if handled:
    return handled

  area = 'settings'
  avatars = display.DEFAULT_AVATARS
  backgrounds = display.DEFAULT_BACKGROUNDS
  actor_url = '/channel/%s' % nick

  if page == 'index':
    pass
  elif page == 'badge':
    badges = [{'id': 'badge-stream',
               'width': '200',
               'height': '300',
               'src': '/themes/%s/badge.swf' % settings.DEFAULT_THEME,
               'title': 'Stream',
               },
              {'id': 'badge-map',
               'width': '200',
               'height': '255',
               'src': '/themes/%s/badge-map.swf' % settings.DEFAULT_THEME,
               'title': 'Map',
               },
              {'id': 'badge-simple',
               'width': '200',
               'height': '200',
               'src': '/themes/%s/badge-simple.swf' % settings.DEFAULT_THEME,
               'title': 'Simple',
               },
              ]
  elif page == 'delete':
    full_page = "Xóa"
  elif page == 'design':
    full_page = u"Hiển thị"
  elif page == 'details':
    full_page = "Thông tin bổ sung"
  elif page == 'photo':
    full_page = "Ảnh đại diện"
  else:
    return common_views.common_404(request)

  # full_page adds the title of the sub-component.  Not useful if it's the
  # main settings page
#  if page != 'index':
#    full_page = page.capitalize()

  # rendering
  c = template.RequestContext(request, locals())
  t = loader.get_template('channel/templates/settings_%s.html' % page)
  return http.HttpResponse(t.render(c))
