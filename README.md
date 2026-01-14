# Datapolis Website - Static HTML Version

Czysta wersja HTML strony Datapolis bez zależności od CMS.

## Struktura projektu

```
datapolis_com/
├── index.html              # Strona główna
├── solutions.html          # Strona rozwiązań
├── it-sector-solutions.html # IT Sector Solutions
├── includes/               # ⭐ NOWE: Współdzielone komponenty
│   ├── header.html         # Menu górne (navbar)
│   ├── footer.html         # Stopka
│   └── loader.js           # Skrypt ładujący header i footer
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

## ⭐ System Includes - Wspólne komponenty

Strona wykorzystuje **system dynamicznego ładowania** header i footer, co znacznie ułatwia zarządzanie menu i stopką.

### Jak to działa?

1. **Header i Footer w osobnych plikach:**
   - `includes/header.html` - zawiera całe menu nawigacyjne
   - `includes/footer.html` - zawiera stopkę ze wszystkimi linkami

2. **Automatyczne ładowanie:**
   - Skrypt `includes/loader.js` automatycznie ładuje header i footer do każdej strony
   - Każda strona HTML zawiera tylko placeholdery:
     ```html
     <div id="header-placeholder"></div>
     <div id="footer-placeholder"></div>
     ```

3. **Zalety:**
   - ✅ **Edytuj raz** - zmiana w `header.html` automatycznie aktualizuje wszystkie strony
   - ✅ **Łatwe zarządzanie** - nie trzeba edytować menu w każdym pliku osobno
   - ✅ **Spójność** - wszystkie strony mają identyczne menu i stopkę
   - ✅ **Szybkie dodawanie nowych stron** - wystarczy skopiować szablon

### Dodawanie nowej strony

Aby dodać nową stronę do projektu:

1. Skopiuj `index.html` jako szablon
2. Zmień tylko zawartość między placeholderami:
   ```html
   <div id="header-placeholder"></div>
   
   <main class="main">
       <!-- Twoja zawartość tutaj -->
   </main>
   
   <div id="footer-placeholder"></div>
   ```
3. Header i footer załadują się automatycznie!

### Edycja menu

Aby zmienić menu nawigacyjne we wszystkich stronach:
1. Otwórz `includes/header.html`
2. Edytuj strukturę menu
3. Zapisz - zmiany pojawią się na wszystkich stronach!

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

### Istniejące strony
Projekt zawiera następujące strony:
- ✅ `index.html` - strona główna
- ✅ `solutions.html` - strona rozwiązań
- ✅ `it-sector-solutions.html` - IT Sector Solutions

### Dodatkowe strony do stworzenia
Możesz stworzyć osobne pliki HTML dla:
- `products.html` - strona produktów
- `customers.html` - strona klientów
- `company.html` - o firmie
- `support.html` - wsparcie techniczne
- `licensing.html` - licencjonowanie
- `contact.html` - strona kontaktowa
- `blog.html` - blog
- `electronic-document-workflow.html` - Electronic Document Workflow
- `human-resources.html` - Human Resources (HR)
- `customer-service.html` - Customer Service
- `finance.html` - Finance
- `purchasing-logistics.html` - Purchasing and Logistics
- `operations-production.html` - Operations and Production
- `audit-compliance.html` - Audit & Compliance

**Pamiętaj:** Każda nowa strona automatycznie odziedziczy menu i stopkę dzięki systemowi includes!

## Kontakt

Dla pytań technicznych skontaktuj się:
- Email: office@datapolis.com
- Tel: +48 601 33 20 56

---

**Projekt zaktualizowany:** Styczeń 2026
