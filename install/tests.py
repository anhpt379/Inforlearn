#! coding: utf-8
from google.appengine.api import users

from common import api
from common.test import base

def _true():
  return True

class InstallTest(base.ViewTestCase):

  # override fixtures, so that there is no root user
  fixtures = []

  def patch_users(self):
    users.get_current_user_old = users.get_current_user
    users.get_current_user = _true
    users.is_current_user_admin_old = users.is_current_user_admin
    users.is_current_user_admin = _true

  def unpatch_users(self):
    users.get_current_user = users.get_current_user_old
    users.is_current_user_admin = users.is_current_user_admin_old

  def setUp(self):
    super(InstallTest, self).setUp()
    self.patch_users()

  def tearDown(self):
    super(InstallTest, self).tearDown()
    self.unpatch_users()

  def test_noroot(self):
    r = self.client.get('/install')
    self.assertContains(r, 'Thiết lập tài khoản root')

  def test_root(self):
    api.user_create_root(api.ROOT)
    r = self.client.get('/install')
    self.assertContains(r, 'root@example.com đã được kích hoạt.')

