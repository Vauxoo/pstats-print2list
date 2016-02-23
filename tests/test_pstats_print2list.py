#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pstats_print2list
----------------------------------

Tests for `pstats_print2list` module.
"""

import os
import unittest
from cProfile import Profile

from pstats_print2list import pstats_print2list


class TestPstatsPrint2list(unittest.TestCase):

    def setUp(self):
        self.dirname_demo = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'demo')
        self.fstats_fib = os.path.join(self.dirname_demo, 'fib_dump.stats')
        self.fstats_fib_list = [
            self.get_fname_stats('_%d' % index) for index in range(5)]

    def get_fname_stats(self, suffix):
        fname, fext = os.path.splitext(self.fstats_fib)
        fname += suffix + fext
        return fname

    def tearDown(self):
        pass

    def test_010_limit_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib, filter_fnames=None, exclude_fnames=None, limit=1)
        self.assertEqual(len(result), 1)

    def test_020_filter_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib,
            filter_fnames='seq', exclude_fnames=None, limit=None)
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')

    def test_030_exclude_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib,
            filter_fnames=None, exclude_fnames='seq', limit=None)
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')

    def test_040_none_print_pstats(self):
        result = pstats_print2list.print_stats(self.fstats_fib)
        self.assertEqual(len(result), 2)

    def test_050_filter_exclude_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib,
            filter_fnames='seq', exclude_fnames='fib', limit=None)
        self.assertEqual(len(result), 0)

    def test_060_wo_filter_fnames_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib,
            filter_fnames=[], exclude_fnames=None, limit=None)
        self.assertEqual(len(result), 2)

    def test_060_fnonexistent_print_pstats(self):
        result = pstats_print2list.print_stats(
            '/tmp/nonexistent.stats',
            filter_fnames=[], exclude_fnames=None, limit=None)
        self.assertFalse(result)

    def test_070_fempty_print_pstats(self):
        fname = self.get_fname_stats('_empty')
        fobj = open(fname, "w")
        result = pstats_print2list.print_stats(
            fname,
            filter_fnames=[], exclude_fnames=None, limit=None)
        fobj.close()
        self.assertFalse(result)

    def test_080_fnovalid_print_pstats(self):
        fname = self.get_fname_stats('_novalid')
        Profile().dump_stats(fname)
        result = pstats_print2list.print_stats(
            fname,
            filter_fnames=[], exclude_fnames=None, limit=None)
        self.assertFalse(result)

    def test_090_sort_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib, sort='cumulative')
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib.py')

    def test_100_sort_print_pstats(self):
        result = pstats_print2list.print_stats(self.fstats_fib, sort='calls')
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib_seq.py')

    def test_110_sort_reverse_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib, sort='calls', sort_reverse=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib.py')

    def test_120_sort_reverse_print_pstats(self):
        result = pstats_print2list.print_stats(
            self.fstats_fib, sort='cumulative', sort_reverse=True)
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib_seq.py')

    def test_130_multifiles_print_pstats(self):
        result_onefile = pstats_print2list.print_stats(self.fstats_fib)
        result_multifiles = pstats_print2list.print_stats(self.fstats_fib_list)
        self.assertEqual(result_onefile, result_multifiles)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
