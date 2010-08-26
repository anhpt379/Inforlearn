from common import util
from common.models import CachingModel

class CacheMiddleware(object):
  def process_request(self, request):
    CachingModel.enable_cache(True)
    CachingModel.reset_cache()

  def process_response(self, request, response):
    # don't cache anything by default
    # we'll set caching headers manually on appropriate views if they should
    # be cached anyway
    # TODO(termie): add the caching headers
    response = util.add_caching_headers(response, util.CACHE_NEVER_HEADERS)
    return response
