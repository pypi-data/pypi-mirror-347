# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- Tests for the SEM parser
# :Created:   gio 24 nov 2016 01:03:00 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019, 2020 Lele Gaifax
#

from io import StringIO

import pytest

from metapensiero.markup.semtext import html_to_text, parse_html, parse_text, text_to_html
from metapensiero.markup.semtext.visitor import ASTPrinter, HTMLPrinter, SEMPrinter


SEM_TEXTS = (
    (  # 0
        'Abra',
        """\
<text>
  <paragraph>
    <span>Abra</span>
  </paragraph>
</text>
"""
    ),

    (  # 1
        '*Cadabra*',
        """\
<text>
  <paragraph>
    <span style="bold">Cadabra</span>
  </paragraph>
</text>
"""
    ),

    (  # 2
        '/Foo/ *Bar*',
        """\
<text>
  <paragraph>
    <span style="italic">Foo</span><span> </span><span style="bold">Bar</span>
  </paragraph>
</text>
"""
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
        """\
<text>
  <paragraph>
    <span>first list:</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>item continued</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>second</span>
      </paragraph>
    </item>
  </list>
  <paragraph>
    <span>second:</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>foo</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>bar</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 4
        """\
- be /fool/

- *be* stoned
""",
        """\
<text>
  <list style="dotted">
    <item>
      <paragraph>
        <span>be </span><span style="italic">fool</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span style="bold">be</span><span> stoned</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 5
        """\
1. first

   - a

   - b

10) tenth
""",
        """\
<text>
  <list style="numeric">
    <item index="1">
      <paragraph>
        <span>first</span>
      </paragraph>
      <list style="dotted">
        <item>
          <paragraph>
            <span>a</span>
          </paragraph>
        </item>
        <item>
          <paragraph>
            <span>b</span>
          </paragraph>
        </item>
      </list>
    </item>
    <item index="10">
      <paragraph>
        <span>tenth</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 6
        """\
This is *just* a tiny /test/:

- One

- Two

  Three

Whoa!
""",
        """\
<text>
  <paragraph>
    <span>This is </span><span style="bold">just</span><span> a tiny </span><span style="italic">test</span><span>:</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>One</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>Two</span>
      </paragraph>
      <paragraph>
        <span>Three</span>
      </paragraph>
    </item>
  </list>
  <paragraph>
    <span>Whoa!</span>
  </paragraph>
</text>
"""
    ),

    (  # 7
        '`Abra <Cadabra>`',
        """\
<text>
  <paragraph>
    <link address="Cadabra">Abra</link>
  </paragraph>
</text>
"""
    ),

    (  # 8
        """\
= H1 =

Foo
""",
        """\
<text>
  <heading level="1">
    <span>H1</span>
  </heading>
  <paragraph>
    <span>Foo</span>
  </paragraph>
</text>
"""
    ),

    (  # 9
        """<b foo="bar">not bold's</b>""",
        """\
<text>
  <paragraph>
    <span><b foo="bar">not bold's</b></span>
  </paragraph>
</text>
"""
    ),

    (  # 10
        '`Abra <"Cadabra">`',
        """\
<text>
  <paragraph>
    <link address=""Cadabra"">Abra</link>
  </paragraph>
</text>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(SEM_TEXTS)))
def test_ast_printer(index):
    text, ast = SEM_TEXTS[index]
    parsed = parse_text(text)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast


@pytest.mark.parametrize('index', range(len(SEM_TEXTS)))
def test_sem_printer(index):
    text, ast = SEM_TEXTS[index]
    parsed = parse_text(text)
    stream = StringIO()
    SEMPrinter(where=stream).visit(parsed)
    reprinted = stream.getvalue()
    reparsed = parse_text(reprinted)
    stream = StringIO()
    ASTPrinter(where=stream).visit(reparsed)
    reast = stream.getvalue()
    assert reast == ast, reprinted


@pytest.mark.parametrize('index', range(len(SEM_TEXTS)))
def test_html_roundtrip(index):
    text, ast = SEM_TEXTS[index]
    parsed = parse_text(text)
    stream = StringIO()
    HTMLPrinter(where=stream).visit(parsed)
    html = stream.getvalue()
    reparsed = parse_html(html)
    stream = StringIO()
    ASTPrinter(where=stream).visit(reparsed)
    assert stream.getvalue() == ast, html


@pytest.mark.parametrize('index', range(len(SEM_TEXTS)))
def test_full_roundtrip(index):
    text, ast = SEM_TEXTS[index]
    html = text_to_html(text)
    text = html_to_text(html)
    parsed = parse_text(text)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast


# Following cases are invalid, exercize the parse_as_plain_text_on_errors flag

BAD_SEM_TEXTS = (
    (  # 0
        """\
*In macchina
Autostrada del Brennero A22 fino al casello di Bressanone...
Autostrada A27 fino a Ponte nelle Alpi,...
Autostrada A27 fino all'uscita di Belluno,...

*In treno
Brunico - 37 Km
Bolzano (via Passo Gardena) - 72 Km...
Collegamento stazione ferroviaria...

*In aereo
Venezia Treviso / Venezia Marco Polo – 180 / 200 km
Verona – 213 km
Milano Bergamo / Milano Malpensa - 310 / 400 km
""",
        """\
<text>
  <paragraph>
    <span>*In macchina
Autostrada del Brennero A22 fino al casello di Bressanone...
Autostrada A27 fino a Ponte nelle Alpi,...
Autostrada A27 fino all'uscita di Belluno,...</span>
  </paragraph>
  <paragraph>
    <span>*In treno
Brunico - 37 Km
Bolzano (via Passo Gardena) - 72 Km...
Collegamento stazione ferroviaria...</span>
  </paragraph>
  <paragraph>
    <span>*In aereo
Venezia Treviso / Venezia Marco Polo – 180 / 200 km
Verona – 213 km
Milano Bergamo / Milano Malpensa - 310 / 400 km</span>
  </paragraph>
</text>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(BAD_SEM_TEXTS)))
def test_bad_sem_texts_ast_printer(index):
    text, ast = BAD_SEM_TEXTS[index]
    parsed = parse_text(text, parse_as_plain_text_on_errors=True)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast
