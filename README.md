# Datapolis Website - Static HTML Version

Czysta wersja HTML strony Datapolis bez zależności od CMS.

## Struktura projektu

```
datapolis_com/
├── index.html              # Strona główna
├── assets/
│   ├── css/
│   │   ├── main.min.css    # Główne style
│   │   └── async.min.css   # Style ładowane asynchronicznie
│   ├── js/
│   │   ├── main.min.js     # Główny JavaScript
│   │   ├── vendors.min.js  # Biblioteki zewnętrzne
│   │   ├── functions.min.js # Funkcje pomocnicze
│   │   └── async.min.js    # Skrypty asynchroniczne
│   └── img/
│       ├── favicon/        # Ikony favicons
│       ├── top-img-618x555.png
│       └── img-text-2-522x670.jpg
└── storage/
    └── files/
        └── klienci/        # Loga klientów
```

## Zmiany w porównaniu do wersji CMS

### Usunięte elementy:
- ✅ Tag `<base href>` - wszystkie ścieżki są teraz relatywne
- ✅ Meta tag `csrf-token` - niepotrzebny w statycznej stronie
- ✅ Formularz POST - usunięty z końca strony
- ✅ Skrypt `js-localization` - usunięty, nie potrzebny bez backendu
- ✅ Skrypt Google Analytics - usunięte preconnect i tracking
- ✅ Facebook Pixel - usunięte preconnect

### Zmienione elementy:
- ✅ Wszystkie linki wewnętrzne wskazują na anchory (#) lub index.html
- ✅ Linki do języków wskazują na anchory
- ✅ Usunięte dynamiczne ścieżki generowane przez CMS
- ✅ Copyright zaktualizowany (usunięty link do studia)

### Zachowane elementy:
- ✅ Całe CSS i JavaScript
- ✅ Web Font Loader - do ładowania czcionek Adobe Typekit
- ✅ Wszystkie obrazy i grafiki
- ✅ Struktura HTML i wszystkie sekcje
- ✅ Linki do social media
- ✅ Linki zewnętrzne (np. do YouTube Demo)

## Jak uruchomić?

### Opcja 1: Prosty serwer HTTP (Python)
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Następnie otwórz w przeglądarce: `http://localhost:8000`

### Opcja 2: Live Server (VS Code / Cursor)
1. Zainstaluj rozszerzenie "Live Server"
2. Kliknij prawym przyciskiem na `index.html`
3. Wybierz "Open with Live Server"

### Opcja 3: Bezpośrednio w przeglądarce
Możesz otworzyć plik `index.html` bezpośrednio w przeglądarce, ale niektóre funkcje mogą nie działać poprawnie (np. ładowanie czcionek).

## Funkcjonalność

### Działające elementy:
- ✅ Responsywny design (mobile, tablet, desktop)
- ✅ Menu mobilne (hamburger)
- ✅ Dropdown z wyborem języka
- ✅ Accordion (rozwijane sekcje)
- ✅ Slider z logotypami klientów (Swiper)
- ✅ Animacje przy scrollowaniu (AOS)
- ✅ Smooth scroll do sekcji
- ✅ Sticky header

### Do implementacji (jeśli potrzebne):
- ⚠️ Formularz kontaktowy - wymaga backendu
- ⚠️ Wersje językowe - wymagają osobnych plików HTML
- ⚠️ Blog - wymaga osobnych stron

## Zależności JavaScript

Projekt wykorzystuje:
- **Swiper.js** - slider/carousel
- **AOS (Animate On Scroll)** - animacje przy scrollowaniu
- **Web Font Loader** - ładowanie czcionek Adobe Typekit

Wszystkie biblioteki są już zawarte w plikach `vendors.min.js`.

## Dalszy rozwój

### Wersje językowe
Aby dodać inne wersje językowe, stwórz:
- `index-pl.html` - polska wersja
- `index-es.html` - hiszpańska wersja

I zaktualizuj linki w dropdownie języków.

### Dodatkowe strony
Możesz stworzyć osobne pliki HTML dla:
- `solutions.html` - strona rozwiązań
- `products.html` - strona produktów
- `contact.html` - strona kontaktowa
- etc.

## Kontakt

Dla pytań technicznych skontaktuj się:
- Email: office@datapolis.com
- Tel: +48 601 33 20 56

---

**Projekt zaktualizowany:** Styczeń 2026
