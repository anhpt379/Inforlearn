import simplejson
from django import template
from common import util

register = template.Library()

@register.filter(name="escapejson")
@util.safe
def escapejson(value, arg=None):
  base = simplejson.dumps(value)
  return base.replace('/', r'\/')
