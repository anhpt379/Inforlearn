#!/bin/sh
mv .local_settings.py local_settings.py
python2.6 manage.py update -e AloneRoad@Gmail.com
mv local_settings.py .local_settings.py
rm -f local_settings.pyc
