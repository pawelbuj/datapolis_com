# -*- coding: utf-8 -*-
"""Buduje /sharepoint we wszystkich czterech językach z jednego szablonu.

    python3 tools/i18n/wf3_build.py

Po wygenerowaniu uruchomić:
    python3 tools/build-includes.py      # nagłówek, stopka, JSON-LD
    python3 tools/build-sitemap.py       # wpisy w sitemapie
"""
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from wf3_tpl import TPL          # noqa: E402
from wf3_en import EN            # noqa: E402
from wf3_pl import PL            # noqa: E402
from wf3_de import DE            # noqa: E402
from wf3_es import ES            # noqa: E402

LANGS = {
    "en": dict(data=EN, out="sharepoint.html",    path="sharepoint",    a="",     locale="en_US"),
    "pl": dict(data=PL, out="pl/sharepoint.html", path="pl/sharepoint", a="../",  locale="pl_PL"),
    "de": dict(data=DE, out="de/sharepoint.html", path="de/sharepoint", a="../",  locale="de_DE"),
    "es": dict(data=ES, out="es/sharepoint.html", path="es/sharepoint", a="../",  locale="es_ES"),
}

REQUIRED = set(re.findall(r"\{([a-z0-9_]+)\}", TPL)) - {"a", "lang", "path", "modified", "og_locale"}


def main():
    modified = date.today().isoformat()
    for lang, cfg in LANGS.items():
        data = cfg["data"]
        missing = REQUIRED - set(data)
        if missing:
            sys.exit(f"{lang}: brakuje pól w słowniku: {sorted(missing)}")

        html = TPL.format(
            lang=lang,
            a=cfg["a"],
            path=cfg["path"],
            og_locale=cfg["locale"],
            modified=modified,
            **data,
        )
        target = os.path.join(ROOT, cfg["out"])
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(html)
        words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", html)))
        print(f"{cfg['out']:24s} {len(html):>7,} B  ~{words} słów")

    print("\nTeraz: python3 tools/build-includes.py && python3 tools/build-sitemap.py")


if __name__ == "__main__":
    main()
