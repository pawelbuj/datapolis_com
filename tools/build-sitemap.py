#!/usr/bin/env python3
"""
Generuje sitemap.xml ze stanu katalogu.

Co robi:
  - bierze wszystkie strony EN (*.html w katalogu głównym) oraz pl/ de/ es/
  - pomija strony z <meta name="robots" content="noindex...">
    (wygaszone strony i wewnętrzne makiety wypadają automatycznie)
  - <lastmod> z daty ostatniego commita danego pliku (git log -1),
    a jeśli plik nie jest w gicie — z mtime
  - hreflang tylko dla tych języków, w których strona faktycznie istnieje
    (np. /sharepoint jest tylko po angielsku i nie dostaje alternatywnych linków)
  - x-default zawsze na wersję EN

Użycie:
    python3 tools/build-sitemap.py            # zapisuje sitemap.xml
    python3 tools/build-sitemap.py --check    # nic nie zapisuje, tylko pokazuje różnice
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://datapolis.com"
LANGS = ("pl", "de", "es")          # EN mieszka w katalogu głównym
NOINDEX = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', re.I)

# Priorytety. Google ich nie używa w rankingu, ale trzymamy zgodność z tym,
# co było w sitemapie dotąd.
PRIORITY_EXACT = {"": "1.0"}                     # strona główna EN
PRIORITY_LANG_ROOT = "0.9"                       # /pl /de /es
PRIORITY_BY_SLUG = {"app-creator": "0.9"}
PRIORITY_DEFAULT = "0.7"


def slug_of(path: Path) -> str:
    """app-creator.html -> 'app-creator'; index.html -> ''"""
    return "" if path.stem == "index" else path.stem


def url_for(lang: str | None, slug: str) -> str:
    parts = [p for p in (lang, slug) if p]
    return BASE + "/" + "/".join(parts) if parts else BASE + "/"


def indexable(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return False
    return not NOINDEX.search(head)


def git_lastmod(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        ).stdout.strip()
        if out:
            return out[:10]
    except (OSError, subprocess.SubprocessError):
        pass
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return ts.strftime("%Y-%m-%d")


def priority_for(lang: str | None, slug: str) -> str:
    if lang is None and slug in PRIORITY_EXACT:
        return PRIORITY_EXACT[slug]
    if lang is not None and slug == "":
        return PRIORITY_LANG_ROOT
    return PRIORITY_BY_SLUG.get(slug, PRIORITY_DEFAULT)


def collect() -> dict[str, dict[str | None, Path]]:
    """slug -> {None|'pl'|'de'|'es': ścieżka}, tylko strony indeksowalne"""
    pages: dict[str, dict[str | None, Path]] = {}
    for path in sorted(ROOT.glob("*.html")):
        if indexable(path):
            pages.setdefault(slug_of(path), {})[None] = path
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            if indexable(path):
                pages.setdefault(slug_of(path), {})[lang] = path
    return pages


def build() -> str:
    pages = collect()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    def sort_key(item):
        lang, slug = item
        return (lang or "", "" if slug == "" else slug)

    entries = sorted(
        ((lang, slug) for slug, by_lang in pages.items() for lang in by_lang),
        key=sort_key,
    )

    for lang, slug in entries:
        by_lang = pages[slug]
        path = by_lang[lang]
        lines.append("  <url>")
        lines.append(f"    <loc>{url_for(lang, slug)}</loc>")
        lines.append(f"    <lastmod>{git_lastmod(path)}</lastmod>")
        if len(by_lang) > 1:
            if None in by_lang:
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{url_for(None, slug)}"/>'
                )
            for other in LANGS:
                if other in by_lang:
                    lines.append(
                        f'    <xhtml:link rel="alternate" hreflang="{other}" '
                        f'href="{url_for(other, slug)}"/>'
                    )
            if None in by_lang:
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="x-default" '
                    f'href="{url_for(None, slug)}"/>'
                )
        lines.append(f"    <priority>{priority_for(lang, slug)}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    target = ROOT / "sitemap.xml"
    new = build()
    count = new.count("<url>")

    if "--check" in sys.argv:
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        old_locs = set(re.findall(r"<loc>(.*?)</loc>", old))
        new_locs = set(re.findall(r"<loc>(.*?)</loc>", new))
        print(f"obecnie: {len(old_locs)} URL-i, po przebudowie: {len(new_locs)}")
        for u in sorted(new_locs - old_locs):
            print("  + ", u)
        for u in sorted(old_locs - new_locs):
            print("  - ", u)
        if old_locs == new_locs:
            print("  (ten sam zestaw adresów; zmieniają się tylko znaczniki lastmod)")
        return 0

    target.write_text(new, encoding="utf-8")
    print(f"sitemap.xml: {count} URL-i")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
