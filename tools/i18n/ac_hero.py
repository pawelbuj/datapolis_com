# -*- coding: utf-8 -*-
"""Hero App Creatora: trzy zakladki zamiast eksponatu .v7-extract.
   Jedno zrodlo prawdy dla EN/PL/DE/ES. Uruchamiac z katalogu repo."""
import io, re

HUMAN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7.5" r="3.5"></circle>'
         '<path d="M5.2 20c.6-4.2 2.9-6.3 6.8-6.3s6.2 2.1 6.8 6.3"></path></svg>')
BOT = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="6" width="15" height="13" rx="3"></rect>'
       '<circle cx="9.2" cy="12" r="1"></circle><circle cx="14.8" cy="12" r="1"></circle>'
       '<path d="M9 16h6M12 3v3M9.5 3h5"></path></svg>')

EDGES = [('0-1', 'M95 200 C145 200 165 296 205 296'),
         ('1-2', 'M222 296 C270 296 288 200 322 200'),
         ('2-3', 'M338 200 C386 200 402 296 438 296'),
         ('3-4', 'M442 262 C442 220 442 180 442 132'),
         ('3-5', 'M494 292 C530 292 534 232 546 210'),
         ('4-5', 'M494 100 C532 100 538 158 548 188'),
         ('2-0', 'M326 152 C326 68 250 42 180 42 C118 42 90 94 89 152')]

T = {}

T['en'] = dict(
    tabs=['Analysis documentation', 'Technical documentation', 'The application'],
    crumb1=('AppSpecification/business/', 'process-nonconformity.md', 'Business process', 'CONFIRMED', 'Revision 3'),
    crumb2=('AppSpecification/workflows/', 'workflow-spec-ncr.md', 'Workflow specification', 'CONFIRMED', 'Revision 5'),
    tree1=[('h', 'BUSINESS LAYER'), ('i', 'Brief'), ('i', 'Glossary'), ('i', 'Actors and permissions'),
           ('i', 'Domain model'), ('g', 'Business processes'), ('s', 'Nonconformity|on'), ('s', 'Actions'),
           ('s', '8D case'), ('s', 'Supplier request'), ('i', 'Use cases'), ('i', 'Screens'),
           ('i', 'Business rules'), ('i', 'Integrations')],
    tree2=[('h', 'SPECIFICATION'), ('i', 'Application specification'), ('g', 'Workflows'), ('s', '8D case'),
           ('s', 'Actions'), ('s', 'Nonconformity|on'), ('s', 'SCAR request'), ('g', 'Data tables'),
           ('s', 'Audits'), ('s', 'Cases'), ('s', 'Dispositions'), ('s', 'Evidence'), ('g', 'Pages'),
           ('s', 'Nonconformity register'), ('s', 'Quality dashboard')],
    d1_title='Business process: nonconformity handling',
    d1_h1='1. Process overview',
    d1_items=[('Process code:', 'PROC-NCR-01'),
              ('Trigger:', 'a defect or deviation found during incoming inspection, production, final inspection, a customer complaint or an audit.'),
              ('Process owner:', 'Quality Engineer'),
              ('Main entities:', 'Nonconformity, Action, Approval, Evidence, 8D case')],
    d1_h2='2. Flow',
    d1_steps=[('Step 1 — raise.', 'The originator enters the plant, line, source, part number, quantity and defect description. State: <code>Submitted</code>.'),
              ('Step 2 — verification.', 'The Quality Engineer sets the defect type and severity, and flags whether containment is required.')],
    ai_h='SUGGESTION FROM PROCEDURE QP-08',
    ai_p='§4.2 has an “effectiveness verification” step after 30 days — it is missing from this description. Add it as step 7?',
    ai_b=['Add it', 'Show in the procedure', 'Dismiss'],
    d2_title='Nonconformity',
    d2_lead='The life of one nonconformity, from the moment somebody on the floor raises it to the moment it is closed: verification, containment, the disposition and its approval, the customer concession when the part is under an OEM contract, the execution of the disposition and the decision whether a full 8D case is needed.',
    d2_h1='Roles', d2_rh=['ROLE', 'WHO HOLDS IT'],
    d2_roles=[('Originator', 'Operators, inspectors and incoming-inspection storekeepers who raise nonconformities.'),
              ('Quality Engineer', 'Verifies and classifies, carries the case; approves a disposition that is not Critical.'),
              ('Quality Manager', 'Approves a Critical severity or a Use-As-Is disposition, and records the customer concession.'),
              ('Action Owner', 'Carries out containment and the physical disposition.')],
    d2_h2='Fields', d2_fh=['FIELD', 'TYPE', 'REQ.', 'HOLDS'],
    d2_fields=[('NCR Number', 'Text', 'no', 'NCR-YYYY-nnnnn, assigned automatically.'),
               ('Title', 'Text', 'yes', 'One line saying what is wrong.'),
               ('Source', 'Choice', 'yes', 'Incoming inspection, production, final inspection, complaint, audit.'),
               ('Plant', 'Choice', 'yes', 'Mielec or Rzeszow.'),
               ('Quantity', 'Number', 'yes', 'Pieces affected by the nonconformity.')],
    subs=[('data', 'Data'), ('wf', 'Workflows'), ('pages', 'Pages')],
    map_kicker='PROCESS IN THE APPLICATION', map_case='Nonconformity NCR-2026-00184', map_running='RUNNING',
    map_aria='The nonconformity process in the finished application: states, roles and transitions.',
    cur_label='ACTIVE STATE',
    states=[('Submitted', 'Human · Originator', 'HUMAN · ORIGINATOR', 'Describe the defect, plant, part and quantity', 'human'),
            ('Triage', 'Digital · Triage', 'DIGITAL WORKER · CLASSIFICATION', 'Set the defect type and initial severity', 'digital'),
            ('Verification', 'Human · Engineer', 'HUMAN · QUALITY ENGINEER', 'Check the evidence and confirm the severity', 'human'),
            ('Disposition', 'Human · Engineer', 'HUMAN · QUALITY ENGINEER', 'Choose the disposition for the affected parts', 'human'),
            ('Approval', 'Human · Manager', 'HUMAN · QUALITY MANAGER', 'Approve a critical disposition', 'human'),
            ('Closed', 'Digital · Closure', 'DIGITAL WORKER · CLOSURE', 'Update the register and archive the case', 'digital')],
    routes=['critical', 'no approval needed', 'returned to originator'],
    wf_note='This is a <b>platform object</b> — states, transitions and roles. Not code and not a drawing in a document: this is how the process looks in the editor and how it runs in the application.',
    cols=[('NCR Number', 'Text · auto'), ('Title', 'Text · required'), ('Source', 'Choice · 5 values'),
          ('Plant', 'Choice · 2 values'), ('Quantity', 'Number'), ('Photos', 'Attachments'),
          ('Disposition', 'Relation → Dispositions')],
    data_h=['NUMBER', 'TITLE', 'PLANT', 'STATE'],
    data_rows=[('NCR-2026-00184', 'Hole diameter deviation, pos. 14', 'Mielec', 'Verification', 'b'),
               ('NCR-2026-00183', 'Material certificate missing', 'Rzeszow', 'Closed', ''),
               ('NCR-2026-00182', 'Coating damaged in transport', 'Mielec', 'Disposition', 'b'),
               ('NCR-2026-00181', 'Torque out of specification', 'Mielec', 'Closed', '')],
    data_note='A table of <b>typed fields and relations</b> — defined in the editor, not in database migrations.',
    page_title='Nonconformity register',
    page_filters=['Plant: all', 'State: open', 'My cases'],
    page_h=['NUMBER', 'TITLE', 'OWNER', 'DUE'],
    page_rows=[('NCR-2026-00184', 'Hole diameter deviation, pos. 14', 'A. Nowak', 'in 2 days'),
               ('NCR-2026-00182', 'Coating damaged in transport', 'M. Zajac', 'today'),
               ('NCR-2026-00179', 'Flange dimension out of tolerance', 'A. Nowak', 'in 5 days')],
    page_cols=[('Nonconformity register', 'List · visible to everyone'), ('Quality dashboard', 'Metrics · management'),
               ('Action schedule', 'Calendar · action owners')],
    page_note='Pages are <b>views over the processes</b> — columns, filters and access set in the editor.',
)

