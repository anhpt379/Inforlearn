import logging
import os.path
from django.conf import settings


# public variable with the intent of referencing it in templates
# and allowing tests to easily adjust the values
loaded = {}

def install_components():
  global loaded
  root_dir = os.path.dirname(os.path.dirname(__file__))
  component_dir = os.path.join(root_dir, 'components')

  possibles = os.listdir(component_dir)
  logging.info("Trying to load components in %s...", possibles)
  for p in possibles:
    # verify that we haven't manually disabled this in settings
    is_enabled = getattr(settings, 'COMPONENT_%s_DISABLED' % (p.upper()), True)
    if not is_enabled:
      continue

    path = os.path.join(component_dir, p)
    if not os.path.isdir(path):
      logging.debug("Not a dir %s", p)
      continue

    try:
      loaded[p] = __import__('components.%s' % p, {}, {}, p)
      logging.debug('Loaded component: %s', p)
    except ValueError:
      # bad module name, things like .svn and whatnot trigger this
      continue
    except ImportError:
      import traceback
      logging.debug('Exception loading component: %s', traceback.format_exc())
      continue

def include(*names):
  global loaded
  for name in names:
    rv = loaded.get(name)
    if rv:
      return rv
  return rv

def require(*names):
  mod = include(*names)
  if not mod:
    raise Exception("Ultimate doom")
  return mod

class LoadedOrDummy(object):
  def __getitem__(self, key):
    rv = include(key, "dummy_%s" % key)
    if not rv:
      raise KeyError(key)
    return rv

  def __contains__(self, key):
    rv = include(key, "dummy_%s" % key)
    if rv:
      return True
    return False

best = LoadedOrDummy()
