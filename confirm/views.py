#! coding: utf-8
from common import api
from common import decorator
from common import util

@decorator.login_required
def confirm_email(request, code):
  rel_ref = api.activation_activate_email(request.user,
                                          request.user.nick,
                                          code)
  return util.RedirectFlash(request.user.url() + "/overview",
                            u"Địa chỉ '%s' đã được xác nhận. Bạn có thể kích hoạt tính năng nhận thông báo qua email <a href='%s/user/Admin/settings/notifications'>ở đây</a>" % (rel_ref.target, request.user.url()))
