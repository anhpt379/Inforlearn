#! coding: utf-8
import logging
import traceback

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings

from common import exception
from common import util


class ExceptionMiddleware(object):
  def process_exception(self, request, exc):
    if isinstance(exc, exception.RedirectException):
      url = exc.build_url(request)
      return HttpResponseRedirect(url)
    if isinstance(exc, exception.Error):
      logging.warning("RedirectError: %s", traceback.format_exc())
      return util.RedirectError(exc.message.encode('utf-8'))
    if not isinstance(exc, Http404):
      logging.error("5xx: %s", traceback.format_exc())
    if settings.DEBUG and not isinstance(exc, Http404):
      # fake out the technical_500_response because app engine
      # is annoying when it tries to rollback our stuff on 500
      import sys
      from django.views import debug
      exc_info = sys.exc_info()
      reporter = debug.ExceptionReporter(request, *exc_info)
      html = reporter.get_traceback_html()
      return HttpResponse(html, mimetype='text/html')
    return None
