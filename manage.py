#!/usr/bin/env python

# import __main__ as a way to pass a variable into the settings file
import logging
import os
import sys

logging.getLogger().setLevel(logging.INFO)

import build
build.bootstrap(only_check_for_zips=True)

for x in os.listdir('.'):
  if x.endswith('.zip'):
    if x in sys.path:
      continue
    logging.debug("Adding %s to the sys.path", x)
    sys.path.insert(1, x)

from appengine_django import InstallAppengineHelperForDjango

InstallAppengineHelperForDjango()

from common import component
component.install_components()

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
  execute_manager(settings)
