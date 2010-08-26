from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from common import decorator
from settings import NS_DOMAIN
from common import api
from common.memcache import client as cache
from common.slimmer import html_slimmer

ENTRIES_PER_PAGE = 5
SIDEBAR_LIMIT = 9
SIDEBAR_FETCH_LIMIT = 50

def front_front(request):
  # if the user is logged in take them to their overview
  green_top = True
  sidebar_green_top = True
  
  if request.user:
    url = request.user.url(request=request)
    return HttpResponseRedirect(url + "/overview")
  
  key_name = "html:homepage"
  cached_data = cache.get(key_name)
  if cached_data:
    return HttpResponse(cached_data);

  # NOTE: grab a bunch of extra so that we don't ever end up with
  #       less than 5
#  per_page = ENTRIES_PER_PAGE * 2
#
#  inbox = api.inbox_get_explore(request.user, limit=per_page)
#
#  # START inbox generation chaos
#  # TODO(termie): refacccttttooorrrrr
#  entries = api.entry_get_entries(request.user, inbox)
#  per_page = per_page - (len(inbox) - len(entries))
#  entries, more = util.page_entries(request, entries, per_page)
#
#  stream_keys = [e.stream for e in entries]
#  streams = api.stream_get_streams(request.user, stream_keys)
#
#  actor_nicks = [e.owner for e in entries] + [e.actor for e in entries]
#  actors = api.actor_get_actors(request.user, actor_nicks)
#
#  # take it back down and don't show a more link
#  entries = entries[:ENTRIES_PER_PAGE]
#  more = None
#
#  # here comes lots of munging data into shape
#  streams = prep_stream_dict(streams, actors)
#  entries = prep_entry_list(entries, streams, actors)

  # END inbox generation chaos
#
#  try:
#    # Featured Channels -- Ones to which the ROOT user is a member
#    featured_channels = api.actor_get_channels_member(
#        request.user, api.ROOT.nick, limit=SIDEBAR_FETCH_LIMIT)
#    random.shuffle(featured_channels)
#
#    # Just in case any are deleted:
#    featured_channels = featured_channels[:2 * SIDEBAR_LIMIT]
#    featured_channels = api.channel_get_channels(
#        request.user, featured_channels)
#    featured_channels = [x for x in featured_channels.values() if x]
#    featured_channels = featured_channels[:SIDEBAR_LIMIT]
#
#    featured_members = api.actor_get_contacts(
#        request.user, api.ROOT.nick, limit=SIDEBAR_FETCH_LIMIT)
#    random.shuffle(featured_members)
#
#    # Just in case any are deleted:
#    featured_members = featured_members[:2 * SIDEBAR_LIMIT]
#    featured_members = api.actor_get_actors(request.user, featured_members)
#    featured_members = [x for x in featured_members.values() if x]
#    featured_members = featured_members[:SIDEBAR_LIMIT]
#
#  except exception.ApiNotFound:
#    pass

#  root = api.ROOT

  channels = api.channel_browse(request.user, 15)
#  for channel in channels:
#    print channel.extra["description"]
  area = 'frontpage'

  t = loader.get_template('front/templates/front.html')
  c = RequestContext(request, locals())
  html = html_slimmer(t.render(c))
  cache.set(key_name, html, 120)
  
  return HttpResponse(html);
