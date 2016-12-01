# -*- coding: utf-8 -*-

import binascii
import os

import pytest

import flake

V = flake.Violation


FLAKE8_EXAMPLE_OUTPUT = """
xxx/migrations/env.py:5:1:F401:'sys' imported but unused
xxx/migrations/env.py:6:1:F401:'re' imported but unused
xxx/migrations/env.py:9:1:E302:expected 2 blank lines, found 1
xxx/migrations/env.py:10:1:F401:'xxx._compat.text_type' imported but unused
xxx/migrations/env.py:16:1:E402:module level import not at top of file
xxx/migrations/env.py:17:1:E402:module level import not at top of file
xxx/migrations/env.py:97:1:E305:expected 2 blank lines after class or function definition, found 1
xxx/migrations/env.py:141:25:F821:undefined name 'xrange'
xxx/migrations/env.py:198:1:W391:blank line at end of file
xxx/migrations/env.py:200:1:E302:expected 2 blank lines, found 1
xxx/migrations/env.py:201:1:E999:something hypothetical: with a colon in it
"""  # noqa

EXPECTED_PARSE_RESULT = [
    V(path='xxx/migrations/env.py', row=5, col=1, code='F401',
      text="'sys' imported but unused"),
    V(path='xxx/migrations/env.py', row=6, col=1, code='F401',
      text="'re' imported but unused"),
    V(path='xxx/migrations/env.py', row=9, col=1, code='E302',
      text='expected 2 blank lines, found 1'),
    V(path='xxx/migrations/env.py', row=10, col=1, code='F401',
      text="'xxx._compat.text_type' imported but unused"),
    V(path='xxx/migrations/env.py', row=16, col=1, code='E402',
      text='module level import not at top of file'),
    V(path='xxx/migrations/env.py', row=17, col=1, code='E402',
      text='module level import not at top of file'),
    V(path='xxx/migrations/env.py', row=97, col=1, code='E305',
      text='expected 2 blank lines after class or function definition, found 1'),  # noqa
    V(path='xxx/migrations/env.py', row=141, col=25, code='F821',
      text="undefined name 'xrange'"),
    V(path='xxx/migrations/env.py', row=198, col=1, code='W391',
      text='blank line at end of file'),
    V(path='xxx/migrations/env.py', row=200, col=1, code='E302',
      text='expected 2 blank lines, found 1'),
    V(path='xxx/migrations/env.py', row=201, col=1, code='E999',
      text='something hypothetical: with a colon in it'),
]


def test_parse():
    assert flake.parse(FLAKE8_EXAMPLE_OUTPUT) == EXPECTED_PARSE_RESULT


class TestEnvironment(object):
    def test_creates_config_file(self):
        with flake.environment('config stuff', 'foo', 'foo/bar.py') as env:
            assert open(env.config_filename).read() == 'config stuff'

    @pytest.mark.parametrize('filename', [
        'foo.py'
        'bar/foo.py',
        'deeply/nested/directories.py',
        '.flake8',  # check we don't conflict with the config file
        'setup.py',
    ])
    def test_creates_check_file(self, filename):
        content = binascii.hexlify(os.urandom(32)).decode('utf8')
        with flake.environment('config stuff', content, filename) as env:
            assert open(env.filename).read() == content

    def test_cleans_up(self):
        with flake.environment('config stuff', 'foo', 'foo/bar.py') as env:
            pass
        assert not os.path.exists(env.config_filename)
        assert not os.path.exists(env.filename)
