import datetime
from django.conf import settings
from common import api
from common import exception
from common import profile
from common.test import base
from common.test import util as test_util


class TaskSpecTest(base.FixturesTestCase):
  pass

class QueueTest(base.FixturesTestCase):
  def setUp(self):
    self.old_utcnow = test_util.utcnow
    self.now = test_util.utcnow()
    self.delta = datetime.timedelta(seconds=api.DEFAULT_TASK_EXPIRE)
    self.old_enabled = settings.QUEUE_ENABLED

    super(QueueTest, self).setUp()

    settings.QUEUE_ENABLED = True

  def tearDown(self):
    test_util.utcnow = self.old_utcnow
    super(QueueTest, self).tearDown()

    settings.QUEUE_ENABLED = self.old_enabled

  def test_task_crud(self):
    # make a fake task for posting a simple message
    nick = 'popular@example.com'
    action = 'post'
    uuid = 'forever'
    message = 'more'

    actor_ref = api.actor_get(api.ROOT, nick)

    # STOP TIME! OMG!
    test_util.utcnow = lambda: self.now

    # makin
    l = profile.label('api_task_create')
    task_ref = api.task_create(actor_ref,
                               nick,
                               action,
                               uuid,
                               args=[],
                               kw={'nick': nick,
                                   'message': message,
                                   'uuid': uuid
                                   }
                               )
    l.stop()

    # grabbin
    l = profile.label('api_task_get (unlocked)')
    task_ref = api.task_get(actor_ref, nick, action, uuid)
    l.stop()

    # grab again, LOCK VILLE
    def _again():
      task_ref = api.task_get(actor_ref, nick, action, uuid)


    l = profile.label('api_task_get (locked)')
    self.assertRaises(exception.ApiLocked, _again)
    l.stop()

    # increment time
    new_now = self.now + self.delta
    test_util.utcnow = lambda: new_now

    # grab again, EXPIRED
    task_ref = api.task_get(actor_ref, nick, action, uuid)

    # locked if we try again
    self.assertRaises(exception.ApiLocked, _again)

    # updatin
    l = profile.label('api_task_update')
    task_ref = api.task_update(actor_ref, nick, action, uuid, '1')
    l.stop()
    self.assertEqual(task_ref.progress, '1')

    # grab again, FRESH AND CLEAN
    task_ref = api.task_get(actor_ref, nick, action, uuid)
    self.assertEqual(task_ref.progress, '1')

    # removin
    l = profile.label('api_task_remove')
    api.task_remove(actor_ref, nick, action, uuid)
    l.stop()

    # grab again, NOT FOUND
    def _not_found():
      task_ref = api.task_get(actor_ref, nick, action, uuid)

    self.assertRaises(exception.ApiNotFound, _not_found)
