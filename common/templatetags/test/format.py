# -*- coding: utf-8 -*-
from django import test
from common import models
from common.templatetags import format
from common.test import base


class FormatTest(test.TestCase):

  def test_truncate(self):
    test_strings = [(u"Testing", 7, u"Testing"),
                    ("Testing", 6, u"Testin\u2026"),
                    (u"åäöåäöåäöåäö", 10, u"åäöåäöåäöå…")]

    for orig_str, max_len, trunc_str in test_strings:
      a = format.truncate(orig_str, max_len)
      self.assertEqual(a, trunc_str)


class FormatFixtureTest(base.FixturesTestCase):

  # TODO(jonasnockert): Improve test method... but how?
  def test_linked_entry_truncated_title(self):
    # Get all StreamEntries to make sure both posts and comments are
    # tested.
    entries = models.StreamEntry.all()

    for e in entries:
      # Truncate to one character to ensure truncation takes place and
      # an ellipsis is added. 
      trunc_url = format.linked_entry_truncated_title(e, 1)
      # Construct a link with made-up one character+ellipsis entry title.
      trunc_ref_url = u"<a href=\"%s\">x\u2026</a>" % e.url()
      self.assertEqual(len(trunc_url), len(trunc_ref_url))
