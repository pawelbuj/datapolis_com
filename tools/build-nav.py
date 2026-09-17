#!/usr/bin/env python3
"""Generator nawigacji (desktop + mobile) dla wszystkich czterech jezykow naraz.

    python3 tools/build-nav.py && python3 tools/build-includes.py

Zrodlem prawdy jest tabela w tym pliku, nie includes/*.html —
dzieki temu EN/PL/DE/ES nie moga sie rozjechac.
"""
import re, os

CHEV = ('<svg class="dp-nav__chevron" width="10" height="6" viewBox="0 0 10 6" fill="none">'
        '<path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
MCHEV = ('<svg class="dp-mobile-nav__chevron" width="12" height="7" viewBox="0 0 10 6" fill="none">'
         '<path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def AC(lang):
    return "app-creator.html"

def menu(lang):
    L = lambda en, pl, de, es: {"en": en, "pl": pl, "de": de, "es": es}[lang]
    return [
        dict(key="platform", label=L("Platform", "Platforma", "Plattform", "Plataforma"),
             intro=L("One platform: applications are built from your documentation, then run under your rules.",
                     "Jedna platforma: aplikacje powstają z Twojej dokumentacji, a potem działają według Twoich reguł.",
                     "Eine Plattform: Anwendungen entstehen aus Ihrer Dokumentation und laufen dann nach Ihren Regeln.",
                     "Una plataforma: las aplicaciones nacen de tu documentación y luego funcionan según tus reglas."),
             items=[
              ("platform-2to2.html",
               L("Platform overview", "Przegląd platformy", "Plattform im Überblick", "Visión general"),
               L("What 2to2 is and what runs on it", "Czym jest 2to2 i co na nim działa",
                 "Was 2to2 ist und was darauf läuft", "Qué es 2to2 y qué funciona sobre él")),
              (AC(lang),
               L("App Creator", "App Creator", "App Creator", "App Creator"),
               L("Turn documentation into a working application", "Zamień dokumentację w działającą aplikację",
                 "Aus Dokumentation wird eine laufende Anwendung", "Convierte la documentación en una aplicación en marcha")),
              ("process-apps.html",
               L("Process Apps", "Aplikacje procesowe", "Prozess-Apps", "Aplicaciones de proceso"),
               L("What users get: apps that carry the work", "To, co dostają użytkownicy: aplikacje, które prowadzą pracę",
                 "Was Anwender bekommen: Apps, die die Arbeit führen", "Lo que reciben los usuarios: apps que llevan el trabajo")),
              ("orchestration-engine.html",
               L("Orchestration Engine", "Silnik orkiestracji", "Orchestrierungs-Engine", "Motor de orquestación"),
               L("The state-based engine that moves work forward", "Stanowy silnik, który popycha pracę do przodu",
                 "Die zustandsbasierte Engine, die Arbeit vorantreibt", "El motor por estados que hace avanzar el trabajo")),
              ("security-governance.html",
               L("Security &amp; Governance", "Bezpieczeństwo i nadzór", "Sicherheit &amp; Governance", "Seguridad y gobierno"),
               L("Rules, roles, permissions and the audit trail", "Reguły, role, uprawnienia i ślad audytowy",
                 "Regeln, Rollen, Berechtigungen und Audit-Trail", "Reglas, roles, permisos y traza de auditoría")),
             ]),
        dict(key="workers", label=L("Digital Workers", "Digital Workers", "Digital Workers", "Digital Workers"),
             intro=L("AI executes steps inside the same processes your people work in.",
                     "AI wykonuje kroki w tych samych procesach, w których pracują Twoi ludzie.",
                     "KI führt Schritte in denselben Prozessen aus, in denen Ihre Leute arbeiten.",
                     "La IA ejecuta pasos dentro de los mismos procesos en los que trabaja tu gente."),
             items=[
              ("digital-workers.html",
               L("Digital Workers", "Digital Workers", "Digital Workers", "Digital Workers"),
               L("AI that takes a step in the process, not a chat window",
                 "AI, która wykonuje krok w procesie, a nie okno czatu",
                 "KI, die einen Schritt im Prozess übernimmt — kein Chatfenster",
                 "IA que ejecuta un paso del proceso, no una ventana de chat")),
              ("humans-agents.html",
               L("Humans + Digital Workers", "Ludzie i Digital Workers", "Menschen + Digital Workers", "Personas + Digital Workers"),
               L("One process, one audit trail, two kinds of executor",
                 "Jeden proces, jeden ślad audytowy, dwa rodzaje wykonawców",
                 "Ein Prozess, ein Audit-Trail, zwei Arten von Ausführenden",
                 "Un proceso, una traza de auditoría, dos tipos de ejecutor")),
              ("why-not-copilots.html",
               L("Why not copilots", "Dlaczego nie copiloty", "Warum keine Copilots", "Por qué no copilotos"),
               L("Where prompt-based assistants stop being enough",
                 "Gdzie asystenci na promptach przestają wystarczać",
                 "Wo prompt-basierte Assistenten nicht mehr ausreichen",
                 "Dónde dejan de bastar los asistentes basados en prompts")),
             ]),
        dict(key="howitworks", label=L("How work runs", "Jak przebiega praca", "Wie die Arbeit läuft", "Cómo funciona el trabajo"),
             link="how-it-works-overview.html"),
        dict(key="customers", label=L("Customers", "Klienci", "Kunden", "Clientes"),
             intro=L("Twenty years in production — and the path from one process to many.",
                     "20 lat na produkcji — i droga od jednego procesu do wielu.",
                     "20 Jahre im Produktivbetrieb — und der Weg vom ersten Prozess zu vielen.",
                     "20 años en producción — y el camino de un proceso a muchos."),
             items=[
              ("customers.html",
               L("Customers", "Klienci", "Kunden", "Clientes"),
               L("Who runs on Datapolis today", "Kto dziś pracuje na Datapolis",
                 "Wer heute auf Datapolis arbeitet", "Quién trabaja hoy sobre Datapolis")),
              ("pilot-scale.html",
               L("Pilot → Scale", "Pilotaż → skala", "Pilot → Skalierung", "Piloto → Escala"),
               L("From a first process to an enterprise rollout", "Od pierwszego procesu do wdrożenia w całej firmie",
                 "Vom ersten Prozess zum unternehmensweiten Rollout", "Del primer proceso al despliegue en toda la empresa")),
             ]),
        dict(key="company", label=L("Company", "Firma", "Unternehmen", "Empresa"),
             items=[
              ("about.html", L("About Datapolis", "O Datapolis", "Über Datapolis", "Sobre Datapolis"), None),
              ("contact.html", L("Contact", "Kontakt", "Kontakt", "Contacto"), None),
             ]),
    ]

def desktop(lang):
    out = ['                <ul class="dp-nav__list">']
    for g in menu(lang):
        if g.get("link"):
            out += ['                    <li class="dp-nav__item">',
                    '                        <a href="%s" class="dp-nav__link dp-nav__link--simple">%s</a>' % (g["link"], g["label"]),
                    '                    </li>', '']
            continue
        mid = "dp-menu-" + g["key"]
        out += ['                    <li class="dp-nav__item dp-nav__item--has-dropdown" data-nav="%s">' % g["key"],
                '                        <button class="dp-nav__link" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="%s">' % mid,
                '                            %s' % g["label"],
                '                            %s' % CHEV,
                '                        </button>',
                '                        <div class="dp-dropdown" id="%s" role="menu" aria-label="%s">' % (mid, re.sub("&amp;", "and", g["label"]))]
        if g.get("intro"):
            out.append('                            <p class="dp-dropdown__intro">%s</p>' % g["intro"])
        for href, title, desc in g["items"]:
            cls = "dp-dropdown__item dp-dropdown__item--with-desc" if desc else "dp-dropdown__item"
            out.append('                            <a href="%s" class="%s" role="menuitem">' % (href, cls))
            out.append('                                <span class="dp-dropdown__title">%s</span>' % title)
            if desc:
                out.append('                                <span class="dp-dropdown__desc">%s</span>' % desc)
            out.append('                            </a>')
        out += ['                        </div>', '                    </li>', '']
    out.append('                </ul>')
    return "\n".join(out)

def mobile(lang):
    out = ['                <nav class="dp-mobile-nav">']
    for g in menu(lang):
        if g.get("link"):
            out += ['                    <a href="%s" class="dp-mobile-nav__simple-link">%s</a>' % (g["link"], g["label"]), '']
            continue
        out += ['                    <div class="dp-mobile-nav__item">',
                '                        <button class="dp-mobile-nav__trigger" type="button" aria-expanded="false">',
                '                            %s' % g["label"],
                '                            %s' % MCHEV,
                '                        </button>',
                '                        <div class="dp-mobile-nav__panel">']
        for href, title, _desc in g["items"]:
            out.append('                            <a href="%s" class="dp-mobile-nav__link">%s</a>' % (href, title))
        out += ['                        </div>', '                    </div>', '']
    out.append('                </nav>')
    return "\n".join(out)

for lang, d in (("en", "includes"), ("pl", "pl/includes"), ("de", "de/includes"), ("es", "es/includes")):
    p = os.path.join(d, "header.html")
    s = open(p, encoding="utf-8").read()
    pat_d = re.compile(r'                <ul class="dp-nav__list">.*?                </ul>', re.S)
    assert pat_d.search(s), "nie znaleziono nawigacji desktop w " + p
    s2 = pat_d.sub(lambda _m: desktop(lang), s, count=1)
    pat_m = re.compile(r'                <nav class="dp-mobile-nav">.*?                </nav>', re.S)
    assert pat_m.search(s2), "nie znaleziono nawigacji mobilnej w " + p
    s3 = pat_m.sub(lambda _m: mobile(lang), s2, count=1)
    open(p, "w", encoding="utf-8").write(s3)
    print("ok", p, "(bez zmian)" if s3 == s else "")
