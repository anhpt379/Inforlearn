#! coding: utf-8
# pylint: disable-msg=W0311
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from django import http
from django import template
from django.conf import settings
from django.template import loader

from common import decorator

@decorator.cache_forever
def flat_tour(request, page='create'):
  page_num = ['create', 'contacts', 'mobile', 'faqs'].index(page) + 1

  # config for template
  green_top = True
  area = 'tour'

  c = template.RequestContext(request, locals())
  t = loader.get_template('flat/templates/tour_%s.html' % page)
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_about(request):
  sidebar_green_top = True

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/about.html')
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_privacy(request):
  # for template
  sidebar_green_top = True

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/privacy.html')
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_roadmap(request):
  # for template
  sidebar_green_top = True

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/roadmap.html')
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_sourcecode(request):
  # for template
  sidebar_green_top = True

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/sourcecode.html')
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_terms(request):
  # for template
  sidebar_green_top = True

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/terms.html')
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_press(request):
  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/terms.html')
  return http.HttpResponse(t.render(c))

@decorator.cache_forever
def flat_help(request, page='index'):
  paths = {
    'index': 'Inforlearn - Các câu hỏi thường gặp',
    'sms': 'Gửi tin qua tin nhắn SMS',
    'im': 'Gửi tin thông qua Instant Messaging',
    'commands': 'Cú pháp khi sử dụng SMS và IM',
  }

  path = paths[page]

  # config for template
  green_top = False

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/help_%s.html' % page)
  return http.HttpResponse(t.render(c))

