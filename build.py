"""Zostaví index.html + style.css s cache bustingom (?v=hash).
Obsah je zo stránok hurbanmurarstvo.sk (podklady/*.html): o nás, služby, galéria, referencie, certifikáty, kontakt.
Fotky pripravuje spracuj_foto.py (foto.json), polohy obcí a rieky sú z OpenStreetMap (podklady/geo/)."""
import hashlib, json, math
from html import escape as esc
from pathlib import Path
D = Path(__file__).parent
F = json.load(open(D / 'foto.json'))
G = D / 'podklady' / 'geo'


def im(n, alt='', cls='', lazy=True):
    f = F[n]
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="img/{n}.jpg" alt="{esc(alt)}" width="{f["w"]}" height="{f["h"]}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


LOGO = f'<img class="logo" src="img/logo.png" alt="" width="{F["logo"]["w"]}" height="{F["logo"]["h"]}">'

# ---------- služby (stránka Služby + referencie) ----------
SLUZBY = [
    ('Prípravné a zemné práce', 'Príprava pre stavbu, zemné a výkopové práce a s nimi spojená pokládka zámkovej dlažby.', 'zakladanie'),
    ('Novostavby domov a firemných budov', 'Rodinné domy, chaty aj firemné stavby: servisná hala v Kostolišti či autosalón so servisnými garážami v Malackách.', 'cierna-voda'),
    ('Rekonštrukcie budov a rodinných domov', 'Rekonštrukcie domov aj s vonkajšími úpravami, napríklad v Lábe na 250 m² a v Stupave na 230 m².', 'rohoznik-3'),
    ('Strojové omietky', 'Vnútorné aj vonkajšie, vlastnou technikou. V bytovej výstavbe v Bratislave sme ich naniesli na 6 000 m².', 'malacky-dom'),
    ('Zateplenie a fasády', 'Zateplenie stavby a konečná úprava fasády ucelenými systémami STOMIX, BAUMIT, TERANOVA a RELIUS.', 'rohoznik-1'),
    ('Maliarske a natieračské práce', 'Maľovanie a nátery na záver, aby bola stavba hotová do posledného detailu.', 'jakubov'),
    ('Vlastná autodoprava', 'Materiál aj techniku vozíme na stavbu vlastnými autami.', 'blatne'),
]
sluzby = '\n' + '\n'.join(
    f'      <li class="svc rv" data-img="img/{n}.jpg"><span class="svc__n">{i:02d}</span>'
    f'<h3 class="svc__t">{t}</h3><p class="svc__p">{p}</p>{im(n, t, "svc__m")}<span class="svc__a" aria-hidden="true">↗</span></li>'
    for i, (t, p, n) in enumerate(SLUZBY, 1)) + '\n    '

MARQ = ['Výkopové práce', 'Zámková dlažba', 'Novostavby', 'Rekonštrukcie', 'Strojové omietky', 'Zateplenie', 'Fasády', 'Maľovanie', 'Vlastná autodoprava']
tehla = '<svg class="mq__b" viewBox="0 0 24 12" aria-hidden="true"><rect x="0.5" y="0.5" width="23" height="11" rx="1"/></svg>'
marquee = ''.join(f'<span>{m}</span>{tehla}' for m in MARQ)
marquee = f'<div class="mq__row">{marquee}</div><div class="mq__row" aria-hidden="true">{marquee}</div>'

# ---------- hero: fotky ako výtlačky ----------
HERO = [('rohoznik-2', 'Rohožník'), ('malacky-peugeot', 'Malacky, autosalón'), ('blatne', 'Blatné'), ('chata', 'stavba chaty')]
prints = ''.join(f'<figure class="print print--{i}" style="--i:{i}">{im(n, F[n]["popis"] + (" – " + F[n]["obec"] if F[n]["obec"] else ""), lazy=False)}'
                 f'<figcaption>{c}</figcaption></figure>' for i, (n, c) in enumerate(HERO))

