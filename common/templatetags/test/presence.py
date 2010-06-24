from common.templatetags import presence
from django import test

class PresenceTest(test.TestCase):
  def test_presence_str(self):
    self.assertEquals(u'str', presence.location(u'str'))

  def test_presence_country(self):
    self.assertEquals(u'co', presence.location({'country': {'name': u'co'}}))

  def test_presence_city(self):
    self.assertEquals(u'ci', presence.location({'city': {'name': u'ci'}}))

  def test_presence_base(self):
    self.assertEquals(u'ba', presence.location(
        {'base': {'current': {'name': u'ba'}}}))

  def test_presence_cell(self):
    self.assertEquals(u'ce', presence.location({'cell': {'name': u'ce'}}))

  def test_presence_join(self):
    self.assertEquals(u'ce, ci, co', presence.location({
      'cell': {'name': u'ce'},
      'city': {'name': u'ci'},
      'country': {'name': u'co'}}))

  def test_presence_join_unicode(self):
    self.assertEquals(u'c\xe4, ci, co', presence.location({
      'cell': {'name': u'c\xe4'},
      'city': {'name': u'ci'},
      'country': {'name': u'co'}}))