T['pl'] = dict(
    tabs=['Dokumentacja analityczna', 'Dokumentacja techniczna', 'Aplikacja'],
    crumb1=('AppSpecification/business/', 'proces-niezgodnosc.md', 'Proces biznesowy', 'ZATWIERDZONY', 'Wersja 3'),
    crumb2=('AppSpecification/workflows/', 'workflow-spec-ncr.md', 'Specyfikacja procesu', 'ZATWIERDZONY', 'Wersja 5'),
    tree1=[('h', 'WARSTWA BIZNESOWA'), ('i', 'Brief'), ('i', 'Słownik pojęć'), ('i', 'Aktorzy i uprawnienia'),
           ('i', 'Model dziedziny'), ('g', 'Procesy biznesowe'), ('s', 'Niezgodność|on'), ('s', 'Akcje'),
           ('s', 'Sprawa 8D'), ('s', 'Zgłoszenie do dostawcy'), ('i', 'Przypadki użycia'), ('i', 'Ekrany'),
           ('i', 'Reguły biznesowe'), ('i', 'Integracje')],
    tree2=[('h', 'SPECYFIKACJA'), ('i', 'Specyfikacja aplikacji'), ('g', 'Procesy'), ('s', 'Sprawa 8D'),
           ('s', 'Akcje'), ('s', 'Niezgodność|on'), ('s', 'Zgłoszenie SCAR'), ('g', 'Tabele danych'),
           ('s', 'Audyty'), ('s', 'Sprawy'), ('s', 'Dyspozycje'), ('s', 'Dowody'), ('g', 'Strony'),
           ('s', 'Rejestr niezgodności'), ('s', 'Pulpit jakości')],
    d1_title='Proces biznesowy: obsługa niezgodności',
    d1_h1='1. Przegląd procesu',
    d1_items=[('Kod procesu:', 'PROC-NCR-01'),
              ('Wyzwalacz:', 'wykrycie wady lub odchylenia podczas kontroli wejściowej, produkcji, kontroli końcowej, reklamacji klienta albo audytu.'),
              ('Właściciel procesu:', 'inżynier jakości'),
              ('Główne encje:', 'Niezgodność, Akcja, Zatwierdzenie, Dowód, Sprawa 8D')],
    d1_h2='2. Przebieg',
    d1_steps=[('Krok 1 — zgłoszenie.', 'Zgłaszający wprowadza zakład, linię, źródło, numer części, ilość i opis wady. Stan: <code>Zgłoszona</code>.'),
              ('Krok 2 — weryfikacja.', 'Inżynier jakości nadaje typ wady i istotność, oznacza konieczność zabezpieczenia.')],
    ai_h='PROPOZYCJA NA PODSTAWIE PROCEDURY QP-08',
    ai_p='W §4.2 jest krok „weryfikacja skuteczności działań” po 30 dniach — nie ma go w opisie. Dopisać jako krok 7?',
    ai_b=['Dopisz', 'Pokaż w procedurze', 'Odrzuć'],
    d2_title='Niezgodność',
    d2_lead='Życie jednej niezgodności — od zgłoszenia na hali do zamknięcia: weryfikacja, zabezpieczenie, dyspozycja i jej zatwierdzenie, zgoda klienta przy częściach objętych kontraktem OEM, wykonanie dyspozycji i decyzja, czy potrzebna jest pełna sprawa 8D.',
    d2_h1='Role', d2_rh=['ROLA', 'KTO JĄ PEŁNI'],
    d2_roles=[('Zgłaszający', 'Operatorzy, kontrolerzy i magazynierzy kontroli wejściowej.'),
              ('Inżynier jakości', 'Weryfikuje i klasyfikuje, prowadzi sprawę; zatwierdza dyspozycję inną niż krytyczna.'),
              ('Kierownik jakości', 'Zatwierdza istotność krytyczną i dyspozycję „użyj jak jest”; zapisuje zgodę klienta.'),
              ('Wykonawca akcji', 'Realizuje zabezpieczenie i fizyczną dyspozycję.')],
    d2_h2='Pola', d2_fh=['POLE', 'TYP', 'WYM.', 'CO PRZECHOWUJE'],
    d2_fields=[('Numer NCR', 'Tekst', 'nie', 'NCR-RRRR-nnnnn, nadawany automatycznie.'),
               ('Tytuł', 'Tekst', 'tak', 'Jedno zdanie: co jest nie tak.'),
               ('Źródło', 'Wybór', 'tak', 'Kontrola wejściowa, produkcja, kontrola końcowa, reklamacja, audyt.'),
               ('Zakład', 'Wybór', 'tak', 'Mielec albo Rzeszów.'),
               ('Ilość', 'Liczba', 'tak', 'Sztuki objęte niezgodnością.')],
    subs=[('data', 'Dane'), ('wf', 'Workflowy'), ('pages', 'Strony')],
    map_kicker='PROCES W APLIKACJI', map_case='Niezgodność NCR-2026-00184', map_running='DZIAŁA',
    map_aria='Proces niezgodności w gotowej aplikacji: stany, role i przejścia.',
    cur_label='AKTYWNY STAN',
    states=[('Zgłoszona', 'Człowiek · Zgłaszający', 'CZŁOWIEK · ZGŁASZAJĄCY', 'Opisz wadę, zakład, część i ilość', 'human'),
            ('Klasyfikacja', 'Digital · Klasyfikacja', 'DIGITAL WORKER · KLASYFIKACJA', 'Nadaj typ wady i wstępną istotność', 'digital'),
            ('W weryfikacji', 'Człowiek · Inżynier', 'CZŁOWIEK · INŻYNIER JAKOŚCI', 'Sprawdź dowody i potwierdź istotność', 'human'),
            ('Dyspozycja', 'Człowiek · Inżynier', 'CZŁOWIEK · INŻYNIER JAKOŚCI', 'Wybierz dyspozycję dla wadliwych sztuk', 'human'),
            ('Akceptacja', 'Człowiek · Kierownik', 'CZŁOWIEK · KIEROWNIK JAKOŚCI', 'Zatwierdź dyspozycję krytyczną', 'human'),
            ('Zamknięta', 'Digital · Zamknięcie', 'DIGITAL WORKER · ZAMKNIĘCIE', 'Uzupełnij rejestr i zarchiwizuj sprawę', 'digital')],
    routes=['krytyczna', 'bez zatwierdzenia', 'zwrot do zgłaszającego'],
    wf_note='To jest <b>obiekt platformy</b> — stany, przejścia i role. Nie kod i nie rysunek w dokumencie: tak wygląda proces w edytorze i tak działa w aplikacji.',
    cols=[('Numer NCR', 'Tekst · auto'), ('Tytuł', 'Tekst · wymagane'), ('Źródło', 'Wybór · 5 wartości'),
          ('Zakład', 'Wybór · 2 wartości'), ('Ilość', 'Liczba'), ('Zdjęcia', 'Załączniki'),
          ('Dyspozycja', 'Relacja → Dyspozycje')],
    data_h=['NUMER', 'TYTUŁ', 'ZAKŁAD', 'STAN'],
    data_rows=[('NCR-2026-00184', 'Odchyłka średnicy otworu, poz. 14', 'Mielec', 'W weryfikacji', 'b'),
               ('NCR-2026-00183', 'Brak świadectwa materiału', 'Rzeszów', 'Zamknięta', ''),
               ('NCR-2026-00182', 'Uszkodzenie powłoki w transporcie', 'Mielec', 'Dyspozycja', 'b'),
               ('NCR-2026-00181', 'Niezgodny moment dokręcenia', 'Mielec', 'Zamknięta', '')],
    data_note='Tabela z <b>typowanymi polami i relacjami</b> — definiowana w edytorze, nie w migracjach bazy.',
    page_title='Rejestr niezgodności',
    page_filters=['Zakład: wszystkie', 'Stan: otwarte', 'Moje sprawy'],
    page_h=['NUMER', 'TYTUŁ', 'OSOBA', 'TERMIN'],
    page_rows=[('NCR-2026-00184', 'Odchyłka średnicy otworu, poz. 14', 'A. Nowak', 'za 2 dni'),
               ('NCR-2026-00182', 'Uszkodzenie powłoki w transporcie', 'M. Zając', 'dziś'),
               ('NCR-2026-00179', 'Niezgodność wymiaru kołnierza', 'A. Nowak', 'za 5 dni')],
    page_cols=[('Rejestr niezgodności', 'Lista · widoczna dla wszystkich'), ('Pulpit jakości', 'Wskaźniki · kierownictwo'),
               ('Harmonogram akcji', 'Kalendarz · wykonawcy')],
    page_note='Strony to <b>widoki nad procesami</b> — kolumny, filtry i dostęp ustawiane w edytorze.',
)

