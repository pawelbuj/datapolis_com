# -*- coding: utf-8 -*-
"""Hero platform-2to2: w srodku aplikacja procesowa, pierscien to proces,
   kropka na pierscieniu pokazuje, gdzie proces jest teraz, i zapala mijane
   wezly.

   Sklada CALY diagram od zera (poza <defs>, ktore zostaja z oryginalu).
   Skladanie od zera zamiast latania po kawalku - pierwsza wersja tego skryptu
   trafiala regexem w zagniezdzone <g> ikon i dublowala etykiety wezlow.

   Uruchamiac z katalogu repo: python3 tools/i18n/p2_diagram.py
"""
import io, re

L = {
    'platform-2to2.html':    dict(c1='PROCESS',    c2='APP',         ring='PROCESS',
                                  human='HUMAN',    dw='DIGITAL WORKER', data='DATA',  sys='SYSTEMS'),
    'pl/platform-2to2.html': dict(c1='APLIKACJA',  c2='PROCESOWA',   ring='PROCES',
                                  human='CZŁOWIEK', dw='DIGITAL WORKER', data='DANE',  sys='SYSTEMY'),
    'de/platform-2to2.html': dict(c1='PROZESS-',   c2='ANWENDUNG',   ring='PROZESS',
                                  human='MENSCH',   dw='DIGITAL WORKER', data='DATEN', sys='SYSTEME'),
    'es/platform-2to2.html': dict(c1='APLICACIÓN', c2='DE PROCESO',  ring='PROCESO',
                                  human='HUMANO',   dw='DIGITAL WORKER', data='DATOS', sys='SISTEMAS'),
}

R = 128                       # promien orbity - przechodzi przez srodki czterech wezlow
I = '\n                        '
I2 = I + '    '
I3 = I + '        '

ICONS = {
    'human':   I3 + '<circle cx="100" cy="110" r="10"></circle>'
             + I3 + '<path d="M85 135 Q100 125 115 135"></path>',
    'worker':  I3 + '<g transform="translate(282 102) scale(1.5)">'
             + I3 + '    <rect x="4.5" y="6" width="15" height="13" rx="3"></rect>'
             + I3 + '    <circle cx="9.2" cy="12" r="1"></circle><circle cx="14.8" cy="12" r="1"></circle>'
             + I3 + '    <path d="M9 16h6M12 3v3M9.5 3h5"></path>'
             + I3 + '</g>',
    'data':    I3 + '<rect x="82" y="264" width="36" height="30" rx="4"></rect>'
             + I3 + '<path d="M82 274 H118 M82 284 H118 M94 264 V294"></path>',
    'systems': I3 + '<rect x="280" y="263" width="16" height="13" rx="2.5"></rect>'
             + I3 + '<rect x="304" y="263" width="16" height="13" rx="2.5"></rect>'
             + I3 + '<rect x="292" y="288" width="16" height="13" rx="2.5"></rect>'
             + I3 + '<path d="M296 269.5 H304 M288 276 V282 H300 V288 M312 276 V282 H300"></path>',
}

NODES = [('human', 100, 120, 'human'), ('worker', 300, 120, 'dw'),
         ('data', 100, 280, 'data'), ('systems', 300, 280, 'sys')]


def node(cls, cx, cy, label):
    return (I + '<g class="p2t2-node p2t2-node--%s">' % cls
            + I2 + '<circle class="p2t2-node__bg" cx="%d" cy="%d" r="40" stroke="#334155" stroke-width="2"/>' % (cx, cy)
            + I2 + '<g class="p2t2-node__icon" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
            + ICONS[cls]
            + I2 + '</g>'
            + I2 + '<text class="p2t2-node__label" x="%d" y="%d" text-anchor="middle" font-size="9" '
                   'font-weight="600" font-family="system-ui, sans-serif" letter-spacing="0.03em">%s</text>' % (cx, cy + 55, label)
            + I + '</g>')


