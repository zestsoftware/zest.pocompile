Introduction
============

This package compiles po files.  It contains a `zest.releaser`_ entry
point and a stand-alone command line tool.


Goal
====

You want to release a package that has a ``locales`` dir (or
``locale``, or something else as long as it has a ``LC_MESSAGES``
folder somewhere in it) with translations in ``.po`` files.  You want
to include the compiled ``.mo`` files in your release as well, but you
do not want to keep those in a revision control system (like
subversion) as they are binary and can be easily recreated.  That is
good.  This package helps with that.


Want ``.mo`` files?  Add a ``MANIFEST.in`` file.
================================================

When you use ``python setup.py sdist`` to create a source
distribution, distutils (or setuptools or distribute or distutils2)
knows which files it should include by looking at the information of
the revision control system (RCS).  This is why in the case of
subversion you should use a checkout and not an export: you need the
versioning information.  (For other RCS or for subversion 1.7+ you
currently need to install extra packages like setuptools-git.)

Since the compiled ``.mo`` files are best not stored in subversion (or
any other RCS), you need to give a hint on which files to include.  You
do this by adding a ``MANIFEST.in`` file.  Let's say your package has
roughly these contents (not all files are shown)::

  your.package/setup.py
  your.package/your/package/locales/nl/LC_MESSAGES/domain.po

Then you need a MANIFEST.in like this::

  recursive-include your *
  global-exclude *pyc

This tells distutils to recursively include all (``*``) files and
directories within the ``your`` directory.  Try it: create a directory
structure like the above example with a proper ``setup.py``, copy the
``domain.po`` file to ``domain.mo`` as a silly test, run ``python
setup.py sdist`` and check that the ``.mo`` file ends up in the
created distribution.

Note that the line ``global-exclude *pyc`` may not be strictly
necessary (at least when using ``zest.releaser`` as it does a fresh
checkout of a tag when releasing), but it avoids unnecessarily adding
compiled python files in the release and it does not hurt, except that
you may get a warning during release::

  warning: no previously-included files matching '*pyc' found anywhere in distribution

With that part working, the only thing this ``zest.pocompile`` package
needs to do, is to actually find all ``.po`` files and compile them to
``.mo`` files.  It looks for directories that are named
``LC_MESSAGES`` and compiles all ``.po`` files in there.


Command line tool
=================

When you ``easy_install zest.pocompile`` you get a command line tool
``pocompile``.  When you run it, this walks the current directory,
finds all po translation files in a properly formed locales directory
and compiles them into mo files.  You can also give it a list of
directories as arguments instead.  Run it with the ``--help`` option
to get some help.

In the above example, if you are in the ``your.package`` directory and
run ``pocompile`` it will create this file::

  your.package/your/package/locales/nl/LC_MESSAGES/domain.mo


zest.releaser entry point
=========================

You do not need `zest.releaser`_ for proper functioning of
``zest.pocompile``.  But if you use the two together, in combination
with a proper ``MANIFEST.in`` file, releasing a source distribution
with compiled ``.mo`` files is made easy.

The ``release`` (or ``fullrelease``) command of ``zest.releaser``
creates a (subversion or other) tag, checks out this tag, creates a
source distribution (``sdist``) and uploads it to PyPI.  When
``zest.pocompile`` is added to the mix, it compiles the ``.po`` files
immediately after checking out the tag, right in time for creating the
``sdist``, which should now contain the ``.mo`` files.


Credits
=======

This package has been cobbled together by Maurits van Rees.
 
It depends on the `python-gettext`_ package, which itself suggests
using the Babel_ package, but it does exactly what we need and its
releases are stored on PyPI, so we ignore that suggestion.

The main functions are taken from the ``build_mo`` command of
`collective.releaser`_.

Thanks!


To Do
=====

- Add tests.


.. _`zest.releaser`: http://pypi.python.org/pypi/zest.releaser
.. _`python-gettext`: http://pypi.python.org/pypi/python-gettext
.. _Babel: http://pypi.python.org/pypi/Babel
.. _`collective.releaser`: http://pypi.python.org/pypi/collective.releaser
