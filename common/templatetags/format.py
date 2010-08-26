#! coding: utf-8
# pylint: disable-msg=W0311
import datetime
import re
from os import listdir
from random import choice
from markdown import markdown2
from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.timesince import timesince
from common.util import safe, display_nick, url_nick
from common import clean
from common import models
from common.memcache import client as memcache

register = template.Library()

link_regex = re.compile(r'\[([^\]]+)\]\((http[^\)]+)\)')

r'(^|\s|>)([A-Za-z][A-Za-z0-9+.-]{1,120}:[A-Za-z0-9/](([A-Za-z0-9$_.+!*,;/?:@&~=-])|%[A-Fa-f0-9]{2}){1,333}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*,;/?:@&~=%-]{0,1000}))?)'

# lifted largely from: 
# http://www.manamplified.org/archives/2006/10/url-regex-pattern.html
autolink_regex = re.compile(r'(^|\s|>)([A-Za-z][A-Za-z0-9+.-]{1,120}:[A-Za-z0-9/](([A-Za-z0-9$_.+!*,;/?:@&~=-])|%[A-Fa-f0-9]{2}){1,333}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*,;/?:@&~=%-]{0,1000}))?)')
bold_regex = re.compile(r'\*([^*]+)\*')
italic_regex = re.compile(r'_([^_]+)_')
emoticons_style = "style='display: inline; vertical-align: middle; margin-bottom: 7px;'"
emoticons = [
[":))", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/21.gif'>"],
[':)]', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/100.gif'>"],
[":((", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/20.gif'>"],
[":)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/1.gif'"],
[':(|)', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/51.gif'>"],
[":(", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/2.gif'>"],
[";)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/3.gif'>"],
[":D", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/4.gif'>"],
[";;)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/5.gif'>"],
[">:D<", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/6.gif'>"],
[":-/", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/7.gif'>"],
[":x", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/8.gif'>"],
[':">', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/9.gif'>"],
[":P", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/10.gif'>"],
[":-*", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/11.gif'>"],
["=((", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/12.gif'>"],
[":-O", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/13.gif'>"],
["X(", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/14.gif'>"],
[":>", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/15.gif'>"],
["B-)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/16.gif'>"],
[":-S", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/17.gif'>"],
["#:-S", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/18.gif'>"],
[">:)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/19.gif'>"],
[":|", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/22.gif'>"],
["/:)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/23.gif'>"],
["=))", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/24.gif'>"],
["O:)", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/25.gif'>"],
[":-B", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/26.gif'>"],
["=;", "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/27.gif'>"],
[':-c', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/101.gif'>"],
['~X(', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/102.gif'>"],
[':-h', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/103.gif'>"],
[':-t', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/104.gif'>"],
['8->', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/105.gif'>"],
['I-|', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/28.gif'>"],
['8-|', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/29.gif'>"],
['L-)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/30.gif'>"],
[':-&', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/31.gif'>"],
[':-$', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/32.gif'>"],
['[-(', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/33.gif'>"],
[':O)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/34.gif'>"],
['8-}', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/35.gif'>"],
['<:-P', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/36.gif'>"],
['(:|', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/37.gif'>"],
['=P~', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/38.gif'>"],
[':-?', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/39.gif'>"],
['#-o', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/40.gif'>"],
['=D>', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/41.gif'>"],
[':-SS', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/42.gif'>"],
['@-)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/43.gif'>"],
[':^o', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/44.gif'>"],
[':-w', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/45.gif'>"],
[':-<', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/46.gif'>"],
['>:P', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/47.gif'>"],
['<):)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/48.gif'>"],
['X_X', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/109.gif'>"],
[':!!', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/110.gif'>"],
['\\m/', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/111.gif'>"],
[':-q', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/112.gif'>"],
[':-bd', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/113.gif'>"],
['^#(^', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/114.gif'>"],
[':ar!', "<img src='http://l.yimg.com/a/i/us/msg/emoticons/pirate_2.gif'>"],
[':-??', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/106.gif'>"],
['%-(', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/107.gif'>"],
[':@)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/49.gif'>"],
['3:-O', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/50.gif'>"],
['~:>', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/52.gif'>"],
['@};-', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/53.gif'>"],
['%%-', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/54.gif'>"],
['**==', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/55.gif'>"],
['(~~)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/56.gif'>"],
['~O)', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/57.gif'>"],
['*-:)', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/58.gif'>"],
['8-X', " <img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/59.gif'>"],
['=:)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/60.gif'>"],
['>-)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/61.gif'>"],
[':-L', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/62.gif'>"],
['[-O<', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/63.gif'>"],
['$-)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/64.gif'>"],
[':-"', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/65.gif'>"],
['b-(', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/66.gif'>"],
[':)>-', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/67.gif'>"],
['[-X', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/68.gif'>"],
['\\:D/', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/69.gif'>"],
['>:/', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/70.gif'>"],
[';))', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/71.gif'>"],
[':-@', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/76.gif'>"],
['^:)^', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/77.gif'>"],
[':-j', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/78.gif'>"],
['(*)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/79.gif'>"],
['o->', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/72.gif'>"],
['o=>', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/73.gif'>"],
['o-+', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/74.gif'>"],
['(%)', "<img src='http://us.i1.yimg.com/us.yimg.com/i/mesg/emoticons7/75.gif'>"],
[':bz', "<img src='http://l.yimg.com/us.yimg.com/i/mesg/emoticons7/115.gif'>"],
['[..]', "<img src='http://l.yimg.com/a/i/us/msg/emoticons/transformer.gif'>"]
]

@register.filter(name="format_metadata")
@safe
def format_metadata(value, arg=None):
  """  
  ![text](link) -> text
  [text](link) -> text
  """
  display_text = re.compile("\[.*\]")
  image = re.compile("!\[.*\]\(.*\)")
  matches = image.findall(value)
  if matches:
    value = value.replace(matches[0], display_text.findall(matches[0])[0][1:-1]) # remove '[' and ']'
    
  link = re.compile("\[.*\]\(.*\)")
  matches = link.findall(value)
  if matches:
    value = value.replace(matches[0], display_text.findall(matches[0])[0][1:-1]) # remove '[' and ']'
  return value

@register.filter(name="random_tips")
@safe
def random_tips(value, arg=None):
  files = listdir("channel/templates/tips")
  filename = choice(files)
  value = memcache.get(filename)
  if not value:
    value = open("channel/templates/tips/%s" % choice(files)).read()
    memcache.set(filename, value)
  return value

@register.filter(name="format_emoticons")
@safe
def format_emoticons(value, arg=None):
  for e in emoticons:
    value = value.replace(e[0], e[1].replace("img src", "img %s src" % emoticons_style))
  return value

@register.filter(name="auto_background")
@safe
def auto_background(value, arg=None):
  hour = datetime.datetime.now().hour + 7 # from utc to hanoi
  if hour >= 24:
    hour = hour - 24
  if hour in range(5, 8):
    value = "1" + choice(["a"]) + ".jpg"
  elif hour in range(8, 16):
    value = "2" + choice(["a"]) + ".jpg"
  elif hour in range(16, 19):
    value = "3" + choice(["a"]) + ".jpg"
  else:
    value = "4" + choice(["a"]) + ".jpg"
  return value

@register.filter(name="format_fancy")
@safe
def format_fancy(value, arg=None):
  value = italic_regex.sub(r'<i>\1</i>', value)
  value = bold_regex.sub(r'<b>\1</b>', value)
  return value

@register.filter(name="format_links")
@safe
def format_links(value, arg=None):
  value = link_regex.sub(r'<a href="\2" target=_new>\1</a>', value)
  return value

@register.filter(name="format_autolinks")
@safe
def format_autolinks(value, arg=None):
  value = autolink_regex.sub(r'\1<a href="\2" target="_new">\2</a>', value)
  return value

# TODO(tyler): Combine these with validate
user_regex = re.compile(
    r'@([a-zA-Z][a-zA-Z0-9]{%d,%d})'
    % (clean.NICK_MIN_LENGTH - 1, clean.NICK_MAX_LENGTH - 1)
    )
channel_regex = re.compile(
    r'#([a-zA-Z][a-zA-Z0-9]{%d,%d})'
    % (clean.NICK_MIN_LENGTH - 1, clean.NICK_MAX_LENGTH - 1)
    )

@register.filter(name="format_actor_links")
@safe
def format_actor_links(value, request=None):
  """Formats usernames / channels
  """
#  actor_link = '<a href="%s" rel="user" id="popup_%s">@%s</a>'
#  actor_popup = """
#  <script type='text/javascript'>
#  new Tip("tooltip_{{actor.nick}}", "Tên đầy đủ: {{actor.extra.full_name}}<br>" +
#                                    "Trang cá nhân: <a href='{{actor.extra.homepage}}' target='_new'>{{actor.extra.homepage}}</a><br>" 
#                                  , {
#    title: "{{ actor.display_nick }}",
#    stem: 'bottomRight',
#    hideOn: false,
#    hideAfter: 0.25,
#    delay: 0.5,
#    closeButton: true,
#    hook: {target: 'topMiddle', tip: 'bottomRight'},
#  });
#  </script>
#  """
  value = re.sub(user_regex,
                 lambda match: '<a href="%s" rel="user">@%s</a>' % (
                   models.actor_url(match.group(1), 'user', request=request),
                   match.group(1)),
                 value)

  value = re.sub(channel_regex,
                 lambda match: '<a href="%s" rel="channel">#%s</a>' % (
                   models.actor_url(match.group(1), 'channel', request=request),
                   match.group(1)),
                 value)
  return value

@register.filter(name="format_markdown")
@safe
def format_markdown(value, arg=None):
  return markdown2.markdown(value)

@register.filter(name="format_comment")
@safe
def format_comment(value, request=None):
  content = escape(value.extra.get('content', 'no title'))
  content = format_markdown(content)
  content = format_autolinks(content)
  content = format_actor_links(content, request)
  content = format_emoticons(content)
  return content

@register.filter(name="truncate")
def truncate(value, arg):
  """
  Truncates a string after a certain number of characters. Adds an
  ellipsis if truncation occurs.
  
  Due to the added ellipsis, truncating to 10 characters results in an
  11 character string unless the original string is <= 10 characters
  or ends with whitespace.

  Argument: Number of characters to truncate after.
  """
  try:
    max_len = int(arg)
  except:
    return value # No truncation/fail silently.

  if len(value) > max_len:
    # Truncate, strip rightmost whitespace, and add ellipsis
    return value[:max_len].rstrip() + u"\u2026"
  else:
    return value

@register.filter(name="entry_icon")
@safe
def entry_icon(value, arg=None):
  icon = value.extra.get('icon', None)
  if not icon:
    return ""
  return '<img src="/themes/%s/icons/%s.gif" alt="%s" class="icon" style="margin-left: -5px;"/>' % (settings.DEFAULT_THEME, icon, icon)

@register.filter(name="linked_entry_title")
@safe
def linked_entry_title(value, request=None):
  """
  Returns an entry link.

  value     an entry object.
  request   a HttpRequest (optional).
  """
  content = escape(value.extra.get('title'))
#  content = format_fancy(content)
  content = format_markdown(content)
  content = format_autolinks(content)
  content = format_actor_links(content, request)
  content = format_emoticons(content)
  return content


@register.filter
@safe
def linked_entry_truncated_title(value, arg):
  """
  Returns a link to an entry using a truncated entry title as source anchor.

  Argument: Number of characters to truncate after.
  """
  try:
    max_len = int(arg)
  except:
    max_len = None # No truncation/fail silently.

  if value.is_comment():
    title = escape(truncate(value.extra['entry_title'].replace('\n', ' '),
                            max_len))
  else:
    title = escape(truncate(value.extra['title'].replace('\n', ' '), max_len))

  return '<a href="%s">%s</a>' % (value.url(), title)

@register.filter(name="stream_icon")
@safe
def stream_icon(value, arg=None):
  return '<img src="/themes/%s/icons/feed.png" style="width: 12px; height: 12px;" class="icon" />' % settings.DEFAULT_THEME
  if type(value) is type(1):
    return '<!-- TODO entry icon goes here -->'
  return '<!-- TODO entry icon goes here -->'

@register.filter(name="je_timesince")
@safe
def je_timesince(value, arg=None):
  d = value
  if (datetime.datetime.now() - d) < datetime.timedelta(0, 60, 0):
    return u"0 phút"
  else:
    return timesince(d)

@register.filter
@safe
def entry_actor_link(value, request=None):
  """
  Returns an actor html link.

  value     an entry_actor object.
  request   a HttpRequest (optional).
  """
  return '<a href="%s">%s</a>' % (models.actor_url(url_nick(value),
                                                   'user',
                                                   request=request),
                                  display_nick(value))

class URLForNode(template.Node):
  def __init__(self, entity, request):
    self.entity = template.Variable(entity)
    self.request = template.Variable(request)

  def render(self, context):
    try:
      actual_entity = self.entity.resolve(context)
      actual_request = self.request.resolve(context)

      try:
        return actual_entity.url(request=actual_request)
      except AttributeError:
        # treat actual_entity as a string
        try:
          mobile = actual_request.mobile
        except AttributeError:
          mobile = False

        if mobile and settings.SUBDOMAINS_ENABLED:
          return 'http://m.' + settings.HOSTED_DOMAIN
        else:
          return 'http://' + str(actual_entity)

    except template.VariableDoesNotExist:
      return ''

@register.tag
def url_for(parser, token):
  """
  Custom tag for more easily being able to pass an HttpRequest object to
  underlying url() functions.
  
  One use case is being able to return mobile links for mobile users and
  regular links for others. This depends on request.mobile being set or
  not.

  Observe that if entity is not an object with the method url(), it is
  assumed to be a string.

  Parameters: entity, request.
  """
  try:
    params = token.split_contents()
    entity = params[1]
    request = params[2]

  except ValueError:
    raise template.TemplateSyntaxError, \
      "%r tag requires exactly two arguments" % token.contents.split()[0]
  return URLForNode(entity, request)

class ActorLinkNode(template.Node):
  def __init__(self, actor, request):
    self.actor = template.Variable(actor)
    self.request = template.Variable(request)

  def render(self, context):
    try:
      actual_actor = self.actor.resolve(context)
      actual_request = self.request.resolve(context)

      try:
        url = actual_actor.url(request=actual_request)
        return '<a href="%s">%s</a>' % (url, actual_actor.display_nick())
      except AttributeError:
        return ''
    except template.VariableDoesNotExist:
      return ''

class GoBackLink(template.Node):
  def __init__(self, actor, request):
    self.actor = template.Variable(actor)
    self.request = template.Variable(request)

  def render(self, context):
    try:
      actual_actor = self.actor.resolve(context)
      actual_request = self.request.resolve(context)

      try:
        url = actual_actor.url(request=actual_request)
        return u'<a href="%s">&#171; Quay lại %s</a>' % (url, actual_actor.display_nick())
      except AttributeError:
        return ''
    except template.VariableDoesNotExist:
      return ''

@register.tag
def actor_link(parser, token):
  """
  Custom tag for more easily being able to pass an HttpRequest object to
  underlying url() functions.
  
  One use case is being able to return mobile links for mobile users and
  regular links for others. This depends on request.mobile being set or
  not.

  Parameters: actor, request.
  """
  try:
    params = token.split_contents()
    actor = params[1]
    request = params[2]
  except ValueError:
    raise template.TemplateSyntaxError, \
      "%r tag requires exactly two arguments" % token.contents.split()[0]
  return ActorLinkNode(actor, request)

@register.tag
def go_back(parser, token):
  """
  Custom tag for more easily being able to pass an HttpRequest object to
  underlying url() functions.
  
  One use case is being able to return mobile links for mobile users and
  regular links for others. This depends on request.mobile being set or
  not.

  Parameters: actor, request.
  """
  try:
    params = token.split_contents()
    actor = params[1]
    request = params[2]
  except ValueError:
    raise template.TemplateSyntaxError, \
      "%r tag requires exactly two arguments" % token.contents.split()[0]
  return GoBackLink(actor, request)
@register.filter(name="popup_description")
@safe
def popup_description(value, request=None):
  from django.utils.text import normalize_newlines
  value = normalize_newlines(value)
  value = value.replace("\"", "\\\"")
  return value.replace("\n", "<br>")
  
