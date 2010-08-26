#! coding: utf-8
# pylint: disable-msg=W0311
from django import http
from django import template
from django.conf import settings
from django.template import loader

from common import api
from common import clean
from common import exception
from common import util
from common import display
from common import views as common_views
#from cachepy import cachepy as cache
from common.memcache import client as cache
from common.slimmer import html_slimmer
from hashlib import md5
import re


ENTRIES_PER_PAGE = 20
CONTACTS_PER_PAGE = 48
CHANNELS_PER_PAGE = 48

# This is a decorator to make it a bit easier to deal with the possibility
# the nick coming in via the subdomain
def alternate_nick(f):
  def _wrap(request, *args, **kw):
    if settings.WILDCARD_USER_SUBDOMAINS_ENABLED:
      # grab the nick from the subdomain
      if hasattr(request, 'subdomain'):
        kw['nick'] = request.subdomain
    return f(request, *args, **kw)
  _wrap.func_name = f.func_name
  return _wrap

def get_text(begin_str, end_str, document):
  """ Trả về các ký tự nằm giữa 2 chuỗi """
  s = begin_str + '(.*?)' + end_str
  return re.compile(s, re.DOTALL |  re.IGNORECASE).findall(document)

@alternate_nick
def actor_post(request, format='html'):
  s = str(request.COOKIES.get('user'))       \
    + str(request.META.get("HTTP_REFERER"))  \
    + str(request.META.get("PATH_INFO"))
  key_name = "html:%s" % md5(s).hexdigest()
    
  nick = request.COOKIES.get("user")
  if nick is None:
    redirect_to = "%s?message=%s" % (request.META.get("PATH_INFO"), 
                                     request.GET.get("message"))
    return http.HttpResponseRedirect("/login?redirect_to=%s" % redirect_to)
  nick = clean.nick(nick)

  view = api.actor_lookup_nick(request.user, nick)

  if not view:
    raise exception.UserDoesNotExistError(nick, request.user)

  if not request.user or view.nick != request.user.nick:
    # Instead of displaying the overview, redirect to the public-facing page
    return http.HttpResponseRedirect(view.url())

  handled = common_views.handle_view_action(
      request,
      {
        'entry_remove': request.path,
        'entry_remove_comment': request.path,
        'entry_mark_as_spam': request.path,
        'presence_set': request.path,
        'settings_hide_comments': request.path,
        'post': request.path,
      }
  )
  if handled:
    cache.delete(key_name)
    s = str(request.COOKIES.get('user'))       \
      + str(request.META.get("HTTP_REFERER"))  \
      + str(request.META.get("PATH_INFO")).replace("/overview", "")
    key_name = "html:%s" % md5(s).hexdigest()
    cache.delete(key_name)
    return handled
  
  message = request.GET.get("message")
  cached_data = cache.get(key_name)
  if cached_data and format == "html":
    if message:
      replace_text = get_text('<textarea id="message" name="message" rows="4" cols="25">', '</textarea>', cached_data)[0]
#      print replace_text
      cached_data = cached_data.replace(replace_text, message)
    return http.HttpResponse(cached_data)
  
  
  per_page = ENTRIES_PER_PAGE
  offset, prev = util.page_offset(request)

  inbox = api.inbox_get_actor_overview(request.user,
                                       view.nick,
                                       limit=100,#(per_page + 1),
                                       offset=offset)

  actor_streams = api.stream_get_actor(request.user, view.nick)
  entries, more = _get_inbox_entries(request, inbox,
                                     view.extra.get('comments_hide', 0))
  contacts, channels, streams, entries = _assemble_inbox_data(request,
                                                              entries,
                                                              actor_streams,
                                                              view)

  # Check for unconfirmed emails
  unconfirmeds = api.activation_get_actor_email(request.user, view.nick)
  if unconfirmeds:
    unconfirmed_email = unconfirmeds[0].content

  # If not logged in, cannot write
  is_owner = False
  try:
    is_owner = view.nick == request.user.nick
  except:
    pass
  presence = api.presence_get(request.user, view.nick)

  # for sidebar streams
  view_streams = _get_sidebar_streams(actor_streams, streams)

  # for sidebar_contacts
  contacts_count = view.extra.get('contact_count', 0)
  contacts_more = contacts_count > CONTACTS_PER_PAGE

  # for sidebar channels
  channels_count = view.extra.get('channel_count', 0)
  channels_more = channels_count > CHANNELS_PER_PAGE

  # Config for the template
  green_top = True
  sidebar_green_top = True
  selectable_icons = display.SELECTABLE_ICONS

  area = 'home'

  # TODO(tyler/termie):  This conflicts with the global settings import.
  # Also, this seems fishy.  Do none of the settings.* items work in templates?
  import settings

  c = template.RequestContext(request, locals())

  if format == 'html':
    t = loader.get_template('actor/templates/overview.html')
    html = html_slimmer(t.render(c))
    cache.set(key_name, html)
#    print "not cache"
    return http.HttpResponse(html)
  elif format == 'json':
    t = loader.get_template('actor/templates/overview.json')
    return util.HttpJsonResponse(t.render(c), request)
  elif format == 'atom':
    t = loader.get_template('actor/templates/overview.atom')
    return util.HttpAtomResponse(t.render(c), request)
  elif format == 'rss':
    t = loader.get_template('actor/templates/overview.rss')
    return util.HttpRssResponse(t.render(c), request)

def _assemble_inbox_data(request, entries, actor_streams, inbox_owner_ref):
  stream_keys = [e.stream for e in entries]
  stream_keys += [s.key().name() for s in actor_streams]
  streams = api.stream_get_streams(request.user, stream_keys)

  contact_nicks = api.actor_get_contacts_safe(request.user,
                                              inbox_owner_ref.nick,
                                              limit=CONTACTS_PER_PAGE)
  channel_nicks = api.actor_get_channels_member_safe(request.user,
                                                     inbox_owner_ref.nick,
                                                     limit=CHANNELS_PER_PAGE)
  actor_nicks = (contact_nicks +
                 channel_nicks +
                 [inbox_owner_ref.nick] +
                 [s.owner for s in streams.values()] +
                 [e.owner for e in entries] +
                 [e.actor for e in entries])
  actors = api.actor_get_actors(request.user, actor_nicks)

  # here comes lots of munging data into shape
  contacts = [actors[x] for x in contact_nicks if actors[x]]
  channels = [actors[x] for x in channel_nicks if actors[x]]
  streams = display.prep_stream_dict(streams, actors)
  entries = display.prep_entry_list(entries, streams, actors)

  return (contacts, channels, streams, entries)

def _get_sidebar_streams(actor_streams, streams, request_user=None):
  result = dict([(x.key().name(), streams[x.key().name()])
                 for x in actor_streams])
  # un/subscribe buttons are possible only when logged in
  if request_user:
    # TODO(termie): what if there are quite a lot of streams?
    for stream in result.values():
      stream.subscribed = api.subscription_exists(
          request_user,
          stream.key().name(),
          'inbox/%s/overview' % request_user.nick
          )
  return result

def _get_inbox_entries(request, inbox, hide_comments=False):
  entries = api.entry_get_entries(request.user, inbox, hide_comments)
  per_page = 20# ENTRIES_PER_PAGE #- (len(inbox) - len(entries))
  return util.page_entries(request, entries, per_page)
