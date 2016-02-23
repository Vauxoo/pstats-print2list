#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pstats_filter
----------------------------------

Tests for `pstats_filter` module.
"""

import os
import unittest

from pstats_filter import pstats_filter
from cProfile import Profile

class TestPstatsFilter(unittest.TestCase):

    def setUp(self):
        self.dirname_demo = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'demo')
        self.fstats_fib = os.path.join(self.dirname_demo, 'fib_dump.stats')

    def get_fname_stats(self, suffix):
        fname, fext = os.path.splitext(self.fstats_fib)
        fname += suffix + fext
        return fname

    def tearDown(self):
        pass

    def test_010_limit_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames=None, exclude_fnames=None, limit=1,
            fname=self.fstats_fib)
        self.assertEqual(len(result), 1)

    def test_020_filter_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames='seq', exclude_fnames=None, limit=None,
            fname=self.fstats_fib)
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')

    def test_030_exclude_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames=None, exclude_fnames='seq', limit=None,
            fname=self.fstats_fib)
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')

    def test_040_none_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames=None, exclude_fnames=None, limit=None,
            fname=self.fstats_fib)
        self.assertEqual(len(result), 2)

    def test_050_filter_exclude_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames='seq', exclude_fnames='fib', limit=None,
            fname=self.fstats_fib)
        self.assertEqual(len(result), 0)

    def test_060_wo_filter_fnames_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames=[], exclude_fnames=None, limit=None,
            fname=self.fstats_fib)
        self.assertEqual(len(result), 2)

    def test_060_fnonexistent_print_pstats(self):
        result = pstats_filter.print_stats(
            filter_fnames=[], exclude_fnames=None, limit=None,
            fname='/tmp/nonexistent.stats')
        self.assertFalse(result)

    def test_070_fempty_print_pstats(self):
        fname = self.get_fname_stats('_empty')
        fobj = open(fname, "w")
        result = pstats_filter.print_stats(
            filter_fnames=[], exclude_fnames=None, limit=None,
            fname=fname)
        fobj.close()
        self.assertFalse(result)

    def test_080_fnovalid_print_pstats(self):
        fname = self.get_fname_stats('_novalid')
        Profile().dump_stats(fname)
        result = pstats_filter.print_stats(
            filter_fnames=[], exclude_fnames=None, limit=None,
            fname=fname)
        self.assertFalse(result)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
