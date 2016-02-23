#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pstats
import sys
import StringIO
import re


def is_fname_match(fname, fmatch_list):
    if isinstance(fmatch_list, basestring):
        fmatch_list = [fmatch_list]
    if not fmatch_list:
        return True
    for fmatch in fmatch_list:
        if fmatch in fname:
            return True
    return False


def is_exclude(fname, exclude_fnames):
    if isinstance(exclude_fnames, basestring):
        exclude_fnames = [exclude_fnames]
    for exclude_fname in exclude_fnames:
        if exclude_fname in fname:
            return True
    return False


def print_stats(filter_fnames=None, exclude_fnames=None,
                sort_index=0, limit=None, fname=None):
    """Print stats with a filter or exclude filenames, sort index and limit
    :param list filter_fnames: Relative paths to filter and show them.
    :param list exclude_fnames: Relative paths to avoid show them.
    :param int sort_index: Index of `pstats tuple` to sort the result.
    :param int limit: Limit max result.
    :returns: Directly print of `pstats` summarize info.
    """
    if filter_fnames is None:
        filter_fnames = ['.py']
    if exclude_fnames is None:
        exclude_fnames = []

    if fname is None:
        fname = os.path.expanduser('~/.openerp_server.stats')

    if not os.path.isfile(fname):
        print "No cProfile stats to report."
        return False
    try:
        fstats = pstats.Stats(fname)
    except TypeError:
        print "No cProfile stats valid."
        return False

    stream = StringIO.StringIO()
    stats = pstats.Stats(fname, stream=stream)
    stats.print_stats()
    stream.seek(0)
    fields_list = ['ncalls', 'tottime', 'percall', 'cumtime', 'percall2', 'file', 'lineno', 'method']
    line_stats_re = re.compile(r'(?P<ncalls>\d+/?\d+)\s+(?P<tottime>\d+\.?\d+)\s+(?P<percall>\d+\.?\d+)\s+(?P<cumtime>\d+\.?\d+)\s+(?P<percall2>\d+\.?\d+)\s+(?P<file>.*):(?P<lineno>\d+)(?P<method>.*)')
    stats_list = []
    count = 0
    for line in stream:
        line = line.strip('\r\n ')
        line_stats_match = line_stats_re.match(line) if line else None
        fname = line_stats_match.group('file') if line_stats_match else None
        if fname and is_fname_match(fname, filter_fnames) and not is_exclude(fname, exclude_fnames):
            stats_list.append(dict([(field, line_stats_match.group(field)) for field in fields_list]))
            count += 1
            if limit and count >= limit:
                break
    return stats_list
