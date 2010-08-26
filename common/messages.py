#! coding: utf-8

"""User-visible strings for confirmation and flash messages.
"""

__author__ = 'AloneRoad@Gmail.com'

# api call -> (confirmation message, flash message)
# If the confirmation message is None, no confirmation is required.
_message_table__ = {
  'activation_activate_mobile':
      (None,
       'Đã kích hoạt việc sử dụng điện thoại để cập nhật.'),
  'activation_request_email':
      (None,
       'Một thư xác nhận đã được gửi đến hòm thư của bạn.'),
  'activation_request_mobile':
      (None,
       'Mã số kích hoạt đã được gửi tới điện thoại của bạn.'),
  'actor_add_contact':
      (None,
       'Người này đã được thêm vào danh sách liên hệ của bạn.'),
  'actor_remove' :
      (None,
       'Tài khoản vừa rồi đã được xóa khỏi danh sách liên hệ của bạn.'),
  'actor_remove_contact':
      (None,
       'Tài khoản vừa rồi đã được xóa khỏi danh sách liên hệ của bạn.'),
  'channel_create':
      (None,
       'Tạo nhóm thành công'),
  'channel_join':
      (None,
       'Bạn đã gia nhập thành công :)'),
  'channel_update':
      (None,
       'Các thiết lập dành cho nhóm này đã được cập nhật.'),
  'channel_part':
      (None,
       'Bạn đã rời khỏi nhóm này.'),
  'channel_post':
      (None,
       'Tin nhắn đã gửi thành công :)'),
  'entry_add_comment':
      (None,
       'Ý kiến đã gửi thành công :)'),
  'entry_mark_as_spam':
      (None,
       'Đánh dấu là spam.'),
  'entry_remove' :
      (None,
       'Tin nhắn đã được xóa.'),
  'entry_remove_comment':
      (None,
       'Đã xóa ý kiến vừa rồi.'),
  'invite_accept':
      (None,
       'Thư mời của bạn đã được đồng ý'),
  'invite_reject':
      (None,
       'Thư mời của bạn bị từ chối :('),
  'invite_request_email':
      (None,
       'Một thư mời đã được gửi đến email vừa rồi.'),
  'login_forgot':
      (None,
       'Mật khẩu mới đã được gửi đến hòm thư của bạn'),
  'oauth_consumer_delete':
      ('Xóa khóa này',
       'API Key đã bị xóa!'),
  'oauth_consumer_update':
      (None,
       'API Key information updated'),
  'oauth_generate_consumer':
      (None,
       'New API key generated'),
  'oauth_revoke_access_token':
      (None,
       'API token revoked.'),
  'presence_set':
      (None,
       'Vị trí của bạn đã được cập nhật lại.'),
  'post':
      (None,
       'Tin nhắn đã gửi thành công :)'),
  'settings_change_notify':
      (None,
       'Các thiết lập đã được cập nhật lại thành công.'),
  'settings_change_privacy':
      (None,
       'Các thiết lập đã được cập nhật lại.'),
  'settings_hide_comments':
      (None,
       'Thiết lập của bạn đã được lưu.'),
  'settings_update_account':
      (None,
       'Hồ sơ của bạn đã được cập nhật lại.'),
  'subscription_remove':
      (None,
       'Nguồn tin vừa rồi đã được xóa khỏi danh sách theo dõi của bạn.'),
  'subscription_request':
      (None,
       'Nguồn tin vừa rồi đã được thêm vào danh sách theo dõi của bạn.'),
}

def confirmation(api_call):
  msg = title(api_call)
  if msg is None:
    return None
  return ('Bạn chắc chắn muốn thực hiện?')

def title(api_call):
  if _message_table__.has_key(api_call):
    return _message_table__[api_call][0]
  return None

def flash(api_call):
  return _message_table__[api_call][1]
