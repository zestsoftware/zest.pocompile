Changelog
=========

1.5.0 (2020-01-29)
------------------

- Claim Python 2 and 3 compatibility.
  Seems to work fine.
  [maurits]


1.4 (2013-07-05)
----------------

- Moved to https://github.com/zestsoftware/zest.pocompile.
  [maurits]


1.3 (2011-12-16)
----------------

- Fixed the example MANIFEST.in.
  [maurits]


1.2 (2011-12-16)
----------------

- Added a larger example of a MANIFEST.in file in the readme.  Also
  add a MANIFEST.in in zest.pocompile itself, so the CHANGES.txt is
  included in the source distribution.
  [maurits]


1.1 (2011-12-15)
----------------

- Look for ``.po`` files in any ``LC_MESSAGES`` directory.  It no
  longer matters if this is contained in a language directory within a
  ``locales`` or ``locale`` directory, as they could also have names
  like ``plonelocales`` or ``locales_for_version_2_only``.  Note that
  in Plone ``.po`` files can also be in an i18n directory, but those
  should not be compiled; this does not have a ``LC_MESSAGES``
  directory, so we automatically skip it.
  [maurits]


1.0 (2010-10-19)
----------------

- Initial release
