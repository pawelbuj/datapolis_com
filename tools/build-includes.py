#!/usr/bin/env python3
"""Datapolis.com — build statyczny.

1. Wkleja naglowek i stopke (includes/*.html danego jezyka) wprost w HTML strony,
   zamiast doklejac je JS-em. Dzieki temu linki wewnetrzne widza roboty, ktore
   nie wykonuja JavaScriptu (GPTBot, ClaudeBot, PerplexityBot).
2. Wstrzykuje dane strukturalne JSON-LD (Organization, WebSite, WebPage,
   BreadcrumbList, SoftwareApplication na stronie platformy).

Skrypt jest idempotentny — uruchamiaj po KAZDEJ zmianie w includes/*.html.

    python3 tools/build-includes.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://datapolis.com"
OG = f"{BASE}/assets/img/og-image-1200x630.png"
DIRS = {"en": ".", "pl": "pl", "de": "de", "es": "es"}
HOME = {"en": "Home", "pl": "Strona główna", "de": "Startseite", "es": "Inicio"}

H_START, H_END = "<!--build:header-->", "<!--/build:header-->"
F_START, F_END = "<!--build:footer-->", "<!--/build:footer-->"
J_START, J_END = "    <!-- JSON-LD -->\n", "    <!-- /JSON-LD -->\n"

ORG_ID = f"{BASE}/#organization"
SITE_ID = f"{BASE}/#website"


def url_for(lang, page):
    prefix = "" if lang == "en" else f"/{lang}"
    if page == "index":
        return f"{BASE}/" if lang == "en" else f"{BASE}{prefix}"
    return f"{BASE}{prefix}/{page}"


def organization():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Datapolis",
        "legalName": "Datapolis Sp. z o.o.",
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": f"{BASE}/logos/logo.svg"},
        "image": OG,
        "email": "office@datapolis.com",
        "address": {"@type": "PostalAddress", "addressCountry": "PL"},
        "sameAs": [
            "https://www.linkedin.com/company/datapolis-com",
            "https://www.youtube.com/@datapolisworkbox",
        ],
        "contactPoint": [{
            "@type": "ContactPoint",
            "contactType": "sales",
            "email": "office@datapolis.com",
            "availableLanguage": ["en", "pl", "de", "es"],
        }],
    }


def website():
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": f"{BASE}/",
        "name": "Datapolis",
        "publisher": {"@id": ORG_ID},
        "inLanguage": ["en", "pl", "de", "es"],
    }


def graph_for(lang, page, title, desc):
    url = url_for(lang, page)
    nodes = [organization(), website()]

    webpage = {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": title,
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": ORG_ID},
        "inLanguage": lang,
        "primaryImageOfPage": {"@type": "ImageObject", "url": OG},
    }
    if desc:
        webpage["description"] = desc

    if page != "index":
        webpage["breadcrumb"] = {"@id": f"{url}#breadcrumb"}
        nodes.append({
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1,
                 "name": HOME[lang], "item": url_for(lang, "index")},
                {"@type": "ListItem", "position": 2, "name": title},
            ],
        })

    nodes.append(webpage)

    if page == "platform-2to2":
        nodes.append({
            "@type": "SoftwareApplication",
            "@id": f"{BASE}/#2to2",
            "name": "2to2",
            "url": "https://2to2.ai",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "publisher": {"@id": ORG_ID},
            "description": ("Operating layer for governed work: process apps that humans "
                            "and digital workers execute inside one audited, permissioned layer."),
        })

    return {"@context": "https://schema.org", "@graph": nodes}


def read_include(lang, name):
    p = os.path.join(ROOT, DIRS[lang], "includes", name)
    if not os.path.exists(p):
        p = os.path.join(ROOT, "includes", name)
    return open(p, encoding="utf-8").read().rstrip("\n")


def inline_shell(html, lang, includes):
    """Wkleja naglowek/stopke w placeholdery. Nadpisuje poprzedni build."""
    for pid, start, end, name in (
            ("header-placeholder", H_START, H_END, "header.html"),
            ("footer-placeholder", F_START, F_END, "footer.html")):
        block = f'<div id="{pid}">{start}\n{includes[name]}\n{end}</div>'
        pat_built = re.compile(rf'<div id="{pid}">{re.escape(start)}.*?{re.escape(end)}</div>', re.S)
        if pat_built.search(html):
            html = pat_built.sub(lambda _m: block, html, count=1)
        else:
            html = re.sub(rf'<div id="{pid}">\s*</div>', lambda _m: block, html, count=1)
    return html


def inject_jsonld(html, payload):
    block = (J_START
             + '    <script type="application/ld+json">\n'
             + json.dumps(payload, ensure_ascii=False, indent=2)
             + "\n    </script>\n"
             + J_END)
    old = re.compile(re.escape(J_START) + r".*?" + re.escape(J_END), re.S)
    if old.search(html):
        return old.sub(lambda _m: block, html, count=1)
    return html.replace("</head>", "\n" + block + "</head>", 1)


def main():
    changed = links_before = links_after = 0
    pages = 0
    for lang, d in DIRS.items():
        includes = {n: read_include(lang, n) for n in ("header.html", "footer.html")}
        folder = os.path.join(ROOT, d)
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".html"):
                continue
            path = os.path.join(folder, fn)
            html = orig = open(path, encoding="utf-8").read()
            page = fn[:-5]
            pages += 1

            links_before += len(set(re.findall(r'href="(?!http)[^"]+\.html"', html)))

            if "header-placeholder" in html:
                html = inline_shell(html, lang, includes)

            title = re.search(r"<title>(.*?)</title>", html, re.S)
            title = re.sub(r"\s+", " ", title.group(1)).strip() if title else "Datapolis"
            desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
            desc = re.sub(r"\s+", " ", desc.group(1)).strip() if desc else ""

            html = inject_jsonld(html, graph_for(lang, page, title, desc))

            links_after += len(set(re.findall(r'href="(?!http)[^"]+\.html"', html)))

            if html != orig:
                open(path, "w", encoding="utf-8").write(html)
                changed += 1

    print(f"stron przetworzonych: {pages}, zmienionych: {changed}")
    print(f"unikalne linki wewnetrzne w surowym HTML: {links_before} -> {links_after}")


if __name__ == "__main__":
    main()