def body(d, caption):
    top = 200 - R
    w = max(46, 13 + 7 * len(d['ring']))
    out = []
    out.append(I + '<!-- Tlo -->')
    for cx, cy, op in ((50, 80, .3), (350, 90, .25), (40, 320, .2), (360, 310, .25), (200, 45, .2)):
        out.append(I + '<circle cx="%d" cy="%d" r="2" fill="#14b8a6" opacity="%s"/>' % (cx, cy, op))
    out.append(I + '<circle cx="200" cy="200" r="160" stroke="#334155" stroke-width="1" fill="none" opacity="0.3"/>')

    # Pierscien procesu jest kreskowany i kreci sie razem z kropka - to on
    # pokazuje, ze proces idzie. Dlugosc kreski dobrana tak, zeby 56 segmentow
    # zmiescilo sie w obwodzie bez widocznego szwu.
    out.append(I + '<!-- Pierscien procesu: kreskowany, obraca sie razem z kropka -->')
    out.append(I + '<g class="p2t2-orbit">')
    out.append(I2 + '<circle cx="200" cy="200" r="%d" fill="none" stroke="#14b8a6" stroke-width="1.5" '
                    'stroke-opacity="0.5" stroke-dasharray="7.18 7.18"/>' % R)
    out.append(I + '</g>')
    out.append(I + '<rect x="%.0f" y="%d" width="%d" height="18" rx="9" fill="#020617" stroke="#14b8a6" stroke-opacity="0.4"/>'
               % (200 - w / 2.0, top - 9, w))
    out.append(I + '<text x="200" y="%.1f" text-anchor="middle" fill="#5eead4" font-size="8.5" font-weight="700" '
                   'font-family="system-ui, sans-serif" letter-spacing="0.12em">%s</text>' % (top + 3.5, d['ring']))

    out.append(I + '<!-- Aplikacja procesowa -->')
    out.append(I + '<g filter="url(#glowP2t2)">')
    out.append(I2 + '<circle cx="200" cy="200" r="60" fill="url(#processGradP2t2)"/>')
    for k, y in (('c1', 196), ('c2', 212)):
        out.append(I2 + '<text x="200" y="%d" text-anchor="middle" fill="#020617" font-size="11" font-weight="700" '
                        'font-family="system-ui, sans-serif" letter-spacing="0.05em">%s</text>' % (y, d[k]))
    out.append(I + '</g>')

    out.append(I + '<!-- Wezly -->')
    for cls, cx, cy, key in NODES:
        out.append(node(cls, cx, cy, d[key]))

    out.append(I + '<!-- Szprychy: aplikacja siega po kazdy z nich -->')
    for x1, y1, x2, y2 in ((140, 140, 160, 175), (260, 140, 240, 175), (140, 260, 160, 225), (260, 260, 240, 225)):
        out.append(I + '<path d="M%d %d L%d %d" stroke="#14b8a6" stroke-width="2" stroke-opacity="0.35" stroke-dasharray="6 4"/>'
                   % (x1, y1, x2, y2))

    out.append(I + '<!-- Kropka procesu - rysowana po wezlach, zeby sie za nimi nie chowala -->')
    out.append(I + '<g class="p2t2-orbit">')
    # Kropka lzejsza niz na mapie stanow - tutaj diagram jest rzadszy i mocny
    # bialy pierscien wychodzil z rytmu strony. Zostaje halo + maly rdzen.
    out.append(I2 + '<circle cx="200" cy="%d" r="11" fill="#60a5fa" opacity="0.14"/>' % (200 + R))
    out.append(I2 + '<circle cx="200" cy="%d" r="5.5" fill="#3b82f6" fill-opacity="0.9" '
                    'stroke="#93c5fd" stroke-width="1.5"/>' % (200 + R))
    out.append(I + '</g>')

    out.append(I + '<text x="200" y="382" text-anchor="middle" fill="#64748b" font-size="9" '
                   'font-family="system-ui, sans-serif" letter-spacing="0.08em">%s</text>' % caption)
    return ''.join(out) + '\n                    '


for f, d in L.items():
    s = io.open(f, encoding='utf-8').read()
    i = s.find('<svg class="p2t2-platform-diagram"')
    j = s.find('</svg>', i)
    assert i > 0 and j > i, f
    svg = s[i:j]

    head_end = svg.index('</defs>') + len('</defs>')
    caption = re.findall(r'<text x="200" y="382"[^>]*>([^<]+)</text>', svg)
    assert caption, (f, 'brak podpisu pod diagramem')

    new = svg[:head_end] + body(d, caption[0])
    assert new.count('p2t2-node--') == 4 and new.count('p2t2-orbit') == 2, (f, 'wezly/orbity')
    assert len(re.findall(r'</text>', new)) == 8, (f, 'liczba etykiet', len(re.findall(r'</text>', new)))
    io.open(f, 'w', encoding='utf-8').write(s[:i] + new + s[j:])
    print('ok', f)
