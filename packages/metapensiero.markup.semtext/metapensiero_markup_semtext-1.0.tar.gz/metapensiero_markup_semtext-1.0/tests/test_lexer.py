# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- Tests for the SEM lexer
# :Created:   gio 24 nov 2016 00:47:10 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019 Lele Gaifax
#

import pytest

from metapensiero.markup.semtext.lexer import Lexer, SemError


GOOD_SEM_TEXTS = (
    (  # 0
        'Abra',
        ('TEXT', 'SEPARATOR')
    ),

    (  # 1
        '*Cadabra*',
        ('BOLD_START', 'TEXT', 'BOLD_STOP', 'SEPARATOR')
    ),

    (  # 2
        '/Foo/ *Bar*',
        ('ITALIC_START', 'TEXT', 'ITALIC_STOP',
         'TEXT',
         'BOLD_START', 'TEXT', 'BOLD_STOP',
         'SEPARATOR')
    ),

    (  # 3
        '- item',
        ('DOT_ITEM', 'INDENT', 'TEXT', 'SEPARATOR', 'DEDENT')
    ),

    (  # 4
        '- item\n  continued',
        ('DOT_ITEM', 'INDENT', 'TEXT', 'NEWLINE',
         'TEXT', 'SEPARATOR', 'DEDENT')
    ),

    (  # 5
        '- item\n  continued\n\n  other',
        ('DOT_ITEM', 'INDENT', 'TEXT', 'NEWLINE',
         'TEXT', 'SEPARATOR', 'TEXT', 'SEPARATOR',
         'DEDENT')
    ),

    (  # 6
        '1. item',
        ('NUM_ITEM', 'INDENT', 'TEXT', 'SEPARATOR', 'DEDENT')
    ),

    (  # 7
        '1. first\n\n   - a\n\n   - b\n\n10) tenth',
        ('NUM_ITEM', 'INDENT', 'TEXT', 'SEPARATOR',
         'DOT_ITEM', 'INDENT', 'TEXT', 'SEPARATOR', 'DEDENT',
         'DOT_ITEM', 'INDENT', 'TEXT', 'SEPARATOR', 'DEDENT',
         'DEDENT',
         'NUM_ITEM', 'INDENT', 'TEXT', 'SEPARATOR', 'DEDENT')
    ),

    (  # 8
        '/Foo!/ *Bar!* `foo <bar>`',
        ('ITALIC_START', 'TEXT', 'ITALIC_STOP',
         'TEXT',
         'BOLD_START', 'TEXT', 'BOLD_STOP',
         'TEXT',
         'LINK_START', 'TEXT', 'LINK_STOP',
         'SEPARATOR')
    ),

    (  # 9
        '= heading 1 =\n== heading2 ==\n= foo ==',
        ('HEADING_START', 'TEXT', 'HEADING_STOP', 'NEWLINE',
         'HEADING_START', 'TEXT', 'HEADING_STOP', 'NEWLINE',
         'TEXT', 'SEPARATOR')
    ),
)


@pytest.mark.parametrize('index', range(len(GOOD_SEM_TEXTS)))
def test_good_cases(index):
    text, tokens = GOOD_SEM_TEXTS[index]
    lexer = Lexer()
    assert tuple(t.type for t in lexer.tokenize(text)) == tokens


BAD_SEM_TEXTS = (
    (  # 0
        '/Abra',
        (1, 1)
    ),

    (  # 1
        'Abra/',
        (1, 5)
    ),

    (  # 3
        '*Abra',
        (1, 1)
    ),

    (  # 4
        'Abra*',
        (1, 5)
    ),

    (  # 5
        '/Abra *Cadabra*',
        (1, 7)
    ),

    (  # 6
        '*Abra /Cadabra/',
        (1, 7)
    ),

    (  # 7
        '`Abra /Cadabra/',
        (1, 7)
    ),
)


@pytest.mark.parametrize('index', range(len(BAD_SEM_TEXTS)))
def test_bad_cases(index):
    text, errpos = BAD_SEM_TEXTS[index]
    lexer = Lexer()
    try:
        all(lexer.tokenize(text))
    except SemError as e:
        assert e.position == errpos
    else:
        assert False, "Should raise an error"