T['de'] = dict(
    tabs=['Fachliche Dokumentation', 'Technische Dokumentation', 'Die Anwendung'],
    crumb1=('AppSpecification/business/', 'prozess-abweichung.md', 'Geschäftsprozess', 'FREIGEGEBEN', 'Revision 3'),
    crumb2=('AppSpecification/workflows/', 'workflow-spec-ncr.md', 'Prozessspezifikation', 'FREIGEGEBEN', 'Revision 5'),
    tree1=[('h', 'FACHLICHE EBENE'), ('i', 'Brief'), ('i', 'Glossar'), ('i', 'Akteure und Berechtigungen'),
           ('i', 'Domänenmodell'), ('g', 'Geschäftsprozesse'), ('s', 'Abweichung|on'), ('s', 'Maßnahmen'),
           ('s', '8D-Fall'), ('s', 'Lieferantenmeldung'), ('i', 'Anwendungsfälle'), ('i', 'Screens'),
           ('i', 'Geschäftsregeln'), ('i', 'Integrationen')],
    tree2=[('h', 'SPEZIFIKATION'), ('i', 'Anwendungsspezifikation'), ('g', 'Prozesse'), ('s', '8D-Fall'),
           ('s', 'Maßnahmen'), ('s', 'Abweichung|on'), ('s', 'SCAR-Meldung'), ('g', 'Datentabellen'),
           ('s', 'Audits'), ('s', 'Fälle'), ('s', 'Dispositionen'), ('s', 'Nachweise'), ('g', 'Seiten'),
           ('s', 'Abweichungsregister'), ('s', 'Qualitäts-Dashboard')],
    d1_title='Geschäftsprozess: Bearbeitung von Abweichungen',
    d1_h1='1. Prozessübersicht',
    d1_items=[('Prozesscode:', 'PROC-NCR-01'),
              ('Auslöser:', 'ein Fehler oder eine Abweichung, festgestellt bei Wareneingangsprüfung, Produktion, Endprüfung, Kundenreklamation oder Audit.'),
              ('Prozessverantwortlicher:', 'Qualitätsingenieur'),
              ('Hauptentitäten:', 'Abweichung, Maßnahme, Freigabe, Nachweis, 8D-Fall')],
    d1_h2='2. Ablauf',
    d1_steps=[('Schritt 1 — Meldung.', 'Der Melder erfasst Werk, Linie, Quelle, Teilenummer, Menge und Fehlerbeschreibung. Zustand: <code>Gemeldet</code>.'),
              ('Schritt 2 — Prüfung.', 'Der Qualitätsingenieur setzt Fehlerart und Schweregrad und markiert, ob eine Sofortmaßnahme nötig ist.')],
    ai_h='VORSCHLAG AUS DER VERFAHRENSANWEISUNG QP-08',
    ai_p='In §4.2 gibt es einen Schritt „Wirksamkeitsprüfung“ nach 30 Tagen — er fehlt in dieser Beschreibung. Als Schritt 7 ergänzen?',
    ai_b=['Ergänzen', 'In der Anweisung zeigen', 'Verwerfen'],
    d2_title='Abweichung',
    d2_lead='Das Leben einer Abweichung — von der Meldung in der Fertigung bis zum Abschluss: Prüfung, Sofortmaßnahme, Disposition und deren Freigabe, Kundenzugeständnis bei Teilen unter OEM-Vertrag, Ausführung der Disposition und die Entscheidung, ob ein vollständiger 8D-Fall nötig ist.',
    d2_h1='Rollen', d2_rh=['ROLLE', 'WER SIE INNEHAT'],
    d2_roles=[('Melder', 'Werker, Prüfer und Lageristen der Wareneingangsprüfung.'),
              ('Qualitätsingenieur', 'Prüft und klassifiziert, führt den Fall; gibt eine nicht kritische Disposition frei.'),
              ('Qualitätsmanager', 'Gibt kritischen Schweregrad und „Use-As-Is“ frei und erfasst das Kundenzugeständnis.'),
              ('Maßnahmenverantwortlicher', 'Führt Sofortmaßnahme und physische Disposition aus.')],
    d2_h2='Felder', d2_fh=['FELD', 'TYP', 'PFLICHT', 'INHALT'],
    d2_fields=[('NCR-Nummer', 'Text', 'nein', 'NCR-JJJJ-nnnnn, automatisch vergeben.'),
               ('Titel', 'Text', 'ja', 'Ein Satz: was nicht stimmt.'),
               ('Quelle', 'Auswahl', 'ja', 'Wareneingang, Produktion, Endprüfung, Reklamation, Audit.'),
               ('Werk', 'Auswahl', 'ja', 'Mielec oder Rzeszów.'),
               ('Menge', 'Zahl', 'ja', 'Betroffene Stückzahl.')],
    subs=[('data', 'Daten'), ('wf', 'Workflows'), ('pages', 'Seiten')],
    map_kicker='PROZESS IN DER ANWENDUNG', map_case='Abweichung NCR-2026-00184', map_running='LÄUFT',
    map_aria='Der Abweichungsprozess in der fertigen Anwendung: Zustände, Rollen und Übergänge.',
    cur_label='AKTIVER ZUSTAND',
    states=[('Gemeldet', 'Mensch · Melder', 'MENSCH · MELDER', 'Fehler, Werk, Teil und Menge beschreiben', 'human'),
            ('Einstufung', 'Digital · Triage', 'DIGITAL WORKER · KLASSIFIZIERUNG', 'Fehlerart und ersten Schweregrad setzen', 'digital'),
            ('In Prüfung', 'Mensch · Ingenieur', 'MENSCH · QUALITÄTSINGENIEUR', 'Nachweise prüfen und Schweregrad bestätigen', 'human'),
            ('Disposition', 'Mensch · Ingenieur', 'MENSCH · QUALITÄTSINGENIEUR', 'Disposition für die betroffenen Teile wählen', 'human'),
            ('Freigabe', 'Mensch · Manager', 'MENSCH · QUALITÄTSMANAGER', 'Kritische Disposition freigeben', 'human'),
            ('Geschlossen', 'Digital · Abschluss', 'DIGITAL WORKER · ABSCHLUSS', 'Register ergänzen und Fall archivieren', 'digital')],
    routes=['kritisch', 'ohne Freigabe', 'zurück an Melder'],
    wf_note='Das ist ein <b>Objekt der Plattform</b> — Zustände, Übergänge und Rollen. Kein Code und keine Zeichnung im Dokument: So sieht der Prozess im Editor aus und so läuft er in der Anwendung.',
    cols=[('NCR-Nummer', 'Text · auto'), ('Titel', 'Text · Pflicht'), ('Quelle', 'Auswahl · 5 Werte'),
          ('Werk', 'Auswahl · 2 Werte'), ('Menge', 'Zahl'), ('Fotos', 'Anhänge'),
          ('Disposition', 'Relation → Dispositionen')],
    data_h=['NUMMER', 'TITEL', 'WERK', 'ZUSTAND'],
    data_rows=[('NCR-2026-00184', 'Bohrungsdurchmesser abweichend, Pos. 14', 'Mielec', 'In Prüfung', 'b'),
               ('NCR-2026-00183', 'Werkszeugnis fehlt', 'Rzeszów', 'Geschlossen', ''),
               ('NCR-2026-00182', 'Beschichtung im Transport beschädigt', 'Mielec', 'Disposition', 'b'),
               ('NCR-2026-00181', 'Anzugsmoment außerhalb der Spezifikation', 'Mielec', 'Geschlossen', '')],
    data_note='Eine Tabelle mit <b>typisierten Feldern und Relationen</b> — im Editor definiert, nicht in Datenbankmigrationen.',
    page_title='Abweichungsregister',
    page_filters=['Werk: alle', 'Zustand: offen', 'Meine Fälle'],
    page_h=['NUMMER', 'TITEL', 'PERSON', 'FRIST'],
    page_rows=[('NCR-2026-00184', 'Bohrungsdurchmesser abweichend, Pos. 14', 'A. Nowak', 'in 2 Tagen'),
               ('NCR-2026-00182', 'Beschichtung im Transport beschädigt', 'M. Zajac', 'heute'),
               ('NCR-2026-00179', 'Flanschmaß außerhalb der Toleranz', 'A. Nowak', 'in 5 Tagen')],
    page_cols=[('Abweichungsregister', 'Liste · für alle sichtbar'), ('Qualitäts-Dashboard', 'Kennzahlen · Leitung'),
               ('Maßnahmenplan', 'Kalender · Verantwortliche')],
    page_note='Seiten sind <b>Sichten auf die Prozesse</b> — Spalten, Filter und Zugriff im Editor gesetzt.',
)

