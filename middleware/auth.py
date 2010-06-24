# TODO andy: this is very basic to begin with, it will need to do some
#            fancy bits if we are going to support more kinds of wild
#            authenticatory neatness

# copied largely from django's contrib.auth stuff
class LazyUser(object):
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      from common import user
      request._cached_user = user.get_user_from_request(request)
    return request._cached_user

class AuthenticationMiddleware(object):
  def process_request(self, request):
    request.__class__.user = LazyUser()
