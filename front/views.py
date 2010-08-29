from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from common import api
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
    return HttpResponseRedirect(url + "/unread_messages")
  
  channels = api.channel_browse(request.user, 15)
  area = 'frontpage'

  t = loader.get_template('front/templates/front.html')
  c = RequestContext(request, locals())
  html = html_slimmer(t.render(c))
  
  return HttpResponse(html);
