#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pstats_filter
----------------------------------

Tests for `pstats_filter` module.
"""

import unittest

from pstats_filter import pstats_filter
from pprint import pprint

class TestPstats_filter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_print_pstats(self):
        result = pstats_filter.print_stats(
                filter_fnames='/root/', exclude_fnames='odoo-8.0', limit=11)

        print pprint(result)
        print len(result)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
