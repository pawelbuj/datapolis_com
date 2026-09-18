#!/usr/bin/env python3
"""
Zgłasza adresy do IndexNow (Bing, Copilot, Yandex, Naver, Seznam — jedno API dla wszystkich).

Po co: Microsoft mówi wprost, że silniki generatywne cenią świeżość treści i że
IndexNow jest sposobem, żeby ją wypchnąć od razu po publikacji, zamiast czekać,
aż robot sam wróci. Google nie obsługuje IndexNow — tam działa sitemapa z lastmod.

Wymaga: plik <klucz>.txt w katalogu głównym serwisu, zawierający sam klucz.
Musi być dostępny publicznie PRZED pierwszym zgłoszeniem, inaczej API odrzuci żądanie.

Użycie:
    python3 tools/indexnow.py --changed        # adresy zmienione w ostatnim commicie
    python3 tools/indexnow.py --all            # wszystko z sitemap.xml (max 10 000)
    python3 tools/indexnow.py /pl/app-creator /sharepoint
    python3 tools/indexnow.py --changed --dry-run
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "datapolis.com"
BASE = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/IndexNow"


def find_key() -> str:
    keys = [p for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{8,128}", p.stem)]
    if not keys:
        sys.exit("Brak pliku z kluczem IndexNow (<klucz>.txt) w katalogu głównym.")
    if len(keys) > 1:
        sys.exit(f"Więcej niż jeden plik klucza: {[k.name for k in keys]}")
    return keys[0].stem


def url_for_file(rel: str) -> str | None:
    if not rel.endswith(".html"):
        return None
    path = rel[:-5]
    if path.endswith("index"):
        path = path[: -len("index")].rstrip("/")
    return f"{BASE}/{path}" if path else f"{BASE}/"


def changed_urls() -> list[str]:
    out = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    urls = {u for u in (url_for_file(f) for f in out) if u}
    # tylko adresy, które faktycznie są w sitemapie — strony noindex
    # (wygaszone, wewnętrzne makiety) nie mają po co trafiać do IndexNow
    return sorted(urls & set(sitemap_urls()))


def sitemap_urls() -> list[str]:
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>(.*?)</loc>", xml)


def submit(urls: list[str], key: str) -> None:
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE}/{key}.txt",
        "urlList": urls[:10000],
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow: HTTP {resp.status} — zgłoszono {len(payload['urlList'])} adresów")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:300]
        print(f"IndexNow: HTTP {exc.code} — {body}")
        if exc.code == 403:
            print(f"  403 znaczy, że {BASE}/{key}.txt nie jest jeszcze publicznie dostępny.")
        raise SystemExit(1)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    if "--all" in flags:
        urls = sitemap_urls()
    elif "--changed" in flags:
        urls = changed_urls()
    elif args:
        urls = [a if a.startswith("http") else BASE + "/" + a.lstrip("/") for a in args]
    else:
        sys.exit(__doc__)

    if not urls:
        print("Nic do zgłoszenia.")
        return 0

    for u in urls:
        print("  ", u)
    if "--dry-run" in flags:
        print(f"(--dry-run: {len(urls)} adresów, nic nie wysłano)")
        return 0

    submit(urls, find_key())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
