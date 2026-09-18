#!/usr/bin/env python3
"""Datapolis.com — build statyczny.

1. Wkleja naglowek i stopke (includes/*.html danego jezyka) wprost w HTML strony,
   zamiast doklejac je JS-em. Dzieki temu linki wewnetrzne widza roboty, ktore
   nie wykonuja JavaScriptu (GPTBot, ClaudeBot, PerplexityBot).
2. Wstrzykuje dane strukturalne JSON-LD (Organization, WebSite, WebPage,
   BreadcrumbList, SoftwareApplication na stronach produktowych).

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


def _wf3_modified():
    """Data ostatniej zmiany sharepoint.html — realny sygnał świeżości.

    Bierzemy późniejszą z dwóch: daty ostatniego commita i daty modyfikacji
    pliku. Dzięki temu strona przebudowana, ale jeszcze niezacommitowana,
    nie ogłasza daty starszej niż jej własna treść.
    """
    import os
    import subprocess
    from datetime import date, datetime, timezone

    candidates = []
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", "sharepoint.html"],
                             cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        if out:
            candidates.append(out[:10])
    except Exception:
        pass

    path = os.path.join(ROOT, "sharepoint.html")
    if os.path.exists(path):
        ts = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
        candidates.append(ts.strftime("%Y-%m-%d"))

    return max(candidates) if candidates else date.today().isoformat()


WF3_MODIFIED = _wf3_modified()


# ============================================================
#  Zgoda na ciasteczka + Google Analytics
#  Jeden blok wstrzykiwany w <head> każdej strony, idempotentnie.
#  Kolejność ma znaczenie: domyślne odmowy (Consent Mode v2) muszą
#  wykonać się PRZED załadowaniem gtag.js, inaczej GA zdąży zapisać
#  ciasteczko zanim użytkownik cokolwiek kliknie.
# ============================================================

GA_ID = "G-41L2VC300P"
C_START, C_END = "<!--build:consent-->", "<!--/build:consent-->"

CONSENT_TEXT = {
    "en": {
        "msg": "We use Google Analytics to see which pages get read. No analytics cookies are stored without your consent.",
        "yes": "I agree", "no": "Essential only", "more": "Privacy policy",
    },
    "pl": {
        "msg": "Używamy Google Analytics, żeby wiedzieć, które strony są czytane. Bez Twojej zgody nie zapisujemy żadnych ciasteczek analitycznych.",
        "yes": "Zgadzam się", "no": "Tylko niezbędne", "more": "Polityka prywatności",
    },
    "de": {
        "msg": "Wir nutzen Google Analytics, um zu sehen, welche Seiten gelesen werden. Ohne Ihre Einwilligung werden keine Analyse-Cookies gesetzt.",
        "yes": "Einverstanden", "no": "Nur notwendige", "more": "Datenschutz",
    },
    "es": {
        "msg": "Usamos Google Analytics para saber qué páginas se leen. Sin su consentimiento no se guarda ninguna cookie analítica.",
        "yes": "Acepto", "no": "Solo esenciales", "more": "Política de privacidad",
    },
}


def consent_block(lang):
    t = CONSENT_TEXT.get(lang, CONSENT_TEXT["en"])
    return f"""{C_START}
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('consent', 'default', {{
        'ad_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied',
        'analytics_storage': 'denied',
        'functionality_storage': 'denied',
        'personalization_storage': 'denied',
        'security_storage': 'granted',
        'wait_for_update': 500
      }});
      try {{
        if (localStorage.getItem('dp-consent') === 'granted') {{
          gtag('consent', 'update', {{'analytics_storage': 'granted'}});
        }}
      }} catch (e) {{}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}', {{'anonymize_ip': true}});
    </script>
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <style>
      .dp-consent{{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:760px;margin:0 auto;
        display:none;gap:18px;align-items:center;flex-wrap:wrap;justify-content:space-between;
        padding:18px 20px;border:1px solid rgba(148,163,184,.22);border-radius:14px;
        background:rgba(11,18,32,.97);backdrop-filter:blur(10px);
        box-shadow:0 18px 50px rgba(0,0,0,.45);color:#cbd5e1;
        font-family:Inter,system-ui,sans-serif;font-size:.92rem;line-height:1.55}}
      .dp-consent[data-show="1"]{{display:flex}}
      .dp-consent p{{margin:0;flex:1 1 320px}}
      .dp-consent a{{color:#7dd3fc}}
      .dp-consent div{{display:flex;gap:10px;flex:0 0 auto}}
      .dp-consent button{{font:inherit;cursor:pointer;border-radius:9px;padding:9px 16px;border:1px solid transparent;white-space:nowrap}}
      .dp-consent .dp-consent__yes{{background:#14b8a6;color:#04211f;font-weight:600}}
      .dp-consent .dp-consent__no{{background:transparent;color:#cbd5e1;border-color:rgba(148,163,184,.35)}}
      @media (max-width:560px){{.dp-consent div{{width:100%}}.dp-consent button{{flex:1}}}}
    </style>
    <script>
      (function () {{
        function store(v) {{ try {{ localStorage.setItem('dp-consent', v); }} catch (e) {{}} }}
        function saved() {{ try {{ return localStorage.getItem('dp-consent'); }} catch (e) {{ return null; }} }}
        if (saved()) return;
        document.addEventListener('DOMContentLoaded', function () {{
          var bar = document.createElement('aside');
          bar.className = 'dp-consent';
          bar.setAttribute('role', 'dialog');
          bar.setAttribute('aria-live', 'polite');
          bar.innerHTML = '<p>{t["msg"]} <a href="legal.html">{t["more"]}</a></p>'
            + '<div><button type="button" class="dp-consent__no">{t["no"]}</button>'
            + '<button type="button" class="dp-consent__yes">{t["yes"]}</button></div>';
          document.body.appendChild(bar);
          bar.setAttribute('data-show', '1');
          bar.querySelector('.dp-consent__yes').addEventListener('click', function () {{
            store('granted');
            gtag('consent', 'update', {{'analytics_storage': 'granted'}});
            bar.remove();
          }});
          bar.querySelector('.dp-consent__no').addEventListener('click', function () {{
            store('denied');
            bar.remove();
          }});
        }});
      }})();
    </script>
    {C_END}"""


def inject_consent(html, lang):
    block = consent_block(lang)
    old = re.compile(re.escape(C_START) + r".*?" + re.escape(C_END), re.S)
    if old.search(html):
        return old.sub(lambda _m: block, html, count=1)
    return html.replace("</head>", "\n    " + block + "\n</head>", 1)


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

    if page == "sharepoint":
        # Strona-kompendium o wyłączeniu przepływów SharePoint 2010/2013.
        # TechArticle + dateModified: data aktualizacji jest tu sygnałem,
        # bo treść opisuje zdarzenie sprzed dni, nie stan trwały.
        nodes.append({
            "@type": "TechArticle",
            "@id": f"{url}#article",
            "headline": title,
            "description": desc,
            "inLanguage": lang,
            "isPartOf": {"@id": f"{url}#webpage"},
            "mainEntityOfPage": {"@id": f"{url}#webpage"},
            "author": {"@id": ORG_ID},
            "publisher": {"@id": ORG_ID},
            "datePublished": "2026-09-18",
            "dateModified": WF3_MODIFIED,
            "about": [
                {"@type": "Thing", "name": "SharePoint Server Subscription Edition"},
                {"@type": "Thing", "name": "SharePoint 2010 workflows"},
                {"@type": "Thing", "name": "SharePoint 2013 workflows"},
                {"@type": "Thing", "name": "KB5002908"},
            ],
        })

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

    if page == "app-creator":
        nodes.append({
            "@type": "SoftwareApplication",
            "@id": f"{BASE}/app-creator#software",
            "name": "2to2 App Creator",
            "url": f"{BASE}/app-creator",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "publisher": {"@id": ORG_ID},
            "description": ("AI-assisted application creation from business documentation. "
                            "The specification and the governed application remain synchronized "
                            "as one living model."),
            "featureList": [
                "Create business applications from documentation",
                "Keep specification and application synchronized",
                "Generate workflow, data, pages, roles, and permissions",
                "Review and govern changes before publication",
            ],
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
            html = inject_consent(html, lang)

            links_after += len(set(re.findall(r'href="(?!http)[^"]+\.html"', html)))

            if html != orig:
                open(path, "w", encoding="utf-8").write(html)
                changed += 1

    print(f"stron przetworzonych: {pages}, zmienionych: {changed}")
    print(f"unikalne linki wewnetrzne w surowym HTML: {links_before} -> {links_after}")


if __name__ == "__main__":
    main()
