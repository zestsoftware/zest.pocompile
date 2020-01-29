# -*- coding: utf-8 -*-
"""Compiles po files.

This walks through the given directories, finds all po translation
files in a properly formed locales directory and compiles them info mo
files.

When no directories are specified, the current directory is taken.
"""
# Note that the above doc string is used as help text (description) by
# the option parser.  Do not rely on formatting: line endings are
# ignored.

from optparse import OptionParser
from os.path import join
from pythongettext.msgfmt import Msgfmt

import logging
import os
import sys


try:
    from zest.releaser.utils import ask

    ask  # pyflakes
except ImportError:
    # No zest.releaser available
    ask = None

logger = logging.getLogger("zest.pocompile")


def find_lc_messages(path, dry_run=False):
    """Find 'LC_MESSAGES' directories and compile all .po files in it.

    Accepts an optional dry_run argument and passes this on.

    Adapted from collective.releaser.
    """
    for directory in os.listdir(path):
        dir_path = join(path, directory)
        if not os.path.isdir(dir_path):
            continue

        if directory == "LC_MESSAGES":
            compile_po(dir_path, dry_run=dry_run)
        else:
            find_lc_messages(dir_path, dry_run=dry_run)


def compile_po(path, dry_run=False):
    """path is a LC_MESSAGES directory.  Compile *.po into *.mo.

    Accepts an optional dry_run argument.  When True, only reports the
    found po files, without compiling them.

    Adapted from collective.releaser.
    """
    for domain_file in os.listdir(path):
        if domain_file.endswith(".po"):
            file_path = join(path, domain_file)
            if dry_run:
                logger.info("Found .po file: %s" % file_path)
                continue
            logger.info("Building .mo for %s" % file_path)
            mo_file = join(path, "%s.mo" % domain_file[:-3])
            mo_content = Msgfmt(file_path, name=file_path).get()
            mo = open(mo_file, "wb")
            mo.write(mo_content)
            mo.close()


def compile_in_tag(data):
    """Compile all po files in the tag.

    We expect to get a dictionary from zest.releaser, with a tagdir.

    When an exception occurs during finding/compiling, and we were
    indeed called as an entry point of zest.releaser, we ask the user
    what to do: continue with the release or not.
    """
    tagdir = data.get("tagdir")
    if not tagdir:
        logger.warn("Aborted compiling of po files: no tagdir found in data.")
        return
    logger.info("Finding and compiling po files in %s", tagdir)
    try:
        find_lc_messages(tagdir)
    except Exception:
        logger.warn("Finding and compiling aborted after exception.", exc_info=True)
        if data and ask:
            # We were called as an entry point of zest.releaser.
            if not ask(
                "Error compiling po file.  This could mean some "
                "languages have no working translations.  Do you want "
                "to continue with the release?"
            ):
                sys.exit(1)


def main(*args, **kwargs):
    """Run as stand-alone program.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Parsing arguments.  Note that the parse_args call might already
    # stop the program, displaying a help or usage message.
    usage = "usage: %prog [options] <directories>"
    parser = OptionParser(usage=usage, description=__doc__)
    parser.add_option(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Only report found po files, without compiling them.",
    )
    options, directories = parser.parse_args()

    if not directories:
        # Run only in the current working directory.
        directories = [os.getcwd()]

    # This might very well raise an exception like 'Not a directory'
    # and that is fine.
    for directory in directories:
        logger.info("Finding and compiling po files in %s", directory)
        find_lc_messages(directory, options.dry_run)
