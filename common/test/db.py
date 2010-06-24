import datetime
from django import test
from common import api
from common import models
from common import properties

class DbCacheTest(test.TestCase):
  entry_keys = ('stream/popular@example.com/presence/12345',
                'stream/popular@example.com/presence/12346')

  def test_with_cache(self):
    models.CachingModel.reset_get_count()
    models.CachingModel.reset_cache()
    models.CachingModel.enable_cache()
    api.entry_get_entries(api.ROOT, self.entry_keys)
    self.assertNotEqual(models.CachingModel.db_get_count(), 0)
    first_count = models.CachingModel.db_get_count()
    api.entry_get_entries(api.ROOT, self.entry_keys)
    self.assertEqual(models.CachingModel.db_get_count(), first_count)

  def test_without_cache(self):
    models.CachingModel.reset_get_count()
    models.CachingModel.reset_cache()
    models.CachingModel.enable_cache(False)
    api.entry_get_entries(api.ROOT, self.entry_keys)
    self.assertNotEqual(models.CachingModel.db_get_count(), 0)
    first_count = models.CachingModel.db_get_count()
    api.entry_get_entries(api.ROOT, self.entry_keys)
    self.assertNotEqual(models.CachingModel.db_get_count(), first_count)

class PropertyTestCase(test.TestCase):
  def test_datetimeproperty_validate(self):
    p = properties.DateTimeProperty()
    validated = p.validate("2008-01-01 02:03:04")
    self.assertEquals(validated, datetime.datetime(2008, 01, 01, 02, 03, 04))

    validated = None
    try:
      validated = p.validate("2008-01-01")
    except:
      pass

    self.assertEquals(validated, None)

    p = properties.DateTimeProperty()
    validated = p.validate("2008-01-01 02:03:04.000567")
    self.assertEquals(validated,
                      datetime.datetime(2008, 01, 01, 02, 03, 04, 567))


