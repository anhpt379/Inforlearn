""" A library to export some stats that we can use for monitoring.
"""

def export(values):
  o = []
  for k, v in sorted(values.items()):
    o.append('%s %s' % (escape(k), build_value(v)))
  return '\n'.join(o)

class ExportedMap(object):
  def __init__(self, label, value):
    self.label = label
    self.value = value

  def __str__(self):
    o = ['map:%s' % escape(self.label)]
    for k, v in sorted(self.value.items()):
      o.append('%s:%s' % (escape(k), escape(v)))
    return ' '.join(o)

class ExportedList(object):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return '/'.join([escape(v) for v in self.value])

class ExportedCallable(object):
  def __init__(self, callable):
    self.callable = callable

  def __str__(self):
    return make_value(self.callable())

def build_value(value):
  """ attempt to do some inference of types """
  # a dict, with label
  if type(value) is type(tuple()) and type(value[1]) is type(dict()):
    return ExportedMap(label=value[0], value=value[1])
  elif type(value) is type(tuple()) or type(value) is type(list()):
    return ExportedList(value)
  elif callable(value):
    return ExportedCallable(value)
  else:
    return escape(value)

def escape(value):
  return str(value).replace('\\', '\\\\').replace(':', '\\:').replace(' ', '-')
