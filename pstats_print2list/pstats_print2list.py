# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import pstats
import re
import StringIO


def get_field_list():
    "Get field list of pstats report standard."
    field_list = [
        'ncalls',
        'tottime', 'tt_percall',
        'cumtime', 'ct_percall',
        'file', 'lineno', 'method',
    ]
    return field_list


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


def get_pstats_print2list(fnames, filter_fnames=None, exclude_fnames=None,
                          sort=None, sort_reverse=None, limit=None):
    """Print stats with a filter or exclude filenames, sort index and limit.
    :param list fnames: cProfile standard files to process.
    :param list filter_fnames: Relative paths to filter and show them.
    :param list exclude_fnames: Relative paths to avoid show them.
    :param str sort: Standard `pstats` key of value to sort the result.
        \n\t\t\t'calls' (call count)
        \n\t\t\t'cumulative' (cumulative time)
        \n\t\t\t'cumtime' (cumulative time)
        \n\t\t\t'file' (file name)
        \n\t\t\t'filename' (file name)
        \n\t\t\t'module' (file name)
        \n\t\t\t'ncalls' (call count)
        \n\t\t\t'pcalls' (primitive call count)
        \n\t\t\t'line' (line number)
        \n\t\t\t'name' (function name)
        \n\t\t\t'nfl' (name/file/line)
        \n\t\t\t'stdname' (standard name)
        \n\t\t\t'time' (internal time)
        \n\t\t\t'tottime' (internal time)
    :param bool sort_reverse: Reverse sort order.
    :param int limit: Limit max result.
    :returns: List of dicts with `pstats` print result after filters, sorted
        and limited.
    """

    if isinstance(fnames, basestring):
        fnames = [fnames]
    fnames_expanded = [
        os.path.expandvars(os.path.expanduser(fname)) for fname in fnames]
    stream = StringIO.StringIO()
    try:
        stats = pstats.Stats(fnames[0], stream=stream)
        for fname in fnames_expanded[1:]:
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

    stats.print_stats()
    stream.seek(0)
    field_list = get_field_list()
    line_stats_re = re.compile(
        r'(?P<%s>\d+/?\d+|\d+)\s+(?P<%s>\d+\.?\d+)\s+(?P<%s>\d+\.?\d+)\s+'
        r'(?P<%s>\d+\.?\d+)\s+(?P<%s>\d+\.?\d+)\s+(?P<%s>.*):(?P<%s>\d+)'
        r'\((?P<%s>.*)\)' % tuple(field_list))
    stats_list = []
    count = 0
    for line in stream:
        line = line.strip('\r\n ')
        line_stats_match = line_stats_re.match(line) if line else None
        fname = line_stats_match.group('file') if line_stats_match else None
        if fname and is_fname_match(fname, filter_fnames) and \
                not is_exclude(fname, exclude_fnames):
            data = dict([(field, line_stats_match.group(field))
                         for field in field_list])
            data['rcalls'], data['calls'] = (
                data.get('ncalls', '') + '/' + data.get('ncalls', '')
            ).split('/')[:2]
            data['factor'] = "%.2f" % (
                (float(data['rcalls']) - float(data['calls']) + 1) *
                float(data['cumtime']))
            data['cumulative'] = data['cumtime']
            stats_list.append(data)
            count += 1
    return sorted(stats_list, key=lambda key: float(key[sort or 'factor']),
                  reverse=not sort_reverse)[:limit]


def print_pstats_list(pstats, pformat=None):
    """Print list of pstats dict formatted
    :param list pstats: pstats dicts to print
    :param str format: String.format style to show fields with keys:
        ncalls, tottime, tt_percall, cumtime, ct_percall, file, lineno, method
        rcalls, calls
    :return: Directly print of result formatted and return True"""
    if not pstats:
        return False
    if pformat is None:
        pformat = ("{method:<40s} {factor:>16s} {cumtime:>10s} "
                   "{calls:>10s} {rcalls:>10s} {tottime:>10s} "
                   "{tt_percall:>10s} {ct_percall:>10s} "
                   "<{file}:{lineno}")
    for pstat_line in [dict(zip(pstats[0].keys(), pstats[0].keys()))] + pstats:
        print(pformat.format(**pstat_line))
    return True
