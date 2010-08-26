#! coding: utf-8
import logging
import re

from django.conf import settings

from common import api
from common import clean
from common import exception
from common import patterns
from common import user
from common import util
from common.protocol import base


HELP_HUH = "Lệnh \"%s\" không đúng. Gõ HELP để xem danh sách các lệnh được hỗ trợ"
HELP_WELCOME = u"Chào bạn, %s!\n"
HELP_WELCOME_NICK = u"Chào bạn, %s!\n"
HELP_NOT_SIGNED_IN = u"Bạn đã đăng xuất khỏi tài khoản của mình\n"
HELP_SIGNED_IN_AS = u"Bạn đã đăng nhập với tên '%s'\n"
HELP_FOLLOW_ONLY = u"You are signed in as a follow-only user\n"
HELP_PASSWORD = u"Mật khẩu của bạn là: %s\n" \
                u"Sử dụng nó để đăng nhập trên website Inforlearn tại địa chỉ http://%s/\n" % ('%s', settings.DOMAIN)
HELP_POST = u"- Để gửi tin, gõ nội dung muốn gửi và nhấn Enter"
HELP_CHANNEL_POST = u"- Thêm #channelid vào đầu tin nhắn để gửi tin vào một nhóm"
HELP_COMMENT = u"- Thêm @user để bình luận cho tin vừa nhận được từ người gửi"
HELP_FOLLOW = u"- Để gia nhập một nhóm hoặc xin kết bạn với một người, gõ FOLLOW <user/#channel>"
HELP_FOLLOW_NEW = u"- Gõ FOLLOW <user/#channel> để nhận tin nhắn từ một người hoặc một nhóm mà không cần đăng ký"
HELP_LEAVE = u"- Để ngừng nhận tin từ một người hoặc một nhóm, gõ LEAVE <user/#channel>"
HELP_STOP = u"- Để dừng nhận mọi thông báo, gõ STOP"
HELP_START = u"- Để tiếp tục nhận thông báo, gõ START"
HELP_SIGN_OUT = u"- Để đăng xuất, gõ SIGN OUT"
HELP_DELETE_ME = u"- Để xóa tài khoản của bạn, gõ DELETE ME"
HELP_SIGN_IN = u"- Để đăng nhập, gõ SIGN IN <username> <password>"
HELP_SIGN_UP = u"- Để đăng ký tài khoản, gõ SIGN UP <username>"
HELP_MORE = u"- Để xem danh sách các lệnh hỗ trợ, gõ HELP"
HELP_FOOTER = u"\n" \
              u"Hãy xem qua hướng dẫn tại http://%s/help/im\n"  \
              u"Nếu gặp khó khăn hãy liên hệ với chúng tôi qua email support@inforlearn.com hoặc gửi câu hỏi trực tiếp tại http://support.inforlearn.com/" % (settings.DOMAIN)
HELP_FOOTER_INFORMAL = u"\n" \
                       u"Hướng dẫn sử dụng: http://%s/help/im" % (settings.DOMAIN)
HELP_OTR = u"Your IM client has tried to initiate an OTR (off-the-record) session. However, this bot does not support OTR."

HELP_START_NOTIFICATIONS = u"Chế độ thông báo qua IM đã được kích hoạt. Gõ STOP để vô hiệu hóa, HELP để được giúp đỡ."

HELP_STOP_NOTIFICATIONS = u"Chế độ thông báo qua IM đã được vô hiệu hóa. Gõ START để kích hoạt lại, HELP để được giúp đỡ."

# TODO(tyler): Merge with validate/clean/nick/whatever
NICK_RE = re.compile(r"""^[a-zA-Z][a-zA-Z0-9]{2,15}$""")


