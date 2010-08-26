from django import template
from common.util import safe

register = template.Library()

@register.filter(name="vcard_full")
@safe
def vcard_full(value, arg=None):
  return value.shortnick()

