from google.appengine.api import xmpp

def send_message(jids, body, from_jid=None,
                 message_type=xmpp.MESSAGE_TYPE_CHAT, raw_xml=False):
  return xmpp.send_message(jids, body, from_jid, message_type, raw_xml)


def from_request(cls, request):
  params = {'sender': request.REQUEST.get('from'),
            'target': request.REQUEST.get('to'),
            'message': request.REQUEST.get('body'),
            }
  return cls(**params)

