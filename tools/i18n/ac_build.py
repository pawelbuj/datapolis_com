# -*- coding: utf-8 -*-
"""Generuje app-creator.html dla pl/de/es z wersji angielskiej:
   - hero v7 z szablonu (kolejnosc slow w zdaniach zachowana w tlumaczeniu),
   - reszta strony przez podmiane calych zdan (najdluzsze najpierw),
   - linki, meta, hreflang i canonical przestawione na wersje jezykowa."""
import re, sys, os, importlib

HERO = """        <section class="v7-page-hero" aria-labelledby="app-creator-title" data-spec-app-exhibit>
            <div class="v7-container v7-page-hero__layout">
                <div>
                    <p class="v7-eyebrow">2to2 App Creator</p>
                    <h1 class="v7-page-hero__title" id="app-creator-title">
                        {h1}
                        <em>{h1_em}</em>
                    </h1>
                    <p class="v7-page-hero__lead">{lead}</p>

                    <div class="v7-exhibit__actions">
                        <a class="v7-btn v7-btn--primary" href="#how-it-works">{cta1} <span aria-hidden="true">↓</span></a>
                        <a class="v7-btn v7-btn--ghost" href="contact.html">{cta2}</a>
                    </div>

                    <ul class="v7-points">
                        <li><span aria-hidden="true">✓</span> {pt1}</li>
                        <li><span aria-hidden="true">✓</span> {pt2}</li>
                        <li><span aria-hidden="true">✓</span> {pt3}</li>
                    </ul>
                </div>

                <div class="v7-extract">
                    <div class="v7-stage">
                        <div class="v7-pane">
                            <div class="v7-pane__head">
                                <span class="v7-pane__label">{pane_doc}</span>
                                <span class="v7-pane__meta">{pane_doc_meta}</span>
                            </div>
                            <div class="v7-pane__body">
                                <p class="v7-doc__title">{doc_title}</p>

                                <p class="v7-doc__heading">{h_32}</p>
                                <p class="v7-doc__p">{par_32}</p>

                                <p class="v7-doc__heading">{h_33}</p>
                                <p class="v7-doc__p">{par_33}</p>

                                <p class="v7-doc__heading">{h_34}</p>
                                <p class="v7-doc__p">{par_34}</p>
                            </div>
                        </div>

                        <div class="v7-stage__divider" aria-hidden="true"></div>

                        <div class="v7-pane">
                            <div class="v7-pane__head">
                                <span class="v7-pane__label">{pane_spec}</span>
                                <span class="v7-pane__meta">{pane_spec_meta}</span>
                            </div>
                            <div class="v7-pane__body">
                                <div class="v7-items">
                                    <div class="v7-item" data-link="role" tabindex="0">
                                        <span class="v7-item__label">{l_role}</span>
                                        <span class="v7-item__value">{v_role}<small>{d_role}</small></span>
                                    </div>
                                    <div class="v7-item" data-link="data" tabindex="0">
                                        <span class="v7-item__label">{l_data}</span>
                                        <span class="v7-item__value">{v_data}<small>{d_data}</small></span>
                                    </div>
                                    <div class="v7-item" data-link="rule" tabindex="0">
                                        <span class="v7-item__label">{l_rule}</span>
                                        <span class="v7-item__value">{v_rule}<small>{d_rule}</small></span>
                                    </div>
                                    <div class="v7-item" data-link="audit" tabindex="0">
                                        <span class="v7-item__label">{l_audit}</span>
                                        <span class="v7-item__value">{v_audit}<small>{d_audit}</small></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <p class="v7-extract__hint">{hint}</p>
                </div>
            </div>
        </section>"""

def build(lang):
    mod = importlib.import_module("ac_" + lang)
    hero_d, body_d, meta_d = mod.HERO, mod.BODY, mod.META

    s = open("app-creator.html", encoding="utf-8").read()

    # 1) hero v7 -> wersja jezykowa
    pat_hero = re.compile(r'        <section class="v7-page-hero".*?\n        </section>', re.S)
    assert pat_hero.search(s), "nie znaleziono hero v7"
    s = pat_hero.sub(lambda _m: HERO.format(**hero_d), s, count=1)

    # 2) reszta tresci: najdluzsze frazy najpierw
    missing = []
    for en in sorted(body_d, key=len, reverse=True):
        pl = body_d[en]
        if en not in s:
            missing.append(en); continue
        s = s.replace(en, pl)
    if missing:
        print("  !! nie znaleziono %d fraz:" % len(missing))
        for m in missing[:6]: print("     -", m[:70])

    # 3) sciezki do zasobow o poziom wyzej
    s = re.sub(r'(href|src)="assets/', r'\1="../assets/', s)
    s = re.sub(r'(href|src)="logos/', r'\1="../logos/', s)
    s = re.sub(r'(href|src)="storage/', r'\1="../storage/', s)
    s = s.replace('src="includes/loader.js"', 'src="../includes/loader.js"')
    # sciezki skladane w inline-JS (loadScript), nie tylko w atrybutach
    s = s.replace("'assets/", "'../assets/")

    # 4) meta / jezyk / canonical / hreflang
    s = s.replace('<html lang="en">', '<html lang="%s">' % lang, 1)
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % meta_d["title"], s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content=".*?">',
               '<meta name="description" content="%s">' % meta_d["desc"], s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content=".*?">',
               '<meta property="og:title" content="%s">' % meta_d["og"], s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:description" content=".*?">',
               '<meta property="og:description" content="%s">' % meta_d["desc"], s, count=1, flags=re.S)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               '<link rel="canonical" href="https://datapolis.com/%s/app-creator">' % lang, s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">',
               '<meta property="og:url" content="https://datapolis.com/%s/app-creator">' % lang, s, count=1)
    s = re.sub(r'<meta property="og:locale" content="[^"]*">',
               '<meta property="og:locale" content="%s">' % meta_d["locale"], s, count=1)
    hre = "\n".join(
        '    <link rel="alternate" hreflang="%s" href="https://datapolis.com/%sapp-creator">' % (l, p)
        for l, p in (("en",""), ("pl","pl/"), ("de","de/"), ("es","es/")))
    hre += '\n    <link rel="alternate" hreflang="x-default" href="https://datapolis.com/app-creator">'
    s = re.sub(r'(    <link rel="alternate" hreflang="[^"]*" href="[^"]*">\n)+'
               r'(    <link rel="alternate" hreflang="x-default" href="[^"]*">)',
               lambda _m: hre, s, count=1)

    out = "%s/app-creator.html" % lang
    open(out, "w", encoding="utf-8").write(s)
    print("ok", out)

if __name__ == "__main__":
    sys.path.insert(0, os.environ["HOME"] + "/v7")
    for lang in sys.argv[1:]:
        print("---", lang)
        build(lang)
