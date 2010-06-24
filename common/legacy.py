from django.conf import settings
from common import api
from common import util

def generate_personal_key(actor_ref):
  salt = settings.LEGACY_SECRET_KEY
  nick = actor_ref.display_nick()
  password = actor_ref.password
  to_hash = '%s%sapi_key%s' % (nick, password, salt)
  hashed = util.sha1(to_hash)
  return hashed[10:-12]

def authenticate_user_personal_key(nick, key):
  actor_ref = api.actor_get(api.ROOT, nick)
  check_key = generate_personal_key(actor_ref)

  if check_key != key:
    return None

  actor_ref.access_level = api.WRITE_ACCESS
  return actor_ref

