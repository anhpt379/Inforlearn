from django.conf import settings as django_settings
from common import component
from common import util


def settings(request):

  d = dict([(k, getattr(django_settings, k))
            for k in django_settings.get_all_members()])
  return dict(**d)

def components(request):
  return {'component': component}

def flash(request):
  if 'flash' not in request.REQUEST:
    return {}

  flash = request.REQUEST['flash']
  nonce = util.create_nonce(None, flash)
  if nonce != request.REQUEST.get('_flash', ''):
    return {}
  return {'flash': flash}

def gaia(request):
  try:
    gaia_user = users.GetCurrentUser()
    gaia_login = users.CreateLoginURL(request.META['PATH_INFO'])
    gaia_logout = users.CreateLogoutURL('/logout')
  except:
    gaia_user = None
    gaia_login = "gaia_login"
    gaia_logout = "gaia_logout"
  return locals()
