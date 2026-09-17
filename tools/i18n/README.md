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

## Zasady, których te pliki pilnują

- `Run work. Speed up the flow.` oraz `Apps that run work.` — nigdy nie tłumaczone.
- H1 strony głównej zostaje po angielsku w każdym języku.
- `governed`: PL „nadzorowany", DE „gesteuert", ES „gobernado".
- Procesy się wdraża albo automatyzuje — nie uruchamia.
