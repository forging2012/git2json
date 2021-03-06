#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_git2json
----------------------------------

Tests for `git2json` module.
"""

import git2json
from nose.tools import eq_


def get_tst_path():
    '''Find where this test module is located so we can reference the fixtures
    folder.

    Named with tst to avoid Nose's pattern-matching.'''
    import os
    tp = os.path.split(__file__)[0] + '/'
    return tp


def int_test_parse_commits():
    '''Integration test: try to parse an entire git log from a file'''
    fixture = open(get_tst_path() + 'fixtures/test_git2json-1.txt')
    commits = list(git2json.parse_commits(fixture.read()))
    parent = commits[0]['parents']
    assert len(parent) == 2

    parent = commits[1]['parents']
    assert len(parent) == 1

    author = commits[0]['author']['name']
    eq_(author, 'Fernando Perez')

    email = commits[0]['author']['email']
    eq_(email.strip(), 'fernando.perez@berkeley.edu')

    author = commits[1]['author']['name']
    eq_(author, 'MinRK')

    email = commits[1]['author']['email']
    eq_(email, 'benjaminrk@gmail.com')

    committer = commits[0]['committer']['name']
    eq_(committer, 'Fernando Perez')

    email = commits[0]['committer']['email']
    eq_(email.strip(), 'fernando.perez@berkeley.edu')

    committer = commits[1]['committer']['name']
    eq_(committer, 'MinRK')

    email = commits[1]['committer']['email']
    eq_(email, 'benjaminrk@gmail.com')

    eq_(len(commits[0]['changes']), 0)
    eq_(len(commits[1]['changes']), 1)


def reg_test_7_hidden_files():
    '''Ensure leading periods in hidden file names are parsed.

    Regression test for:
    https://github.com/tarmstrong/git2json/issues/7
    '''
    fixture = open(get_tst_path() + 'fixtures/test_git2json-2.txt')
    commits = list(git2json.parse_commits(fixture.read()))
    second_commit = commits[1]
    changes = second_commit['changes']
    second_change = changes[1]
    fname = second_change[2]
    eq_(fname, '.travis.yml')


# I think git is stripping out the carriage return in the fixture files
# so I'm going to just hardcode this fixture here.
# In order to appease flake8 I've had to put in some line breaks in the message
# in weird places. This makes the test kind of unreadable, but it works.
CARRIAGE_RETURN_FIXTURE = '''commit 0829acac93a476ff5c13cb95de7ba7d00cf0c563
tree 0a1caf6f9510fb11a8d3a6a45c4af6000d778a5e
parent f4b6fd2ff84ee5edd261bfa9e1771326db1ed2e0
author Tavish Armstrong <tavisharmstrong@gmail.com> 1520702534 +0000
committer Tavish Armstrong <tavisharmstrong@gmail.com> 1520702662 +0000

    Hi\rthere\n    \n    Hi\rthere

2\t0\tfoo.txt

commit f4b6fd2ff84ee5edd261bfa9e1771326db1ed2e0
tree cbd2d9864b4b7e1508286ffed2e29c97cf4a6d78
author Tavish Armstrong <tavisharmstrong@gmail.com> 1520702520 +0000
committer Tavish Armstrong <tavisharmstrong@gmail.com> 1520702520 +0000

    initial commit

1\t0\tfoo.txt
'''


def reg_test_empty_message_lines():
    '''Empty lines (usually caused by a carriage return) don't cause crashes.

    Regression test for:
    https://github.com/tarmstrong/git2json/issues/11
    '''
    fixture = CARRIAGE_RETURN_FIXTURE
    commits = list(git2json.parse_commits(fixture))
    eq_(2, len(commits))
    second_commit = commits[0]
    message = second_commit['message']
    expected_message = '''Hi\rthere

Hi\rthere'''
    eq_(message, expected_message)