class ImService(base.Service):
  handlers = [patterns.SignInHandler,
              patterns.SignOutHandler,
              patterns.PromotionHandler,
              patterns.HelpHandler,
              patterns.CommentHandler,
              patterns.OnHandler,
              patterns.OffHandler,
              patterns.ChannelPostHandler,
              patterns.FollowHandler,
              patterns.LeaveHandler,
              patterns.PostHandler,
              ]


  # TODO(termie): the following should probably be part of some sort of
  #               service interface
  def response_ok(self, rv=None):
    return ""

  def response_error(self, exc):
    return str(exc)

  def channel_join(self, from_jid, nick):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError(
          "Bạn phải đăng nhập để thực hiện thao tác này.\nĐể đăng nhập, gõ SIGN IN <username> <password> và nhấn Enter")
    channel = clean.channel(nick)

    try:
      api.channel_join(jid_ref, jid_ref.nick, channel)
      self.send_message((from_jid,),
                        u"Success ^^\n Giờ bạn đã là thành viên của nhóm %s" % (channel.split('@')[0]))

    except:
      self.send_message((from_jid,), "Error :(")

  def channel_part(self, from_jid, nick):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn phải đăng nhập trước khi thực hiện thao tác này")
    channel = clean.channel(nick)

    try:
      api.channel_part(jid_ref, jid_ref.nick, channel)
      self.send_message((from_jid,), u"Success! \nBạn đã rời khỏi nhóm %s" % (channel.split('@')[0]))

    except:
      self.send_message((from_jid,), "Error :(")

  def actor_add_contact(self, from_jid, nick):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError(
          "Bạn phải đăng nhập trước khi thực hiện thao tác này")
    nick = clean.nick(nick)

    try:
      api.actor_add_contact(jid_ref, jid_ref.nick, nick)
      self.send_message((from_jid,), u"Success ^^")

    except:
      self.send_message((from_jid,), "Error :(")

  def actor_remove_contact(self, from_jid, nick):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn phải đăng nhập trước khi thực hiện thao tác này")
    nick = clean.nick(nick)

    try:
      api.actor_remove_contact(jid_ref, jid_ref.nick, nick)
      self.send_message((from_jid,), u"Success ^^")

    except:
      self.send_message((from_jid,), "Error :(")

  def send_message(self, to_jid_list, message):
    self.connection.send_message(to_jid_list, message)

  def unknown(self, from_jid, message):
    self.send_message([from_jid], HELP_HUH % message)

  def sign_in(self, from_jid, nick, password):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if jid_ref:
      raise exception.ValidationError(
          "Bạn đang đăng nhập với tên %s, vui lòng gõ SIGN OUT trước" % jid_ref.nick.split("@")[0])

    user_ref = user.authenticate_user_login(nick, password)
    if not user_ref:
      raise exception.ValidationError("Tên đăng nhập / mật khẩu không hợp lệ")

    api.im_associate(api.ROOT, user_ref.nick, from_jid.base())

    welcome = '\n'.join([HELP_WELCOME_NICK % user_ref.display_nick(),
                         HELP_MORE,
                         HELP_FOOTER])

    self.send_message([from_jid], welcome)

  def sign_out(self, from_jid):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn chưa đăng nhập. Để đăng nhập, gõ SIGN IN <username> <password> và nhấn Enter")

    api.im_disassociate(api.ROOT, jid_ref.nick, from_jid.base())

    self.send_message([from_jid], u"Tạm biệt! Hẹn gặp lại ^^")

  def help(self, from_jid):
    welcome = '\n'.join([HELP_POST,
                         HELP_CHANNEL_POST,
                         HELP_COMMENT,
                         HELP_FOLLOW,
                         HELP_LEAVE,
                         HELP_STOP,
                         HELP_SIGN_IN,
                         HELP_SIGN_OUT,
                         HELP_MORE,
                         HELP_FOOTER])

    self.send_message([from_jid], welcome)

  def start_notifications(self, from_jid):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn phải đăng nhập trước khi thực hiện thao tác này")

    api.settings_change_notify(api.ROOT, jid_ref.nick, im=True)

    self.send_message([from_jid], HELP_START_NOTIFICATIONS)

  def stop_notifications(self, from_jid):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn phải đăng nhập trước khi thực hiện thao tác này")

    api.settings_change_notify(api.ROOT, jid_ref.nick, im=False)

    self.send_message([from_jid], HELP_STOP_NOTIFICATIONS)

  def post(self, from_jid, message):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn phải đăng nhập trước khi thực hiện thao tác này")
    api.post(jid_ref, nick=jid_ref.nick, message=message)

  def channel_post(self, from_jid, channel_nick, message):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError("Bạn phải đăng nhập trước khi thực hiện thao tác này")

    api.channel_post(
        jid_ref,
        message=message,
        nick=jid_ref.nick,
        channel=channel_nick
    )

  def add_comment(self, from_jid, nick, message):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if not jid_ref:
      raise exception.ValidationError(
          "Bạn phải đăng nhập trước khi thực hiện thao tác này")

    logging.debug("comment: %s %s %s", nick, jid_ref.nick, message)

    nick = clean.nick(nick)
    stream_entry = api.reply_get_cache(sender=nick,
                                       target=jid_ref.nick,
                                       service='im')
    if not stream_entry:
      # Well, or memcache timed it out...  Or we crashed... Or... Or...
      raise exception.ValidationError(
          'Tin nhắn bạn muốn trả lời không tồn tại')

    api.entry_add_comment(jid_ref, entry=stream_entry.keyname(),
                          content=message, nick=jid_ref.nick,
                          stream=stream_entry.stream)

  def promote_user(self, from_jid, nick):
    jid_ref = api.actor_lookup_im(api.ROOT, from_jid.base())
    if jid_ref:
      # TODO(tyler): Should we tell the user who they are?
      raise exception.ValidationError("Bạn đã có tài khoản và đang đăng nhập hệ thống.")

    if not NICK_RE.match(nick):
      raise exception.ValidationError(
          "Tên bạn chọn phải sử dụng các ký tự từ A-Z, a-z, 0-9 và dài từ 3 tới 16 ký tự")

    # Create the user.  (user_create will check to see if the account has
    # already been created.)
    password = util.generate_uuid()[:8]

    # TODO(termie): Must have a first/last name. :(
    api.user_create(api.ROOT, nick=nick, password=password,
                            fullname_name=nick)

    # link this im account to the user's account (equivalent of SIGN IN)
    self.sign_in(from_jid, nick, password)

    # Inform the user of their new password
    welcome = HELP_WELCOME_NICK % nick

    self.send_message([from_jid], welcome)
