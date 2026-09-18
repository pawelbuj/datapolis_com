# -*- coding: utf-8 -*-
"""Podmienia sekcję „Privacy Policy" w legal.html we wszystkich czterech językach.

    python3 tools/i18n/legal_privacy.py

Treść opisuje to, co serwis FAKTYCZNIE robi — każdy wymieniony skrypt, plik
i odbiorca danych jest w kodzie strony. Przy zmianie skryptów na stronie
(analityka, osadzone formularze, fonty) trzeba wrócić tutaj i poprawić,
inaczej polityka zacznie kłamać.

Stan na 18.09.2026: GA4 G-41L2VC300P za zgodą, baner zapisujący wybór
w localStorage (dp-consent), formularz www-contacts osadzony z 2to2.ai,
fonty Google z CDN, hosting Vercel.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.join(ROOT, "datapolis_com") if not os.path.exists(os.path.join(ROOT, "legal.html")) else ROOT

H4 = '<h4 style="color: white; margin: 30px 0 15px;">{}</h4>'
P = '<p style="margin-bottom: 15px;">{}</p>'
UL = ('<ul style="margin: 0 0 15px 20px; padding: 0;">{}</ul>')
LI = '<li style="margin-bottom: 8px;">{}</li>'

T = {}

T["en"] = {
    "title": "Privacy Policy",
    "intro": "This policy describes what happens to your data when you visit datapolis.com. It covers this website only — not the 2to2 platform, which has its own terms agreed with each customer.",
    "sections": [
        ("Who is responsible", [
            ("p", "The controller of your personal data is <strong>Datapolis Sp. z o.o.</strong>, ul. Dzielna 21/121a, 01-029 Warsaw, Poland (KRS 0000003324, NIP 5272336739). In any matter concerning your data, write to <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
        ]),
        ("What we collect, and why", [
            ("p", "<strong>Contact form.</strong> Name, e-mail address, company and the content of your message. We use them to answer you and, if it leads somewhere, to carry on the conversation. Legal basis: our legitimate interest in responding to enquiries addressed to us, and steps taken at your request before entering into a contract (Art. 6(1)(f) and 6(1)(b) GDPR). Providing the data is voluntary, but without it we cannot reply."),
            ("p", "<strong>Server logs.</strong> Our hosting provider records the IP address, browser identifier, time and address of each request. We use this to keep the site running and to detect abuse. Legal basis: legitimate interest in the security and reliability of the service (Art. 6(1)(f) GDPR)."),
            ("p", "<strong>Analytics.</strong> If you agree, Google Analytics records which pages you read, how you arrived, approximate location derived from a truncated IP address, and a random identifier stored in your browser. We use it to see which pages are worth writing. Legal basis: your consent (Art. 6(1)(a) GDPR), which you may withdraw at any time. We do not run advertising, remarketing or social-media tracking pixels, and advertising features in Google Analytics are switched off."),
        ]),
        ("Cookies and local storage", [
            ("p", "Until you click “I agree” in the banner, <strong>no analytics cookies are set</strong>. This is enforced technically: consent defaults are sent to Google before the analytics script loads."),
            ("ul", [
                "<strong>_ga, _ga_41L2VC300P</strong> — Google Analytics, distinguish visitors, expire after 2 years. Set only after your consent.",
                "<strong>dp-consent</strong> — not a cookie but an entry in your browser's local storage, holding your answer to the banner so we stop asking. Necessary for the banner to work; kept until you clear your browser data.",
            ]),
            ("p", "To withdraw consent, clear this site's data in your browser settings; the banner will appear again on your next visit."),
        ]),
        ("Who else processes this data", [
            ("ul", [
                "<strong>Vercel Inc.</strong> — hosting of this website and server logs.",
                "<strong>Google Ireland Limited / Google LLC</strong> — Google Analytics, and Google Fonts, which loads typefaces from Google servers. Loading a font transmits your IP address to Google. This happens on every page, before any consent, because the fonts are part of the page layout.",
                "<strong>Datapolis Sp. z o.o.</strong> — the contact form is served from our own 2to2 platform; submissions land in our own systems.",
            ]),
            ("p", "Some of these providers are established outside the European Economic Area or process data there. Such transfers are based on the European Commission's standard contractual clauses."),
        ]),
        ("How long we keep it", [
            ("p", "Correspondence and form submissions: for the duration of the conversation and afterwards for as long as we may need to demonstrate what was agreed, no longer than six years. Server logs: up to 12 months. Analytics data: 14 months, the retention period set in Google Analytics."),
        ]),
        ("Your rights", [
            ("p", "You have the right to access your data and receive a copy, to have it corrected or erased, to restrict or object to its processing, and to receive it in a portable format. Where processing is based on consent, you may withdraw it at any time without affecting the lawfulness of what was done before. Write to <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
            ("p", "If you believe we are handling your data improperly, you may lodge a complaint with the President of the Personal Data Protection Office (Prezes Urzędu Ochrony Danych Osobowych), ul. Stawki 2, 00-193 Warsaw."),
            ("p", "We do not make automated decisions about you and we do not profile you."),
        ]),
    ],
    "updated": "Last updated: 18 September 2026",
}

T["pl"] = {
    "title": "Polityka prywatności",
    "intro": "Ta polityka opisuje, co dzieje się z Twoimi danymi, gdy odwiedzasz datapolis.com. Dotyczy wyłącznie tej strony — nie platformy 2to2, która ma własne warunki uzgadniane z każdym klientem.",
    "sections": [
        ("Kto odpowiada za dane", [
            ("p", "Administratorem Twoich danych osobowych jest <strong>Datapolis Sp. z o.o.</strong>, ul. Dzielna 21/121a, 01-029 Warszawa (KRS 0000003324, NIP 5272336739). W każdej sprawie dotyczącej danych pisz na <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
        ]),
        ("Co zbieramy i po co", [
            ("p", "<strong>Formularz kontaktowy.</strong> Imię, adres e-mail, nazwa firmy i treść wiadomości. Używamy ich, żeby Ci odpowiedzieć, a jeśli rozmowa się rozwinie — żeby ją prowadzić dalej. Podstawa prawna: nasz prawnie uzasadniony interes w odpowiadaniu na kierowane do nas zapytania oraz działania podejmowane na Twoje żądanie przed zawarciem umowy (art. 6 ust. 1 lit. f oraz lit. b RODO). Podanie danych jest dobrowolne, ale bez nich nie mamy jak odpisać."),
            ("p", "<strong>Logi serwera.</strong> Dostawca hostingu zapisuje adres IP, identyfikator przeglądarki, czas i adres każdego żądania. Służy to utrzymaniu strony i wykrywaniu nadużyć. Podstawa prawna: prawnie uzasadniony interes w bezpieczeństwie i niezawodności serwisu (art. 6 ust. 1 lit. f RODO)."),
            ("p", "<strong>Analityka.</strong> Jeśli wyrazisz zgodę, Google Analytics zapisuje, które strony czytasz, skąd przyszedłeś, przybliżoną lokalizację wyliczoną ze skróconego adresu IP oraz losowy identyfikator przechowywany w Twojej przeglądarce. Wykorzystujemy to, żeby wiedzieć, o czym warto pisać. Podstawa prawna: Twoja zgoda (art. 6 ust. 1 lit. a RODO), którą możesz w każdej chwili wycofać. Nie prowadzimy reklamy, remarketingu ani pikseli śledzących z mediów społecznościowych, a funkcje reklamowe w Google Analytics są wyłączone."),
        ]),
        ("Ciasteczka i pamięć przeglądarki", [
            ("p", "Dopóki nie klikniesz „Zgadzam się” w banerze, <strong>żadne ciasteczka analityczne nie są zapisywane</strong>. Jest to wymuszone technicznie: domyślne odmowy trafiają do Google, zanim załaduje się skrypt analityczny."),
            ("ul", [
                "<strong>_ga, _ga_41L2VC300P</strong> — Google Analytics, odróżniają odwiedzających, wygasają po 2 latach. Zapisywane dopiero po Twojej zgodzie.",
                "<strong>dp-consent</strong> — nie ciasteczko, lecz wpis w pamięci lokalnej przeglądarki, przechowujący Twoją odpowiedź na baner, żebyśmy przestali pytać. Niezbędny do działania baneru; zostaje do czasu wyczyszczenia danych przeglądarki.",
            ]),
            ("p", "Żeby wycofać zgodę, wyczyść dane tej witryny w ustawieniach przeglądarki — baner pojawi się przy następnej wizycie."),
        ]),
        ("Kto jeszcze przetwarza te dane", [
            ("ul", [
                "<strong>Vercel Inc.</strong> — hosting tej strony i logi serwera.",
                "<strong>Google Ireland Limited / Google LLC</strong> — Google Analytics oraz Google Fonts, czyli kroje pisma ładowane z serwerów Google. Pobranie fontu przekazuje Google Twój adres IP. Dzieje się to na każdej stronie, przed jakąkolwiek zgodą, ponieważ fonty są częścią układu strony.",
                "<strong>Datapolis Sp. z o.o.</strong> — formularz kontaktowy jest osadzony z naszej własnej platformy 2to2; zgłoszenia trafiają do naszych systemów.",
            ]),
            ("p", "Część z tych podmiotów ma siedzibę poza Europejskim Obszarem Gospodarczym albo tam przetwarza dane. Takie przekazywanie opiera się na standardowych klauzulach umownych Komisji Europejskiej."),
        ]),
        ("Jak długo przechowujemy", [
            ("p", "Korespondencja i zgłoszenia z formularza: przez czas rozmowy, a potem tak długo, jak możemy potrzebować wykazać, co zostało ustalone — nie dłużej niż sześć lat. Logi serwera: do 12 miesięcy. Dane analityczne: 14 miesięcy, zgodnie z okresem ustawionym w Google Analytics."),
        ]),
        ("Twoje prawa", [
            ("p", "Masz prawo dostępu do swoich danych i otrzymania ich kopii, sprostowania ich, usunięcia, ograniczenia przetwarzania, wniesienia sprzeciwu wobec przetwarzania oraz przeniesienia danych. Tam, gdzie podstawą jest zgoda, możesz ją wycofać w każdej chwili — nie wpływa to na zgodność z prawem tego, co zrobiliśmy wcześniej. Pisz na <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
            ("p", "Jeśli uważasz, że przetwarzamy Twoje dane niewłaściwie, możesz wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych, ul. Stawki 2, 00-193 Warszawa."),
            ("p", "Nie podejmujemy wobec Ciebie decyzji w sposób zautomatyzowany i nie profilujemy Cię."),
        ]),
    ],
    "updated": "Ostatnia aktualizacja: 18 września 2026",
}

T["de"] = {
    "title": "Datenschutzerklärung",
    "intro": "Diese Erklärung beschreibt, was mit Ihren Daten geschieht, wenn Sie datapolis.com besuchen. Sie gilt ausschließlich für diese Website — nicht für die Plattform 2to2, für die eigene, mit jedem Kunden vereinbarte Bedingungen gelten.",
    "sections": [
        ("Wer verantwortlich ist", [
            ("p", "Verantwortlich für Ihre personenbezogenen Daten ist <strong>Datapolis Sp. z o.o.</strong>, ul. Dzielna 21/121a, 01-029 Warschau, Polen (KRS 0000003324, NIP 5272336739). In allen Fragen zu Ihren Daten schreiben Sie an <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
        ]),
        ("Was wir erheben und wozu", [
            ("p", "<strong>Kontaktformular.</strong> Name, E-Mail-Adresse, Unternehmen und Inhalt Ihrer Nachricht. Wir nutzen sie, um Ihnen zu antworten und, wenn daraus etwas wird, das Gespräch fortzuführen. Rechtsgrundlage: unser berechtigtes Interesse an der Beantwortung an uns gerichteter Anfragen sowie auf Ihre Anfrage hin erfolgende vorvertragliche Maßnahmen (Art. 6 Abs. 1 lit. f und lit. b DSGVO). Die Angabe ist freiwillig, ohne sie können wir jedoch nicht antworten."),
            ("p", "<strong>Server-Logs.</strong> Unser Hosting-Anbieter protokolliert IP-Adresse, Browserkennung, Zeitpunkt und Adresse jeder Anfrage. Das dient dem Betrieb der Website und der Erkennung von Missbrauch. Rechtsgrundlage: berechtigtes Interesse an Sicherheit und Zuverlässigkeit des Dienstes (Art. 6 Abs. 1 lit. f DSGVO)."),
            ("p", "<strong>Analyse.</strong> Mit Ihrer Einwilligung erfasst Google Analytics, welche Seiten Sie lesen, wie Sie gekommen sind, einen aus der gekürzten IP-Adresse abgeleiteten ungefähren Standort sowie eine zufällige Kennung in Ihrem Browser. Wir nutzen das, um zu sehen, worüber zu schreiben sich lohnt. Rechtsgrundlage: Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO), die Sie jederzeit widerrufen können. Wir betreiben keine Werbung, kein Remarketing und keine Social-Media-Tracking-Pixel; Werbefunktionen in Google Analytics sind abgeschaltet."),
        ]),
        ("Cookies und lokaler Speicher", [
            ("p", "Solange Sie im Banner nicht auf „Einverstanden“ klicken, werden <strong>keine Analyse-Cookies gesetzt</strong>. Das ist technisch erzwungen: Die Voreinstellung „abgelehnt“ geht an Google, bevor das Analyseskript geladen wird."),
            ("ul", [
                "<strong>_ga, _ga_41L2VC300P</strong> — Google Analytics, unterscheiden Besucher, laufen nach 2 Jahren ab. Werden erst nach Ihrer Einwilligung gesetzt.",
                "<strong>dp-consent</strong> — kein Cookie, sondern ein Eintrag im lokalen Speicher Ihres Browsers mit Ihrer Antwort auf das Banner, damit wir nicht erneut fragen. Für die Funktion des Banners notwendig; bleibt, bis Sie Ihre Browserdaten löschen.",
            ]),
            ("p", "Um Ihre Einwilligung zu widerrufen, löschen Sie die Daten dieser Website in den Browsereinstellungen — beim nächsten Besuch erscheint das Banner erneut."),
        ]),
        ("Wer diese Daten außerdem verarbeitet", [
            ("ul", [
                "<strong>Vercel Inc.</strong> — Hosting dieser Website und Server-Logs.",
                "<strong>Google Ireland Limited / Google LLC</strong> — Google Analytics sowie Google Fonts, also von Google-Servern geladene Schriften. Beim Laden einer Schrift wird Ihre IP-Adresse an Google übermittelt. Das geschieht auf jeder Seite, vor jeder Einwilligung, weil die Schriften Teil des Seitenlayouts sind.",
                "<strong>Datapolis Sp. z o.o.</strong> — das Kontaktformular wird aus unserer eigenen Plattform 2to2 eingebunden; Einsendungen landen in unseren eigenen Systemen.",
            ]),
            ("p", "Einige dieser Anbieter haben ihren Sitz außerhalb des Europäischen Wirtschaftsraums oder verarbeiten dort Daten. Solche Übermittlungen stützen sich auf die Standardvertragsklauseln der Europäischen Kommission."),
        ]),
        ("Wie lange wir speichern", [
            ("p", "Korrespondenz und Formulareinsendungen: für die Dauer des Gesprächs und danach so lange, wie wir belegen können müssen, was vereinbart wurde — höchstens sechs Jahre. Server-Logs: bis zu 12 Monate. Analysedaten: 14 Monate, entsprechend der in Google Analytics eingestellten Aufbewahrungsdauer."),
        ]),
        ("Ihre Rechte", [
            ("p", "Sie haben das Recht auf Auskunft und eine Kopie Ihrer Daten, auf Berichtigung, Löschung, Einschränkung der Verarbeitung, Widerspruch gegen die Verarbeitung sowie auf Datenübertragbarkeit. Soweit die Verarbeitung auf Einwilligung beruht, können Sie diese jederzeit widerrufen; die Rechtmäßigkeit der bis dahin erfolgten Verarbeitung bleibt unberührt. Schreiben Sie an <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
            ("p", "Wenn Sie der Ansicht sind, dass wir Ihre Daten nicht ordnungsgemäß verarbeiten, können Sie sich bei der polnischen Datenschutzbehörde beschweren: Prezes Urzędu Ochrony Danych Osobowych, ul. Stawki 2, 00-193 Warschau. Ihnen steht ebenso die Beschwerde bei der für Sie zuständigen Aufsichtsbehörde offen."),
            ("p", "Wir treffen keine automatisierten Entscheidungen über Sie und erstellen kein Profil von Ihnen."),
        ]),
    ],
    "updated": "Zuletzt aktualisiert: 18. September 2026",
}

T["es"] = {
    "title": "Política de privacidad",
    "intro": "Esta política describe qué ocurre con sus datos cuando visita datapolis.com. Se refiere únicamente a este sitio web, no a la plataforma 2to2, que tiene sus propias condiciones acordadas con cada cliente.",
    "sections": [
        ("Quién es responsable", [
            ("p", "El responsable del tratamiento de sus datos personales es <strong>Datapolis Sp. z o.o.</strong>, ul. Dzielna 21/121a, 01-029 Varsovia, Polonia (KRS 0000003324, NIP 5272336739). Para cualquier asunto relacionado con sus datos, escriba a <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
        ]),
        ("Qué recogemos y para qué", [
            ("p", "<strong>Formulario de contacto.</strong> Nombre, dirección de correo electrónico, empresa y contenido de su mensaje. Los usamos para responderle y, si la conversación avanza, para continuarla. Base jurídica: nuestro interés legítimo en responder a las consultas que se nos dirigen y las actuaciones precontractuales realizadas a petición suya (art. 6.1.f y 6.1.b del RGPD). Facilitar los datos es voluntario, pero sin ellos no podemos responder."),
            ("p", "<strong>Registros del servidor.</strong> Nuestro proveedor de alojamiento registra la dirección IP, el identificador del navegador, la hora y la dirección de cada petición. Sirve para mantener el sitio en funcionamiento y detectar abusos. Base jurídica: interés legítimo en la seguridad y fiabilidad del servicio (art. 6.1.f del RGPD)."),
            ("p", "<strong>Analítica.</strong> Si da su consentimiento, Google Analytics registra qué páginas lee, cómo ha llegado, una ubicación aproximada derivada de una dirección IP truncada y un identificador aleatorio guardado en su navegador. Lo usamos para saber sobre qué merece la pena escribir. Base jurídica: su consentimiento (art. 6.1.a del RGPD), que puede retirar en cualquier momento. No hacemos publicidad, ni remarketing, ni usamos píxeles de seguimiento de redes sociales, y las funciones publicitarias de Google Analytics están desactivadas."),
        ]),
        ("Cookies y almacenamiento local", [
            ("p", "Hasta que pulse «Acepto» en el aviso, <strong>no se guarda ninguna cookie analítica</strong>. Está garantizado técnicamente: la denegación por defecto se envía a Google antes de que se cargue el script de analítica."),
            ("ul", [
                "<strong>_ga, _ga_41L2VC300P</strong> — Google Analytics, distinguen a los visitantes, caducan a los 2 años. Solo se guardan tras su consentimiento.",
                "<strong>dp-consent</strong> — no es una cookie, sino una entrada en el almacenamiento local de su navegador con su respuesta al aviso, para dejar de preguntarle. Necesaria para que el aviso funcione; permanece hasta que borre los datos del navegador.",
            ]),
            ("p", "Para retirar el consentimiento, borre los datos de este sitio en la configuración de su navegador; el aviso reaparecerá en su próxima visita."),
        ]),
        ("Quién más trata estos datos", [
            ("ul", [
                "<strong>Vercel Inc.</strong> — alojamiento de este sitio web y registros del servidor.",
                "<strong>Google Ireland Limited / Google LLC</strong> — Google Analytics y Google Fonts, es decir, tipografías cargadas desde servidores de Google. Al cargar una tipografía se transmite su dirección IP a Google. Ocurre en todas las páginas, antes de cualquier consentimiento, porque las tipografías forman parte del diseño de la página.",
                "<strong>Datapolis Sp. z o.o.</strong> — el formulario de contacto está incrustado desde nuestra propia plataforma 2to2; los envíos llegan a nuestros sistemas.",
            ]),
            ("p", "Algunos de estos proveedores están establecidos fuera del Espacio Económico Europeo o tratan datos allí. Dichas transferencias se basan en las cláusulas contractuales tipo de la Comisión Europea."),
        ]),
        ("Cuánto tiempo los conservamos", [
            ("p", "Correspondencia y envíos del formulario: mientras dure la conversación y después durante el tiempo en que podamos necesitar acreditar lo acordado, no más de seis años. Registros del servidor: hasta 12 meses. Datos analíticos: 14 meses, el periodo de conservación configurado en Google Analytics."),
        ]),
        ("Sus derechos", [
            ("p", "Tiene derecho a acceder a sus datos y obtener una copia, a rectificarlos o suprimirlos, a limitar u oponerse a su tratamiento y a recibirlos en un formato portátil. Cuando el tratamiento se base en el consentimiento, puede retirarlo en cualquier momento, sin que ello afecte a la licitud del tratamiento previo. Escriba a <a href=\"mailto:office@datapolis.com\">office@datapolis.com</a>."),
            ("p", "Si considera que tratamos sus datos de forma indebida, puede presentar una reclamación ante la autoridad polaca de protección de datos: Prezes Urzędu Ochrony Danych Osobowych, ul. Stawki 2, 00-193 Varsovia. También puede dirigirse a la autoridad de control de su país de residencia."),
            ("p", "No tomamos decisiones automatizadas sobre usted ni elaboramos perfiles."),
        ]),
    ],
    "updated": "Última actualización: 18 de septiembre de 2026",
}


def render(lang):
    d = T[lang]
    out = [
        '        <section id="privacy" class="dp-section">',
        '            <div class="dp-container">',
        f'                <h2 class="dp-subtitle" style="color: white; margin-bottom: 20px;">{d["title"]}</h2>',
        '                <div class="dp-text" style="max-width: 800px;">',
        f'                    <p style="margin-bottom: 20px;">{d["intro"]}</p>',
    ]
    for heading, blocks in d["sections"]:
        out.append("                    " + H4.format(heading))
        for kind, body in blocks:
            if kind == "p":
                out.append("                    " + P.format(body))
            else:
                items = "".join(LI.format(x) for x in body)
                out.append("                    " + UL.format(items))
    out += [
        f'                    <p style="font-size: 0.9rem; color: #64748b; margin-top: 30px;">{d["updated"]}</p>',
        "                </div>",
        "            </div>",
        "        </section>",
    ]
    return "\n".join(out)


def main():
    files = {"en": "legal.html", "pl": "pl/legal.html", "de": "de/legal.html", "es": "es/legal.html"}
    pat = re.compile(r'        <section id="privacy" class="dp-section">.*?\n        </section>', re.S)
    for lang, rel in files.items():
        path = os.path.join(ROOT, rel)
        html = open(path, encoding="utf-8").read()
        if not pat.search(html):
            sys.exit(f"{rel}: nie znalazłem sekcji id=\"privacy\"")
        new = pat.sub(lambda _m: render(lang), html, count=1)
        open(path, "w", encoding="utf-8").write(new)
        words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", render(lang))))
        print(f"{rel:18s} ~{words} słów")
    print("\nTeraz: python3 tools/build-includes.py")


if __name__ == "__main__":
    main()
