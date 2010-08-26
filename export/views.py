#! coding: utf-8
## GAE Datastore export tools
#
# TODO: 
#   * zip data before return
#   * secure this

from django.http import HttpResponse
from common.models import Relation, StreamEntry, File
from google.appengine.ext import db
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from zlib import compress

line_format = "%s\t%s"

def channel_members(request):
  if not os.getenv('SERVER_SOFTWARE', '').startswith('Dev'):
    if not users.is_current_user_admin():
      if users.get_current_user() is None:
        print 'Status: 302'
        print 'Location:', users.create_login_url(os.getenv('PATH_INFO', ''))
      else:
        print 'Status: 403'
        print
        print 'Forbidden'
      return
    
  query = Relation.gql("WHERE relation = :1", "channelmember")
  data = []
  limit = 1000
  offset = 0
  while True:
    results = query.fetch(limit, offset)
    if results == []:
      break
    offset += limit
    for i in results:
      data.append(line_format % (i.owner, i.target))
  content = str("\n".join(x for x in data))
  
  params = {"key_name": "archive/channel_members.zlib",
            "content": db.Blob(compress(content, 9))}
  file = File(**params)
  file.put()
  path = 'Download <a href="http://inforlearn.appspot.com/archive/channel_members.zlib">here</a>'
  return HttpResponse(path)

def user_contacts(request):
  if not os.getenv('SERVER_SOFTWARE', '').startswith('Dev'):
    if not users.is_current_user_admin():
      if users.get_current_user() is None:
        print 'Status: 302'
        print 'Location:', users.create_login_url(os.getenv('PATH_INFO', ''))
      else:
        print 'Status: 403'
        print
        print 'Forbidden'
      return
    
  query = Relation.gql("WHERE relation = :1", "contact")
  data = []
  limit = 1000
  offset = 0
  while True:
    results = query.fetch(limit, offset)
    if results == []:
      break
    offset += limit
    for i in results:
      data.append(line_format % (i.owner, i.target))
  content = str("\n".join(x for x in data))
  
  params = {"key_name": "archive/user_contacts.zlib",
            "content": db.Blob(compress(content, 9))}
  file = File(**params)
  file.put()
  path = 'Download <a href="http://inforlearn.appspot.com/archive/user_contacts.zlib">here</a>'
  return HttpResponse(path)

def channel_admins(request):
  if not os.getenv('SERVER_SOFTWARE', '').startswith('Dev'):
    if not users.is_current_user_admin():
      if users.get_current_user() is None:
        print 'Status: 302'
        print 'Location:', users.create_login_url(os.getenv('PATH_INFO', ''))
      else:
        print 'Status: 403'
        print
        print 'Forbidden'
      return
    
  query = Relation.gql("WHERE relation = :1", "channeladmin")
  data = []
  limit = 1000
  offset = 0
  while True:
    results = query.fetch(limit, offset)
    if results == []:
      break
    offset += limit
    for i in results:
      data.append(line_format % (i.owner, i.target))
  content = str("\n".join(x for x in data))
  
  params = {"key_name": "archive/channel_admins.zlib",
            "content": db.Blob(compress(content, 9))}
  file = File(**params)
  file.put()
  path = 'Download <a href="http://inforlearn.appspot.com/archive/channel_admins.zlib">here</a>'
  return HttpResponse(path)

def user_history(request):
  " owner | actor "  
  if not os.getenv('SERVER_SOFTWARE', '').startswith('Dev'):
    if not users.is_current_user_admin():
      if users.get_current_user() is None:
        print 'Status: 302'
        print 'Location:', users.create_login_url(os.getenv('PATH_INFO', ''))
      else:
        print 'Status: 403'
        print
        print 'Forbidden'
      return
    
  query = StreamEntry.all()
  data = []
  limit = 1000
  offset = 0
  while True:
    entries = query.fetch(limit, offset)
    if entries == []:
      break
    offset += limit
    for entry in entries:
      if not entry.deleted_at and (entry.owner != entry.actor):  # if entry not marked as deleted
        data.append(line_format % (entry.owner, entry.actor))
    content = "\n".join(x for x in data)
  
  params = {"key_name": "archive/user_history.zlib",
            "content": db.Blob(compress(content, 9))}
  file = File(**params)
  file.put()
  path = 'Download <a href="http://inforlearn.appspot.com/archive/user_history.zlib">here</a>'
  return HttpResponse(path)

def user_comments(request):      
  if not os.getenv('SERVER_SOFTWARE', '').startswith('Dev'):
    if not users.is_current_user_admin():
      if users.get_current_user() is None:
        print 'Status: 302'
        print 'Location:', users.create_login_url(os.getenv('PATH_INFO', ''))
      else:
        print 'Status: 403'
        print
        print 'Forbidden'
      return
    
  query = StreamEntry.all()
  data = []
  limit = 1000
  offset = 0
  while True:
    entries = query.fetch(limit, offset)
    if entries == []:
      break
    offset += limit
    for entry in entries:
      if not entry.deleted_at:  # if entry not marked as deleted
        entry_key = entry.entry
        if entry.owner.startswith("#") and entry_key is not None:  # has content of comment
#          print line_format % (entry.actor, entry_key)
          data.append(line_format % (entry.actor, entry_key))
    content = "\n".join(x for x in data)
  
  params = {"key_name": "archive/user_comments.zlib",
            "content": db.Blob(compress(content, 9))}
  file = File(**params)
  file.put()
  path = 'Download <a href="http://www.inforlearn.com/archive/user_comments.zlib">here</a>'
  return HttpResponse(path)