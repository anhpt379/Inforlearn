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
                            "Email '%s' has been confirmed." % (rel_ref.target))
