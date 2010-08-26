#! coding: utf-8
import re
from common import exception
from common import patterns
from common import util
from django.conf import settings

# TODO(teemu): list of banned names should probably reside outside of code.
# Ask Andy, where to move this.
banned_names = [
    'address',
    'admin',
    'action',
    'blog',
    'city',
    'cities',
    'country',
    'countries',
    'create',
    'entry',
    'entries',
    'event',
    'events',
    'get',
    'group',
    'groups',
    'guide',
    'guides',
    'id',
    'hotspot',
    'json',
    'xmlrpc',
    'atom',
    'list',
    'location',
    'manage',
    'network',
    'person',
    'persons',
    'place',
    'places',
    'slug',
    'spot',
    'subscribe',
    'tag',
    'tags',
    'town',
    'towns',
    'user',
    'users',
    'support',
    'atom',
    'feed',
    'rss',
    'www',
    'xml',
    'bar',
    'cafe',
    'fashion',
    'hotel',
    'restaurant',
    'product',
    'review',
    'shop',
    'shopping',
    'static',
    'static1',
    'static2',
    'static3',
    'static4',
    'static5',
    'static6',
    'static7',
    'static8',
    'static9',
    'static10',
    'static11',
    'static12',
    'static13',
    'static14',
    'static15',
    'static16',
    'static17',
    'static18',
    'static19',
    'travel',
    'trip'
]

def avatar_path(path):
  # TODO(tyler): Move this to clean
  if not patterns.AVATAR_PARTIAL_PATH_COMPILED.match(path):
    raise exception.ValidationError('Could not validate avatar path')

def nonce(request, action=''):
  user = request.user

  expected_now = util.create_nonce(user, action)
  expected_older = util.create_nonce(user, action, offset= -1)

  # TODO(termie): we should probably only accept these in POST in the future
  given = request.REQUEST.get('_nonce')
  if given not in (expected_now, expected_older):
    raise exception.ValidationError('Could not validate nonce')

def error_nonce(request, message=''):
  expected_now = util.create_nonce(None, message)
  expected_older = util.create_nonce(None, message, offset= -1)

  given = request.REQUEST.get('_error')
  if given not in (expected_now, expected_older):
    raise exception.ValidationError('Could not validate nonce')


# Mobile number regexps 
_italian = re.compile(r"\+39.*")
_international = re.compile(r"\+.*")
_numeric = re.compile(r"\+\d*$")

def mobile_number(mobile):
  # The standard mobile number validation method django.core.validators.isValidPhone
  # is not suitable for us, as it expects only US numbers in hyphen-format.
  field = "mobile"
  if len(mobile) < 9:
    raise exception.ValidationError("Your mobile phone should be at least 9 digits long including the '+'", field)
  if not _international.match(mobile):
    raise exception.ValidationError("Your mobile number must be in the international format with a '+' in front of it.", field)
  if not _numeric.match(mobile):
    raise exception.ValidationError("Your mobile number can only be numbers besides the '+'", field)
  if _italian.match(mobile):
    raise exception.ValidationError("Sorry, Italian numbers are currently blocked due to abuse.", field)

def mobile_number_not_activated(mobile):
  pass

# TODO(mikie): check what we actually want to do to validate emails, this errs
# on the side of permissiveness
_email = re.compile(r"[^@]+@[^@]+\.[^@]+")
def email(email):
  if len(email) < 3 or not _email.match(email):
    raise exception.ValidationError(u"Bạn phải sử dụng một địa chỉ email hợp lệ. \
    Địa chỉ này sẽ được dùng để khôi phục mật khẩu và thông báo cho bạn các tin tức mới.")
  pass

def email_not_activated(email):
  pass

def sms_message(message):
  pass

def full_name(name):
  length(name, 1, 2 * 60 + 1, u"Tên đầy đủ", 'full_name')

def confirm_dangerous(request, message=None):
  # TODO(termie): change the javascript to submit POST messages
  #               and make this only check request.POST
  if "confirm" not in request.REQUEST:
    raise exception.ConfirmationRequiredException(message)

def name(s, message=u"Tên đầy đủ", field='name'):
  length(s, 1, 60, message, field)

def not_banned_name(s, message=None):
  if util.display_nick(s) in banned_names:
    raise exception.ValidationError(u"Bạn không được phép sử dụng tên %s." % s.split("@")[0], "nick")

def privacy(s, message=None): pass

def password(s, message=u"Mật khẩu của bạn"):
  length(s, 6, 16, message, 'password')

def password_and_confirm(password, confirm, message=u"Mật khẩu của bạn",
                         field=None):
  if password != confirm:
    raise exception.ValidationError('The passwords do not match', field)
  length_password(password, 6, 16, message, 'password')

def length(s, min, max, message=None, field=None):
  if len(s) < min or len(s) > max:
    raise exception.ValidationError(
        (message or 'Tin') + u" phải có chiều dài trong khoảng từ %s đến %s ký tự." % (
            min, max),
        field)
  pass

def length_password(s, min, max, message=None, field=None):
  if len(s) < min or len(s) > max:
    raise exception.ValidationError(
        (message or '') + u" phải dài từ %s đến %s ký tự" % (
            min, max),
        field)
  pass

def avatar_photo_size(file):
  # file.size is in bytes
  if file.size > (settings.MAX_AVATAR_PHOTO_KB << 10):
    raise exception.ValidationError(
        "Avatar photo size must be under %s kilobytes"
        % (settings.MAX_AVATAR_PHOTO_KB,))
  pass

def location(s, message=None):
  pass

def uuid(s, message=None):
  pass

def stream(s, message=None):
  pass

def entry(s, message=None):
  pass

def user_nick(s, message=None):
  pass

def presence_extra(d, message=None):
  allowed_keys = set(['status', 'availability', 'location', 'submit-location',
                      'senders_timestamp', 'activity',
                      'profile', 'presenceline', 'presenceline',
                      'bt', 'calendar', 'generated',
                      's60_settings'])
  if len(allowed_keys.union(set(d.keys()))) != len(allowed_keys):
    raise exception.ValidationError('illegal keys in presence')


def description(s, message=None):
  pass

def external_url(s, message=None):
  pass
