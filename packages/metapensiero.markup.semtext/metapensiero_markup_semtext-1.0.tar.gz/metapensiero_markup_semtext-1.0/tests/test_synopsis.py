# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- Tests for the SynopsisPrinter
# :Created:   ven 22 set 2017 18:09:05 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019 Lele Gaifax
#

from io import StringIO

import pytest

from metapensiero.markup.semtext import parse_text
from metapensiero.markup.semtext.visitor import SynopsisPrinter


SEM_TEXTS = (
    (  # 0
        'Abra',
        80,
        'Abra'
    ),

    (  # 1
        '*Cadabra*',
        80,
        'Cadabra'
    ),

    (  # 2
        '/Foo/ *Bar*',
        80,
        'Foo Bar'
    ),

    (  # 3
        """\
first list:

- item
  continued

- second

second:

- foo

- bar\
""",
        20,
        'first list: - item c…'
    ),

    (  # 4
        '`Abra <cadabra>`',
        80,
        'Abra'
    ),
)


@pytest.mark.parametrize('index', range(len(SEM_TEXTS)))
def test_synopsis_printer(index):
    text, max_length, expected = SEM_TEXTS[index]
    parsed = parse_text(text)
    printed = StringIO()
    SynopsisPrinter(max_length=max_length, where=printed).visit(parsed)
    assert printed.getvalue() == expected
