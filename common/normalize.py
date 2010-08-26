from django.conf import settings

def mobile_number(mobile):
  return mobile

def sms_message(message):
  return message

def nick(nick):
  if not nick or len(nick) == 0:
    return None
  if not '@' in nick:
    return '%s@%s' % (nick, settings.NS_DOMAIN)
  else:
    return nick

def email(email):
  return email

def channel(channel):
  if not channel or len(channel) == 0:
    return None
  if channel[0:1] != '#':
    channel = '#' + channel
  if not '@' in channel:
    return '%s@%s' % (channel, settings.NS_DOMAIN)
  else:
    return channel
