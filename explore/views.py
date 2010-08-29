from django import http
from django import template
from django.template import loader
from common import api, util
from common.display import prep_entry_list, prep_stream_dict
from common.views import handle_view_action
from common.slimmer import html_slimmer

ENTRIES_PER_PAGE = 20

def explore_recent(request, format="html"):
  green_top = True
  handled = handle_view_action(request, {'entry_remove': request.path,
                                         'entry_remove_comment': request.path,
                                         'entry_mark_as_spam': request.path,
                                         'presence_set': request.path,
                                         'settings_hide_comments': request.path,
                                         'post': request.path,})
  if handled:
    return handled

  per_page = ENTRIES_PER_PAGE

  offset, prev = util.page_offset(request)

  inbox = api.inbox_get_explore(request.user, limit=100,
                                offset=offset)

  # START inbox generation chaos
  # TODO(termie): refacccttttooorrrrr
  entries = api.entry_get_entries(request.user, inbox)
#  per_page = per_page - (len(inbox) - len(entries))
  entries, more = util.page_entries(request, entries, per_page)

  stream_keys = [e.stream for e in entries]

  streams = api.stream_get_streams(request.user, stream_keys)

  actor_nicks = [e.owner for e in entries] + [e.actor for e in entries]
  actors = api.actor_get_actors(request.user, actor_nicks)

  # here comes lots of munging data into shape
  streams = prep_stream_dict(streams, actors)
  entries = prep_entry_list(entries, streams, actors)

  # END inbox generation chaos
  channels = api.channel_browse(request.user, 22)
  users = api.top_actors(25)

  area = 'explore'
  sidebar_green_top = True

  c = template.RequestContext(request, locals())

  if format == 'html':
    t = loader.get_template('explore/templates/recent.html')
    html = html_slimmer(t.render(c))
    return http.HttpResponse(html);
  elif format == 'json':
    t = loader.get_template('explore/templates/recent.json')
    return util.HttpJsonResponse(t.render(c), request)
  elif format == 'atom':
    t = loader.get_template('explore/templates/recent.atom')
    return util.HttpAtomResponse(t.render(c), request)
  elif format == 'rss':
    t = loader.get_template('explore/templates/recent.rss')
    return util.HttpRssResponse(t.render(c), request)
