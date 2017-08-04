=================
pstats_print2list
=================

.. image:: https://img.shields.io/pypi/v/pstats_print2list.svg
        :target: https://pypi.python.org/pypi/pstats_print2list

.. image:: https://img.shields.io/travis/Vauxoo/pstats-print2list.svg
        :target: https://travis-ci.org/Vauxoo/pstats-print2list

.. .. image:: https://readthedocs.org/projects/pstats_print2list/badge/?version=latest
..         :target: https://readthedocs.org/projects/pstats_print2list/?badge=latest
..         :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/Vauxoo/pstats-print2list/badge.svg?branch=master 
        :target: https://coveralls.io/github/Vauxoo/pstats-print2list?branch=master

.. image:: https://img.shields.io/pypi/dm/pstats_print2list.svg
        :target: https://pypi.python.org/pypi/pstats_print2list


Add to pstats library of cProfile the feature of get the result in a list with filters, limit and sort.

* Free software: ISC license
* Documentation: https://pythonhosted.org/pstats_print2list/

Features
--------
 
 * Add the posiblity of get profiling report pstats result in a list.
 * Add the posibility of sort the result with a default pstats index.
 * Add the posilibity of add a limit to result.
 * Add the posibility of filter by paths or files.
 * Add the posibility of exclude paths or files.


Installation
------------

 * Using pypi: ``pip install pstats_print2list``

Usage
-----

 * Small example:

.. code-block:: python

   import pstats_print2list
   print "Method docstring", pstats_print2list.get_pstats_print2list.__doc__
   pstats_list = pstats_print2list.get_pstats_print2list(['fname_stat1', 'fname_stat2'])
   pstats_print2list.print_pstats_list(pstats_list)

..


 * Small line command example:
 
 .. code-block:: bash
 
 python -c "from pstats_print2list import get_pstats_print2list, print_pstats_list;print print_pstats_list(get_pstats_print2list('YOUR_FILE'))"


 * Full example:

.. code-block:: python

    from pstats_print2list import get_pstats_print2list, print_pstats_list
    fname_stats = 'my_profiling_out.stats'
    pstats_list = get_pstats_print2list(
        fname_stats,
        filter_fnames=['myfile1.py', 'myfile2.py', 'root_path1'],
        exclude_fnames=['dontshow.py', 'path_dont_show'],
        sort='cumulative',
        limit=5,
    )
    print_pstats_list(pstats_list)
..

Credits
-------

This package was created by Vauxoo_

.. _Vauxoo: https://www.vauxoo.com/

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Authors
-------

Moisés López <moylop260@vauxoo.com>
