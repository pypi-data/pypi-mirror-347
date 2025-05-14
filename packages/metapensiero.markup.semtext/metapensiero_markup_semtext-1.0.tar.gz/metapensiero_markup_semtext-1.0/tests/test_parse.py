# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- Tests for the main entry point
# :Created:   gio 24 nov 2016 10:00:15 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019, 2022 Lele Gaifax
#

from io import StringIO

from metapensiero.markup.semtext import (SpanStyle, UnparsableError,
                                         parse_html, parse_text)
from metapensiero.markup.semtext.visitor import ASTPrinter

import pytest


def test_good_text():
    text = 'abra *cadabra*'
    result = parse_text(text)
    para = result.children[0]
    assert len(para.children) == 2
    assert para.children[1].style == SpanStyle.BOLD


def test_bad_text():
    text = 'abra *cadabra/'
    try:
        parse_text(text)
    except UnparsableError as e:
        assert e.message == 'Could not parse SEM text: token "ITALIC_STOP" at line 1 column 14'
        para = e.text.children[0]
    else:
        assert False, "Should raise an exception"
    assert len(para.children) == 1
    child = para.children[0]
    assert child.text == text
    assert child.style == SpanStyle.PLAIN


SEM_HTMLS = (
    (  # 0
        '<p>Abra</p>',
        """\
<text>
  <paragraph>
    <span>Abra</span>
  </paragraph>
</text>
"""
    ),

    (  # 1
        '<p><strong>Cadabra</strong></p>',
        """\
<text>
  <paragraph>
    <span style="bold">Cadabra</span>
  </paragraph>
</text>
"""
    ),

    (  # 2
        '<p><em>Foo</em> <strong>Bar</strong></p>',
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
<p>first list:</p>

<ul>
  <li>item<br />
    continued
  </li>

  <li>second
  </li>
</ul>

<p>second:</p>

<ul>
<li>foo</li>

<li>bar</li>
</ul>
""",
        """\
<text>
  <paragraph>
    <span>first list:</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>item</span>
      </paragraph>
      <paragraph>
        <span>continued</span>
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
<ul>
  <li>item<br />
    continued
  </li>

  <li>inner list
    <ol>
      <li>one</li>
      <li value="3">three</li>
      <li>four</li>
    </ol>
  </li>
</ul>
""",
        """\
<text>
  <list style="dotted">
    <item>
      <paragraph>
        <span>item</span>
      </paragraph>
      <paragraph>
        <span>continued</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>inner list</span>
      </paragraph>
      <list style="numeric">
        <item index="1">
          <paragraph>
            <span>one</span>
          </paragraph>
        </item>
        <item index="3">
          <paragraph>
            <span>three</span>
          </paragraph>
        </item>
        <item index="4">
          <paragraph>
            <span>four</span>
          </paragraph>
        </item>
      </list>
    </item>
  </list>
</text>
"""
    ),

    (  # 5
        """\
<ul>
  <li>
    item<br />
    continued
  </li>

  <li>
   second item
  </li>

  <li>
   third item
  </li>
</ul>
""",
        """\
<text>
  <list style="dotted">
    <item>
      <paragraph>
        <span>item</span>
      </paragraph>
      <paragraph>
        <span>continued</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>second item</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>third item</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 6
        '<p>abra <STRONG>cadabra</strong></p>',
        """\
<text>
  <paragraph>
    <span>abra </span><span style="bold">cadabra</span>
  </paragraph>
</text>
"""
    ),

    (  # 7
        """\
<p>
  <strong>cadabra</strong>
</p>
""",
        """\
<text>
  <paragraph>
    <span style="bold">cadabra</span>
  </paragraph>
</text>
"""
    ),

    (  # 8
        """\
<p>
  <b>cadabra</b>
</p>
""",
        """\
<text>
  <paragraph>
    <span style="bold">cadabra</span>
  </paragraph>
</text>
"""
    ),

    (  # 9
        """\
<p><br /></p>

<ul>
  <li>item<br /></li>
</ul>
""",
        """\
<text>
  <list style="dotted">
    <item>
      <paragraph>
        <span>item</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),

    (  # 10
        """\
<p>Gita semplice con le ciaspole con le guide alpine di Madonna di Campiglio, mattutina e pomeridiana</p>
<p>Ritrovo: 1^ gita ore 9.30,&nbsp; 2^ gita ore 12.30 presso ufficio guide alpine via Cima Tosa 7, ritorno previsto 1^ gita ore 13.30, 2^ gita ore 16.30</p>
<p></p>
<p>Itinerario: Madonna di Campiglio, risalita con telecabina Spinale, lago Spinale, pian del Graffer, rifugio Boch, rientro con telecabina Grost&egrave;, ritorno a Madonna di Campiglio</p>
<p></p>
<p><br />Per tutte le gite sono necessari scarponcini da trekking o similari alti sulla caviglia, abbigliamento da montagna</p>
<p>Prezzo: &euro; 30 a persona. Gli impianti di risalita e lo skibus sono a carico del cliente.</p>
<p><i>&nbsp;</i></p>
<p></p>
<p>Informazioni e prenotazioni c/o ufficio Guide Alpine</p>
<p>Via Cima Tosa, 7 - &nbsp;Madonna di Campiglio</p>
<p>aperto con orario 17.30-19.30</p>
<p>Tel. 0465/442634 - mob. +39 3357193660</p>
<p><a href="mailto:Info@guidealpinecampiglio.it">info@guidealpinecampiglio.it</a></p>
<p></p>
<p></p>""",
        """\
<text>
  <paragraph>
    <span>Gita semplice con le ciaspole con le guide alpine di Madonna di Campiglio, mattutina e pomeridiana</span>
  </paragraph>
  <paragraph>
    <span>Ritrovo: 1^ gita ore 9.30, 2^ gita ore 12.30 presso ufficio guide alpine via Cima Tosa 7, ritorno previsto 1^ gita ore 13.30, 2^ gita ore 16.30</span>
  </paragraph>
  <paragraph>
    <span>Itinerario: Madonna di Campiglio, risalita con telecabina Spinale, lago Spinale, pian del Graffer, rifugio Boch, rientro con telecabina Grostè, ritorno a Madonna di Campiglio</span>
  </paragraph>
  <paragraph>
    <span>Per tutte le gite sono necessari scarponcini da trekking o similari alti sulla caviglia, abbigliamento da montagna</span>
  </paragraph>
  <paragraph>
    <span>Prezzo: € 30 a persona. Gli impianti di risalita e lo skibus sono a carico del cliente.</span>
  </paragraph>
  <paragraph>
    <span>Informazioni e prenotazioni c/o ufficio Guide Alpine</span>
  </paragraph>
  <paragraph>
    <span>Via Cima Tosa, 7 - Madonna di Campiglio</span>
  </paragraph>
  <paragraph>
    <span>aperto con orario 17.30-19.30</span>
  </paragraph>
  <paragraph>
    <span>Tel. 0465/442634 - mob. +39 3357193660</span>
  </paragraph>
  <paragraph>
    <link address="mailto:Info@guidealpinecampiglio.it">info@guidealpinecampiglio.it</link>
  </paragraph>
</text>
"""
    ),

    (  # 11
        """\
<p><a href="http://example.it/"></a></p>
""",
        """\
<text>
</text>
"""
    ),

    (  # 12
        """\
<p>A paragraph</p>
<p></p>
<p><span style="color: #555555; float: none;">&nbsp;</span></p>
<p></p>
""",
        """\
<text>
  <paragraph>
    <span>A paragraph</span>
  </paragraph>
</text>
"""
    ),

    (  # 13
        """\
<div>simple</div>
""",
        """\
<text>
  <paragraph>
    <span>simple</span>
  </paragraph>
</text>
"""
    ),

    (  # 14
        """\
<div class="grid_4 form_prenota_container floated_right">
<div class="cerca_prenota_container"></div>
</div>
<div class="grid_8 contenuti contenuti_pagine_eventi">
<p>Le strade di Pinzolo si animeranno sabato 30 giugno&nbsp; con i bikers in erba della
<b>"DoloMini"</b>, la staffetta promozionale a squadre organizzata in collaborazione con la MTB
Adamello Brenta. Partenza ad ore 16:30 nel centro di Pinzolo, lungo un percorso ad anello
aperto ai piccoli sportivi (atleti nati dal 01/01/2006 al 31/12/2012).</p>
<p>&nbsp;</p>
<p>La manifestazione &ldquo;Dolomini&rdquo; consiste in una staffetta a squadre (Team Relay
F.C.I. Gioco Ciclismo) da svolgersi in sella a biciclette del tipo: Mountain Bike.<br />
La manifestazione si svolger&agrave; a Pinzolo (TN) il giorno sabato 30 giugno 2018 a partire
dalle ore 16:30; il tracciato proposto dagli organizzatori si svilupper&agrave; nel centro
storico/pedonale del paese su un percorso chiuso ad anello dove saranno presenti piccoli
ostacoli per prove di abilit&agrave;. Il campo di gara sar&agrave; opportunamente segnalato,
delimitato e sorvegliato durante lo svolgimento delle prove con il divieto al transito per
non autorizzati.</p>
<p>Per tutto quanto non espressamente esposto si fa riferimento al regolamento federale.</p>
<p>L&rsquo;organizzazione sar&agrave; curata da: MTB Adamello Brenta, Dolomitica Brenta Bike,
Valrendenaike, APT Madonna di Campiglio Pinzolo Val Rendena.</p>
<p></p>
<p>16-17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Consegna numeri identificativi squadre Dolomini</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; c/o campo gara</p>
<p><b>17.00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </b>partenza<b>&nbsp; Dolomini&nbsp;</b> staffetta a squadre per ragazzi (nati dall&rsquo;1/1/2006 al 31/12/2012</p>
<p></p>
<p></p>
<p><i>info e iscrizioni</i></p>
<p><a href="https://www.campigliodolomiti.it/lang/IT/pagine/dettaglio/dolomitica,181/dolomitica_home_page,1277.html">www.campigliodolomiti.it/dolomitica</a></p>
</div>
""",
        """\
<text>
  <paragraph>
    <span>Le strade di Pinzolo si animeranno sabato 30 giugno con i bikers in erba della </span><span style="bold">"DoloMini"</span><span>, la staffetta promozionale a squadre organizzata in collaborazione con la MTB Adamello Brenta. Partenza ad ore 16:30 nel centro di Pinzolo, lungo un percorso ad anello aperto ai piccoli sportivi (atleti nati dal 01/01/2006 al 31/12/2012).</span>
  </paragraph>
  <paragraph>
    <span>La manifestazione “Dolomini” consiste in una staffetta a squadre (Team Relay F.C.I. Gioco Ciclismo) da svolgersi in sella a biciclette del tipo: Mountain Bike.</span>
  </paragraph>
  <paragraph>
    <span>La manifestazione si svolgerà a Pinzolo (TN) il giorno sabato 30 giugno 2018 a partire dalle ore 16:30; il tracciato proposto dagli organizzatori si svilupperà nel centro storico/pedonale del paese su un percorso chiuso ad anello dove saranno presenti piccoli ostacoli per prove di abilità. Il campo di gara sarà opportunamente segnalato, delimitato e sorvegliato durante lo svolgimento delle prove con il divieto al transito per non autorizzati.</span>
  </paragraph>
  <paragraph>
    <span>Per tutto quanto non espressamente esposto si fa riferimento al regolamento federale.</span>
  </paragraph>
  <paragraph>
    <span>L’organizzazione sarà curata da: MTB Adamello Brenta, Dolomitica Brenta Bike, Valrendenaike, APT Madonna di Campiglio Pinzolo Val Rendena.</span>
  </paragraph>
  <paragraph>
    <span>16-17 Consegna numeri identificativi squadre Dolomini</span>
  </paragraph>
  <paragraph>
    <span>c/o campo gara</span>
  </paragraph>
  <paragraph>
    <span style="bold">17.00 </span><span>partenza</span><span style="bold"> Dolomini </span><span> staffetta a squadre per ragazzi (nati dall’1/1/2006 al 31/12/2012</span>
  </paragraph>
  <paragraph>
    <span style="italic">info e iscrizioni</span>
  </paragraph>
  <paragraph>
    <link address="https://www.campigliodolomiti.it/lang/IT/pagine/dettaglio/dolomitica,181/dolomitica_home_page,1277.html">www.campigliodolomiti.it/dolomitica</link>
  </paragraph>
</text>
"""
    ),

    (  # 15
        """\
<h4><b>Giovenche di Razza Rendena. Sfilata e...dintorni</b><br /><br /></h4>
<p><b>Luned&igrave; 27 agosto<br /></b>Pinzolo - Piazza Carera<br />Ore 17.00</p>
<p></p>
""",
        """\
<text>
  <heading level="4">
    <span style="bold">Giovenche di Razza Rendena. Sfilata e...dintorni</span>
  </heading>
  <paragraph>
    <span style="bold">Lunedì 27 agosto</span>
  </paragraph>
  <paragraph>
    <span>Pinzolo - Piazza Carera</span>
  </paragraph>
  <paragraph>
    <span>Ore 17.00</span>
  </paragraph>
</text>
"""
    ),

    (  # 16
        """\
<p>Arrivo in piazza di Santa Lucia per tutti i bambini del paese...</p>
<br/>
""",
        """\
<text>
  <paragraph>
    <span>Arrivo in piazza di Santa Lucia per tutti i bambini del paese...</span>
  </paragraph>
</text>
"""
    ),

    (  # 17
        """\
<h2><span>Tutti i gioved&igrave;: e</span>scursione al Doss del Sabion con aperitivo a Malga Cioca.</h2>
<p></p>
<p style="margin: 0cm; margin-bottom: .0001pt; line-height: 16.5pt; font-variant-ligatures: normal; font-variant-caps: normal; orphans: 2; text-align: start; widows: 2; -webkit-text-stroke-width: 0px; word-spacing: 0px;"><span style="font-size: 11.5pt; font-family: 'open_sansregular','serif'; color: #333333;">Orario:&nbsp;16.00-19.00</span></p>
<p style="margin: 0cm; margin-bottom: .0001pt; line-height: 16.5pt; font-variant-ligatures: normal; font-variant-caps: normal; orphans: 2; text-align: start; widows: 2; -webkit-text-stroke-width: 0px; word-spacing: 0px;"><span style="font-size: 11.5pt; font-family: 'open_sansregular','serif'; color: #333333;">Costo: &euro;&nbsp;25 adulti, &euro; 15 bambini 10-16 anni. &euro; 5 noleggio attrezzatura</span></p>
<p></p>
<p style="margin: 0cm; margin-bottom: .0001pt; line-height: 16.5pt;"><span style="font-size: 11.5pt; font-family: 'open_sansregular','serif'; color: #333333;">Info e prenotazioni:<br /> tel +39 0465 502111<br /> mobile +39 345 3858648<br /> email<span class="apple-converted-space">&nbsp;</span><a href="mailto:info@mountainfriends.it"><span style="color: #d0112b;">info@mountainfriends.it</span></a></span></p>
""",
        """\
<text>
  <heading level="2">
    <span>Tutti i giovedì: escursione al Doss del Sabion con aperitivo a Malga Cioca.</span>
  </heading>
  <paragraph>
    <span>Orario: 16.00-19.00</span>
  </paragraph>
  <paragraph>
    <span>Costo: € 25 adulti, € 15 bambini 10-16 anni. € 5 noleggio attrezzatura</span>
  </paragraph>
  <paragraph>
    <span>Info e prenotazioni:</span>
  </paragraph>
  <paragraph>
    <span>tel +39 0465 502111</span>
  </paragraph>
  <paragraph>
    <span>mobile +39 345 3858648</span>
  </paragraph>
  <paragraph>
    <span>email </span><link address="mailto:info@mountainfriends.it">info@mountainfriends.it</link>
  </paragraph>
</text>
"""
    ),

    (  # 18
        """\
<div> </div> <div> </div> <div> Da non perdere il <strong>Giro dele fraziòn de
Garniga - 41esima edizione</strong>, mercoledì 15 alle h. 9.00.</div> <div> La settima
edizione di <strong>Garniga Beach Volley</strong> prende il via mercoledì 15 agosto;
finali sabato h. 16.00.</div> <div> </div> <div> <strong>E per i più
piccoli... </strong></div> <div> Giovedì 16 Gara di disegno, Miniolimpiadi, truccabimbi,
palloncini e bolle di sapone.</div> <div> <strong>Novità 2018</strong>: mercoledì 15
agosto alle h. 16.00 <strong>Il tesoro misterioso del bosco odoroso</strong>, attività per
bambini con merenda finale!</div> <div> </div> <div> <a
href="https://www.discovertrento.it/documents/10551/293221/Pieghevole_FESTA+FERRAGOSTO+GARNIGA+2018.pdf">Scarica
l'intero programma!</a></div> <div> </div> <div> Durante la Festa di Ferragosto
<strong>cucina tipica trentina</strong>, aperta tutti i giorni, vaso della fortuna e tutti
i giorni dopo le h. 16.00 <strong>strauben e gelato allo yogurt fresco</strong>!</div>
<div> </div>
""",
        """\
<text>
  <paragraph>
    <span>Da non perdere il </span><span style="bold">Giro dele fraziòn de Garniga - 41esima edizione</span><span>, mercoledì 15 alle h. 9.00.</span>
  </paragraph>
  <paragraph>
    <span>La settima edizione di </span><span style="bold">Garniga Beach Volley</span><span> prende il via mercoledì 15 agosto; finali sabato h. 16.00.</span>
  </paragraph>
  <paragraph>
    <span style="bold">E per i più piccoli...</span>
  </paragraph>
  <paragraph>
    <span>Giovedì 16 Gara di disegno, Miniolimpiadi, truccabimbi, palloncini e bolle di sapone.</span>
  </paragraph>
  <paragraph>
    <span style="bold">Novità 2018</span><span>: mercoledì 15 agosto alle h. 16.00 </span><span style="bold">Il tesoro misterioso del bosco odoroso</span><span>, attività per bambini con merenda finale!</span>
  </paragraph>
  <paragraph>
    <link address="https://www.discovertrento.it/documents/10551/293221/Pieghevole_FESTA+FERRAGOSTO+GARNIGA+2018.pdf">Scarica l'intero programma!</link>
  </paragraph>
  <paragraph>
    <span>Durante la Festa di Ferragosto </span><span style="bold">cucina tipica trentina</span><span>, aperta tutti i giorni, vaso della fortuna e tutti i giorni dopo le h. 16.00 </span><span style="bold">strauben e gelato allo yogurt fresco</span><span>!</span>
  </paragraph>
</text>
"""
    ),

    (  # 19
        """\
<p><strong></strong></p>
<p><strong>Mercatino di Natale ad Arco</strong><br />
17-19 / 24-26 Novembre, 1-3 / 7-10 / 15-17 / 21-24 / 26-31 Dicembre e 1-2 / 4-7 Gennaio 2018</p>
<p><br />
</p>
<p><strong>Di Gusto in Gusto Villaggio di Natale - Riva del Garda</strong><br />
2-3 / 7-10 / 13-17 / 21-24 / 26-31 Dicembre e 1-7 Gennaio 2018&nbsp;</p>
<div><br />
</div>
<div><strong>Orari e Prezzi:&nbsp;</strong><strong>www.gardatrentino.it/Inverno</strong>
<div>
<p><strong></strong></p>
</div>
</div>
""",
        """\
<text>
  <paragraph>
    <span style="bold">Mercatino di Natale ad Arco</span>
  </paragraph>
  <paragraph>
    <span>17-19 / 24-26 Novembre, 1-3 / 7-10 / 15-17 / 21-24 / 26-31 Dicembre e 1-2 / 4-7 Gennaio 2018</span>
  </paragraph>
  <paragraph>
    <span style="bold">Di Gusto in Gusto Villaggio di Natale - Riva del Garda</span>
  </paragraph>
  <paragraph>
    <span>2-3 / 7-10 / 13-17 / 21-24 / 26-31 Dicembre e 1-7 Gennaio 2018</span>
  </paragraph>
  <paragraph>
    <span style="bold">Orari e Prezzi: www.gardatrentino.it/Inverno</span>
  </paragraph>
</text>
"""
    ),

    (  # 20
        """\
<h3>23. -25. Oktober - Carne Salada in festa</h3><p><b>Palameeting, Riva del
Garda</b><br><br>Drei Tage lang steht Garda con Gusto ganz im Zeichen des<b>&nbsp;Carne
Salada</b>. Diese Fleischspezialität gilt als gastronomisches Aushängeschild des nördlichen
Gardasees und wurde als erstes typisches Gericht mit dem lokalen Gütesiegel „De.Co.“
ausgezeichnet.&nbsp;Die Veranstaltung nimmt Besucher mit auf eine&nbsp;<b>Reise in das
Universum des guten Geschmacks</b>, vorbei an einmaligen Rezepten, die Wein und Olivenöl
Extravergine, Soßen, Gemüse und viele andere Köstlichkeiten auf den Tisch zaubern, die so nur
am nördlichen Gardasee und im Trient zu finden
sind.<b>&nbsp;</b></p><p><b>Info&amp;Programm</b>&nbsp;hier:&nbsp;<a
href="http://www.gardatrentino.it/prenota"
class=""><b>www.gardatrentino.it/CarneSalada</b></a></p><h3></h3>
""",
        """\
<text>
  <heading level="3">
    <span>23. -25. Oktober - Carne Salada in festa</span>
  </heading>
  <paragraph>
    <span style="bold">Palameeting, Riva del Garda</span>
  </paragraph>
  <paragraph>
    <span>Drei Tage lang steht Garda con Gusto ganz im Zeichen des</span><span style="bold"> Carne Salada</span><span>. Diese Fleischspezialität gilt als gastronomisches Aushängeschild des nördlichen Gardasees und wurde als erstes typisches Gericht mit dem lokalen Gütesiegel „De.Co.“ ausgezeichnet. Die Veranstaltung nimmt Besucher mit auf eine </span><span style="bold">Reise in das Universum des guten Geschmacks</span><span>, vorbei an einmaligen Rezepten, die Wein und Olivenöl Extravergine, Soßen, Gemüse und viele andere Köstlichkeiten auf den Tisch zaubern, die so nur am nördlichen Gardasee und im Trient zu finden sind.</span>
  </paragraph>
  <paragraph>
    <span style="bold">Info&Programm</span><span> hier: </span><link address="http://www.gardatrentino.it/prenota">www.gardatrentino.it/CarneSalada</link>
  </paragraph>
</text>
"""
    ),

    (  # 21
        '<div>Fofo <p>Abbaia <strong>    Forte   </strong></div>',
        """\
<text>
  <paragraph>
    <span>Fofo</span>
  </paragraph>
  <paragraph>
    <span>Abbaia </span><span style="bold"> Forte</span>
  </paragraph>
</text>
"""
    ),

    (  # 22
        """\
<h3>Schie</h3>\r\n<p>Sie sind ... </p>
<p>Diese kleinen (<em>polenta "moea&rdquo;)</em> serviert.&nbsp;</p>
<p><br></p>
<p><img alt="" src="/public/image/schie%202.jpg"></p>
""",
        """\
<text>
  <heading level="3">
    <span>Schie</span>
  </heading>
  <paragraph>
    <span>Sie sind ...</span>
  </paragraph>
  <paragraph>
    <span>Diese kleinen (</span><span style="italic">polenta "moea”)</span><span> serviert.</span>
  </paragraph>
</text>
"""
    ),

    (  # 23
        """\
<p><span><em>BUFFET DI FERRAGOSTO - ORE 20.00<br />
</em></span></p>
<p><span><em>Per
questa grande Cena di Ferragosto abbiamo pensato ad un elegante
incontro tra &ldquo;cicchetti&rdquo; e stuzzichini vari con alcuni piatti
della tradizione culinaria italiana, accompagnando il tutto con
dell'ottima birra &ldquo;a caduta&rdquo; e da una selezione di vini bianchi e
rossi da noi selezionati.</em></span></p>
<p><span><em>Fatevi
guidare dal nostro percorso a buffet, e lasciatevi trasportare alla
scoperta delle proposte</em></span><span><em> del
nostro chef Mauro e del suo staff.</em></span>
</p>
<p><span><em>Vi
auguriamo una buona serata!</em></span></p>
<style type="text/css">
    P { margin-bottom: 0.21cm; }
</style>
""",
        """\
<text>
  <paragraph>
    <span style="italic">BUFFET DI FERRAGOSTO - ORE 20.00</span>
  </paragraph>
  <paragraph>
    <span style="italic">Per questa grande Cena di Ferragosto abbiamo pensato ad un elegante incontro tra “cicchetti” e stuzzichini vari con alcuni piatti della tradizione culinaria italiana, accompagnando il tutto con dell'ottima birra “a caduta” e da una selezione di vini bianchi e rossi da noi selezionati.</span>
  </paragraph>
  <paragraph>
    <span style="italic">Fatevi guidare dal nostro percorso a buffet, e lasciatevi trasportare alla scoperta delle proposte del nostro chef Mauro e del suo staff.</span>
  </paragraph>
  <paragraph>
    <span style="italic">Vi auguriamo una buona serata!</span>
  </paragraph>
</text>
"""
    ),

    (  # 24
        """\
<h3>Italian music that made everyone dream</h3>
<p>Jesolo Sound, the travelling event that brings&nbsp;the good Italian music&nbsp;in the most beautiful piazzas of the coast returns also in 2018. Jesolband Orkestra is the big band of Jesolo, that will perform in its formation with 4 saxes, 3 trumpets, 3 trombones, two voices, guitar, bass guitar, drums, and piano. The ensemble is directed by M&deg; Ettore Martin.The repertoire has been completely renewed and proposes&nbsp;the most famous pieces of great Italian artists, such as Carosone, Modugno and others, in a swing arrangement&nbsp;and performed with drive and enthusiasm by this orchestra that always has very great audience success. The concerts start at 21.15.&nbsp; Free entrance.</p>
<h5>Calendar:&nbsp;&nbsp;<br />
Thursday 2 August - piazza I&deg; Maggio<br />
Thursday 23&nbsp; August - piazza Milano<br />
Thursday 30 August - piazzetta Carducci&nbsp;</h5>
<div id="radePasteHelper">
<div>
<div><section id="block-views-events-block-1">
<div>
<div>
<div>
<div>
<div>
<div>
</div>
</div>
</div>
</div>
</div>
</div>
</section></div>
</div>
</div>
""",
        """\
<text>
  <heading level="3">
    <span>Italian music that made everyone dream</span>
  </heading>
  <paragraph>
    <span>Jesolo Sound, the travelling event that brings the good Italian music in the most beautiful piazzas of the coast returns also in 2018. Jesolband Orkestra is the big band of Jesolo, that will perform in its formation with 4 saxes, 3 trumpets, 3 trombones, two voices, guitar, bass guitar, drums, and piano. The ensemble is directed by M° Ettore Martin.The repertoire has been completely renewed and proposes the most famous pieces of great Italian artists, such as Carosone, Modugno and others, in a swing arrangement and performed with drive and enthusiasm by this orchestra that always has very great audience success. The concerts start at 21.15. Free entrance.</span>
  </paragraph>
  <heading level="5">
    <span>Calendar:</span>
  </heading>
  <heading level="5">
    <span>Thursday 2 August - piazza I° Maggio</span>
  </heading>
  <heading level="5">
    <span>Thursday 23 August - piazza Milano</span>
  </heading>
  <heading level="5">
    <span>Thursday 30 August - piazzetta Carducci</span>
  </heading>
</text>
"""
    ),

    (  # 25
        """\
<h3><a></a>Der</h3>
""",
        """\
<text>
  <heading level="3">
    <span>Der</span>
  </heading>
</text>
"""
    ),

    (  # 26
        """\
<h3>Panorama Tour Dolomiti di Brenta</h3>\r\n<p><strong>Dal 6.07 al 1.09, 2019<br>\r\nPercorso ad anello</strong> unico, che alterna ...:</p>\r\n<ul>\r\n    <li>Madonna di Campiglio- navetta Vallesinella;</li>\r\n    <li>Vallesinella-Plaza a piedi;</li>\r\n    <li>Risalita con telacabina Plaza-Colarin/Colarin; Patascoss;</li>\r\n    <li>Patascoss-Ritort (a piedi e con trenino gratuito);</li>\r\n    <li>Colarin-Madonna di Campiglio con bus navetta oppure Patascoss-Piazza Brenta Alta cn bus navetta.</li>\r\n    <li>\r\n    <strong><br>\r\n    </strong></li>\r\n</ul>\r\n<p>Specifico depliant presso Apt.</p>'""",
        """\
<text>
  <heading level="3">
    <span>Panorama Tour Dolomiti di Brenta</span>
  </heading>
  <paragraph>
    <span style="bold">Dal 6.07 al 1.09, 2019</span>
  </paragraph>
  <paragraph>
    <span style="bold">Percorso ad anello</span><span> unico, che alterna ...:</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>Madonna di Campiglio- navetta Vallesinella;</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>Vallesinella-Plaza a piedi;</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>Risalita con telacabina Plaza-Colarin/Colarin; Patascoss;</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>Patascoss-Ritort (a piedi e con trenino gratuito);</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>Colarin-Madonna di Campiglio con bus navetta oppure Patascoss-Piazza Brenta Alta cn bus navetta.</span>
      </paragraph>
    </item>
  </list>
  <paragraph>
    <span>Specifico depliant presso Apt.</span>
  </paragraph>
  <paragraph>
    <span>'</span>
  </paragraph>
</text>
"""
    ),

    (  # 27
        '<p>Abra</p><script type="text/javascript">$("body").text("<p>Foo</p>");</script>',
        """\
<text>
  <paragraph>
    <span>Abra</span>
  </paragraph>
</text>
"""
    ),

    (  # 28
        '<p>Abra</p><iframe src="/foo/bar">Fallback</iframe>',
        """\
<text>
  <paragraph>
    <span>Abra</span>
  </paragraph>
</text>
"""
    ),

    (  # 29
        '<p>Abra</p><table><table><thead><tr><th colspan="2">The table header</th></tr></thead><tbody><tr><td>The table body</td><td>with two columns</td></tr><tr><td>And</td><td>a second row</td></tr></tbody></table>',
        """\
<text>
  <paragraph>
    <span>Abra</span>
  </paragraph>
  <paragraph>
    <span>The table header</span>
  </paragraph>
  <paragraph>
    <span>The table body with two columns</span>
  </paragraph>
  <paragraph>
    <span>And a second row</span>
  </paragraph>
</text>
"""
    ),

    (  # 30
        '<strong>Calendario 2022<br /> </strong>(date e programmi sono soggetti ad eventuali cambiamenti) <ul>     <li>08 maggio Vaie, Sagra del Canestrello di Vaie </li>     <li>02 giugno Borgone Susa, Sagra dell’Olio Valsusino </li></ul>',
        """\
<text>
  <paragraph>
    <span style="bold">Calendario 2022</span>
  </paragraph>
  <paragraph>
    <span>(date e programmi sono soggetti ad eventuali cambiamenti)</span>
  </paragraph>
  <list style="dotted">
    <item>
      <paragraph>
        <span>08 maggio Vaie, Sagra del Canestrello di Vaie</span>
      </paragraph>
    </item>
    <item>
      <paragraph>
        <span>02 giugno Borgone Susa, Sagra dell’Olio Valsusino</span>
      </paragraph>
    </item>
  </list>
</text>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(SEM_HTMLS)))
def test_good_html(index):
    html, ast = SEM_HTMLS[index]
    parsed = parse_html(html)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast, html


BAD_HTMLS = (
    (  # 0
        """\
<strong>Weihnachtsmarkt Arco</strong><br>
17.-19. / 24.-26. November, 1.-3. / 7.-10. / 15.-17./ 21.-24. / 26.-31. Dezember &amp; 1.-2. / 4.-7. January 2018<br>
<br>
<br>
<strong>So schmeckt Weihnachten - Riva del Garda</strong><br>
2-3 / 7-10 / 13-17 / 21-24 / 26-31 Dezember &amp; 1-7 January 2018&nbsp;<br>
<strong><br>
</strong>
<div><strong><br>
</strong></div>
<div><strong>Mehr hier: www.gardatrentino.it/Inverno</strong>
<p><strong><a href="http://www.gardatrentino.it/Inverno"></a></strong></p>
</div>
""",
        """\
<text>
  <paragraph>
    <span style="bold">Weihnachtsmarkt Arco</span>
  </paragraph>
  <paragraph>
    <span>17.-19. / 24.-26. November, 1.-3. / 7.-10. / 15.-17./ 21.-24. / 26.-31. Dezember & 1.-2. / 4.-7. January 2018</span>
  </paragraph>
  <paragraph>
    <span style="bold">So schmeckt Weihnachten - Riva del Garda</span>
  </paragraph>
  <paragraph>
    <span>2-3 / 7-10 / 13-17 / 21-24 / 26-31 Dezember & 1-7 January 2018</span>
  </paragraph>
  <paragraph>
    <span style="bold">Mehr hier: www.gardatrentino.it/Inverno</span>
  </paragraph>
</text>
"""
    ),

    (  # 2
        """<h2>Una Gran Fondo d\'&eacute;lite per una location d\'&eacute;lite</h2>
<h3>Programma&nbsp;</h3>\n<p><b>Venerd&igrave; 6 settembre 2019<a href="https://foo/bar"></a>
</b><br /><a href="https://foo/bar"><b>Due ruote e un casco</b></a><br />""",
        """\
<text>
  <heading level="2">
    <span>Una Gran Fondo d'élite per una location d'élite</span>
  </heading>
  <heading level="3">
    <span>Programma</span>
  </heading>
  <paragraph>
    <span style="bold">Venerdì 6 settembre 2019</span>
  </paragraph>
  <paragraph>
    <link address="https://foo/bar">Due ruote e un casco</link>
  </paragraph>
</text>
"""
    ),

    (  # 3
        """\
<pre>
  foo
    bar
</pre>
""",
        """\
<text>
  <paragraph>
    <span>foo bar</span>
  </paragraph>
</text>
"""
    ),
)


@pytest.mark.parametrize('index', range(len(BAD_HTMLS)))
def test_bad_html(index):
    html, ast = BAD_HTMLS[index]
    parsed = parse_html(html)
    printed = StringIO()
    ASTPrinter(where=printed).visit(parsed)
    assert printed.getvalue() == ast, html
