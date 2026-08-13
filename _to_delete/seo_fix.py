#!/usr/bin/env python3
"""Datapolis.com — ujednolicenie cache CSS, fonty, canonical, hreflang, OG, sitemap, robots.
Skrypt jest idempotentny: ponowne uruchomienie nic nie zepsuje."""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://datapolis.com"
VER = "20260813"
OG_IMAGE = f"{BASE}/assets/img/og-image-1200x630.png"
LANGS = ["en", "pl", "de", "es"]
LOCALE = {"en": "en_US", "pl": "pl_PL", "de": "de_DE", "es": "es_ES"}
DIRS = {"en": ".", "pl": "pl", "de": "de", "es": "es"}

FONTS = (
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@300;400;500;600;700&amp;family=Instrument+Sans:wght@400;500;600;700&amp;display=swap">\n'
)

MARK_START = "    <!-- SEO: canonical / hreflang / open graph -->\n"
MARK_END = "    <!-- /SEO -->\n"


def url_for(lang, page):
    prefix = "" if lang == "en" else f"/{lang}"
    if page == "index":
        return f"{BASE}/" if lang == "en" else f"{BASE}{prefix}"
    return f"{BASE}{prefix}/{page}"


def pages_by_lang():
    """{page: [langs, w ktorych istnieje]}"""
    out = {}
    for lang, d in DIRS.items():
        path = os.path.join(ROOT, d)
        for fn in sorted(os.listdir(path)):
            if not fn.endswith(".html"):
                continue
            out.setdefault(fn[:-5], []).append(lang)
    return out


def seo_block(lang, page, langs):
    L = [MARK_START, f'    <link rel="canonical" href="{url_for(lang, page)}">\n']
    if len(langs) > 1:
        for other in LANGS:
            if other in langs:
                L.append(f'    <link rel="alternate" hreflang="{other}" href="{url_for(other, page)}">\n')
        if "en" in langs:
            L.append(f'    <link rel="alternate" hreflang="x-default" href="{url_for("en", page)}">\n')
    L.append(f'    <meta property="og:url" content="{url_for(lang, page)}">\n')
    L.append(f'    <meta property="og:locale" content="{LOCALE[lang]}">\n')
    L.append(f'    <meta property="og:image" content="{OG_IMAGE}">\n')
    L.append('    <meta property="og:image:width" content="1200">\n')
    L.append('    <meta property="og:image:height" content="630">\n')
    L.append('    <meta name="twitter:card" content="summary_large_image">\n')
    L.append(MARK_END)
    return "".join(L)


def bump_versions(html):
    """Jeden wspolny parametr ?v= dla wszystkich lokalnych CSS/JS."""
    def repl(m):
        return f'{m.group(1)}?v={VER}"'
    html = re.sub(r'((?:href|src)="assets/[^"?]+\.(?:css|js))(?:\?v=[^"]*)?"', repl, html)
    return html


def strip_old(html):
    """Usuwa wczesniejszy blok SEO oraz stare, zdublowane tagi."""
    html = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), "", html, flags=re.S)
    # stare pojedyncze tagi, ktore teraz generujemy sami
    for pat in (r'\s*<link rel="canonical"[^>]*>',
                r'\s*<link rel="alternate" hreflang[^>]*>',
                r'\s*<meta property="og:url"[^>]*>',
                r'\s*<meta property="og:image[^>]*>',
                r'\s*<meta property="og:locale"[^>]*>',
                r'\s*<meta name="twitter:card"[^>]*>',
                r'\s*<link rel="preconnect" href="https://fonts\.[^>]*>',
                r'\s*<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>'):
        html = re.sub(pat, "", html)
    return html


def process(lang, page, langs):
    path = os.path.join(ROOT, DIRS[lang], page + ".html")
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "<head>" not in html:
        return False
    orig = html
    html = strip_old(html)
    html = bump_versions(html)

    block = seo_block(lang, page, langs)
    needs_fonts = "dark-theme.css" in html
    inject = block + ("\n" + FONTS if needs_fonts else "")

    m = re.search(r'^[ \t]*<link rel="stylesheet"', html, flags=re.M)
    if m:
        html = html[:m.start()] + inject + "\n" + html[m.start():]
    else:  # np. sharepoint.html – brak zewnetrznych arkuszy
        html = html.replace("</head>", inject + "</head>", 1)

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def fix_font_import():
    """@import po regule :root jest ignorowany przez przegladarke – usuwamy,
    fonty ladujemy <link>-iem w <head>."""
    p = os.path.join(ROOT, "assets", "css", "dark-theme.css")
    with open(p, encoding="utf-8") as f:
        css = f.read()
    new = re.sub(r'/\*\s*Import fonts\s*\*/\s*\n?', '', css)
    new = re.sub(r'@import\s+url\([^)]*fonts\.googleapis[^)]*\);\s*\n?', '', new)
    if new != css:
        with open(p, "w", encoding="utf-8") as f:
            f.write(new)
        return True
    return False


def write_sitemap(pmap):
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in sorted(pmap):
        langs = pmap[page]
        for lang in LANGS:
            if lang not in langs:
                continue
            prio = "1.0" if page == "index" and lang == "en" else ("0.9" if page == "index" else "0.7")
            rows.append("  <url>")
            rows.append(f"    <loc>{url_for(lang, page)}</loc>")
            if len(langs) > 1:
                for other in LANGS:
                    if other in langs:
                        rows.append(f'    <xhtml:link rel="alternate" hreflang="{other}" href="{url_for(other, page)}"/>')
                if "en" in langs:
                    rows.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_for("en", page)}"/>')
            rows.append(f"    <priority>{prio}</priority>")
            rows.append("  </url>")
    rows.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    return sum(len(v) for v in pmap.values())


def write_robots():
    txt = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /_to_delete/\n"
        "Disallow: /includes/\n"
        "\n"
        f"Sitemap: {BASE}/sitemap.xml\n"
    )
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    pmap = pages_by_lang()
    changed = 0
    for page, langs in pmap.items():
        for lang in langs:
            if process(lang, page, langs):
                changed += 1
    print(f"zmienione strony: {changed}")
    print(f"@import fontow usuniety: {fix_font_import()}")
    print(f"sitemap.xml: {write_sitemap(pmap)} URL-i")
    write_robots()
    print("robots.txt: OK")
