#! coding: utf-8
from common import exception

class Connection(object):
  pass

class Service(object):
  connection = None
  handlers = None
  _handlers = None

  def __init__(self, connection):
    self.connection = connection
    self._handlers = []

  def init_handlers(self):
    if not self.handlers:
      return

    for handler_class in self.handlers:
      self._handlers.append(handler_class(self))

  def handle_message(self, sender, target, message):
    matched = None
    handler = None
    for h in self._handlers:
      matched = h.match(sender, message)
      if matched:
        handler = h
        break

    if not matched:
      rv = self.unknown(sender, message)
      return self.response_ok(rv)

    try:
      rv = handler.handle(sender, matched, message)
      return self.response_ok(rv)
    except exception.UserVisibleError, e:
      exception.log_exception()
      self.send_message([sender], str(e))
      return self.response_error(e)
    except exception.Error:
      exception.log_exception()
