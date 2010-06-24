from common import api
from common import clock
from common import exception
from common import throttle
from common.test import base
from common.test import util as test_util


class ThrottleTest(base.FixturesTestCase):
  def setUp(self):
    super(ThrottleTest, self).setUp()
    self.popular = api.actor_get(api.ROOT, 'popular@example.com')

  def test_basic(self):

    # lather
    # succeed the first two times, fail the third
    throttle.throttle(self.popular, 'test', minute=2)
    throttle.throttle(self.popular, 'test', minute=2)

    def _failPants():
      throttle.throttle(self.popular, 'test', minute=2)

    self.assertRaises(exception.ApiThrottled, _failPants)

    # rinse
    # magically advance time by a couple minutes
    o = test_util.override_clock(clock, seconds=120)

    # repeat
    # succeed the first two times, fail the third
    throttle.throttle(self.popular, 'test', minute=2)
    throttle.throttle(self.popular, 'test', minute=2)

    self.assertRaises(exception.ApiThrottled, _failPants)

    o.reset()