T['es'] = dict(
    tabs=['Documentación de análisis', 'Documentación técnica', 'La aplicación'],
    crumb1=('AppSpecification/business/', 'proceso-no-conformidad.md', 'Proceso de negocio', 'CONFIRMADO', 'Revisión 3'),
    crumb2=('AppSpecification/workflows/', 'workflow-spec-ncr.md', 'Especificación de proceso', 'CONFIRMADO', 'Revisión 5'),
    tree1=[('h', 'CAPA DE NEGOCIO'), ('i', 'Brief'), ('i', 'Glosario'), ('i', 'Actores y permisos'),
           ('i', 'Modelo de dominio'), ('g', 'Procesos de negocio'), ('s', 'No conformidad|on'), ('s', 'Acciones'),
           ('s', 'Caso 8D'), ('s', 'Aviso a proveedor'), ('i', 'Casos de uso'), ('i', 'Pantallas'),
           ('i', 'Reglas de negocio'), ('i', 'Integraciones')],
    tree2=[('h', 'ESPECIFICACIÓN'), ('i', 'Especificación de la aplicación'), ('g', 'Procesos'), ('s', 'Caso 8D'),
           ('s', 'Acciones'), ('s', 'No conformidad|on'), ('s', 'Aviso SCAR'), ('g', 'Tablas de datos'),
           ('s', 'Auditorías'), ('s', 'Casos'), ('s', 'Disposiciones'), ('s', 'Evidencias'), ('g', 'Páginas'),
           ('s', 'Registro de no conformidades'), ('s', 'Panel de calidad')],
    d1_title='Proceso de negocio: gestión de no conformidades',
    d1_h1='1. Resumen del proceso',
    d1_items=[('Código del proceso:', 'PROC-NCR-01'),
              ('Disparador:', 'un defecto o desviación detectado en inspección de entrada, producción, inspección final, reclamación de cliente o auditoría.'),
              ('Responsable del proceso:', 'ingeniero de calidad'),
              ('Entidades principales:', 'No conformidad, Acción, Aprobación, Evidencia, Caso 8D')],
    d1_h2='2. Flujo',
    d1_steps=[('Paso 1 — registro.', 'Quien la detecta introduce planta, línea, origen, número de pieza, cantidad y descripción del defecto. Estado: <code>Registrada</code>.'),
              ('Paso 2 — verificación.', 'El ingeniero de calidad asigna tipo de defecto y severidad, y marca si hace falta contención.')],
    ai_h='PROPUESTA A PARTIR DEL PROCEDIMIENTO QP-08',
    ai_p='En §4.2 hay un paso de «verificación de eficacia» a los 30 días — no está en esta descripción. ¿Añadirlo como paso 7?',
    ai_b=['Añadir', 'Ver en el procedimiento', 'Descartar'],
    d2_title='No conformidad',
    d2_lead='La vida de una no conformidad, desde que alguien la registra en planta hasta que se cierra: verificación, contención, la disposición y su aprobación, la concesión del cliente cuando la pieza está bajo contrato OEM, la ejecución de la disposición y la decisión de si hace falta un caso 8D completo.',
    d2_h1='Roles', d2_rh=['ROL', 'QUIÉN LO OCUPA'],
    d2_roles=[('Registrador', 'Operarios, inspectores y almaceneros de inspección de entrada.'),
              ('Ingeniero de calidad', 'Verifica y clasifica, lleva el caso; aprueba una disposición no crítica.'),
              ('Responsable de calidad', 'Aprueba severidad crítica y la disposición «usar tal cual», y registra la concesión del cliente.'),
              ('Responsable de acción', 'Ejecuta la contención y la disposición física.')],
    d2_h2='Campos', d2_fh=['CAMPO', 'TIPO', 'OBLIG.', 'CONTIENE'],
    d2_fields=[('Número NCR', 'Texto', 'no', 'NCR-AAAA-nnnnn, asignado automáticamente.'),
               ('Título', 'Texto', 'sí', 'Una línea: qué está mal.'),
               ('Origen', 'Selección', 'sí', 'Entrada, producción, inspección final, reclamación, auditoría.'),
               ('Planta', 'Selección', 'sí', 'Mielec o Rzeszów.'),
               ('Cantidad', 'Número', 'sí', 'Piezas afectadas.')],
    subs=[('data', 'Datos'), ('wf', 'Workflows'), ('pages', 'Páginas')],
    map_kicker='PROCESO EN LA APLICACIÓN', map_case='No conformidad NCR-2026-00184', map_running='EN MARCHA',
    map_aria='El proceso de no conformidad en la aplicación terminada: estados, roles y transiciones.',
    cur_label='ESTADO ACTIVO',
    states=[('Registrada', 'Humano · Registrador', 'HUMANO · REGISTRADOR', 'Describe el defecto, la planta, la pieza y la cantidad', 'human'),
            ('Clasificación', 'Digital · Triaje', 'DIGITAL WORKER · CLASIFICACIÓN', 'Asigna tipo de defecto y severidad inicial', 'digital'),
            ('Verificación', 'Humano · Ingeniero', 'HUMANO · INGENIERO DE CALIDAD', 'Revisa las evidencias y confirma la severidad', 'human'),
            ('Disposición', 'Humano · Ingeniero', 'HUMANO · INGENIERO DE CALIDAD', 'Elige la disposición de las piezas afectadas', 'human'),
            ('Aprobación', 'Humano · Responsable', 'HUMANO · RESPONSABLE DE CALIDAD', 'Aprueba la disposición crítica', 'human'),
            ('Cerrada', 'Digital · Cierre', 'DIGITAL WORKER · CIERRE', 'Completa el registro y archiva el caso', 'digital')],
    routes=['crítica', 'sin aprobación', 'devuelta al registrador'],
    wf_note='Esto es un <b>objeto de la plataforma</b> — estados, transiciones y roles. Ni código ni un dibujo en un documento: así se ve el proceso en el editor y así funciona en la aplicación.',
    cols=[('Número NCR', 'Texto · auto'), ('Título', 'Texto · obligatorio'), ('Origen', 'Selección · 5 valores'),
          ('Planta', 'Selección · 2 valores'), ('Cantidad', 'Número'), ('Fotos', 'Adjuntos'),
          ('Disposición', 'Relación → Disposiciones')],
    data_h=['NÚMERO', 'TÍTULO', 'PLANTA', 'ESTADO'],
    data_rows=[('NCR-2026-00184', 'Desviación de diámetro de taladro, pos. 14', 'Mielec', 'Verificación', 'b'),
               ('NCR-2026-00183', 'Falta certificado de material', 'Rzeszów', 'Cerrada', ''),
               ('NCR-2026-00182', 'Recubrimiento dañado en transporte', 'Mielec', 'Disposición', 'b'),
               ('NCR-2026-00181', 'Par de apriete fuera de especificación', 'Mielec', 'Cerrada', '')],
    data_note='Una tabla con <b>campos tipados y relaciones</b> — definida en el editor, no en migraciones de base de datos.',
    page_title='Registro de no conformidades',
    page_filters=['Planta: todas', 'Estado: abiertas', 'Mis casos'],
    page_h=['NÚMERO', 'TÍTULO', 'PERSONA', 'PLAZO'],
    page_rows=[('NCR-2026-00184', 'Desviación de diámetro de taladro, pos. 14', 'A. Nowak', 'en 2 días'),
               ('NCR-2026-00182', 'Recubrimiento dañado en transporte', 'M. Zajac', 'hoy'),
               ('NCR-2026-00179', 'Dimensión de brida fuera de tolerancia', 'A. Nowak', 'en 5 días')],
    page_cols=[('Registro de no conformidades', 'Lista · visible para todos'), ('Panel de calidad', 'Indicadores · dirección'),
               ('Calendario de acciones', 'Calendario · responsables')],
    page_note='Las páginas son <b>vistas sobre los procesos</b> — columnas, filtros y acceso definidos en el editor.',
)

