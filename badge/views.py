from django import http
from django import template
from django.template import loader
from common import api


def badge_badge(request, format, nick):
  view = api.actor_get(request.user, nick)

  presence = api.presence_get(request.user, view.nick)

  if not presence:
    # look offline please
    line = 'Offline'
    light = 'gray'
    location = ''
  else:
    line = presence.extra.get('status', 'Offline')
    light = presence.extra.get('light', 'gray')
    location = presence.extra.get('location', '')

  if format == 'image':
    # TODO: Create badge images
    return http.HttpResponseRedirect('/images/badge_%s.gif' % light)

  if format == 'js-small':
    multiline = len(line) > 17
    truncated_line = len(line) > 30 and "%s..." % (line[:27]) or line
    content_type = 'text/javascript'
    template_path = 'js_small.js'
  elif format == 'js-medium' or format == 'js-large':
    truncated_line = len(line) > 40 and "%s..." % (line[:27]) or line
    content_type = 'text/javascript'
    template_path = '%s.js' % format.replace('-', '_')
  elif format == 'json':
    # TODO: Create badge.json template
    content_type = 'application/json'
    template_path = 'badge.json'
  elif format == 'xml':
    content_type = 'application/xml'
    # TODO: Create badge.xml template
    template_path = 'badge.xml'

  c = template.RequestContext(request, locals())
  t = loader.get_template('badge/templates/%s' % template_path)
  r = http.HttpResponse(t.render(c))
  r['Content-type'] = content_type
  return r
