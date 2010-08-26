import settings
from common import models
from common.templatetags import avatar
from common.test import base

class AvatarTest(base.FixturesTestCase):
  def setUp(self):
    self.popular = models.Actor(nick="popular@example.com")

  def tearDown(self):
    settings.DEBUG = True

  def test_avatar_url(self):
    self.assertEquals("http://localhost:8080/image/avatar_default_u.jpg",
                      avatar.avatar_url(self.popular, "u"))

  def test_avatar(self):
    expected = ('<img src="http://localhost:8080/image/avatar_default_t.jpg"'
                ' class="photo" alt="popular" width="50" height="50" />')
    self.assertEquals(expected, avatar.avatar(self.popular, "t"))

  @staticmethod
  def _raise_exception():
    raise Exception()

  def test_safe_avatar_debug(self):
    f = avatar.safe_avatar(AvatarTest._raise_exception)
    self.assertEquals("FAIL", f())

  def test_safe_avatar_non_debug(self):
    f = avatar.safe_avatar(AvatarTest._raise_exception)
    settings.DEBUG = False
    self.assertEquals("", f())
