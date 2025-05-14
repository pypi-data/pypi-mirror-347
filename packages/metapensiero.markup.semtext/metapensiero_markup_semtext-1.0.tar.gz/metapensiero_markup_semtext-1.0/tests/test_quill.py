# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- Tests for Quill interoperability
# :Created:   ven 28 lug 2017 18:04:04 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019, 2020 Lele Gaifax
#

from io import StringIO

import pytest

from metapensiero.markup.semtext import InvalidNestingError, from_delta, parse_text, to_delta
from metapensiero.markup.semtext.visitor import ASTPrinter, HTMLPrinter, SEMPrinter


# See https://codepen.io/anon/pen/EvVQEx for an easy way to build deltas

DELTAS = (
    (  # 0
        { "ops": [ { "insert": "Abra\n" } ] },
        """\
<text>
  <paragraph>
    <span>Abra</span>
  </paragraph>
</text>
"""
    ),

    (  # 1
        { "ops": [ { "attributes": { "bold": True }, "insert": "Cadabra" },
                   { "insert": "\n" }
        ]},
        """\
<text>
  <paragraph>
    <span style="bold">Cadabra</span>
  </paragraph>
</text>
"""
    ),

    (  # 2
        { "ops": [ { "attributes": { "italic": True }, "insert": "Foo " },
                   { "attributes": { "bold": True }, "insert": "Bar" },
                   { "insert": "\n" }
        ]},
        """\
<text>
  <paragraph>
    <span style="italic">Foo</span><span> </span><span style="bold">Bar</span>
  </paragraph>
</text>
"""
    ),

    (  # 3
        { "ops": [ { "insert": "first list:\nfirst item" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "insert": "second" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "insert": "second:\nfoo" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "insert": "bar" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" }
         ]},
        """\
<text>
  <paragraph>
    <span>first list:</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>first item</span>
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
        { "ops": [ { "insert": "be " },
                   { "attributes": { "italic": True }, "insert": "fool" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "attributes": { "bold": True }, "insert": "be" },
                   { "insert": " stoned" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" }
        ]},
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
        { "ops": [ { "insert": "This is " },
                   { "attributes": { "bold": True }, "insert": "just" },
                   { "insert": " a tiny " },
                   { "attributes": { "italic": True }, "insert": "test" },
                   { "insert": ":\nOne" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "insert": "Two" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "insert": "Three" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" },
                   { "insert": "Whoa!\n" }
        ]},
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
    </item>
    <item>
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

    (  # 6
        { "ops": [ { "insert": "one" },
                   { "attributes": { "list": "ordered" }, "insert": "\n" },
                   { "insert": "first" },
                   { "attributes": { "list": "bullet" }, "insert": "\n" }
        ]},
        """\
<text>
  <list style="numeric">
    <item>
      <paragraph>
        <span>one</span>
      </paragraph>
    </item>
  </list>
  <list style="dotted">
    <item>
      <paragraph>
        <span>first</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 7
        { "ops": [ { "insert": "one" },
                   { "attributes": { "list": "ordered" }, "insert": "\n" },
                   { "insert": "second" },
                   { "attributes": { "indent": 1, "list": "bullet" }, "insert": "\n" }
        ]},
        """\
<text>
  <list style="numeric">
    <item>
      <paragraph>
        <span>one</span>
      </paragraph>
      <list style="dotted">
        <item>
          <paragraph>
            <span>second</span>
          </paragraph>
        </item>
      </list>
    </item>
  </list>
</text>
"""
    ),

    (  # 8
        { "ops": [ { "insert": "one" },
                   { "attributes": { "list": "ordered" }, "insert": "\n" },
                   { "insert": "first" },
                   { "attributes": { "indent": 1, "list": "bullet" }, "insert": "\n" },
                   { "insert": "second" },
                   { "attributes": { "indent": 1, "list": "bullet" }, "insert": "\n" },
                   { "insert": "two" },
                   { "attributes": { "list": "ordered" }, "insert": "\n" }
        ]},
        """\
<text>
  <list style="numeric">
    <item>
      <paragraph>
        <span>one</span>
      </paragraph>
      <list style="dotted">
        <item>
          <paragraph>
            <span>first</span>
          </paragraph>
        </item>
        <item>
          <paragraph>
            <span>second</span>
          </paragraph>
        </item>
      </list>
    </item>
    <item>
      <paragraph>
        <span>two</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 9
        { "ops": [ { "insert": "Paragraph\n\none" },
                   { "attributes": { "list": "ordered" }, "insert": "\n" },
                   { "insert": "two" },
                   { "attributes": { "list": "ordered" }, "insert": "\n" },
                   { "insert": "point" },
                   { "attributes": { "indent": 1, "list": "bullet" }, "insert": "\n" },
                   { "insert": "other point" },
                   { "attributes": { "indent": 1, "list": "bullet" }, "insert": "\n" }
        ]},
        """\
<text>
  <paragraph>
    <span>Paragraph</span>
  </paragraph>
  <list style="numeric">
    <item>
      <paragraph>
        <span>one</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>two</span>
      </paragraph>
      <list style="dotted">
        <item>
          <paragraph>
            <span>point</span>
          </paragraph>
        </item>
        <item>
          <paragraph>
            <span>other point</span>
          </paragraph>
        </item>
      </list>
    </item>
  </list>
</text>
"""
    ),

    (  # 10
        { "ops": [ { "insert": "Gandalf the " },
                   { "attributes": { "link": "foo.ask" }, "insert": "Grey" },
                   { "insert": "\n" }
        ]},
        """\
<text>
  <paragraph>
    <span>Gandalf the </span><link address="foo.ask">Grey</link>
  </paragraph>
</text>
"""
    ),

    (  # 11
        { "ops": [ { "attributes": { "bold": True }, "insert": "Gandalf the Grey" },
                   { "insert": "\nCippa\n" }
        ]},
        """\
<text>
  <paragraph>
    <span style="bold">Gandalf the Grey</span>
  </paragraph>
  <paragraph>
    <span>Cippa</span>
  </paragraph>
</text>
"""
    ),

    (  # 12
        { "ops": [ { "insert": "Gandalf the Grey" }, { "attributes": { "header": 1 },
                                                       "insert": "\n" },
                   { "insert": "Gandalf is " },
                   { "attributes": { "bold": True }, "insert": "the" },
                   { "insert": " magician!\n" }
        ]},
        """\
<text>
  <heading level="1">
    <span>Gandalf the Grey</span>
  </heading>
  <paragraph>
    <span>Gandalf is </span><span style="bold">the</span><span> magician!</span>
  </paragraph>
</text>
"""
    ),

    (  # 13
        {'ops': [{'insert': '23. -25. Oktober - Carne Salada in festa'},
                 {'attributes': {'header': 3}, 'insert': '\n'},
                 {'insert': 'Palameeting, Riva del Garda'},
                 {'attributes': {'bold': 1}, 'insert': ' Carne Salada'},
                 {'insert': '. Diese Fleischspezialität gilt als gastronomisches '
                  'Aushängeschild des nördlichen Gardasees und wurde als '
                  'erstes typisches Gericht mit dem lokalen Gütesiegel '
                  '„De.Co.“ ausgezeichnet. '},
                 {'attributes': {'bold': 1},
                  'insert': 'Reise in das Universum des guten Geschmacks'},
                 {'insert': ', vorbei an einmaligen Rezepten, die Wein und Olivenöl '
                  'Extravergine, Soßen, Gemüse und viele andere '
                  'Köstlichkeiten auf den Tisch zaubern, die so nur am '
                  'nördlichen Gardasee und im Trient zu finden sind.'},
                 {'attributes': {'bold': 1}, 'insert': ' Info & Programm'},
                 {'insert': ' hier: '},
                 {'attributes': {'link': 'http://www.gardatrentino.it/prenota'},
                  'insert': 'http://www.gardatrentino.it/prenota'}]},
        """\
<text>
  <heading level="3">
    <span>23. -25. Oktober - Carne Salada in festa</span>
  </heading>
  <paragraph>
    <span>Palameeting, Riva del Garda</span><span> </span><span style="bold">Carne Salada</span><span>. Diese Fleischspezialität gilt als gastronomisches Aushängeschild des nördlichen Gardasees und wurde als erstes typisches Gericht mit dem lokalen Gütesiegel „De.Co.“ ausgezeichnet. </span><span style="bold">Reise in das Universum des guten Geschmacks</span><span>, vorbei an einmaligen Rezepten, die Wein und Olivenöl Extravergine, Soßen, Gemüse und viele andere Köstlichkeiten auf den Tisch zaubern, die so nur am nördlichen Gardasee und im Trient zu finden sind.</span><span> </span><span style="bold">Info & Programm</span><span> hier: </span><link address="http://www.gardatrentino.it/prenota">http://www.gardatrentino.it/prenota</link>
  </paragraph>
</text>
"""
    ),

    (  # 14
        {"ops": [{"insert": "Kirche Madonna dell‘Angelo"},
                 {"attributes": {"align": "justify", "code-block": True}, "insert": "\n"}]},
        """\
<text>
  <paragraph>
    <span>Kirche Madonna dell‘Angelo</span>
  </paragraph>
</text>
"""
    ),

    (  # 15
        {'ops': [{'insert': 'All activity'},
                 {'attributes': {'header': 2}, 'insert': '\n'},
                 {'attributes': {'alt': '@foo',
                                 'height': '32',
                                 'link': 'https://github.com/foo',
                                 'width': '32'},
                  'insert': {'image': 'https://foo.bar.com/u/abc?s=64&v=4'}},
                 {'attributes': {'link': 'https://github.com/deezer/spleeter/stargazers'},
                  'insert': '5.8k'},
                 {'insert': '\nUpdated Nov 8\n'}]},
        """\
<text>
  <heading level="2">
    <span>All activity</span>
  </heading>
  <paragraph>
    <link address="https://github.com/deezer/spleeter/stargazers">5.8k</link>
  </paragraph>
  <paragraph>
    <span>Updated Nov 8</span>
  </paragraph>
</text>
"""
    ),

    (  # 16
        {'ops': [{'attributes': {'header': 1}, 'insert': '\n'}]},
        """\
<text>
</text>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(DELTAS)))
def test_from_delta(index):
    delta, ast = DELTAS[index]
    parsed = from_delta(delta)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast


@pytest.mark.parametrize('index', range(len(DELTAS)))
def test_roundtrip(index):
    delta, ast = DELTAS[index]
    parsed = from_delta(delta)
    new_delta = to_delta(parsed)
    reparsed = from_delta(new_delta)
    printed = StringIO()
    ASTPrinter(where=printed).visit(reparsed)
    result = printed.getvalue()
    assert result == ast


@pytest.mark.parametrize('index', range(len(DELTAS)))
def test_sem_printer(index):
    delta, ast = DELTAS[index]
    parsed = from_delta(delta)
    stream = StringIO()
    SEMPrinter(where=stream).visit(parsed)
    semtext = stream.getvalue()
    reparsed = parse_text(semtext)
    stream = StringIO()
    SEMPrinter(where=stream).visit(reparsed)
    semtext2 = stream.getvalue()
    assert semtext == semtext2


def test_invalid_nesting():
    delta = {
        "ops": [ { "insert": "Paragraph\n\none" },
                 { "attributes": { "list": "ordered" }, "insert": "\n" },
                 { "insert": "two" },
                 { "attributes": { "list": "ordered" }, "insert": "\n" },
                 { "insert": "point" },
                 { "attributes": { "indent": 1, "list": "bullet" }, "insert": "\n" },
                 { "insert": "other point" },
                 { "attributes": { "indent": 3, "list": "bullet" }, "insert": "\n" }
        ]}
    with pytest.raises(InvalidNestingError) as error:
        from_delta(delta)
    assert error.value.expected == 2
    assert error.value.got == 3


RICH_DELTAS = (
    (  # 0
        {"ops": [
            {
                "attributes": {
                    "color": "#ff9900"
                },
                "insert": "Gandalf"
            },
            {
                "insert": " "
            },
            {
                "attributes": {
                    "background": "#facccc"
                },
                "insert": "the"
            },
            {
                "insert": " "
            },
            {
                "attributes": {
                    "size": "large",
                    "font": "monospace",
                    "script": "sub"
                },
                "insert": "Grey"
            },
            {
                "attributes": {
                    "align": "center"
                },
                "insert": "\n"
            }
        ]},
        """\
<text>
  <paragraph>
    <span>Gandalf</span><span> </span><span>the</span><span> </span><span>Grey</span>
  </paragraph>
</text>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(RICH_DELTAS)))
def test_from_rich_delta(index):
    delta, ast = RICH_DELTAS[index]
    parsed = from_delta(delta)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast


PROBLEMATIC_DELTAS = (
    (  # 0
        {"ops": [
            {"attributes": {
                "bold": True,
                "link": "https://e.io/145/"},
             "insert": "Text: \"Quoted"},
            {"attributes": {
                "link": "https://e.io/145/"},
             "insert": "\""},
            {"insert": "\n"},
            {"attributes": {"color": "#272727"},
             "insert": "Text..."},
            {"insert": "\n"},
            {"attributes": {
                "color": "#272727",
                "bold": True},
             "insert": "Text "},
            {"attributes": {
                "bold": True,
                "color": "#272727",
                "link": "https://e.io/145/"},
             "insert": "link."},
            {"insert": "\n"}]},
        """\
<p><a href="https://e.io/145/">Text: &quot;Quoted</a><a href="https://e.io/145/">&quot;</a></p>
<p>Text...</p>
<p><strong>Text</strong> <a href="https://e.io/145/">link.</a></p>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(PROBLEMATIC_DELTAS)))
def test_delta_to_html(index):
    delta, html = PROBLEMATIC_DELTAS[index]
    parsed = from_delta(delta)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    ast = printed.getvalue()
    printed = StringIO()
    HTMLPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == html, ast
