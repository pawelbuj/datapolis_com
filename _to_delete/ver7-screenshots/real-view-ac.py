# -*- coding: utf-8 -*-
"""ver7: drugi widok eksponatu w hero strony App Creator — prawdziwa specyfikacja."""
import re

T = {
 "en": dict(model="Example", real="Product screenshot",
   bar="2to2 · Application specification",
   alt="The application specification as a tree of confirmed, versioned documents.",
   hint="The specification of a real application. Click to enlarge.",
   cap="<b>The specification is a set of documents, not a prompt.</b> Brief, glossary, actors, domain model, business rules, use cases, screens — each one versioned and confirmed. This is what 2to2 executes."),
 "pl": dict(model="Przykład", real="Zrzut z produktu",
   bar="2to2 · specyfikacja aplikacji",
   alt="Specyfikacja aplikacji jako drzewo zatwierdzonych, wersjonowanych dokumentów.",
   hint="Specyfikacja prawdziwej aplikacji. Kliknij, żeby powiększyć.",
   cap="<b>Specyfikacja to zestaw dokumentów, a nie prompt.</b> Brief, słownik, aktorzy, model dziedziny, reguły biznesowe, przypadki użycia, ekrany — każdy z wersją i statusem zatwierdzenia. To właśnie wykonuje 2to2."),
 "de": dict(model="Beispiel", real="Screenshot aus dem Produkt",
   bar="2to2 · Anwendungsspezifikation",
   alt="Die Anwendungsspezifikation als Baum aus freigegebenen, versionierten Dokumenten.",
   hint="Die Spezifikation einer echten Anwendung. Zum Vergrößern klicken.",
   cap="<b>Die Spezifikation ist eine Sammlung von Dokumenten, kein Prompt.</b> Brief, Glossar, Akteure, Domänenmodell, Geschäftsregeln, Anwendungsfälle, Masken — jedes versioniert und freigegeben. Genau das führt 2to2 aus."),
 "es": dict(model="Ejemplo", real="Captura del producto",
   bar="2to2 · especificación de la aplicación",
   alt="La especificación de la aplicación como un árbol de documentos confirmados y versionados.",
   hint="La especificación de una aplicación real. Haz clic para ampliar.",
   cap="<b>La especificación es un conjunto de documentos, no un prompt.</b> Brief, glosario, actores, modelo de dominio, reglas de negocio, casos de uso, pantallas — cada uno versionado y confirmado. Esto es lo que ejecuta 2to2."),
}
SHOT = "img/product/specification-docs.webp"

def block(lang):
    t = T[lang]
    pre = "assets" if lang == "en" else "../assets"
    i = " " * 20
    esc = lambda x: x.replace('"', "&quot;")
    return "\n".join([
      '%s<div class="v7-extract__switch">' % i,
      '%s    <span class="v7-view" role="group">' % i,
      '%s        <button type="button" class="v7-view__opt is-on" data-stage-view="model" aria-pressed="true">%s</button>' % (i, t["model"]),
      '%s        <button type="button" class="v7-view__opt" data-stage-view="real" aria-pressed="false">%s</button>' % (i, t["real"]),
      '%s    </span>' % i,
      '%s</div>' % i,
    ]), "\n".join([
      '%s<figure class="v7-real">' % i,
      '%s    <div class="v7-real__bar"><i aria-hidden="true"></i>%s</div>' % (i, t["bar"]),
      '%s    <button type="button" class="v7-real__shot"' % i,
      '%s            data-peek-src="%s/%s"' % (i, pre, SHOT),
      '%s            data-peek-bar="%s"' % (i, esc(t["bar"])),
      '%s            data-peek-alt="%s"' % (i, esc(t["alt"])),
      '%s            data-peek-cap="%s">' % (i, esc(t["cap"])),
      '%s        <img src="%s/%s" alt="%s" loading="lazy" decoding="async">' % (i, pre, SHOT, t["alt"]),
      '%s    </button>' % i,
      '%s    <figcaption class="v7-real__cap">%s</figcaption>' % (i, t["cap"]),
      '%s</figure>' % i,
    ])

def apply(lang, path):
    s = open(path, encoding="utf-8").read()
    if "v7-real" in s:
        print("   juz jest:", path); return
    sw, fig = block(lang)
    anchor_stage = '                    <div class="v7-stage">'
    assert anchor_stage in s, path
    s = s.replace(anchor_stage, sw + "\n" + anchor_stage, 1)
    anchor_hint = '                    <p class="v7-extract__hint">'
    assert anchor_hint in s, path
    s = s.replace(anchor_hint, fig + "\n" + anchor_hint, 1)
    t = T[lang]
    # data-hint-idle bierzemy z tresci elementu, zeby nie duplikowac tlumaczen
    m = re.search(r'<p class="v7-extract__hint">(.*?)</p>', s, re.S)
    idle = re.sub(r"\s+", " ", m.group(1)).strip()
    s = s.replace('<p class="v7-extract__hint">',
                  '<p class="v7-extract__hint" data-exhibit-hint data-hint-idle="%s" data-hint-real="%s">'
                  % (idle.replace('"', "&quot;"), t["hint"].replace('"', "&quot;")), 1)
    if "product-peek.js" not in s:
        pre = "assets" if lang == "en" else "../assets"
        s = s.replace("</body>", '    <script src="%s/js/product-peek.js?v=1"></script>\n</body>' % pre, 1)
    open(path, "w", encoding="utf-8").write(s)
    print("   ok", path)

if __name__ == "__main__":
    for lang, d in (("en",""), ("pl","pl/"), ("de","de/"), ("es","es/")):
        print("---", lang)
        apply(lang, d + "app-creator.html")
