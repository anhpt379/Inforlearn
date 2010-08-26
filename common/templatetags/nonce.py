from django import template
from common.util import create_nonce, safe

register = template.Library()

@register.filter(name="nonceparam")
def nonceparam(value, arg):
  nonce = create_nonce(value, arg)
  return "_nonce=%s" % nonce

@register.filter(name="noncefield")
@safe
def noncefield(value, arg):
  nonce = create_nonce(value, arg)
  return '<input type="hidden" name="_nonce" value="%s" />' % nonce


