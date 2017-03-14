#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_pstats_print2list
----------------------------------

Tests for `get_pstats_print2list` module.
"""

from __future__ import print_function

import os
import unittest
from cProfile import Profile

from pstats_print2list import get_pstats_print2list, print_pstats_list


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

    def test_010_limit(self):
        result = get_pstats_print2list(
            self.fstats_fib, filter_fnames=None, exclude_fnames=None, limit=1)
        self.assertEqual(len(result), 1)

    def test_020_filter(self):
        result = get_pstats_print2list(
            self.fstats_fib,
            filter_fnames='seq', exclude_fnames=None, limit=None)
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')

    def test_030_exclude(self):
        result = get_pstats_print2list(
            self.fstats_fib, filter_fnames=None,
            exclude_fnames=['seq', '>', 'profile'], limit=None)
        self.assertEqual(len(result), 1)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')

    def test_040_none(self):
        result = get_pstats_print2list(
            self.fstats_fib, exclude_fnames=['>', 'profile'])
        self.assertEqual(len(result), 2)

    def test_050_filter_exclude(self):
        result = get_pstats_print2list(
            self.fstats_fib,
            filter_fnames='seq', exclude_fnames='fib', limit=None)
        self.assertEqual(len(result), 0)

    def test_060_wo_filter_fnames(self):
        result = get_pstats_print2list(
            self.fstats_fib,
            filter_fnames=[], exclude_fnames=None, limit=None)
        self.assertEqual(len(result), 4)

    def test_060_fnonexistent(self):
        result = get_pstats_print2list(
            '/tmp/nonexistent.stats',
            filter_fnames=[], exclude_fnames=None, limit=None)
        self.assertFalse(result)

    def test_070_fempty(self):
        fname = self.get_fname_stats('_empty')
        fobj = open(fname, "w")
        result = get_pstats_print2list(
            fname,
            filter_fnames=[], exclude_fnames=None, limit=None)
        fobj.close()
        self.assertFalse(result)

    def test_080_fnovalid(self):
        fname = self.get_fname_stats('_novalid')
        Profile().dump_stats(fname)
        result = get_pstats_print2list(
            fname,
            filter_fnames=[], exclude_fnames=None, limit=None)
        self.assertFalse(result)

    def test_090_sort_cumulative(self):
        result = get_pstats_print2list(
            self.fstats_fib, sort='cumulative',
            exclude_fnames=['>', 'profile'])
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib.py')

    def test_100_sort_calls(self):
        result = get_pstats_print2list(
            self.fstats_fib, sort='calls', exclude_fnames=['>', 'profile'])
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib_seq.py')

    def test_110_sort_calls_reverse(self):
        result = get_pstats_print2list(
            self.fstats_fib, sort='calls', sort_reverse=True,
            exclude_fnames=['>', 'profile'])
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib_seq.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib.py')

    def test_120_sort_cumulative_reverse(self):
        result = get_pstats_print2list(
            self.fstats_fib, sort='cumulative', sort_reverse=True,
            exclude_fnames=['>', 'profile'])
        self.assertEqual(len(result), 2)
        self.assertEqual(os.path.basename(result[0]['file']), 'fib.py')
        self.assertEqual(os.path.basename(result[1]['file']), 'fib_seq.py')

    def test_130_multifiles(self):
        result_onefile = get_pstats_print2list(self.fstats_fib)
        result_multifiles = get_pstats_print2list(self.fstats_fib_list)
        self.assertEqual(result_onefile, result_multifiles)

    def test_140_print_list(self):
        pstats_list = get_pstats_print2list(self.fstats_fib)
        print("\n")
        self.assertTrue(print_pstats_list(pstats_list))

    def test_150_print_empty_list(self):
        pstats_list = get_pstats_print2list(self.fstats_fib, 'without_files')
        self.assertEqual(pstats_list, [])
        self.assertFalse(print_pstats_list(pstats_list))

    def test_160_print_None(self):
        self.assertFalse(print_pstats_list(None))


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
