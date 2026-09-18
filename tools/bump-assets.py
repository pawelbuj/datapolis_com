#!/usr/bin/env python3
"""Ustawia ?v= przy arkuszach i skryptach na SKROT ICH TRESCI.

    python3 tools/bump-assets.py            # wszystkie assets/css + assets/js
    python3 tools/bump-assets.py home-v7.css

Wersja zmienia sie wtedy i tylko wtedy, gdy zmienila sie zawartosc pliku,
wiec nie da sie wypuscic zmiany w CSS, ktorej przegladarka nie zobaczy
(data w ?v= tego nie zalatwiala: dwie zmiany tego samego dnia mialy
ten sam znacznik i uzytkownik dostawal stary arkusz).

Uruchamiac po kazdej zmianie w assets/ i przed commitem.
"""
import re, sys, glob, os, hashlib

def digest(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:8]

def pages():
    for p in glob.glob("*.html") + glob.glob("*/*.html"):
        if "/includes/" in p or p.startswith("_to_delete"):
            continue
        yield p
    for p in glob.glob("includes/*.html") + glob.glob("*/includes/*.html"):
        yield p

def main(names):
    assets = {}
    for f in glob.glob("assets/css/*.css") + glob.glob("assets/js/*.js"):
        b = os.path.basename(f)
        if names and b not in names:
            continue
        assets[b] = digest(f)
    if not assets:
        print("nic nie pasuje do:", names); return

    touched, changed = 0, set()
    for p in pages():
        s = open(p, encoding="utf-8").read()
        o = s
        for b, d in assets.items():
            def sub(m, d=d):
                if m.group(2) != d:
                    changed.add(m.group(1))
                return "%s?v=%s" % (m.group(1), d)
            # (?<![\w.-]) - nazwa pliku musi zaczynac sie na granicy sciezki.
            # Bez tego "homepage.css" lapalo sie w srodku "new-homepage.css"
            # i wpisywalo tam cudzy skrot: plik zmieniony, ?v= bez zmian.
            s = re.sub(r"(?<![\w.-])(%s)\?v=([A-Za-z0-9]+)" % re.escape(b), sub, s)
        if s != o:
            open(p, "w", encoding="utf-8").write(s); touched += 1
    print("plikow z nowa wersja: %d %s" % (len(changed), sorted(changed)))
    print("stron zaktualizowanych:", touched)

if __name__ == "__main__":
    main(sys.argv[1:])