I = '\n                            '


def tree(rows):
    out = []
    for kind, txt in rows:
        if kind == 'h':
            out.append('<h5>%s</h5>' % txt)
        elif kind == 'g':
            out.append('<h6>%s</h6>' % txt)
        else:
            on = txt.endswith('|on')
            name = txt[:-3] if on else txt
            cls = ('sub ' if kind == 's' else '') + ('on' if on else '')
            out.append('<span%s>%s</span>' % ((' class="%s"' % cls.strip()) if cls.strip() else '', name))
    return I + I.join(out)


def crumb(c):
    return ('<div class="v7-ac__crumb">%s <b>%s</b> · %s <span class="v7-ac__pill">%s</span>'
            '<span class="v7-ac__rev">%s</span></div>' % c)


def build(d):
    states = ''.join(
        '\n                                    <div class="dp-workflow-state dp-workflow-state--%d" data-home-state-index="%d" data-role-label="%s" data-task="%s">'
        '\n                                        <span class="dp-workflow-role dp-workflow-role--%s">%s</span>'
        '\n                                        <strong>%s</strong><small>%s</small>'
        '\n                                    </div>' % (i, i, rl, task, role, BOT if role == 'digital' else HUMAN, name, small)
        for i, (name, small, rl, task, role) in enumerate(d['states']))
    edges = ''.join('\n                                        <path data-home-edge="%s" d="%s"></path>' % e for e in EDGES)

    p1 = ('<div class="v7-ac__panel is-on" data-ac-panel="1">' + crumb(d['crumb1']) +
          '<div class="v7-ac__split"><nav class="v7-ac__tree">' + tree(d['tree1']) + '</nav><div class="v7-ac__doc">'
          '<h3>%s</h3><h4>%s</h4>' % (d['d1_title'], d['d1_h1']) +
          ''.join('<p class="v7-ac__li"><span><b>%s</b> %s</span></p>' % it for it in d['d1_items']) +
          '<h4>%s</h4>' % d['d1_h2'] +
          ''.join('<p class="v7-ac__li"><span><b>%s</b> %s</span></p>' % it for it in d['d1_steps']) +
          '<div class="v7-ac__ai"><h6><span>AI</span> %s</h6><p>%s</p><div>' % (d['ai_h'], d['ai_p']) +
          '<button type="button" class="v7-ac__mini acc">%s</button><button type="button" class="v7-ac__mini">%s</button><button type="button" class="v7-ac__mini">%s</button>' % tuple(d['ai_b']) +
          '</div></div></div></div></div>')

    p2 = ('<div class="v7-ac__panel" data-ac-panel="2">' + crumb(d['crumb2']) +
          '<div class="v7-ac__split"><nav class="v7-ac__tree">' + tree(d['tree2']) + '</nav><div class="v7-ac__doc">'
          '<h3>%s</h3><p>%s</p><h4>%s</h4>' % (d['d2_title'], d['d2_lead'], d['d2_h1']) +
          '<table class="v7-ac__tbl"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>' % tuple(d['d2_rh']) +
          ''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in d['d2_roles']) +
          '</tbody></table><h4>%s</h4>' % d['d2_h2'] +
          '<table class="v7-ac__tbl"><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>' % tuple(d['d2_fh']) +
          ''.join('<tr><td>%s</td><td><span class="v7-ac__ty">%s</span></td><td>%s</td><td>%s</td></tr>' % f for f in d['d2_fields']) +
          '</tbody></table></div></div></div>')

    wire_data = ('<div class="v7-ac__wire"><div class="v7-ac__row h"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></div>' % tuple(d['data_h']) +
                 ''.join('<div class="v7-ac__row"><span>%s</span><span>%s</span><span>%s</span><span class="v7-ac__st %s">%s</span></div>'
                         % (r[0], r[1], r[2], r[4], r[3]) for r in d['data_rows']) + '</div>')

    wire_pages = ('<div class="v7-ac__wire"><div class="v7-ac__wire-top"><b>%s</b>' % d['page_title'] +
                  ''.join('<span class="v7-ac__f">%s</span>' % f for f in d['page_filters']) + '</div>' +
                  '<div class="v7-ac__row h"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></div>' % tuple(d['page_h']) +
                  ''.join('<div class="v7-ac__row"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></div>' % r for r in d['page_rows']) +
                  '</div>')

    p3 = ('<div class="v7-ac__panel" data-ac-panel="3"><div class="v7-ac__sub" role="tablist">' +
          ''.join('<button type="button" class="v7-ac__sbtn" role="tab" aria-selected="%s" data-ac-sub="%s">%s</button>'
                  % ('true' if k == 'wf' else 'false', k, lab) for k, lab in d['subs']) + '</div>'
          '<div class="v7-ac__view" data-ac-view="data">'
          '<div class="v7-ac__cols">' + ''.join('<div class="v7-ac__col"><b>%s</b><span>%s</span></div>' % c for c in d['cols']) + '</div>' +
          wire_data + '<p class="v7-ac__note">%s</p></div>' % d['data_note'] +
          '<div class="v7-ac__view is-on" data-ac-view="wf"><div class="dp-hero__visual">'
          '<div class="dp-workflow-map" data-home-workflow-map data-step="0" data-role="human" role="img" aria-label="%s">'
          '<div class="dp-workflow-map__head"><span><small>%s</small><strong>%s</strong></span><em><i></i> %s</em></div>'
          '<div class="dp-workflow-map__canvas">'
          '<svg class="dp-workflow-map__lines" viewBox="0 0 640 390" preserveAspectRatio="none" aria-hidden="true">%s\n                                    </svg>%s'
          '\n                                    <span class="dp-workflow-map__route-label dp-workflow-map__route-label--r1">%s</span>'
          '<span class="dp-workflow-map__route-label dp-workflow-map__route-label--r2">%s</span>'
          '<span class="dp-workflow-map__route-label dp-workflow-map__route-label--r3">%s</span>'
          '<span class="dp-workflow-map__token" aria-hidden="true"><i></i></span></div>'
          '<div class="dp-workflow-map__current"><span>%s</span><strong data-home-current-state>%s</strong><i></i>'
          '<small data-home-current-role>%s</small><b data-home-current-task>%s</b></div>'
          '</div></div><p class="v7-ac__note">%s</p></div>'
          % (d['map_aria'], d['map_kicker'], d['map_case'], d['map_running'], edges, states,
             d['routes'][0], d['routes'][1], d['routes'][2], d['cur_label'],
             d['states'][0][0].upper(), d['states'][0][2], d['states'][0][3], d['wf_note']) +
          '<div class="v7-ac__view" data-ac-view="pages">' + wire_pages +
          '<div class="v7-ac__cols" style="margin-top:11px">' +
          ''.join('<div class="v7-ac__col"><b>%s</b><span>%s</span></div>' % c for c in d['page_cols']) + '</div>'
          '<p class="v7-ac__note">%s</p></div></div>' % d['page_note'])

    tabs = ''.join('<button type="button" class="v7-ac__tab" role="tab" aria-selected="%s" data-ac-tab="%d"><i>%d</i> %s</button>'
                   % ('true' if n == 1 else 'false', n, n, lab) for n, lab in enumerate(d['tabs'], 1))

    return ('<div class="v7-ac" data-ac-tabs>\n                    <div class="v7-ac__tabs" role="tablist">%s</div>'
            '\n                    <div class="v7-ac__body">%s%s%s</div>\n                </div>' % (tabs, p1, p2, p3))


