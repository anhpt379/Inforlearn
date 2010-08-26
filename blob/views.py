import logging
import re
from django import http
from common import decorator
from common import exception
from common import api
from common.models import File
from common.slimmer import css_slimmer
from common.jsmin import jsmin
from cachepy import cachepy as cache

@decorator.cache_forever
def blob_image_jpg(request, nick, path):
  try:
    img = api.image_get(request.user, nick, path, format='jpg')
    if not img:
      return http.HttpResponseNotFound()
    content_type = "image/jpg"
    response = http.HttpResponse(content_type=content_type)
    response.write(img.content)
    return response
  except exception.ApiException, e:
    logging.info("exc %s", e)
    return http.HttpResponseForbidden()
  except Exception:
    return http.HttpResponseNotFound()

def get_archive(request):
  try:
    key_name = request.path_info[1:] # remove '/' at begin of path
    file = File.get_by_key_name(key_name)
    if not file:
      return http.HttpResponseNotFound()
    content_type = "application/x-deflate"
    response = http.HttpResponse(content_type=content_type)
    response.write(file.content)
    return response  
  except Exception:
    return http.HttpResponseNotFound()
  
@decorator.cache_forever
def css(request):
  content_type = "text/css"
  response = http.HttpResponse(content_type=content_type)
  
  path = request.path_info[1:] # remove '/' at begin of path
  css_data = cache.get(path)
  if css_data:
    response.write(css_data)
    return response
  
  try:
    css_data = open(path).read()
  except IOError:
    return http.HttpResponseNotFound()
  
  css_data = css_slimmer(css_data)
  cache.set(path, css_data)
  
  response.write(css_data)
  return response

@decorator.cache_forever
def js(request):
  content_type = "text/x-js"
  response = http.HttpResponse(content_type=content_type)
  
  path = request.path_info[1:] # remove '/' at begin of path
  js_data = cache.get(path)
  if js_data:
    response.write(js_data)
    return response
  
  try:
    js_data = open(path).read()
  except IOError:
    return http.HttpResponseNotFound()
  
  js_data = jsmin(js_data)
  cache.set(path, js_data)
  
  response.write(js_data)
  return response
  