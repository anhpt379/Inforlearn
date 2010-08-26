#! coding: utf-8
# pylint: disable-msg=W0311
from django import http
from django import template
from django.template import loader
from common import decorator


@decorator.cache_forever
def flat_tour(request, page='create'):
  page_num = ['create', 'contacts', 'mobile', 'faqs'].index(page) + 1

  # config for template
  green_top = True
  sidebar_green_top = True
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
    'index': 'Thông tin liên hệ',
    'sms': 'Gửi tin qua tin nhắn SMS',
    'im': 'Gửi và nhận tin qua IM Client',
    'commands': 'Cú pháp khi sử dụng IM Client',
    'im_clients': "Danh sách IM Client hỗ trợ XMPP"
  }

  path = paths[page]

  # config for template
  green_top = False

  c = template.RequestContext(request, locals())

  t = loader.get_template('flat/templates/help_%s.html' % page)
  return http.HttpResponse(t.render(c))

