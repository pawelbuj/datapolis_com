# -*- coding: utf-8 -*-
"""ver7: wplecenie kadrowanych zrzutow z produktu — jeden zestaw na cztery jezyki."""
import re, os, sys

SHOTS = {
 "workflow": dict(
   file="workflow-nonconformity",
   bar={"en":"2to2 · Nonconformity process","pl":"2to2 · proces niezgodności",
        "de":"2to2 · Nonconformity-Prozess","es":"2to2 · proceso de no conformidad"},
   alt={"en":"A nonconformity process in 2to2: states, transitions and approvals on one canvas.",
        "pl":"Proces niezgodności w 2to2: stany, przejścia i akceptacje na jednym płótnie.",
        "de":"Ein Nonconformity-Prozess in 2to2: Zustände, Übergänge und Genehmigungen auf einer Fläche.",
        "es":"Un proceso de no conformidad en 2to2: estados, transiciones y aprobaciones en un lienzo."},
   cap={"en":"<b>A real process running on 2to2.</b> States, transitions, approvals and the path a Quality Engineer sees — a screenshot from the product, not a mockup.",
        "pl":"<b>Prawdziwy proces działający na 2to2.</b> Stany, przejścia, akceptacje i ścieżka, którą widzi inżynier jakości — zrzut z produktu, nie makieta.",
        "de":"<b>Ein echter Prozess, der auf 2to2 läuft.</b> Zustände, Übergänge, Genehmigungen und der Pfad, den ein Qualitätsingenieur sieht — ein Screenshot aus dem Produkt, keine Attrappe.",
        "es":"<b>Un proceso real funcionando sobre 2to2.</b> Estados, transiciones, aprobaciones y el camino que ve un ingeniero de calidad — una captura del producto, no una maqueta."},
   fade=True, zoom="2"),
 "processes": dict(
   file="processes-published",
   bar={"en":"2to2 · Published processes","pl":"2to2 · opublikowane procesy",
        "de":"2to2 · Veröffentlichte Prozesse","es":"2to2 · procesos publicados"},
   alt={"en":"Four published processes of one application, each with its fields, states, forms and automations.",
        "pl":"Cztery opublikowane procesy jednej aplikacji, każdy z polami, stanami, formularzami i automatyzacjami.",
        "de":"Vier veröffentlichte Prozesse einer Anwendung, jeder mit Feldern, Zuständen, Formularen und Automatisierungen.",
        "es":"Cuatro procesos publicados de una aplicación, cada uno con sus campos, estados, formularios y automatizaciones."},
   cap={"en":"<b>Four processes of one quality-management application.</b> Each with its own states, forms and automations — published and running. The field list is the data model the business described, not a developer's table.",
        "pl":"<b>Cztery procesy jednej aplikacji do zarządzania jakością.</b> Każdy z własnymi stanami, formularzami i automatyzacjami — opublikowany i działający. Lista pól to model danych opisany przez biznes, a nie tabela od programisty.",
        "de":"<b>Vier Prozesse einer Qualitätsmanagement-Anwendung.</b> Jeder mit eigenen Zuständen, Formularen und Automatisierungen — veröffentlicht und im Betrieb. Die Feldliste ist das Datenmodell, das der Fachbereich beschrieben hat, keine Entwicklertabelle.",
        "es":"<b>Cuatro procesos de una misma aplicación de gestión de calidad.</b> Cada uno con sus estados, formularios y automatizaciones — publicado y en marcha. La lista de campos es el modelo de datos que describió el negocio, no una tabla de un programador."},
   fade=True, zoom="2"),
 "spec": dict(
   file="specification-docs",
   bar={"en":"2to2 · Application specification","pl":"2to2 · specyfikacja aplikacji",
        "de":"2to2 · Anwendungsspezifikation","es":"2to2 · especificación de la aplicación"},
   alt={"en":"The application specification as a tree of confirmed, versioned documents.",
        "pl":"Specyfikacja aplikacji jako drzewo zatwierdzonych, wersjonowanych dokumentów.",
        "de":"Die Anwendungsspezifikation als Baum aus freigegebenen, versionierten Dokumenten.",
        "es":"La especificación de la aplicación como un árbol de documentos confirmados y versionados."},
   cap={"en":"<b>The specification is a set of documents, not a prompt.</b> Brief, glossary, actors, domain model, business rules, use cases, screens — each one versioned and confirmed. This is what 2to2 executes.",
        "pl":"<b>Specyfikacja to zestaw dokumentów, a nie prompt.</b> Brief, słownik, aktorzy, model dziedziny, reguły biznesowe, przypadki użycia, ekrany — każdy z wersją i statusem zatwierdzenia. To właśnie wykonuje 2to2.",
        "de":"<b>Die Spezifikation ist eine Sammlung von Dokumenten, kein Prompt.</b> Brief, Glossar, Akteure, Domänenmodell, Geschäftsregeln, Anwendungsfälle, Masken — jedes versioniert und freigegeben. Genau das führt 2to2 aus.",
        "es":"<b>La especificación es un conjunto de documentos, no un prompt.</b> Brief, glosario, actores, modelo de dominio, reglas de negocio, casos de uso, pantallas — cada uno versionado y confirmado. Esto es lo que ejecuta 2to2."},
   fade=False, zoom="1.5"),
}