FILES = {'en': 'app-creator.html', 'pl': 'pl/app-creator.html', 'de': 'de/app-creator.html', 'es': 'es/app-creator.html'}

for lang, f in FILES.items():
    s = io.open(f, encoding='utf-8').read()
    up = '../' if lang != 'en' else ''
    m = re.search(r'<div class="v7-extract">.*?</div>\s*\n\s*</div>\s*\n\s*</section>', s, re.S)
    if m:
        block = build(T[lang])
        s = s[:m.start()] + block + '\n            </div>\n        </section>' + s[m.end():]
    else:
        assert 'data-ac-tabs' in s, (f, 'nie znaleziono ani eksponatu, ani zakladek')
        s = re.sub(r'<div class="v7-ac" data-ac-tabs>.*?\n                </div>', build(T[lang]), s, count=1, flags=re.S)

    if 'homepage-workflow-map.css' not in s:
        s = s.replace('<link rel="stylesheet" href="%sassets/css/app-creator-page.css' % up,
                      '<link rel="stylesheet" href="%sassets/css/homepage-workflow-map.css">\n'
                      '    <link rel="stylesheet" href="%sassets/css/app-creator-page.css' % (up, up), 1)
    if 'app-creator-tabs.js' not in s:
        s = s.replace('<script src="%sassets/js/spec-app-exhibit.js' % up,
                      '<script src="%sassets/js/homepage-workflow-map.js"></script>\n'
                      '    <script src="%sassets/js/app-creator-tabs.js"></script>\n'
                      '    <script src="%sassets/js/spec-app-exhibit.js' % (up, up, up), 1)
    io.open(f, 'w', encoding='utf-8').write(s)
    print('ok', f)
