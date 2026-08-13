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
- **Nowa strona** — dodaj plik we wszystkich czterech językach, uruchom build,
  a następnie dopisz ją do `sitemap.xml`. Bloki `canonical` / `hreflang` / OG
  leżą między znacznikami `<!-- SEO: … -->` … `<!-- /SEO -->`.
- **Usunięta strona** — dopisz regułę 301 w `vercel.json` i usuń wpis z sitemapy.

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
