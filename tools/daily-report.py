#!/usr/bin/env python3
"""Dzienny raport: Google Analytics 4 + Google Search Console.

Wypisuje zwięzłe podsumowanie na standardowe wyjście. Uruchamiany przez
zaplanowane zadanie, ale można też ręcznie:

    python3 tools/daily-report.py            # wczoraj vs przedwczoraj
    python3 tools/daily-report.py --days 7   # ostatnie 7 dni

Wymaga:
    pip3 install --user google-auth requests
    plik klucza konta usługi wskazany przez DATAPOLIS_SA_KEY
    (domyślnie <repo>/.datapolis/ga-service-account.json — katalog jest w .gitignore)

Konto usługi musi mieć:
    - rolę Viewer w usłudze GA4 (Administracja → Dostęp do usługi)
    - dostęp do właściwości w Search Console (Ustawienia → Użytkownicy)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date, timedelta

GA_PROPERTY = "398529147"
GSC_SITE = "https://datapolis.com/"
# Klucz leży w katalogu repozytorium, bo tylko podpięte foldery są widoczne
# dla powłoki, przez którą uruchamia się zaplanowane zadanie.
# .datapolis/ jest w .gitignore — plik nigdy nie trafi do repo.
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.environ.get(
    "DATAPOLIS_SA_KEY", os.path.join(_REPO, ".datapolis", "ga-service-account.json")
)
SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/webmasters.readonly",
]

AI_HOSTS = ("chatgpt.com", "perplexity.ai", "claude.ai", "copilot.microsoft.com",
            "gemini.google.com", "openai.com", "bing.com")


def session():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("Brak bibliotek. Uruchom: pip3 install --user google-auth requests")
    if not os.path.exists(KEY_PATH):
        sys.exit(f"Nie znaleziono klucza konta usługi: {KEY_PATH}")
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    return AuthorizedSession(creds)


def ga(s, body):
    r = s.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{GA_PROPERTY}:runReport",
        json=body, timeout=60,
    )
    if r.status_code != 200:
        return {"_error": f"GA4 HTTP {r.status_code}: {r.text[:200]}"}
    return r.json()


def rows(res, n=None):
    if "_error" in res:
        return []
    out = [([d["value"] for d in row.get("dimensionValues", [])],
            [m["value"] for m in row.get("metricValues", [])])
           for row in res.get("rows", [])]
    return out[:n] if n else out


def total(res, i=0):
    if "_error" in res:
        return None
    t = res.get("totals") or []
    if not t:
        return 0
    return int(t[0]["metricValues"][i]["value"])


def gsc(s, body):
    r = s.post(
        f"https://searchconsole.googleapis.com/webmasters/v3/sites/"
        f"{GSC_SITE.replace(':', '%3A').replace('/', '%2F')}/searchAnalytics/query",
        json=body, timeout=60,
    )
    if r.status_code != 200:
        return {"_error": f"GSC HTTP {r.status_code}: {r.text[:200]}"}
    return r.json()


def main() -> int:
    days = 1
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])

    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days - 1)
    rng = {"startDate": start.isoformat(), "endDate": end.isoformat()}
    prev = {"startDate": prev_start.isoformat(), "endDate": prev_end.isoformat()}

    s = session()
    print(f"# datapolis.com — {start} … {end}\n")

    # --- ruch ogółem, z porównaniem
    now = ga(s, {"dateRanges": [rng], "metrics": [{"name": "sessions"}, {"name": "totalUsers"}]})
    was = ga(s, {"dateRanges": [prev], "metrics": [{"name": "sessions"}, {"name": "totalUsers"}]})
    if "_error" in now:
        print("GA4:", now["_error"])
    else:
        ns, nu = total(now, 0), total(now, 1)
        ps, pu = total(was, 0), total(was, 1)
        d = f"{ns - ps:+d}" if ps is not None else "?"
        print(f"RUCH: {ns} sesji ({d} wobec poprzedniego okresu), {nu} użytkowników")

    # --- najczęściej czytane strony
    top = ga(s, {"dateRanges": [rng],
                 "dimensions": [{"name": "pagePath"}],
                 "metrics": [{"name": "screenPageViews"}],
                 "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
                 "limit": 8})
    if rows(top):
        print("\nNAJCZĘŚCIEJ CZYTANE:")
        for dims, mets in rows(top, 8):
            print(f"  {mets[0]:>5}  {dims[0]}")

    # --- skąd przyszli
    src = ga(s, {"dateRanges": [rng],
                 "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSource"}],
                 "metrics": [{"name": "sessions"}],
                 "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
                 "limit": 12})
    if rows(src):
        print("\nŹRÓDŁA:")
        ai = 0
        for dims, mets in rows(src, 12):
            mark = ""
            if dims[0] == "AI Assistant" or any(h in dims[1].lower() for h in AI_HOSTS):
                mark = "  <-- asystent AI"
                ai += int(mets[0])
            print(f"  {mets[0]:>5}  {dims[0]} / {dims[1]}{mark}")
        print(f"\n  Z asystentów AI łącznie: {ai} sesji")

    # --- Search Console (dane mają 2-3 dni opóźnienia)
    g_end = date.today() - timedelta(days=3)
    g_start = g_end - timedelta(days=days - 1)
    perf = gsc(s, {"startDate": g_start.isoformat(), "endDate": g_end.isoformat(),
                   "dimensions": ["query"], "rowLimit": 10})
    print(f"\nSEARCH CONSOLE ({g_start} … {g_end}, dane Google mają ~3 dni opóźnienia):")
    if "_error" in perf:
        print("  " + perf["_error"])
    elif not perf.get("rows"):
        print("  brak wyświetleń w tym okresie")
    else:
        tot_i = sum(r["impressions"] for r in perf["rows"])
        tot_c = sum(r["clicks"] for r in perf["rows"])
        print(f"  {tot_i} wyświetleń, {tot_c} kliknięć")
        print("  Zapytania:")
        for r in perf["rows"][:10]:
            print(f"    {r['impressions']:>4} wyśw. {r['clicks']:>3} klik.  poz. "
                  f"{r['position']:.1f}  {r['keys'][0]}")

    pages = gsc(s, {"startDate": g_start.isoformat(), "endDate": g_end.isoformat(),
                    "dimensions": ["page"], "rowLimit": 8})
    if pages.get("rows"):
        print("  Strony:")
        for r in pages["rows"][:8]:
            print(f"    {r['impressions']:>4} wyśw. {r['clicks']:>3} klik.  {r['keys'][0]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
