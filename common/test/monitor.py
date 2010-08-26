# -*- coding: utf-8 -*-
from django import test
from common import monitor
from common import exception


class MonitorTest(test.TestCase):

  def _test_normalization(self, data):
    for t, example in data:
      try:
        result = self.cleaner(t)
      except exception.ValidationError, e:
        message = ("%s(%s) failed validation [%s]" %
            (self.cleaner.__name__, t, e))
        raise AssertionError, message
      self.assertEqual(result, example)

  def test_export_dict(self):
    data = {'good-name': ('label-time', {'some':0,
                                         'mapping':1,
                                         'variables': 5.0}
                          )
            }

    o = monitor.export(data)
    self.assertEquals(
        o, 'good-name map:label-time mapping:1 some:0 variables:5.0')

  def test_export_list(self):
    data = {'good-name': (0, 2, 8, 256)
            }

    o = monitor.export(data)
    self.assertEquals(
        o, 'good-name 0/2/8/256')


  def test_export_multiple(self):
    data = {'good-name': (0, 2, 8, 256),
            'party-time': 2,
            'dicto': ('label-time', {'heya': 0, 'foo': 0})
            }

    o = monitor.export(data)
    self.assertEquals(
        o, ('dicto map:label-time foo:0 heya:0\n'
            'good-name 0/2/8/256\n'
            'party-time 2'))

