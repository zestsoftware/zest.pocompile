Introduction
============

This package compiles po files.
It contains a `zest.releaser`_ entrypoint and a stand-alone command line tool.


Goal
====

You want to release a package that has a ``locales`` dir
(or ``locale``, or something else as long as it has a ``LC_MESSAGES`` folder somewhere in it)
with translations in ``.po`` files.
You want to include the compiled ``.mo`` files in your release as well,
but you do not want to keep those in a revision control system (like git) as they are binary and can be easily recreated.
That is good.
This package helps with that.


Want ``.mo`` files?  Add a ``MANIFEST.in`` file.
================================================

When you use ``python setup.py sdist`` to create a source distribution, Python does *not* automatically include all files.
It might look at the information of the revision control system (RCS), but that may or may not work.
This depends on your RCS, your Python version, setuptools, or extra packages like ``setuptools-git``.

Since the compiled ``.mo`` files are best not stored in git (or any other RCS), you need to give a hint on which files to include.
You do this by adding a ``MANIFEST.in`` file.
Let's say your package has roughly these contents (not all files are shown)::

  your.package/setup.py
  your.package/your/package/locales/nl/LC_MESSAGES/domain.po

Then you need a ``MANIFEST.in`` file like this::

  recursive-include your *

Or with a bigger example::

  recursive-include your *
  recursive-include docs *
  include *
  global-exclude *.pyc

I will explain the lines one by one for clarity.
And yes: I (Maurits) now simply go to this page on PyPI if I want to have an example of a proper ``MANIFEST.in`` file.
So this documentation is now getting slightly larger than strictly needed. :-)

``recursive-include your *``
  This tells distutils to recursively include all (``*``) files and directories within the ``your`` directory.
  Try it: create a directory structure like the above example with a proper ``setup.py``,
  copy the ``domain.po`` file to ``domain.mo`` as a silly test,
  run ``python setup.py sdist``
  and check that the ``.mo`` file ends up in the created distribution.

``recursive-include docs *``
  Include files in the ``docs`` directory.
  If this directory does not exist, you will get a warning, so you may want to remove it then, but leaving it there does not hurt.

``include *``
  Include unrecognized files in the root directory.
  Oterwise by default only standard files like ``README.txt``, ``setup.py``, and ``setup.cfg`` are included.
  So for example a ``CHANGES.txt`` file must be explicitly included (here with ``*``).

``global-exclude *.pyc``
  This avoids unnecessarily adding compiled python files in the release.
  When these are not there, for example after a fresh checkout, you will get a harmless warning: ``no previously-included files matching '*.pyc' found anywhere in distribution``.

For more info on creating a source distribution and how to use ``MANIFEST.in`` see the `Python distutils documentation <http://docs.python.org/distutils/sourcedist.html>`_
or the `setuptools documentation <https://setuptools.readthedocs.io/en/latest/setuptools.html>`_.

With this part working, the only thing this ``zest.pocompile`` package needs to do, is to actually find all ``.po`` files and compile them to ``.mo`` files.
It simply looks for directories that are named ``LC_MESSAGES`` and compiles all ``.po`` files found in there.


Command line tool
=================

When you ``pip install zest.pocompile`` you get a command line tool ``pocompile``.
When you run it, this walks the current directory, finds all po translation files in a properly formed locales directory, and compiles them into ``.mo`` files.
You can also give it a list of directories as arguments instead.
Run it with the ``--help`` option to get some help.

In the above example, if you are in the ``your.package`` directory and run ``pocompile`` it will create this file::

  your.package/your/package/locales/nl/LC_MESSAGES/domain.mo


zest.releaser entry point
=========================

You do not need `zest.releaser`_ for a proper functioning of ``zest.pocompile``.
But if you use the two together, in combination with a proper ``MANIFEST.in`` file, releasing a source distribution with compiled ``.mo`` files is made easy.

The ``release`` (or ``fullrelease``) command of ``zest.releaser`` creates a (git or other) tag and checks out this tag.
Then it creates a source distribution (``sdist``) and possibly a wheel (``bdist_wheel``) and uploads it to PyPI.
When ``zest.pocompile`` is added to the mix, it compiles the ``.po`` files immediately after checking out the tag.
This is right in time for creating the distributions, which should now contain the ``.mo`` files.

You may want the full release to fail early when ``zest.pocompile`` is not available.
Since version 1.6.0 this is possible by editing the ``setup.cfg`` of the package where you want this, and add the following section::

    [zest.releaser]
    prereleaser.before =
        zest.pocompile.available


Credits
=======

This package has been cobbled together by Maurits van Rees.

It depends on the `python-gettext <https://pypi.org/project/python-gettext/>`_ package,.
This itself suggests using the `Babel <https://pypi.org/project/Babel/>`_ package.
But it does exactly what we need and its releases are stored on PyPI, so we ignore that suggestion.

The main functions are taken from the ``build_mo`` command of `collective.releaser <https://pypi.org/project/collective.releaser/>`_.

Thanks!


To Do
=====

- Add tests.


.. _`zest.releaser`: https://pypi.org/project/zest.releaser/
