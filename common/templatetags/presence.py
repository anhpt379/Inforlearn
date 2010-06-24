from django import template

register = template.Library()

@register.filter(name="location")
def location(value, arg=None):
  if type(value) is type('str') or type(value) is type(u'ustr'):
    return value

  try:
    country = value.get('country', {}).get('name', None)
    city = value.get('city', {}).get('name', None)
    base = value.get('base', {}).get('current', {}).get('name', None)
    cell = value.get('cell', {}).get('name', None)
    parts = []
    if base:
      parts.append(base)
    elif cell:
      parts.append(cell)
    if city:
      parts.append(city)
    if country:
      parts.append(country)
    return ', '.join(parts)
  except Exception:
    return '?'
