#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    Copyright (C) 2008 Sylvain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import os, random, string
import mimetypes
import tornado.web
import tornado.wsgi
import tornado.escape

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app

_DEBUG = True

class File(db.Model):
    name = db.StringProperty(indexed=False)
    length = db.IntegerProperty(indexed=False)
    data = db.BlobProperty()
    del_key = db.StringProperty(indexed=False)
    owner = db.UserProperty()
    date = db.DateTimeProperty(auto_now=True)

class BaseRequestHandler(tornado.web.RequestHandler):
    """Implements Google Accounts authentication methods."""
    def get_current_user(self):
        user = users.get_current_user()
        if user: user.administrator = users.is_current_user_admin()
        return user

    def get_login_url(self):
        return users.create_login_url(self.request.uri)
    
    def generate(self, template_name, template_values={}):
        values = {'users': users,
                  'print_file_link': print_file_link}
        values.update(template_values)
        self.render(template_name, **values)
        
class MainPage(BaseRequestHandler):
    def get(self):
        
        if self.current_user:
            files = File.all()
            files.order('-date')
            if not self.current_user.administrator:
                files.filter('owner = ', users.get_current_user())
            files = files.fetch(13)
        else:
            files = []
        template_values = {'files': files}
        self.generate('base.html', template_values)
        
class UploadifyUpload(BaseRequestHandler):
    def post(self):
        
        if 'Filedata' in self.request.files:
            
            user = self.get_argument('user', None)
            if user == 'None':
                owner = None
            else:
                owner = users.User(user)
            
            file_data = self.request.files['Filedata'][0]
            file_name = file_data['filename']
            file = File()
            file.name = file_name
            file.del_key = random_string(10)
            data = file_data['body']
            file.data = db.Blob(data)
            file.length = len(data)
            file.owner = owner
            file.put()
            id = str(file.key().id())
            memcache.add(id, file)
            self.write(print_file_link(file))
 
class Download(BaseRequestHandler):
    def get(self, id, filename):
        
        file = get_file(id)
        if file and tornado.escape.url_escape(file.name, quote_plus=False) == filename:
            
            if self.get_argument('del', None) == file.del_key:
                file.delete()
                
                if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return self.write(id)
                return self.redirect('/')
            
            type_mime = mimetypes.guess_type(filename)[0]
            if type_mime is None:
                type_mime = 'application/octet-stream'
            
            self.set_header('Content-Type', type_mime)
            cd = 'attachment; filename="%s"' % file.name
            self.set_header('Content-Disposition', cd)
            self.write(file.data)
        else:
            self.redirect('/') 
            
def print_file_link(file):
    id = str(file.key().id())
    path = '%s/%s' % (id, file.name)
    link = '<a href="%s">%s</a>' % (path, file.name)
    del_href = 'href="%s?del=%s" class="delete"' %  (path, file.del_key)
    return '<li id="file' + id + '">' + link + '<a ' + del_href + '><b>del</b></a></li>'

#===============================================================================
# # class UploadifyCheck(BaseRequestHandler):
#    def post(self):
#        
#        params = self.request.params
#        folder = self.request.get('folder', None)
#        files = {}
#        for key, file_name in params.items():
#            if key == u'folder':
#                continue
#            path = folder + u"/" + file_name
#            
#            m = hashlib.md5()
#            m.update(path.encode('utf-8'))
#            key_name = m.hexdigest()
# 
#            file = File.get_by_key_name(key_name)
#            if file:
#                files[key] = file_name
# 
#        self.response.out.write(simplejson.dumps(files))
#===============================================================================


def random_string(length=25):
    return ''.join([random.choice(string.ascii_letters + string.digits) 
                    for x in xrange(length)])

def get_file(id):
    file = memcache.get(id)
    if file is not None:
        return file
    else:
        file = File.get_by_id(long(id))
        memcache.add(id, file)
    return file

settings = {
    "debug": os.environ['SERVER_SOFTWARE'].startswith('Dev'),
    "app_title": u"Uploadify",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    }

application = tornado.wsgi.WSGIApplication([
                (r'/', MainPage),
                (r'/uploadify/upload', UploadifyUpload),
                (r'/([0-9]+)/(.*)', Download),
                ], **settings)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
