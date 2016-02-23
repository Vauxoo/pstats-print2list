#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import pstats
import re
import StringIO


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
    if exclude_fnames is None:
        exclude_fnames = []
    if isinstance(exclude_fnames, basestring):
        exclude_fnames = [exclude_fnames]
    for exclude_fname in exclude_fnames:
        if exclude_fname in fname:
            return True
    return False


def print_stats(fnames, filter_fnames=None, exclude_fnames=None,
                sort=None, sort_reverse=None, limit=None):
    """Print stats with a filter or exclude filenames, sort index and limit
    :param list fnames: cProfile standard files to process.
    :param list filter_fnames: Relative paths to filter and show them.
    :param list exclude_fnames: Relative paths to avoid show them.
    :param str sort: Standard `pstats` key of value to sort the result.
      'calls' (call count)
      'cumulative' (cumulative time)
      'cumtime' (cumulative time)
      'file' (file name)
      'filename' (file name)
      'module' (file name)
      'ncalls' (call count)
      'pcalls' (primitive call count)
      'line' (line number)
      'name' (function name)
      'nfl' (name/file/line)
      'stdname' (standard name)
      'time' (internal time)
      'tottime' (internal time)
    :param bool sort_reverse: Reverse sort order.
    :param int limit: Limit max result.
    :returns: Directly print of `pstats` summarize info.
    """

    if isinstance(fnames, basestring):
        fnames = [fnames]

    stream = StringIO.StringIO()

    try:
        stats = pstats.Stats(fnames[0], stream=stream)
        for fname in fnames[1:]:
            stats.add(fname)
    except TypeError:
        print("No cProfile stats valid.")
        return False
    except EOFError:
        print("Empty file cProfile stats valid.")
        return False
    except IOError:
        print("Error to open file.")
        return False

    if sort:
        stats.sort_stats(sort)
    if sort_reverse:
        stats.reverse_order()
    stats.print_stats()
    stream.seek(0)
    fields_list = [
        'ncalls', 'tottime', 'percall', 'cumtime', 'percall2', 'file',
        'lineno', 'method',
    ]
    line_stats_re = re.compile(r'(?P<ncalls>\d+/?\d+)\s+(?P<tottime>\d+\.?\d+)\s+(?P<percall>\d+\.?\d+)\s+(?P<cumtime>\d+\.?\d+)\s+(?P<percall2>\d+\.?\d+)\s+(?P<file>.*):(?P<lineno>\d+)(?P<method>.*)')  # noqa
    stats_list = []
    count = 0
    for line in stream:
        line = line.strip('\r\n ')
        line_stats_match = line_stats_re.match(line) if line else None
        fname = line_stats_match.group('file') if line_stats_match else None
        if fname and is_fname_match(fname, filter_fnames) and \
                not is_exclude(fname, exclude_fnames):
            stats_list.append(dict([(field, line_stats_match.group(field))
                              for field in fields_list]))
            count += 1
            if limit and count >= limit:
                break
    return stats_list