# ---------- zateplenie v reze ----------
KROKY = [
    ('Podklad', 'Murivo skontrolujeme a pripravíme: musí byť rovné, pevné, suché a čisté. Od podkladu sa odvíja všetko ďalšie.'),
    ('Lepiaca malta', 'Izolačné dosky lepíme po obvode a v bodoch, aby k múru celou plochou dobre držali.'),
    ('Tepelný izolant', 'Fasádny polystyrén alebo minerálna vlna, podľa stavby a projektu. Dosky kladieme na väzbu, bez škár.'),
    ('Kotvenie', 'Tanierové hmoždinky podľa kotviaceho plánu systému podržia izolant aj vo vetre.'),
    ('Výstužná vrstva', 'Stierka so sklotextilnou mriežkou. Vďaka nej fasáda nepraská.'),
    ('Penetrácia', 'Zjednotí savosť podkladu, aby omietka všade vyschla rovnomerne.'),
    ('Fasádna omietka', 'Konečná úprava vo farbe a štruktúre podľa Vás. Celé zateplenie robíme jedným systémom od jedného výrobcu.'),
]
kroky = '\n' + '\n'.join(
    f'        <li class="step" data-k="{i}"><b>{i + 1:02d}</b><h3>{t}</h3><p>{p}</p></li>'
    for i, (t, p) in enumerate(KROKY)) + '\n      '

# rez stenou: vrstvy zľava doprava, výška 80–420
Y0, Y1 = 70, 430
tehly = ''
for r, y in enumerate(range(Y0, Y1, 30)):
    off = 0 if r % 2 == 0 else -45
    for x in range(40 + off, 230, 90):
        x0, x1 = max(x, 40), min(x + 86, 226)
        if x1 > x0:
            tehly += f'<rect x="{x0}" y="{y + 2}" width="{x1 - x0}" height="{min(26, Y1 - y - 2)}" rx="1.5"/>'
