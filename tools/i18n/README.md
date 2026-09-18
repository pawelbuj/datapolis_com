# tools/i18n — generatory wersji językowych (ver7)

Jedno źródło prawdy dla czterech języków. Uruchamiać z katalogu głównego repo,
a po każdej zmianie: `python3 tools/build-includes.py`.

## Strona główna

`home_tpl.py` — szablon `<main>` (164 pola). `home_de.py`, `home_es.py` — słowniki.
PL i EN są dziś wpisane w `index.html` / `pl/index.html` bezpośrednio; jeśli mają dołączyć
do szablonu, wystarczy dopisać `home_pl.py` i `home_en.py` w tej samej konwencji.

```
python3 - <<'PY'
import sys; sys.path.insert(0, "tools/i18n")
from home_tpl import TPL
from home_de import DE
print(TPL.format(**DE)[:200])
PY
```

## App Creator

```
python3 tools/i18n/ac_build.py pl de es
```

Bierze `app-creator.html` (EN) jako źródło, podmienia hero z szablonu i resztę treści
przez słownik `ac_<lang>.py`, przestawia ścieżki, meta, canonical i hreflang.
Po wygenerowaniu uruchomić jeszcze raz ujednolicenie CTA (blok `.v7-cta`).

## Hub SharePoint WF3 (`/sharepoint`)

```
python3 tools/i18n/wf3_build.py
python3 tools/build-includes.py
python3 tools/build-sitemap.py
```

`wf3_tpl.py` — szablon całej strony (96 pól). `wf3_en.py`, `wf3_pl.py`, `wf3_de.py`,
`wf3_es.py` — słowniki, wszystkie z identycznym zestawem kluczy; build przerywa,
jeśli w którymś czegoś brakuje. Generuje `sharepoint.html` oraz `pl|de|es/sharepoint.html`
naraz, więc cztery wersje nie mogą się rozjechać.

Strona opisuje zdarzenie z datą (KB5002908 z 8 września 2026), więc:

- **nie zmieniaj dat ani cytatów w jednym języku osobno** — są identyczne we wszystkich
  czterech i wszystkie pochodzą ze źródeł pierwotnych Microsoftu,
- **poleceń PowerShell nie tłumaczymy** (siedzą w szablonie, nie w słownikach),
- `dateModified` w JSON-LD i `lastmod` w sitemapie biorą późniejszą z dwóch dat:
  commita i modyfikacji pliku. Kiedy treść naprawdę się zmieni, przebuduj i zacommituj,
  żeby data mówiła prawdę. Świeżość jest tu sygnałem rankingowym,
- gdy październikowa aktualizacja wyłączy przepływy SharePoint 2013, trzeba wrócić
  do sekcji osi czasu — dziś opisuje to jako zapowiedź z jednego źródła.

Własny arkusz: `assets/css/sharepoint-wf3.css` (tabela stanu, blok z poleceniami,
ramka ostrzeżenia, lista źródeł). Reszta strony jedzie na klasach `.v7-*`.

## Zasady, których te pliki pilnują

- `Run work. Speed up the flow.` oraz `Apps that run work.` — nigdy nie tłumaczone.
- H1 strony głównej zostaje po angielsku w każdym języku.
- `governed`: PL „nadzorowany", DE „gesteuert", ES „gobernado".
- Procesy się wdraża albo automatyzuje — nie uruchamia.
