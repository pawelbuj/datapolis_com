# -*- coding: utf-8 -*-
"""ver7: drugi widok eksponatu — prawdziwy zrzut z produktu.
   Wstawia przelacznik do paska eksponatu i kadr pod scena.
   Bez nowej sekcji: strona nie rosnie."""
import re, os

T = {
 "en": dict(model="Diagram", real="Product screenshot",
   bar="2to2 · Nonconformity process",
   alt="A nonconformity process in 2to2: states, transitions and approvals on one canvas.",
   hint="A different process than the one above — the same platform. Click to enlarge.",
   cap="<b>This is what the canvas really looks like.</b> A nonconformity process in production: states, transitions, approvals and the path one role sees. Another process than the example above — the diagram is our drawing, this is the product."),
 "pl": dict(model="Schemat", real="Zrzut z produktu",
   bar="2to2 · proces niezgodności",
   alt="Proces niezgodności w 2to2: stany, przejścia i akceptacje na jednym płótnie.",
   hint="Inny proces niż powyżej — ta sama platforma. Kliknij, żeby powiększyć.",
   cap="<b>Tak wygląda to płótno naprawdę.</b> Proces niezgodności na produkcji: stany, przejścia, akceptacje i ścieżka, którą widzi jedna rola. To inny proces niż przykład powyżej — schemat jest naszym rysunkiem, to jest produkt."),
 "de": dict(model="Diagramm", real="Screenshot aus dem Produkt",
   bar="2to2 · Nonconformity-Prozess",
   alt="Ein Nonconformity-Prozess in 2to2: Zustände, Übergänge und Genehmigungen auf einer Fläche.",
   hint="Ein anderer Prozess als oben — dieselbe Plattform. Zum Vergrößern klicken.",
   cap="<b>So sieht diese Fläche wirklich aus.</b> Ein Nonconformity-Prozess im Produktivbetrieb: Zustände, Übergänge, Genehmigungen und der Pfad, den eine Rolle sieht. Ein anderer Prozess als das Beispiel oben — das Diagramm ist unsere Zeichnung, das hier ist das Produkt."),
 "es": dict(model="Diagrama", real="Captura del producto",
   bar="2to2 · proceso de no conformidad",
   alt="Un proceso de no conformidad en 2to2: estados, transiciones y aprobaciones en un lienzo.",
   hint="Un proceso distinto al de arriba — la misma plataforma. Haz clic para ampliar.",
   cap="<b>Así es este lienzo de verdad.</b> Un proceso de no conformidad en producción: estados, transiciones, aprobaciones y el camino que ve un rol. Es un proceso distinto al ejemplo de arriba — el diagrama es nuestro dibujo, esto es el producto."),
}

SHOT = "img/product/workflow-nonconformity.webp"

def switch(lang, i="                    "):
    t = T[lang]
    return "\n".join([
      '%s<span class="v7-view" role="group">' % i,
      '%s    <button type="button" class="v7-view__opt is-on" data-stage-view="model" aria-pressed="true">%s</button>' % (i, t["model"]),
      '%s    <button type="button" class="v7-view__opt" data-stage-view="real" aria-pressed="false">%s</button>' % (i, t["real"]),
      '%s</span>' % i,
    ])

def figure(lang, i="                "):
    t = T[lang]
    pre = "assets" if lang == "en" else "../assets"
    cap = t["cap"].replace('"', "&quot;")
    return "\n".join([
      '%s<figure class="v7-real">' % i,
      '%s    <div class="v7-real__bar"><i aria-hidden="true"></i>%s</div>' % (i, t["bar"]),
      '%s    <button type="button" class="v7-real__shot"' % i,
      '%s            data-peek-src="%s/%s"' % (i, pre, SHOT),
      '%s            data-peek-bar="%s"' % (i, t["bar"]),
      '%s            data-peek-alt="%s"' % (i, t["alt"].replace('"', "&quot;")),
      '%s            data-peek-cap="%s">' % (i, cap),
      '%s        <img src="%s/%s" alt="%s" loading="lazy" decoding="async">' % (i, pre, SHOT, t["alt"]),
      '%s    </button>' % i,
      '%s    <figcaption class="v7-real__cap">%s</figcaption>' % (i, t["cap"]),
      '%s</figure>' % i,
    ])

def apply(lang, path):
    s = open(path, encoding="utf-8").read()
    if "v7-real" in s:
        print("   juz jest:", path); return
    # 1) przelacznik w pasku, za przyciskiem kroku
    m = re.search(r'(\n *<p class="v7-hint" data-exhibit-hint)', s)
    assert m, path
    s = s[:m.start(1)] + "\n" + switch(lang) + s[m.start(1):]
    # 2) podpowiedz dla widoku zrzutu
    s = s.replace('data-hint-synced="', 'data-hint-real="%s"\n                       data-hint-synced="' % T[lang]["hint"].replace('"', "&quot;"), 1)
    # 3) kadr tuz po scenie
    anchor = '                <div class="v7-exhibit__foot">'
    assert anchor in s, path + " (nie znaleziono stopki eksponatu)"
    s = s.replace(anchor, figure(lang) + "\n\n" + anchor, 1)
    # 4) skrypt lightboxa
    if "product-peek.js" not in s:
        pre = "assets" if lang == "en" else "../assets"
        s = s.replace("</body>", '    <script src="%s/js/product-peek.js?v=20260918"></script>\n</body>' % pre, 1)
    open(path, "w", encoding="utf-8").write(s)
    print("   ok", path)

if __name__ == "__main__":
    for lang, d in (("en",""), ("pl","pl/"), ("de","de/"), ("es","es/")):
        print("---", lang)
        apply(lang, d + "index.html")