body = ''.join(f'<ellipse cx="{233}" cy="{y}" rx="6" ry="{11 if i % 3 else 18}"/>' for i, y in enumerate(range(Y0 + 22, Y1 - 10, 34)))
eps = ''.join(f'<circle cx="{x}" cy="{y}" r="{1.4 + (x * 7 + y * 3) % 5 * 0.25:.2f}"/>'
              for x in range(254, 376, 13) for y in range(Y0 + 8 + (x // 13 % 2) * 6, Y1 - 4, 13))
hmozd = ''.join(f'<g class="dw"><rect x="168" y="{y - 2.5}" width="214" height="5" rx="2"/><rect x="376" y="{y - 22}" width="6" height="44" rx="2"/></g>'
                for y in (130, 250, 370))
sietka = ''.join(f'<line x1="{386 + (i % 2) * 6}" y1="{Y0}" x2="{386 + (i % 2) * 6}" y2="{Y1}"/>' for i in range(2)) + \
    ''.join(f'<line x1="383" y1="{y}" x2="395" y2="{y}"/>' for y in range(Y0 + 6, Y1, 9))
zrnka = ''.join(f'<circle cx="{404 + (i * 37) % 13}" cy="{Y0 + (i * 53) % (Y1 - Y0)}" r="{0.8 + (i % 3) * 0.4}"/>' for i in range(90))


def lbl(k, y_layer, x_layer, y_txt, t1, t2=''):
    # popis vpravo s vodiacou čiarou
    t2s = f'<text class="lbl lbl--s" x="486" y="{y_txt + 16}">{t2}</text>' if t2 else ''
    return (f'<g class="lb" data-k="{k}"><polyline class="ln" points="{x_layer},{y_layer} {470},{y_txt - 4} 480,{y_txt - 4}"/>'
            f'<circle class="ln-d" cx="{x_layer}" cy="{y_layer}" r="3"/><text class="lbl" x="486" y="{y_txt}">{t1}</text>{t2s}</g>')


REZ = f'''<svg class="rez" viewBox="0 0 700 500" role="img" aria-label="Rez zateplenou stenou: murivo, lepiaca malta, izolant, kotvenie, výstužná vrstva, penetrácia a fasádna omietka">
<defs><clipPath id="rc"><rect x="40" y="{Y0}" width="380" height="{Y1 - Y0}"/></clipPath></defs>
<g class="ly" data-k="0"><rect class="mortar" x="40" y="{Y0}" width="188" height="{Y1 - Y0}"/><g class="brick">{tehly}</g></g>
<g class="ly" data-k="1"><g class="glue">{body}</g></g>
<g class="ly" data-k="2"><rect class="eps" x="240" y="{Y0}" width="140" height="{Y1 - Y0}"/><g class="eps-d">{eps}</g>{''.join(f'<line class="eps-j" x1="240" y1="{y}" x2="380" y2="{y}"/>' for y in (190, 330))}</g>
<g class="ly" data-k="3">{hmozd}</g>
<g class="ly" data-k="4"><rect class="mesh-b" x="380" y="{Y0}" width="18" height="{Y1 - Y0}"/><g class="mesh">{sietka}</g></g>
<g class="ly" data-k="5"><rect class="prime" x="398" y="{Y0}" width="5" height="{Y1 - Y0}"/></g>
<g class="ly" data-k="6"><rect class="plaster" x="403" y="{Y0}" width="17" height="{Y1 - Y0}"/><g class="grain-d">{zrnka}</g></g>
<g class="lbs">
{lbl(0, 110, 132, 96, 'Murivo', 'podklad')}
{lbl(1, 160, 233, 150, 'Lepiaca malta', 'obvod + body')}
{lbl(2, 220, 310, 204, 'Tepelný izolant', 'EPS / minerálna vlna')}
{lbl(3, 250, 379, 258, 'Kotvenie', 'tanierové hmoždinky')}
{lbl(4, 300, 389, 312, 'Výstužná vrstva', 'stierka + mriežka')}
{lbl(5, 350, 400, 366, 'Penetrácia')}
{lbl(6, 400, 412, 412, 'Fasádna omietka', 'farba podľa Vás')}
</g>
<g class="cap"><text x="40" y="{Y0 - 22}">INTERIÉR</text><text x="420" y="{Y0 - 22}" text-anchor="end">EXTERIÉR</text></g>
</svg>'''

CERT = [('BAUMIT', 'zaškolenie zatepľovacím systémom'), ('INEX', 'zaškolenie zatepľovacím systémom'),
        ('STOMIX', 'zaškolenie zatepľovacím systémom'), ('TSUS', 'certifikát pre technológie STOMIX')]
certy = ''.join(f'<li class="rv"><b>{a}</b><span>{b}</span></li>' for a, b in CERT)

# ---------- referencie ----------
# (obec, popis zo stránky Referencie / Galéria, rozsah, fotky)
REF = [
    ('Láb', 'Rekonštrukcia rodinného domu a vonkajšia úprava', '250 m²', []),
    ('Stupava', 'Rekonštrukcia rodinného domu a vonkajšia úprava', '230 m²', []),
    ('Bernolákovo', 'Novostavba rodinného domu', '', []),
    ('Bratislava', 'Strojové omietky v bytovej výstavbe', '6 000 m²', []),
    ('Kostolište', 'Výstavba servisnej haly', '', []),
    ('Malacky', 'Novostavba autosalónu a servisných garáží', '', ['malacky-peugeot']),
    ('Pernek', 'Novostavba rodinného domu', '', []),
    ('Rohožník', 'Novostavba chaty pri priehrade', '', []),
    ('Rohožník', 'Rodinné domy', '3 domy', ['rohoznik-1', 'rohoznik-2', 'rohoznik-3']),
    ('Malacky', 'Rodinný dom', '', ['malacky-dom']),
    ('Jakubov', 'Rodinný dom', '', ['jakubov']),
    ('Čierna Voda', 'Rodinný dom', '', ['cierna-voda']),
    ('Blatné', 'Rodinný dom', '', ['blatne']),
]
OBCE = {k: tuple(v) for k, v in json.load(open(G / 'obce.json')).items()}
refs = ''
for i, (o, t, r, fs) in enumerate(REF):
    th = ''.join(f'<img src="img/{n}.jpg" alt="" width="{F[n]["w"]}" height="{F[n]["h"]}" loading="lazy">' for n in fs[:3])
    data = f' data-fotos="{",".join(fs)}" role="button" tabindex="0" aria-label="{esc(t)}, {o} – fotky"' if fs else ''
    refs += (f'\n          <li class="ref{" ref--f" if fs else ""}" data-obec="{o}"{data}><span class="ref__o">{o}</span>'
             f'<span class="ref__t">{t}</span><span class="ref__r">{r}</span>'
             f'{f"<span class=ref__th>{th}</span>" if th else ""}</li>')
refs += '\n        '
pocty = {}
for o, *_ in REF:
    pocty[o] = pocty.get(o, 0) + 1

# mapa: Záhorie, Bratislava a Senec
LON0, LAT0, LON1, LAT1 = 16.84, 48.50, 17.52, 48.115
KX = math.cos(math.radians(48.3)) * 111.32
KY = 110.57
S = 13  # px na km
proj = lambda lat, lon: ((lon - LON0) * KX * S, (LAT0 - lat) * KY * S)
MW, MH = (LON1 - LON0) * KX * S, (LAT0 - LAT1) * KY * S


def poly(pts, cls, step=2):
    p = [proj(a['lat'], a['lon']) for a in pts]
    p = p[::step] + [p[-1]]
    return f'<polyline class="{cls}" points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in p) + '"/>'


rv = ''
for e in json.load(open(G / 'rivers.json'))['elements']:
    n = e['tags'].get('name') or ''
    if 'Morava' in n or 'Dunaj' in n or 'Donau' in n:
        rv += poly(e['geometry'], 'riv riv--b' if n != 'Malý Dunaj' else 'riv')
    elif n in ('Rudava', 'Malina', 'Čierna voda'):
        rv += poly(e['geometry'], 'riv riv--s')
dl = ''
for e in json.load(open(G / 'lines.json'))['elements']:
    if e['tags'].get('highway') == 'motorway':
        dl += poly(e['geometry'], 'hw', 3)
px, py = proj(*OBCE['Pernek'])
rings = ''.join(f'<circle class="ring" cx="{px:.1f}" cy="{py:.1f}" r="{r * S}"/>'
                f'<text class="ringl" x="{px + r * S * 0.71 + 4:.1f}" y="{py - r * S * 0.71 - 4:.1f}">{r} km</text>' for r in (10, 20, 30))
LBL = {  # posun popisu (dx, dy, kotva)
    'Pernek': (16, 5, 'start'), 'Láb': (0, -17, 'middle'), 'Stupava': (-15, 5, 'end'), 'Bernolákovo': (0, 26, 'middle'),
    'Bratislava': (-16, 5, 'end'), 'Kostolište': (0, -17, 'middle'), 'Malacky': (15, 5, 'start'), 'Rohožník': (15, 5, 'start'),
    'Jakubov': (-15, 5, 'end'), 'Čierna Voda': (-15, 5, 'end'), 'Blatné': (0, -17, 'middle'),
}
pins = ''
for o, (lat, lon) in OBCE.items():
    x, y = proj(lat, lon)
    dx, dy, an = LBL[o]
    home = ' pin--home' if o == 'Pernek' else ''
    pins += (f'<g class="pin{home}" data-obec="{o}" tabindex="0" role="button" aria-label="{o}: {pocty[o]} {"referencia" if pocty[o] == 1 else "referencie"}">'
             f'<circle class="pin__h" cx="{x:.1f}" cy="{y:.1f}" r="15"/><circle class="pin__c" cx="{x:.1f}" cy="{y:.1f}" r="9.5"/>'
             f'<text class="pin__n" x="{x:.1f}" y="{y + 3.5:.1f}" text-anchor="middle">{pocty[o]}</text>'
             f'<text class="pin__l" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{an}">{o}</text></g>')
ax, ay = proj(48.235, 16.905)
kx, ky = proj(48.335, 17.235)
dx_, dy_ = proj(48.124, 17.065)
mx_, my_ = proj(48.215, 16.972)
popisy = (f'<text class="area" transform="translate({ax:.0f},{ay:.0f}) rotate(-90)" text-anchor="middle">RAKÚSKO</text>'
          f'<text class="mtn" transform="translate({kx:.0f},{ky:.0f}) rotate(-52)">Malé Karpaty</text>'
          f'<text class="rivl" transform="translate({mx_:.0f},{my_:.0f}) rotate(-78)">Morava</text>'
          f'<text class="rivl" x="{dx_:.0f}" y="{dy_:.0f}">Dunaj</text>')
sb = (f'<g class="scale"><line x1="24" y1="{MH - 24:.0f}" x2="{24 + 10 * S}" y2="{MH - 24:.0f}"/>'
      f'<line x1="24" y1="{MH - 29:.0f}" x2="24" y2="{MH - 19:.0f}"/><line x1="{24 + 10 * S}" y1="{MH - 29:.0f}" x2="{24 + 10 * S}" y2="{MH - 19:.0f}"/>'
      f'<text x="24" y="{MH - 34:.0f}">10 km</text></g>')
north = f'<g class="north" transform="translate({MW - 30:.0f},36)"><path d="M0-16 6 6 0 1-6 6z"/><text y="21" text-anchor="middle">S</text></g>'
mapa = (f'<svg class="mapsvg" viewBox="0 0 {MW:.0f} {MH:.0f}" role="img" aria-label="Mapa referencií: Pernek, Záhorie, Bratislava a okolie">'
        f'<defs><clipPath id="mc"><rect width="{MW:.0f}" height="{MH:.0f}"/></clipPath>'
        f'<pattern id="mgrid" width="{S * 5}" height="{S * 5}" patternUnits="userSpaceOnUse"><path d="M{S * 5} 0H0V{S * 5}" class="mg"/></pattern></defs>'
        f'<g clip-path="url(#mc)"><rect width="{MW:.0f}" height="{MH:.0f}" fill="url(#mgrid)"/>{rv}{dl}{popisy}{rings}</g>{pins}{sb}{north}</svg>')

# ---------- album ----------
ALBUM = ['rohoznik-1', 'malacky-dom', 'malacky-peugeot', 'jakubov', 'cierna-voda', 'blatne', 'rohoznik-2', 'rohoznik-3', 'chata', 'zakladanie']
album = '\n' + '\n'.join(
    f'      <figure class="ph rv" style="--r:{[-2.2, 1.6, -1, 2.4, -1.8, 1.1, -2.6, 1.9, -1.3, 2.1][i]}deg" data-fotos="{n}" role="button" tabindex="0" '
    f'aria-label="{esc(F[n]["popis"])}{(" – " + F[n]["obec"]) if F[n]["obec"] else ""}, zväčšiť">{im(n, F[n]["popis"] + ((" – " + F[n]["obec"]) if F[n]["obec"] else ""))}'
    f'<figcaption>{F[n]["popis"]}{("<span>" + F[n]["obec"] + "</span>") if F[n]["obec"] else ""}</figcaption></figure>'
    for i, n in enumerate(ALBUM)) + '\n    '

# ---------- formulár ----------
TYPY = ['Výkopové práce', 'Novostavba', 'Rekonštrukcia', 'Strojové omietky', 'Zateplenie a fasáda', 'Maľovanie', 'Zámková dlažba']
typy = ''.join(f'<label class="chip"><input type="checkbox" name="typ" value="{t}"><span>{t}</span></label>' for t in TYPY)

popisy_foto = {n: (F[n]['popis'] + (' – ' + F[n]['obec'] if F[n]['obec'] else '')) for n in F if n != 'logo'}

css = (D / 'fonts/fonts.css').read_text() + '\n' + (D / 'style.src.css').read_text()
(D / 'style.css').write_text(css)
hs = lambda b: hashlib.md5(b).hexdigest()[:8]
html = (D / 'src.html').read_text()
for k, v in dict(logo=LOGO, prints=prints, marquee=marquee, sluzby=sluzby, kroky=kroky, rez=REZ, certy=certy, refs=refs,
                 mapa=mapa, album=album, typy=typy, n_obci=str(len(OBCE)), foto_json=json.dumps(popisy_foto, ensure_ascii=False)).items():
    html = html.replace('{{' + k + '}}', v)
html = html.replace('{{css}}', hs(css.encode())).replace('{{js}}', hs((D / 'main.js').read_bytes()))
assert '{{' not in html, html[html.index('{{'):html.index('{{') + 40]
(D / 'index.html').write_text(html)
(D / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
print('ok', len(REF), 'referencií,', len(OBCE), 'obcí, mapa', round(MW), '×', round(MH))
