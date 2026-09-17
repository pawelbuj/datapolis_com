#!/usr/bin/env python3
"""Generator kolumn stopki dla wszystkich czterech jezykow naraz.

    python3 tools/build-footer.py && python3 tools/build-includes.py

Zrodlem prawdy jest tabela w tym pliku, nie includes/*.html —
dzieki temu EN/PL/DE/ES nie moga sie rozjechac.
"""
import re, os

def cols(lang):
    L = lambda en, pl, de, es: {"en": en, "pl": pl, "de": de, "es": es}[lang]
    ac = "app-creator.html"
    return [
      (L("Platform","Platforma","Plattform","Plataforma"), [
        ("platform-2to2.html", L("Platform overview","Przegląd platformy","Plattform im Überblick","Visión general")),
        (ac,                   L("App Creator","App Creator","App Creator","App Creator")),
        ("process-apps.html",  L("Process Apps","Aplikacje procesowe","Prozess-Apps","Aplicaciones de proceso")),
        ("orchestration-engine.html", L("Orchestration Engine","Silnik orkiestracji","Orchestrierungs-Engine","Motor de orquestación")),
        ("security-governance.html",  L("Security &amp; Governance","Bezpieczeństwo i nadzór","Sicherheit &amp; Governance","Seguridad y gobierno")),
      ]),
      (L("Digital Workers","Digital Workers","Digital Workers","Digital Workers"), [
        ("digital-workers.html", L("Digital Workers","Digital Workers","Digital Workers","Digital Workers")),
        ("humans-agents.html",   L("Humans + Digital Workers","Ludzie i Digital Workers","Menschen + Digital Workers","Personas + Digital Workers")),
        ("why-not-copilots.html",L("Why not copilots","Dlaczego nie copiloty","Warum keine Copilots","Por qué no copilotos")),
      ]),
      (L("Customers","Klienci","Kunden","Clientes"), [
        ("how-it-works-overview.html", L("How work runs","Jak przebiega praca","Wie die Arbeit läuft","Cómo funciona el trabajo")),
        ("customers.html", L("Customers","Klienci","Kunden","Clientes")),
        ("pilot-scale.html", L("Pilot → Scale","Pilotaż → skala","Pilot → Skalierung","Piloto → Escala")),
      ]),
      (L("Company","Firma","Unternehmen","Empresa"), [
        ("about.html",   L("About Datapolis","O Datapolis","Über Datapolis","Sobre Datapolis")),
        ("contact.html", L("Contact","Kontakt","Kontakt","Contacto")),
        ("legal.html",   L("Privacy Policy","Polityka prywatności","Datenschutz","Política de privacidad")),
        ("legal.html",   L("Terms of Service","Regulamin","Nutzungsbedingungen","Términos del servicio")),
      ]),
    ]

def render(lang):
    out = ['            <div class="footer__columns">']
    for label, items in cols(lang):
        out += ['                <div class="footer__column">',
                '                    <div class="footer__label">%s</div>' % label,
                '                    <nav class="footer__nav">',
                '                        <ul class="footer__list">']
        for href, title in items:
            out.append('                            <li><a href="%s">%s</a></li>' % (href, title))
        out += ['                        </ul>', '                    </nav>', '                </div>', '']
    out.append('            </div>')
    return "\n".join(out)

for lang, d in (("en","includes"), ("pl","pl/includes"), ("de","de/includes"), ("es","es/includes")):
    p = os.path.join(d, "footer.html")
    s = open(p, encoding="utf-8").read()
    pat = re.compile(r'            <div class="footer__columns">.*?\n            </div>', re.S)
    assert pat.search(s), "nie znaleziono kolumn stopki w " + p
    s2 = pat.sub(lambda _m: render(lang), s, count=1)
    open(p, "w", encoding="utf-8").write(s2)
    print("ok", p, "(bez zmian)" if s2 == s else "")
