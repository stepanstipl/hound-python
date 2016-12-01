# -*- coding: utf-8 -*-
"""A wrapper around the flake8 CLI."""

import os
import subprocess
from collections import namedtuple
from contextlib import contextmanager
from tempfile import TemporaryDirectory, mkstemp

FLAKE8_REPORT_FORMAT = r'%(path)s:%(row)d:%(col)d:%(code)s:%(text)s'

# A review environment
Environ = namedtuple('Environ', ['config_filename', 'filename'])
# A review violation
Violation = namedtuple('Violation', ['path', 'row', 'col', 'code', 'text'])


def check(config, content, filename):
    """
    Run flake8 with the given ``config`` against the passed file.

    Returns a ``list`` of :py:class:`flake.Violation`.
    """
    with environment(config, content, filename) as env:
        out = subprocess.check_output(['flake8',
                                       '--exit-zero',
                                       '--config',
                                       env.config_filename,
                                       '--format',
                                       FLAKE8_REPORT_FORMAT,
                                       env.filename],
                                      universal_newlines=True)
    return parse(out)


def parse(results):
    violations = []
    for line in results.split('\n'):
        if not line:
            continue
        path, row, col, code, text = line.split(':', 4)
        violations.append(Violation(path=path,
                                    row=int(row),
                                    col=int(col),
                                    code=code,
                                    text=text))
    return violations


@contextmanager
def environment(config, content, filename):
    """
    Create a temporary environment within which to run flake8.

    This context manager creates a temporary directory, within which it
    creates the file to be checked and the flake8 config file. It yields a
    :py:class:`flake.Environ`, which contains references to these files.

    Before yielding, this function changes directory to the temporary
    directory it creates. When leaving the context manager CWD will be
    restored.
    """
    cwd_prev = os.getcwd()
    try:
        with TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Write the config file to a randomly-named file to avoid
            # conflicting with the checked file.
            conf_fd, config_filename = mkstemp(dir=tmpdir)
            conf_fp = os.fdopen(conf_fd, 'w')
            conf_fp.write(config)
            conf_fp.close()

            dirname = os.path.dirname(filename)
            if dirname:
                os.makedirs(dirname)
            with open(filename, 'w') as fp:
                fp.write(content)

            yield Environ(config_filename=config_filename, filename=filename)
    finally:
        os.chdir(cwd_prev)
