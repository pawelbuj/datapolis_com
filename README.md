# datapolis.com

Statyczny serwis (HTML + CSS + JS, bez frameworka), hostowany na Vercelu.
69 stron: 18 EN w katalogu głównym + po 17 w `pl/`, `de/`, `es/`.

## Struktura

```
├── *.html                  strony EN
├── pl/ de/ es/             wersje językowe (te same nazwy plików)
├── includes/               header.html, footer.html, loader.js   ← źródło shellu EN
├── pl|de|es/includes/      header.html, footer.html              ← shell danego języka
├── assets/css|js|img/
├── logos/  storage/        logotypy klientów
├── tools/build-includes.py skrypt build
├── vercel.json             cleanUrls + 162 przekierowania 301
├── sitemap.xml  robots.txt
```

## ⚠️ Po każdej zmianie w `includes/` uruchom build

Nagłówek i stopka są **wklejone na stałe** w każdą stronę — nie doklejane
JavaScriptem. Dzięki temu linki wewnętrzne widzą roboty, które nie wykonują JS
(GPTBot, ClaudeBot, PerplexityBot), a strona nie wykonuje dwóch dodatkowych
zapytań przy każdym wejściu.

Cena: edycja `includes/header.html` **nie zmienia niczego**, dopóki nie przebudujesz stron.

```bash
python3 tools/build-includes.py
```

Skrypt jest idempotentny — można go uruchamiać ile razy trzeba. Podmienia
zawartość między znacznikami `<!--build:header-->` … `<!--/build:header-->`
(analogicznie stopka) i odświeża blok JSON-LD.

Edytuj **`includes/*.html`**, nigdy wklejonego shellu w stronach — nadpisze go
najbliższy build.

## Podgląd lokalny

```bash
npx serve .        # http://localhost:3000, obsługuje czyste URL-e
npx vercel dev     # dodatkowo przekierowania z vercel.json
```

`python3 -m http.server` **nie zadziała** poprawnie — nie obsługuje adresów bez
rozszerzenia `.html`, więc `/de/index` zwróci 404.

## Konwencje

- **Wersjonowanie cache** — wszystkie odwołania do `assets/` mają wspólny
  parametr `?v=RRRRMMDD`. Po zmianie w CSS lub JS podbij go wszędzie naraz,
  inaczej część użytkowników dostanie stary plik.
- **Fonty** — Inter i Instrument Sans wchodzą przez `<link>` w `<head>`.
  Nie wracaj do `@import` w CSS: `@import` postawiony po jakiejkolwiek regule
  stylu jest przez przeglądarki ignorowany (tak było wcześniej — fonty w ogóle
  się nie ładowały).
- **`<meta name="google-site-verification">`** siedzi w `<head>` czterech stron
  głównych (EN/PL/DE/ES) i weryfikuje serwis w Google Search Console.
  Nie usuwaj — usunięcie odpina właściwość i tracimy raporty, w tym ten
  o wyświetleniach w AI Overviews i AI Mode. `build-includes.py` go nie rusza.
- **Nowa strona** — dodaj plik we wszystkich czterech językach, uruchom build,
  a potem `python3 tools/build-sitemap.py`. Bloki `canonical` / `hreflang` / OG
  leżą między znacznikami `<!-- SEO: … -->` … `<!-- /SEO -->`.
- **Usunięta strona** — dopisz regułę 301 w `vercel.json`, wstaw stronie
  `<meta name="robots" content="noindex,follow">` i przebuduj sitemapę.
  Wpis wypadnie z niej sam.

## Analityka i zgoda na ciasteczka

Google Analytics 4 (`G-41L2VC300P`) plus baner zgody wchodzą **jednym blokiem**
`<!--build:consent-->` wstrzykiwanym w `<head>` każdej strony przez
`tools/build-includes.py`. Nie edytuj tego bloku w plikach HTML — najbliższy build go nadpisze.
Teksty baneru dla czterech języków siedzą w słowniku `CONSENT_TEXT` w tym samym skrypcie.

Zasada, której ten blok pilnuje: **Consent Mode v2 z domyślną odmową wykonuje się PRZED
załadowaniem `gtag.js`**. Odwrócenie tej kolejności sprawia, że Google zapisuje ciasteczko,
zanim ktokolwiek cokolwiek kliknie — czyli dokładnie to, czego baner ma zapobiegać.
Domyślnie odmawiamy wszystkiego poza `security_storage`; po kliknięciu „Zgadzam się"
podnosimy wyłącznie `analytics_storage` (reklam nie prowadzimy, więc `ad_*` zostaje odmówione).

Wybór użytkownika ląduje w `localStorage` pod kluczem `dp-consent`.

**Otwarte:** polityka prywatności (`legal.html`) nadal nie wspomina o ciasteczkach
ani o Google Analytics, w żadnym z czterech języków. To treść prawna i wymaga kogoś,
kto za nią odpowiada. Do czasu jej uzupełnienia baner działa, ale link „Polityka prywatności"
prowadzi do dokumentu, który o ciasteczkach milczy.

## Sitemapa i zgłaszanie zmian

`sitemap.xml` **nie jest już pisana ręcznie** — generuje ją skrypt ze stanu katalogu:

```bash
python3 tools/build-sitemap.py            # zapisuje
python3 tools/build-sitemap.py --check    # tylko pokazuje, co by się zmieniło
```

Skrypt sam pomija strony z `noindex`, sam dobiera `hreflang` do tych języków,
w których strona faktycznie istnieje (`/sharepoint` jest tylko po angielsku
i alternatyw nie dostaje), a `<lastmod>` bierze z daty ostatniego commita pliku.
Data jest sygnałem świeżości — wyszukiwarki AI cytują głównie treści
aktualizowane w ciągu ostatniego roku — więc ma odzwierciedlać realne zmiany,
a nie datę ostatniego builda.

Po wdrożeniu zmian na produkcję:

```bash
python3 tools/indexnow.py --changed       # adresy z ostatniego commita
python3 tools/indexnow.py --all           # cała sitemapa (po dużej przebudowie)
```

IndexNow obsługują Bing i Copilot (oraz Yandex, Naver, Seznam) — jedno API dla
wszystkich. Google go nie obsługuje, tam pracuje sitemapa z `lastmod`.
Klucz leży w pliku `<klucz>.txt` w katalogu głównym i **musi być publicznie
dostępny**, zanim pierwszy raz coś zgłosimy — inaczej API odpowiada 403.

## Dane strukturalne

Każda strona ma JSON-LD (`Organization`, `WebSite`, `WebPage`, `BreadcrumbList`;
`SoftwareApplication` na stronach `platform-2to2`). Generuje je build ze
znaczników `<title>` i `<meta name="description">` danej strony — żeby poprawić
opis w danych strukturalnych, popraw meta i przebuduj.

## Formularz kontaktowy

`contact.html` we wszystkich czterech językach osadza ten sam workflow z 2to2:

```html
<script src="https://2to2.ai/embed-workflow.js" data-workflow="www-contacts" …>
```

To jedyny kanał lead capture na stronie — po zmianach w tym miejscu sprawdź, czy
formularz faktycznie się renderuje.
