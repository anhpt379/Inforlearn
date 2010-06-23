#! coding: utf-8
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""User-visible strings for confirmation and flash messages.
"""

__author__ = 'mikie@google.com (Mika Raento)'

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
       'Mobile activation code has been sent.'),
  'actor_add_contact':
      (None,
       'Người này đã được thêm vào danh sách liên hệ của bạn.'),
  'actor_remove' :
      (None,
       'Xóa thành công'),
  'actor_remove_contact':
      (None,
       'Đã xóa khỏi danh sách liên lạc.'),
  'channel_create':
      (None,
       'Tạo nhóm thành công'),
  'channel_join':
      (None,
       'Bạn đã gia nhập nhóm thành công :)'),
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
       'Đã xóa xong.'),
  'entry_remove_comment':
      (None,
       'Đã xóa ý kiến vừa rồi.'),
  'invite_accept':
      (None,
       'Thư mời đã được đồng ý'),
  'invite_reject':
      (None,
       'Thư mời bị từ chối :('),
  'invite_request_email':
      (None,
       'Một thư mời tham gia đã được gửi'),
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
       'Vị trí của bạn đã được cập nhật lại'),
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
       'Comments preferenced stored.'),
  'settings_update_account':
      (None,
       'profile updated'),
  'subscription_remove':
      (None,
       'Unsubscribed.'),
  'subscription_request':
      (None,
       'Subscription requested.'),
}

def confirmation(api_call):
  msg = title(api_call)
  if msg is None:
    return None
  return (u'Bạn chắc chắn muốn ' +
          msg +
          u' chứ?')

def title(api_call):
  if _message_table__.has_key(api_call):
    return _message_table__[api_call][0]
  return None

def flash(api_call):
  return _message_table__[api_call][1]
