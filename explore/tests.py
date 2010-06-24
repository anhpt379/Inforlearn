import re
import simplejson
from common import profile
from common.tests import ViewTestCase


class ExploreTest(ViewTestCase):
  def test_explore_when_signed_out(self):

    l = profile.label('explore_get_public')
    r = self.client.get('/explore')
    l.stop()

    self.assertContains(r, "Latest Public Posts")
    self.assertTemplateUsed(r, 'explore/templates/recent.html')

  def test_explore_when_signed_in(self):
    self.login('popular')

    l = profile.label('explore_get_logged_in')
    r = self.client.get('/explore')
    l.stop()

    self.assertContains(r, "Latest Public Posts")
    self.assertTemplateUsed(r, 'explore/templates/recent.html')

  def test_rss_and_atom_feeds(self):
    r = self.client.get('/explore')
    self.assertContains(r, 'href="/explore/rss"')
    self.assertContains(r, 'href="/explore/atom"')

  def test_json_feed(self):
    urls = ['/feed/json', '/explore/json']
    for u in urls:
      r = self.client.get(u)
      self.assertEqual(r.status_code, 200)
      j = simplejson.loads(r.content)
      self.assertEqual(j['url'], '/explore')
      self.assertTemplateUsed(r, 'explore/templates/recent.json')

  def test_json_feed_with_callback(self):
    urls = ['/feed/json', '/explore/json']
    for u in urls:
      r = self.client.get('/feed/json', {'callback': 'callback'})
      self.assertContains(r, '"url": "\/explore",', status_code=200)
      self.failIf(not re.match('callback\(', r.content))
      self.failIf(not re.search('\);$', r.content))
      self.assertTemplateUsed(r, 'explore/templates/recent.json')