LABEL = {"en":"Look inside the product","pl":"Zajrzyj do produktu",
         "de":"Blick ins Produkt","es":"Mira dentro del producto"}
GO = {"en":"Open","pl":"Otwórz","de":"Öffnen","es":"Abrir"}
TITLE = {
 "workflow": {"en":"A process, running","pl":"Proces, który działa",
              "de":"Ein Prozess, der läuft","es":"Un proceso en marcha"},
 "processes":{"en":"Four published processes","pl":"Cztery opublikowane procesy",
              "de":"Vier veröffentlichte Prozesse","es":"Cuatro procesos publicados"},
 "spec":     {"en":"The specification itself","pl":"Sama specyfikacja",
              "de":"Die Spezifikation selbst","es":"La propia especificación"},
}

def esc(t):
    return t.replace('"', "&quot;")

def peek(key, lang, indent):
    s = SHOTS[key]
    pre = "assets" if lang == "en" else "../assets"
    i = " " * indent
    return "\n".join([
      '%s<button type="button" class="v7-peek"' % i,
      '%s        data-peek-src="%s/img/product/%s.webp"' % (i, pre, s["file"]),
      '%s        data-peek-alt="%s"' % (i, esc(s["alt"][lang])),
      '%s        data-peek-bar="%s"' % (i, esc(s["bar"][lang])),
      '%s        data-peek-cap="%s">' % (i, esc(s["cap"][lang])),
      '%s    <span class="v7-peek__thumb" style="--peek-zoom:%s"><img src="%s/img/product/%s.webp" alt="" loading="lazy" decoding="async"></span>' % (i, s.get("zoom","1.5"), pre, s["file"]),
      '%s    <span class="v7-peek__meta">' % i,
      '%s        <span class="v7-peek__title">%s</span>' % (i, TITLE[key][lang]),
      '%s        <span class="v7-peek__go">%s &#8594;</span>' % (i, GO[lang]),
      '%s    </span>' % i,
      '%s</button>' % i,
    ])

def strip(keys, lang, indent):
    i = " " * indent
    row = "v7-peeks__row" + ("" if len(keys) == 3 else " v7-peeks__row--%d" % len(keys))
    out = ['%s<div class="v7-peeks">' % i,
           '%s    <p class="v7-peeks__label">%s</p>' % (i, LABEL[lang]),
           '%s    <div class="%s">' % (i, row)]
    for k in keys:
        out.append(peek(k, lang, indent + 8))
    out += ['%s    </div>' % i, '%s</div>' % i]
    return "\n".join(out)

def add_script(path, lang):
    s = open(path, encoding="utf-8").read()
    if "product-peek.js" in s:
        return s
    pre = "assets" if lang == "en" else "../assets"
    tag = '    <script src="%s/js/product-peek.js?v=20260918"></script>\n' % pre
    return s.replace("</body>", tag + "</body>", 1)

def band(keys, lang):
    """waskie pasmo dla podstrony — bez naglowka, bez nowej sekcji tresci"""
    return ('        <section class="v7-peekband">\n'
            '            <div class="v7-container">\n'
            + strip(keys, lang, 16) + "\n"
            '            </div>\n'
            '        </section>')

def put(path, lang, keys, anchor, indent, as_band=False):
    s = add_script(path, lang)
    if "v7-peeks" in s:
        print("   juz jest:", path); return
    assert anchor in s, (path, anchor[:40])
    block = band(keys, lang) if as_band else strip(keys, lang, indent)
    s = s.replace(anchor, block + "\n\n" + anchor, 1)
    open(path, "w", encoding="utf-8").write(s)
    print("   ok", path)

if __name__ == "__main__":
    for lang, d in (("en",""), ("pl","pl/"), ("de","de/"), ("es","es/")):
        print("---", lang)
        # strona glowna: trzy dowody w jednym pasku, w sekcji platformy
        put(d + "index.html", lang, ["workflow", "processes", "spec"],
            '                <p class="dp-platform__tagline">', 16)
        # podstrony: jeden podglad, bez nowej sekcji — tuz przed wspolnym CTA
        put(d + "platform-2to2.html", lang, ["processes", "workflow"],
            '        <section class="v7-cta">', 8, as_band=True)
        put(d + "app-creator.html", lang, ["spec", "workflow"],
            '        <section class="v7-cta">', 8, as_band=True)
