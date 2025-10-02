# PROFESJONALNE NARZĘDZIE DO AUDYTU SEO

Stwórz zaawansowaną aplikację React do kompleksowego audytu technicznego SEO z profesjonalną prezentacją wyników, przeznaczoną dla specjalistów SEO do wykorzystania w procesie sprzedażowym i konsultingowym.

---
## 🎯 NAZWA APLIKACJI - SEO AIditor


## 🎯 ARCHITEKTURA I ZAŁOŻENIA TECHNICZNE

### Stack technologiczny:
- **React** z Hooks dla zarządzania stanem
- **Recharts** lub **Chart.js** do wizualizacji danych
- **Tailwind CSS** dla responsywnego designu
- **Lucide React** dla ikonek
- Asynchroniczne wywołania API z obsługą błędów
- localStorage dla cache'owania wyników

### Struktura aplikacji:
1. Strona główna z formularzem
2. Panel audytu z progress tracking
3. Dashboard wyników z interaktywnymi sekcjami
4. Generator raportów PDF/prezentacyjnych

---

## 📊 SZCZEGÓŁOWE KATEGORIE AUDYTU

### **1. FUNDAMENTY TECHNICZNE (20% wagi końcowej)**

#### A) Dostępność i wydajność:
- **Status HTTP** (200, 301, 302, 404, 500, 503)
  - Sprawdź czas odpowiedzi serwera (TTFB < 600ms = 100%, 600-1200ms = 50%, >1200ms = 0%)
  - Test dostępności z różnych lokalizacji (symulacja)
  
#### B) Core Web Vitals (Google PageSpeed Insights API):
- **LCP (Largest Contentful Paint)**: < 2.5s = 100 pkt, 2.5-4s = 50 pkt, >4s = 0 pkt
- **FID (First Input Delay)**: < 100ms = 100 pkt, 100-300ms = 50 pkt, >300ms = 0 pkt
- **CLS (Cumulative Layout Shift)**: < 0.1 = 100 pkt, 0.1-0.25 = 50 pkt, >0.25 = 0 pkt
- **INP (Interaction to Next Paint)**: nowa metryka, < 200ms = optimal
- **TTFB (Time to First Byte)**: < 800ms = dobry

#### C) Mobilność i responsywność:
- Test viewport meta tag
- Touch elements sizing (minimum 48x48px)
- Font size readability (minimum 16px dla body)
- Mobile-friendly test (symulacja różnych rozdzielczości)
- Sprawdź czy strona używa AMP (bonus points)

#### D) Bezpieczeństwo:
- **SSL/HTTPS**: certyfikat ważny, brak mixed content
- **Security headers**: 
  - Content-Security-Policy
  - X-Frame-Options
  - X-Content-Type-Options
  - Strict-Transport-Security
- Test przekierowań HTTP→HTTPS
- Sprawdź wersję TLS (minimum 1.2)

---

### **2. ELEMENTY ON-PAGE (25% wagi końcowej)**

#### A) Meta tagi - szczegółowa analiza:
- **Title Tag**:
  - Długość: 50-60 znaków = 100%, 30-50 lub 60-70 = 70%, <30 lub >70 = 30%
  - Czy zawiera brand?
  - Czy jest unikalny? (sprawdź czy nie duplikuje się z innymi stronami)
  - Pozycja słów kluczowych (im wcześniej tym lepiej)
  - Sprawdź czy nie jest przeklikowy (brak nadmiernych znakówspecjalnych)

- **Meta Description**:
  - Długość: 150-160 znaków = optimal
  - Czy zawiera Call-to-Action?
  - Czy jest unikalny?
  - Sprawdź keyword matching
  - Ocena atrakcyjności (punkty za: pytania, liczby, emocje)

- **Open Graph tags** (Facebook/social):
  - og:title, og:description, og:image, og:type
  - Twitter Card tags
  - Rozmiar i format obrazów OG (1200x630px optimal)

#### B) Struktura nagłówków:
- **Hierarchia H1-H6**:
  - Tylko jeden H1 na stronie = 100%, brak H1 = 0%, więcej niż jeden H1 = 50%
  - Czy H2-H6 są w logicznej kolejności?
  - Długość nagłówków (optimal 20-70 znaków)
  - Keyword optimization w H1 i H2
  - Sprawdź czy nagłówki są semantycznie poprawne (nie używane tylko dla stylowania)

#### C) Obrazy i multimedia:
- **Alt teksty**:
  - % obrazów z alt = score
  - Długość alt (5-125 znaków optimal)
  - Czy alt nie duplikuje dokładnie title?
  - Sprawdź czy alt nie jest keyword stuffing
  
- **Optymalizacja obrazów**:
  - Format (WebP > PNG > JPG dla web)
  - Rozmiar plików (<100KB dla obrazów hero optimal)
  - Lazy loading implementation
  - Responsive images (srcset, sizes)
  - Width/height attributes (prevent CLS)

#### D) Linki:
- **Linki wewnętrzne**:
  - Ilość linków wewnętrznych (10-50 = optimal)
  - Anchor text diversity
  - Sprawdź broken links (404)
  - Głębokość linkowania (max 3 kliknięcia od homepage)
  - Czy są linki do ważnych podstron?

- **Linki zewnętrzne**:
  - Ilość i jakość outbound links
  - Czy są rel="nofollow" tam gdzie powinny?
  - Sprawdź czy linki prowadzą do wiarygodnych źródeł
  - Test dostępności linkowanych stron

---

### **3. INDEKSOWANIE I CRAWLABILITY (20% wagi końcowej)**

#### A) Robots.txt:
- Czy istnieje? (/robots.txt)
- Czy jest poprawnie sformatowany?
- Sprawdź czy nie blokuje ważnych zasobów (CSS, JS, obrazy)
- Czy wskazuje na sitemap?
- Sprawdź dyrektywy User-agent
- Test czy nie blokuje całej strony przypadkowo

#### B) Sitemap.xml:
- Czy istnieje? (sprawdź /sitemap.xml, /sitemap_index.xml)
- Czy jest zgłoszony w robots.txt?
- Ilość URL-i w sitemap (max 50,000)
- Czy wszystkie URL zwracają 200?
- Sprawdź daty ostatniej modyfikacji
- Priority i changefreq values
- Czy jest w formacie XML (nie HTML)?

#### C) Canonical i indeksowanie:
- **Canonical tags**:
  - Czy każda strona ma canonical?
  - Czy canonical wskazuje na siebie lub właściwy URL?
  - Sprawdź czy nie ma canonical chains
  - Self-referencing canonical = best practice

- **Meta robots**:
  - Sprawdź dyrektywy index/noindex
  - follow/nofollow
  - Czy są konflikty z robots.txt?

- **Pagination**:
  - rel="next" i rel="prev" (jeśli dotyczy)
  - Sprawdź parametry URL (?page=2)

#### D) Schema Markup (Structured Data):
- Czy strona używa Schema.org?
- Typy schema: Organization, LocalBusiness, Product, Article, BreadcrumbList, FAQ, Review
- Sprawdź czy schema jest valid (JSON-LD preferred)
- Rich snippets potential (ocena potencjału do wyświetlenia)
- Open Graph i Twitter Cards compliance

---

### **4. CONTENT QUALITY & UX (20% wagi końcowej)**

#### A) Analiza treści:
- **Długość contentu**:
  - Word count: <300 = thin content (20%), 300-600 = acceptable (60%), 600-1500 = good (90%), >1500 = excellent (100%)
  - Text to HTML ratio (>15% = dobry)
  - Sprawdź czy content nie jest AI-generated (podstawowe wskaźniki)

- **Keyword optimization**:
  - Keyword density (1-3% = optimal, >5% = keyword stuffing)
  - LSI keywords presence (synonimy, powiązane terminy)
  - Keyword w pierwszym paragrafie
  - Keyword distribution (równomierne rozmieszczenie)

- **Readability**:
  - Długość zdań (average <20 słów = dobra)
  - Długość paragrafów (<150 słów)
  - Użycie list i bullet points
  - Białe przestrzenie
  - Gunning Fog Index lub Flesch Reading Ease

#### B) User Experience:
- **Nawigacja**:
  - Menu główne (czytelne, max 7 pozycji)
  - Breadcrumbs
  - Search functionality
  - Footer links

- **CTA (Call-to-Action)**:
  - Czy są widoczne CTA?
  - Ilość CTA (1-3 na stronę optimal)
  - Kontrast i visibility

- **Pop-ups i interstitials**:
  - Czy są intrusive pop-ups? (Google penalty risk)
  - Timing pop-upów (nie natychmiast)

#### C) Multimedia i engagement:
- Obecność wideo (bonus points)
- Infografiki
- Interaktywne elementy
- Social sharing buttons
- Komentarze/recenzje

---

### **5. TECHNICAL SEO ADVANCED (15% wagi końcowej)**

#### A) Architektura URL:
- **Struktura**:
  - Długość URL (<75 znaków optimal)
  - Czytelność (human-readable)
  - Separator (dash vs underscore - dash preferred)
  - Brak parametrów dynamicznych (query strings minimalizowane)
  - Lowercase vs uppercase (lowercase preferred)
  - SSL (https://)

- **URL patterns**:
  - Sprawdź trailing slash consistency
  - Duplikaty URL (www vs non-www, index.html vs /)
  - Sprawdź redirects (301 vs 302)

#### B) International SEO:
- **Hreflang tags** (jeśli multi-language):
  - Poprawność implementacji
  - Return tags
  - x-default version

- **Language detection**:
  - HTML lang attribute
  - Content-Language header

#### C) JavaScript i renderowanie:
- Czy strona używa client-side rendering (CSR) czy SSR/SSG?
- Test renderowania JavaScript (czy content jest dostępny bez JS?)
- Hydration issues
- Sprawdź lazy loading implementation

#### D) Paginacja i duplicates:
- Duplicate content detection (basic check)
- Parameter handling
- Sprawdź czy są soft 404

---

## 🎨 SYSTEM SCORINGU I PREZENTACJI WYNIKÓW

### Scoring Algorithm:

```
WYNIK KOŃCOWY = 
  (Fundamenty Techniczne × 0.20) +
  (On-Page × 0.25) +
  (Indeksowanie × 0.20) +
  (Content & UX × 0.20) +
  (Technical Advanced × 0.15)

Klasyfikacja:
90-100: EXCELLENT (zielony) 🟢
75-89: GOOD (jasnozielony) 🟡
60-74: NEEDS IMPROVEMENT (żółty) 🟠
40-59: POOR (pomarańczowy) 🔴
0-39: CRITICAL (ciemnoczerwony) ⛔
```

### Kategoryzacja problemów:

#### 🔴 KRYTYCZNE (Impact Score: 9-10):
- Brak HTTPS
- Strona nie indeksuje się (noindex)
- Brak title lub H1
- Czas ładowania >5s
- Broken strona główna
- Core Web Vitals - wszystkie failed

**Format prezentacji**:
```
❌ PROBLEM: Brak certyfikatu SSL
📊 IMPACT: 10/10 - Krytyczny wpływ na ranking i zaufanie
⏱️ CZAS NAPRAWY: 2-4 godziny
💰 WPŁYW NA BIZNES: -40% ruchu organicznego, utrata zaufania klientów
✅ ROZWIĄZANIE: Zakup i instalacja certyfikatu SSL, przekierowanie HTTP→HTTPS
💵 KOSZT: 0-500 PLN rocznie
```

#### 🟡 WAŻNE (Impact Score: 6-8):
- Słaba meta description
- Brak alt w obrazach
- Długi czas ładowania (2-5s)
- Brak schema markup
- Problemy z mobile

#### 🟢 ZALECENIA (Impact Score: 1-5):
- Optymalizacja keyword density
- Dodanie Open Graph tags
- Poprawa readability
- Dodatkowe linki wewnętrzne

---

## 📈 DASHBOARD WYNIKÓW - SZCZEGÓŁY

### 1. HERO SECTION:
```
┌─────────────────────────────────────┐
│   OGÓLNY WYNIK SEO HEALTH           │
│                                     │
│         ┌─────────┐                 │
│         │   78    │  Wykres kołowy  │
│         │  /100   │  z gradientem   │
│         └─────────┘  koloru         │
│                                     │
│   GOOD - Needs improvement          │
│   🟡 Wymaga uwagi w 12 obszarach   │
└─────────────────────────────────────┘
```

### 2. KATEGORIE - Rozwijane sekcje:

**Każda kategoria pokazuje**:
- Progress bar z wynikiem
- Liczba problemów (ikona alert)
- Rozwijalna lista szczegółów
- Quick fix recommendations

**Przykład wizualizacji**:
```
🔧 FUNDAMENTY TECHNICZNE: 85/100 ████████▌░
   ✅ 4 elementy OK | ⚠️ 2 do poprawy | ❌ 1 krytyczny
   
   [Rozwiń szczegóły ▼]
   
   → Core Web Vitals
     LCP: 2.3s ✅ | FID: 45ms ✅ | CLS: 0.08 ✅
   
   → Bezpieczeństwo
     ⚠️ Brak niektórych security headers
```

### 3. SEKCJA "QUICK WINS" - Priorytetowa:

```
⚡ SZYBKIE WYGRANE (High Impact, Low Effort)

┌────────────────────────────────────────┐
│ 1. Dodaj brakujące alt teksty         │
│    Impact: 8/10 | Czas: 30 min        │
│    Potencjał: +15% click-through      │
│    ✓ 23 obrazy bez alt wykryte        │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 2. Wydłuż meta description             │
│    Impact: 7/10 | Czas: 15 min        │
│    Potencjał: +20% CTR w SERP         │
│    ✓ Obecnie 89 znaków, dodaj 60     │
└────────────────────────────────────────┘
```

### 4. ANALIZA KONKURENCJI:

**Porównanie head-to-head**:
```
           │  TWOJA  │  Konkurent 1  │  Konkurent 2  │ LIDER
──────────────────────────────────────────────────────────────
Wynik SEO  │   78    │      82       │      91       │  95
──────────────────────────────────────────────────────────────
Load Time  │  3.2s   │     2.1s      │     1.8s      │ 1.5s
Słów       │   450   │      890      │     1,200     │ 1,500
Backlinks  │   12    │      45       │      120      │  340
Schema     │   ❌    │      ✅       │      ✅       │  ✅

📊 Jesteś 17 punktów za liderem branży
🎯 Największa luka: Content length i technical optimization
```

### 5. BUSINESS IMPACT CALCULATOR:

```
💼 CO TO ZNACZY DLA TWOJEGO BIZNESU?

Obecny ruch organiczny: ~500 odwiedzin/miesiąc (estymacja)

Po naprawie problemów KRYTYCZNYCH:
  ➜ Potencjalny wzrost: +60-80%
  ➜ Estymowany ruch: ~800-900 odwiedzin/miesiąc
  ➜ Przy konwersji 2%: +6-8 leadów/miesiąc
  ➜ Wartość: ~3,000-4,000 PLN dodatkowego przychodu*

Po implementacji WSZYSTKICH rekomendacji:
  ➜ Potencjalny wzrost: +150-200%
  ➜ Estymowany ruch: ~1,250-1,500 odwiedzin/miesiąc
  ➜ Przy konwersji 2%: +15-20 leadów/miesiąc
  ➜ Wartość: ~7,500-10,000 PLN dodatkowego przychodu*

*Założenia: średnia wartość leada 500 PLN
Czas implementacji: 3-6 miesięcy
ROI: 300-400%

[SLIDER: Dostosuj wartość leada do swoich szacunków]
```

---

## 📄 GENERATOR RAPORTÓW

### Format PDF z sekcjami:

**EXECUTIVE SUMMARY (1 strona)**:
- Ogólny wynik SEO Health Score
- Top 5 problemów krytycznych
- Potencjał wzrostu (liczby)
- Rekomendowany budżet i timeline

**TECHNICAL DEEP DIVE (2-3 strony)**:
- Wszystkie kategorie z wynikami
- Szczegółowe problemy z rozwiązaniami
- Tabele i wykresy

**ACTION PLAN (1 strona)**:
```
PLAN DZIAŁANIA - PRIORYTETYZACJA

FAZA 1 (Miesiąc 1-2): FUNDAMENTY - Budżet: 3,000-5,000 PLN
✓ Naprawa problemów krytycznych
✓ Optymalizacja Core Web Vitals
✓ Implementacja SSL i security

FAZA 2 (Miesiąc 3-4): OPTYMALIZACJA - Budżet: 4,000-6,000 PLN
✓ Przepisanie meta tagów
✓ Optymalizacja obrazów
✓ Dodanie schema markup

FAZA 3 (Miesiąc 5-6): CONTENT & GROWTH - Budżet: 5,000-8,000 PLN
✓ Rozbudowa treści
✓ Link building (podstawy)
✓ Monitoring i dostrajanie
```

**COMPETITIVE ANALYSIS (1 strona)**:
- Twoja pozycja vs top 3 konkurentów
- Gap analysis
- Opportunities

---

## 🛠️ FUNKCJE DODATKOWE

### 1. **Historical Tracking**:
- Zapisz audyt w localStorage
- Porównaj wyniki z poprzednimi audytami
- Pokaż progress timeline
- Wykres trendów

### 2. **Custom Branding**:
```javascript
const brandingConfig = {
  agencyName: "Twoja Agencja SEO",
  logo: "url_to_logo.png",
  primaryColor: "#FF6B35",
  contactInfo: {
    email: "kontakt@agencja.pl",
    phone: "+48 123 456 789"
  }
}
```

### 3. **Pricing Calculator**:
```
WYCENA USŁUG NA PODSTAWIE AUDYTU:

Wykryte problemy: 27
- Krytyczne: 5 × 800 PLN = 4,000 PLN
- Ważne: 12 × 400 PLN = 4,800 PLN
- Zalecenia: 10 × 200 PLN = 2,000 PLN

Pakiet BASIC (tylko krytyczne): 4,000 PLN
Pakiet STANDARD (+ ważne): 8,800 PLN
Pakiet PREMIUM (wszystko + monitoring): 12,500 PLN

[Możliwość edycji stawek]
```

### 4. **Email Report Sender**:
- Wygeneruj unique link do raportu
- Wyślij email z podsumowaniem
- Scheduled follow-up reminders

### 5. **Export Options**:
- **PDF** - pełny raport brandowany
- **CSV** - lista problemów do Excel
- **JSON** - dane surowe dla integracji
- **Prezentacja** - slajdy do klienta (PowerPoint style w HTML)

---

## 💡 ADVANCED FEATURES (dla wyróżnienia)

### 1. **AI-Powered Insights**:
Użyj Claude API (poprzez `fetch` w artifact) do:
- Generowania custom rekomendacji na podstawie branży
- Analiza konkurencyjnych keywords
- Sugestie content improvements
- Personalizowane action plans

**Przykład implementacji**:
```javascript
// Analiza kontekstu biznesowego
const businessContext = `
Audytowana strona: ${url}
Branża: ${industry}
Problemy: ${JSON.stringify(issues)}
`;

// Zapytaj Claude o rekomendacje
const recommendations = await getClaudeRecommendations(businessContext);
```

### 2. **Competitive Keywords Analysis**:
- Scraping meta titles konkurentów
- Analiza najczęstszych keywords
- Gap analysis - czego Ci brakuje
- Keyword difficulty estimation

### 3. **Local SEO Module** (jeśli dotyczy):
- NAP consistency check (Name, Address, Phone)
- Google Business Profile optimization tips
- Local citations
- Schema LocalBusiness

### 4. **Backlink Profile Preview** (basic):
- Estymacja ilości backlinków (poprzez API lub symulację)
- Domain Authority score approximation
- Link quality indicators

### 5. **Real-time Monitoring Dashboard**:
- Zakładaj uptime monitoring (symulacja)
- Speed tracking over time
- Ranking changes (mock data)

---

## 🎨 UX/UI BEST PRACTICES

### Design System:
```css
Kolory:
- Excellent: #10B981 (zielony)
- Good: #84CC16 (limonkowy)
- Warning: #F59E0B (pomarańczowy)
- Poor: #EF4444 (czerwony)
- Critical: #DC2626 (ciemnoczerwony)

Typography:
- Headings: Inter, bold
- Body: Inter, regular
- Mono (code): JetBrains Mono

Spacing:
- Mobile-first approach
- 8px grid system
- Generous whitespace

Animations:
- Smooth transitions (300ms ease-in-out)
- Progress bars animated
- Fade-ins dla wyników
- Skeleton loaders podczas audytu
```

### Responsive Breakpoints:
- Mobile: 320px - 640px
- Tablet: 641px - 1024px
- Desktop: 1025px+

### Accessibility:
- Minimum contrast ratio 4.5:1
- Keyboard navigation
- ARIA labels
- Screen reader friendly
- Focus indicators

---

## 📱 USER JOURNEY

### Krok 1: Landing
```
[LOGO AGENCJI]

Przeprowadź profesjonalny audyt SEO w 60 sekund

┌──────────────────────────────────────┐
│ https://                              │
│ [Wpisz URL strony do audytu]         │
└──────────────────────────────────────┘

[🚀 ROZPOCZNIJ DARMOWY AUDYT]

✓ Bez rejestracji
✓ Raport PDF gratis
✓ Szczegółowa analiza 50+ parametrów
```

### Krok 2: Audyt w toku
```
Analizuję Twoją stronę...

██████░░░░ 60% 

✅ Sprawdzono dostępność
✅ Pobrano HTML
✅ Analiza Core Web Vitals
⏳ Sprawdzanie meta tagów...
⏳ Analiza struktury...

Pozostało około 20 sekund...
```

### Krok 3: Wyniki
```
[Pełny dashboard jak opisany wyżej]

[CTA: POBIERZ PEŁNY RAPORT PDF]
[CTA: UMÓW KONSULTACJĘ]
[CTA: PORÓWNAJ Z KONKURENCJĄ]
```

---

## ⚙️ IMPLEMENTACJA TECHNICZNA

### API Calls i Data Fetching:

**1. Core check - dostępność**:
```javascript
const checkAvailability = async (url) => {
  try {
    const response = await fetch(url, { method: 'HEAD' });
    return {
      status: response.status,
      ssl: url.startsWith('https://'),
      ttfb: performance.now() // simplified
    };
  } catch (error) {
    return { available: false, error: error.message };
  }
};
```

**2. HTML Parsing**:
```javascript
const analyzeHTML = async (url) => {
  const html = await fetch(url).then(r => r.text());
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  
  return {
    title: doc.querySelector('title')?.textContent,
    metaDescription: doc.querySelector('meta[name="description"]')?.content,
    h1: doc.querySelectorAll('h1'),
    images: doc.querySelectorAll('img'),
    links: {
      internal: [...doc.querySelectorAll('a')].filter(a => a.href.includes(domain)),
      external: [...doc.querySelectorAll('a')].filter(a => !a.href.includes(domain))
    },
    // ... więcej
  };
};
```

**3. PageSpeed Insights**:
```javascript
const API_KEY = 'YOUR_KEY'; // instrukcja jak uzyskać
const analyzeSpeed = async (url) => {
  const endpoint = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${url}&key=${API_KEY}`;
  const response = await fetch(endpoint);
  const data = await response.json();
  
  return {
    lcp: data.lighthouseResult.audits['largest-contentful-paint'].numericValue,
    fid: data.lighthouseResult.audits['max-potential-fid'].numericValue,
    cls: data.lighthouseResult.audits['cumulative-layout-shift'].numericValue,
    performance: data.lighthouseResult.categories.performance.score * 100
  };
};
```

### Error Handling:
- Try-catch dla wszystkich API calls
- Fallback values jeśli API fails
- User-friendly error messages
- Retry logic dla timeoutów

### Performance Optimization:
- Debouncing URL input
- Async/await dla równoległych sprawdzeń
- Cache results in localStorage (24h)
- Lazy loading dla wyników
- Progressive enhancement

---

## 📚 TERMINOLOGIA - TOOLTIPS

Każdy termin techniczny powinien mieć tooltip z wyjaśnieniem:

```javascript
const glossary = {
  "Core Web Vitals": "Metryki Google mierzące doświadczenie użytkownika: szybkość ładowania, interaktywność i stabilność wizualną",
  "LCP": "Largest Contentful Paint - czas do wyświetlenia głównego elementu strony (obrazek, nagłówek). Powinien być <2.5s",
  "Meta Description": "Krótki opis strony wyświetlany w wynikach Google. Wpływa na CTR ale nie ranking.",
  // ... wszystkie terminy
};
```

---

## ✅ CHECKLIST PRZED WYDANIEM

- [ ] Wszystkie API calls działają z error handling
- [ ] Responsywny design (mobile-first)
- [ ] Loading states i skeleton screens
- [ ] Tooltips dla terminów technicznych
- [ ] PDF generator działa
- [ ] Branding customization działa
- [ ] Results są zapisywane w localStorage
- [ ] Accessibility: WCAG 2.1 AA
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Performance: Lighthouse score >90
- [ ] SEO: Meta tags dla samego narzędzia
- [ ] Analytics tracking (opcjonalnie)

---

**DODATKOWE WSKAZÓWKI DLA IMPLEMENTACJI**:

1. **Rozpocznij od MVP**: Zaimplementuj podstawowe kategorie audytu, potem dodawaj advanced features

2. **Mock data dla testów**: Przygotuj przykładowe wyniki do testowania UI bez rzeczywistych API calls

3. **Progresywna walidacja**: Dodaj walidację URL przed rozpoczęciem audytu

4. **Instrukcje dla użytkownika**: Dodaj sekcję "Jak korzystać" i FAQ

5. **Legal**: Disclaimer o charakterze informacyjnym wyników

Aplikacja powinna być **production-ready**, wizualnie **na poziomie SaaS tools**, i dostarczać **actionable insights** które można pokazać klientowi podczas spotkania sprzedażowego.


# ZAŁĄCZNIK: IMPLEMENTACJA MVP - WERSJA W 100% DARMOWA

## 🎯 ZAKRES MVP (Minimum Viable Product)

### Wdrażane funkcje z głównego planu:

**✅ KATEGORIA 1: FUNDAMENTY TECHNICZNE (20%)**
- Status HTTP i dostępność
- TTFB (Time to First Byte)
- SSL/HTTPS check
- Security headers
- Core Web Vitals via Google PageSpeed Insights API

**✅ KATEGORIA 2: ON-PAGE (25%)**
- Title tag (długość, struktura)
- Meta description (długość, jakość)
- Nagłówki H1-H6 (hierarchia, ilość)
- Alt teksty w obrazach
- Open Graph tags
- Linki wewnętrzne/zewnętrzne
- Broken links check

**✅ KATEGORIA 3: INDEKSOWANIE (20%)**
- Robots.txt (dostępność, analiza)
- Sitemap.xml (dostępność, analiza)
- Canonical tags
- Meta robots
- Schema markup detection (JSON-LD)

**✅ KATEGORIA 4: CONTENT & UX (20%)**
- Word count
- Keyword density
- Readability score (Flesch Reading Ease)
- Paragraph/sentence length
- Text-to-HTML ratio

**✅ KATEGORIA 5: TECHNICAL ADVANCED (15%)**
- URL structure analysis
- HTML lang attribute
- Viewport meta tag
- Image optimization (sizes, formats)

---

## 🔧 STACK TECHNICZNY - BIBLIOTEKI

### Python Backend (dla zbierania danych):

```bash
pip install requests beautifulsoup4 lxml textstat validators urllib3
```

**Biblioteki:**
- `requests` - HTTP requests, pobranie HTML, API calls
- `beautifulsoup4` - parsing HTML
- `lxml` - szybszy parser dla BS4
- `textstat` - readability scores
- `validators` - walidacja URL
- `urllib3` - dodatkowe funkcje URL

### Frontend (React):

```bash
# Już dostępne w artifacts:
- React (z Hooks)
- Recharts (wykresy)
- Tailwind CSS (styling)
- Lucide React (ikony)
```

---

## 📋 INSTRUKCJA: GOOGLE PAGESPEED INSIGHTS API

### Krok 1: Utworzenie API Key (5 minut)

1. **Przejdź do Google Cloud Console:**
   - https://console.cloud.google.com/

2. **Zaloguj się** (konto Gmail)

3. **Utwórz nowy projekt:**
   - Kliknij dropdown przy logo Google Cloud (góra)
   - "New Project"
   - Nazwa: "SEO Audit Tool"
   - Kliknij "Create"

4. **Włącz PageSpeed Insights API:**
   - W menu bocznym: "APIs & Services" > "Library"
   - Wyszukaj: "PageSpeed Insights API"
   - Kliknij kartę API
   - Przycisk "ENABLE"

5. **Wygeneruj API Key:**
   - "APIs & Services" > "Credentials"
   - "+ CREATE CREDENTIALS" > "API key"
   - Skopiuj klucz (zapisz bezpiecznie!)

6. **Zabezpiecz klucz (opcjonalnie):**
   - Kliknij na nazwę klucza
   - "API restrictions" > wybierz "Restrict key"
   - Zaznacz tylko "PageSpeed Insights API"
   - Save

### Limity darmowe:
- **25,000 zapytań/dzień**
- **Bez kosztów**
- Wystarczy dla ~800 audytów dziennie (zakładając 30 requestów per audyt)

### Użycie w kodzie:

```python
API_KEY = "YOUR_API_KEY_HERE"
url_to_test = "https://example.com"

endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url_to_test}&key={API_KEY}&strategy=mobile"

response = requests.get(endpoint)
data = response.json()
```

---

## 💻 IMPLEMENTACJA KROK PO KROKU

### STRUKTURA PROJEKTU:

```
seo-audit-tool/
├── backend/
│   ├── audit_engine.py          # Główna logika audytu
│   ├── analyzers/
│   │   ├── technical.py         # Analiza techniczna
│   │   ├── onpage.py            # Analiza on-page
│   │   ├── indexing.py          # Robots, sitemap
│   │   ├── content.py           # Content analysis
│   │   └── pagespeed.py         # Google PSI API
│   └── utils.py                 # Helpery
├── frontend/
│   └── SEOAuditApp.jsx          # React artifact
└── config.py                     # API keys, settings
```

---

## 📝 KOD IMPLEMENTACJI

### 1. **config.py** - Konfiguracja

```python
# config.py

# Google PageSpeed Insights API
GOOGLE_PSI_API_KEY = "YOUR_API_KEY_HERE"  # Wstaw swój klucz

# Timeouts
REQUEST_TIMEOUT = 10  # sekundy
PSI_TIMEOUT = 30  # PSI może trwać dłużej

# User agent
USER_AGENT = "SEO-Audit-Tool/1.0 (Educational Purpose)"

# Scoring weights
WEIGHTS = {
    "technical": 0.20,
    "onpage": 0.25,
    "indexing": 0.20,
    "content": 0.20,
    "advanced": 0.15
}

# Thresholds
THRESHOLDS = {
    "title_length_optimal": (50, 60),
    "meta_desc_optimal": (150, 160),
    "page_speed_good": 2500,  # ms
    "word_count_min": 300,
    "word_count_good": 600,
    "keyword_density_optimal": (1, 3)  # %
}
```

### 2. **utils.py** - Funkcje pomocnicze

```python
# utils.py
import requests
import validators
from urllib.parse import urlparse, urljoin
from config import REQUEST_TIMEOUT, USER_AGENT

def validate_url(url):
    """Walidacja i normalizacja URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if validators.url(url):
        return url
    return None

def get_domain(url):
    """Wyciągnij domenę z URL"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def fetch_url(url, timeout=REQUEST_TIMEOUT):
    """Pobierz URL z error handling"""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        return {
            'success': True,
            'status_code': response.status_code,
            'content': response.text,
            'headers': dict(response.headers),
            'url': response.url,  # final URL po redirectach
            'elapsed': response.elapsed.total_seconds()
        }
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Timeout'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}

def is_internal_link(link_url, base_domain):
    """Sprawdź czy link jest wewnętrzny"""
    if not link_url:
        return False
    link_domain = urlparse(link_url).netloc
    base = urlparse(base_domain).netloc
    return link_domain == base or link_domain == ''

def calculate_score(value, min_val, max_val, reverse=False):
    """Oblicz score 0-100 na podstawie wartości"""
    if reverse:
        value = max_val - value + min_val
    
    if value <= min_val:
        return 0
    elif value >= max_val:
        return 100
    else:
        return int(((value - min_val) / (max_val - min_val)) * 100)
```

### 3. **analyzers/technical.py** - Analiza techniczna

```python
# analyzers/technical.py
import requests
from utils import fetch_url, get_domain

def analyze_technical(url, page_data):
    """Analiza fundamentów technicznych"""
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }
    
    # 1. Status HTTP i dostępność
    if page_data['success']:
        results['checks']['http_status'] = {
            'value': page_data['status_code'],
            'pass': page_data['status_code'] == 200,
            'score': 100 if page_data['status_code'] == 200 else 0
        }
        
        if page_data['status_code'] != 200:
            results['issues'].append({
                'severity': 'critical',
                'title': f'Status HTTP: {page_data["status_code"]}',
                'impact': 10,
                'description': 'Strona nie jest dostępna lub zwraca błąd'
            })
    else:
        results['checks']['http_status'] = {'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'critical',
            'title': 'Strona niedostępna',
            'impact': 10,
            'description': page_data.get('error', 'Nie można pobrać strony')
        })
        return results
    
    # 2. SSL/HTTPS
    is_https = url.startswith('https://')
    results['checks']['ssl'] = {
        'value': is_https,
        'pass': is_https,
        'score': 100 if is_https else 0
    }
    
    if not is_https:
        results['issues'].append({
            'severity': 'critical',
            'title': 'Brak certyfikatu SSL',
            'impact': 10,
            'description': 'Strona nie używa HTTPS - krytyczne dla SEO i bezpieczeństwa',
            'fix': 'Zainstaluj certyfikat SSL (darmowy: Let\'s Encrypt) i przekieruj HTTP→HTTPS'
        })
    
    # 3. TTFB (Time to First Byte)
    ttfb = page_data['elapsed'] * 1000  # w milisekundach
    results['checks']['ttfb'] = {
        'value': f"{ttfb:.0f}ms",
        'pass': ttfb < 600,
        'score': 100 if ttfb < 600 else (50 if ttfb < 1200 else 0)
    }
    
    if ttfb > 1200:
        results['issues'].append({
            'severity': 'important',
            'title': f'Wolny czas odpowiedzi serwera: {ttfb:.0f}ms',
            'impact': 7,
            'description': 'TTFB powinien być <600ms. Wpływa na user experience.',
            'fix': 'Optymalizuj serwer, rozważ CDN, włącz caching'
        })
    
    # 4. Security Headers
    headers = page_data.get('headers', {})
    security_headers = {
        'Strict-Transport-Security': 'HSTS',
        'X-Content-Type-Options': 'X-Content-Type',
        'X-Frame-Options': 'X-Frame',
        'Content-Security-Policy': 'CSP'
    }
    
    missing_headers = []
    for header, name in security_headers.items():
        if header not in headers:
            missing_headers.append(name)
    
    results['checks']['security_headers'] = {
        'value': f"{len(security_headers) - len(missing_headers)}/{len(security_headers)}",
        'pass': len(missing_headers) == 0,
        'score': int(((len(security_headers) - len(missing_headers)) / len(security_headers)) * 100)
    }
    
    if missing_headers:
        results['issues'].append({
            'severity': 'recommendation',
            'title': f'Brakuje {len(missing_headers)} security headers',
            'impact': 4,
            'description': f'Brak: {", ".join(missing_headers)}',
            'fix': 'Dodaj security headers w konfiguracji serwera'
        })
    
    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0
    
    return results
```

### 4. **analyzers/onpage.py** - Analiza On-Page

```python
# analyzers/onpage.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import THRESHOLDS
from utils import is_internal_link, get_domain

def analyze_onpage(url, html_content):
    """Analiza elementów on-page"""
    soup = BeautifulSoup(html_content, 'lxml')
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }
    
    # 1. Title Tag
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text().strip()
        title_length = len(title_text)
        optimal_min, optimal_max = THRESHOLDS['title_length_optimal']
        
        if optimal_min <= title_length <= optimal_max:
            title_score = 100
            title_pass = True
        elif 30 <= title_length < optimal_min or optimal_max < title_length <= 70:
            title_score = 70
            title_pass = False
            results['issues'].append({
                'severity': 'important',
                'title': 'Title tag poza optymalną długością',
                'impact': 7,
                'description': f'Długość: {title_length} znaków. Optimal: {optimal_min}-{optimal_max}',
                'fix': f'{"Skróć" if title_length > optimal_max else "Wydłuż"} title do {optimal_min}-{optimal_max} znaków'
            })
        else:
            title_score = 30
            title_pass = False
            results['issues'].append({
                'severity': 'critical',
                'title': 'Title tag zbyt krótki/długi',
                'impact': 9,
                'description': f'Długość: {title_length} znaków. Drastycznie poza normą.',
                'fix': f'Przepisz title tag do długości {optimal_min}-{optimal_max} znaków'
            })
        
        results['checks']['title'] = {
            'value': f"{title_length} znaków",
            'text': title_text[:60] + '...' if len(title_text) > 60 else title_text,
            'pass': title_pass,
            'score': title_score
        }
    else:
        results['checks']['title'] = {'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'critical',
            'title': 'Brak title tag',
            'impact': 10,
            'description': 'Title tag jest fundamentem SEO - musi istnieć na każdej stronie',
            'fix': 'Dodaj <title>Twój Tytuł</title> w <head>'
        })
    
    # 2. Meta Description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc_text = meta_desc.get('content').strip()
        desc_length = len(desc_text)
        optimal_min, optimal_max = THRESHOLDS['meta_desc_optimal']
        
        desc_score = 100 if optimal_min <= desc_length <= optimal_max else 50
        results['checks']['meta_description'] = {
            'value': f"{desc_length} znaków",
            'text': desc_text[:80] + '...' if len(desc_text) > 80 else desc_text,
            'pass': optimal_min <= desc_length <= optimal_max,
            'score': desc_score
        }
        
        if desc_length < optimal_min or desc_length > optimal_max:
            results['issues'].append({
                'severity': 'important',
                'title': 'Meta description poza optymalną długością',
                'impact': 6,
                'description': f'Długość: {desc_length}. Optimal: {optimal_min}-{optimal_max}',
                'fix': 'Dostosuj długość meta description i dodaj CTA'
            })
    else:
        results['checks']['meta_description'] = {'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'important',
            'title': 'Brak meta description',
            'impact': 7,
            'description': 'Meta description wpływa na CTR w wynikach wyszukiwania',
            'fix': 'Dodaj <meta name="description" content="...">'
        })
    
    # 3. Nagłówki H1-H6
    h1_tags = soup.find_all('h1')
    h1_count = len(h1_tags)
    
    if h1_count == 1:
        h1_score = 100
        h1_pass = True
        h1_text = h1_tags[0].get_text().strip()
        results['checks']['h1'] = {
            'value': f"1 H1 (✓)",
            'text': h1_text[:60] + '...' if len(h1_text) > 60 else h1_text,
            'pass': True,
            'score': 100
        }
    elif h1_count == 0:
        results['checks']['h1'] = {'value': 'Brak H1', 'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'critical',
            'title': 'Brak nagłówka H1',
            'impact': 9,
            'description': 'H1 jest kluczowy dla struktury i SEO',
            'fix': 'Dodaj jeden nagłówek H1 z głównym tematem strony'
        })
    else:
        results['checks']['h1'] = {
            'value': f"{h1_count} H1 (za dużo)",
            'pass': False,
            'score': 50
        }
        results['issues'].append({
            'severity': 'important',
            'title': f'Więcej niż jeden H1 ({h1_count})',
            'impact': 6,
            'description': 'Powinna być tylko jedna H1 na stronie',
            'fix': 'Zostaw jedną H1, resztę zamień na H2'
        })
    
    # Hierarchia H2-H6
    heading_structure = {
        'h2': len(soup.find_all('h2')),
        'h3': len(soup.find_all('h3')),
        'h4': len(soup.find_all('h4')),
        'h5': len(soup.find_all('h5')),
        'h6': len(soup.find_all('h6'))
    }
    
    results['checks']['heading_structure'] = {
        'value': f"H2:{heading_structure['h2']}, H3:{heading_structure['h3']}",
        'pass': heading_structure['h2'] > 0,
        'score': 100 if heading_structure['h2'] > 0 else 70
    }
    
    # 4. Obrazy i Alt teksty
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]
    alt_percentage = (len(images_with_alt) / len(images) * 100) if images else 100
    
    results['checks']['images_alt'] = {
        'value': f"{len(images_with_alt)}/{len(images)} z alt",
        'pass': alt_percentage >= 90,
        'score': int(alt_percentage)
    }
    
    if alt_percentage < 90 and len(images) > 0:
        missing_alt = len(images) - len(images_with_alt)
        results['issues'].append({
            'severity': 'important' if alt_percentage < 50 else 'recommendation',
            'title': f'{missing_alt} obrazów bez alt',
            'impact': 8 if alt_percentage < 50 else 5,
            'description': f'{missing_alt} z {len(images)} obrazów nie ma alt tekstu',
            'fix': 'Dodaj opisowe alt teksty do wszystkich obrazów'
        })
    
    # 5. Open Graph tags
    og_tags = {
        'og:title': soup.find('meta', property='og:title'),
        'og:description': soup.find('meta', property='og:description'),
        'og:image': soup.find('meta', property='og:image'),
        'og:type': soup.find('meta', property='og:type')
    }
    
    og_present = sum(1 for tag in og_tags.values() if tag)
    results['checks']['open_graph'] = {
        'value': f"{og_present}/4 OG tags",
        'pass': og_present >= 3,
        'score': int((og_present / 4) * 100)
    }
    
    if og_present < 3:
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Niekompletne Open Graph tags',
            'impact': 4,
            'description': f'Brak {4 - og_present} podstawowych OG tagów dla social media',
            'fix': 'Dodaj og:title, og:description, og:image, og:type'
        })
    
    # 6. Linki
    all_links = soup.find_all('a', href=True)
    base_domain = get_domain(url)
    
    internal_links = [link for link in all_links if is_internal_link(link['href'], base_domain)]
    external_links = [link for link in all_links if not is_internal_link(link['href'], base_domain)]
    
    results['checks']['links'] = {
        'value': f"Wew: {len(internal_links)}, Zew: {len(external_links)}",
        'pass': 5 <= len(internal_links) <= 100,
        'score': 100 if 10 <= len(internal_links) <= 50 else 70
    }
    
    if len(internal_links) < 5:
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Mało linków wewnętrznych',
            'impact': 5,
            'description': f'Tylko {len(internal_links)} linków wewnętrznych',
            'fix': 'Dodaj więcej linków do innych podstron (10-30 optimal)'
        })
    
    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0
    
    return results
```

### 5. **analyzers/indexing.py** - Robots i Sitemap

```python
# analyzers/indexing.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

def analyze_indexing(url, html_content):
    """Analiza crawlability i indexing"""
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }
    
    soup = BeautifulSoup(html_content, 'lxml')
    base_domain = url.rstrip('/')
    
    # 1. Robots.txt
    robots_url = urljoin(base_domain, '/robots.txt')
    try:
        robots_response = requests.get(robots_url, timeout=5)
        if robots_response.status_code == 200:
            robots_content = robots_response.text
            
            # Sprawdź czy nie blokuje wszystkiego
            blocks_all = 'Disallow: /' in robots_content and 'User-agent: *' in robots_content
            has_sitemap = 'Sitemap:' in robots_content
            
            results['checks']['robots_txt'] = {
                'value': 'Istnieje ✓',
                'pass': not blocks_all,
                'score': 100 if (not blocks_all and has_sitemap) else 70,
                'content_preview': robots_content[:200]
            }
            
            if blocks_all:
                results['issues'].append({
                    'severity': 'critical',
                    'title': 'Robots.txt blokuje całą stronę',
                    'impact': 10,
                    'description': 'User-agent: * + Disallow: / blokuje indeksowanie',
                    'fix': 'NATYCHMIAST usuń lub popraw robots.txt!'
                })
            
            if not has_sitemap:
                results['issues'].append({
                    'severity': 'recommendation',
                    'title': 'Robots.txt nie wskazuje sitemap',
                    'impact': 3,
                    'description': 'Brak linku do sitemap.xml w robots.txt',
                    'fix': 'Dodaj linię: Sitemap: https://domain.com/sitemap.xml'
                })
        else:
            results['checks']['robots_txt'] = {
                'value': 'Brak (404)',
                'pass': True,  # Brak robots.txt nie jest błędem
                'score': 80
            }
            results['issues'].append({
                'severity': 'recommendation',
                'title': 'Brak robots.txt',
                'impact': 2,
                'description': 'Warto utworzyć robots.txt dla kontroli crawlingu',
                'fix': 'Utwórz podstawowy robots.txt ze wskazaniem sitemap'
            })
    except:
        results['checks']['robots_txt'] = {'value': 'Error', 'pass': False, 'score': 50}
    
    # 2. Sitemap.xml
    sitemap_url = urljoin(base_domain, '/sitemap.xml')
    try:
        sitemap_response = requests.get(sitemap_url, timeout=5)
        if sitemap_response.status_code == 200:
            # Spróbuj sparsować XML
            try:
                root = ET.fromstring(sitemap_response.content)
                # Policz URLe
                url_count = len(root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
                
                results['checks']['sitemap'] = {
                    'value': f'Istnieje ({url_count} URLs)',
                    'pass': True,
                    'score': 100
                }
                
                if url_count > 50000:
                    results['issues'].append({
                        'severity': 'important',
                        'title': 'Sitemap zbyt duża',
                        'impact': 6,
                        'description': f'{url_count} URLs (max 50,000)',
                        'fix': 'Podziel sitemap na mniejsze pliki (sitemap index)'
                    })
            except:
                results['checks']['sitemap'] = {
                    'value': 'Istnieje (niepoprawny XML)',
                    'pass': False,
                    'score': 50
                }
                results['issues'].append({
                    'severity': 'important',
                    'title': 'Sitemap niepoprawny',
                    'impact': 7,
                    'description': 'Sitemap istnieje ale ma błędy składni XML',
                    'fix': 'Napraw składnię XML w sitemap.xml'
                })
        else:
            results['checks']['sitemap'] = {
                'value': 'Brak (404)',
                'pass': False,
                'score': 0
            }
            results['issues'].append({
                'severity': 'critical',
                'title': 'Brak sitemap.xml',
                'impact': 8,
                'description': 'Sitemap pomaga Google crawlować stronę',
                'fix': 'Wygeneruj i opublikuj sitemap.xml'
            })
    except:
        results['checks']['sitemap'] = {'value': 'Error', 'pass': False, 'score': 0}
    
    # 3. Canonical tag
    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        canonical_url = canonical.get('href')
        results['checks']['canonical'] = {
            'value': 'Istnieje ✓',
            'pass': True,
            'score': 100,
            'url': canonical_url
        }
    else:
        results['checks']['canonical'] = {
            'value': 'Brak',
            'pass': False,
            'score': 60
        }
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Brak canonical tag',
            'impact': 5,
            'description': 'Canonical zapobiega duplicate content',
            'fix': 'Dodaj <link rel="canonical" href="URL"> w <head>'
        })
    
    # 4. Meta robots
    meta_robots = soup.find('meta', attrs={'name': 'robots'})
    if meta_robots:
        content = meta_robots.get('content', '').lower()
        is_noindex = 'noindex' in content
        
        results['checks']['meta_robots'] = {
            'value': content,
            'pass': not is_noindex,
            'score': 0 if is_noindex else 100
        }
        
        if is_noindex:
            results['issues'].append({
                'severity': 'critical',
                'title': 'Strona ma meta noindex!',
                'impact': 10,
                'description': 'Meta robots="noindex" blokuje indeksowanie',
                'fix': 'NATYCHMIAST usuń noindex lub zmień na index'
            })
    else:
        results['checks']['meta_robots'] = {
            'value': 'Brak (index by default)',
            'pass': True,
            'score': 100
        }
    
    # 5. Schema Markup (JSON-LD)
    schema_scripts = soup.find_all('script', type='application/ld+json')
    schema_count = len(schema_scripts)
    
    results['checks']['schema_markup'] = {
        'value': f'{schema_count} schema' if schema_count > 0 else 'Brak',
        'pass': schema_count > 0,
        'score': 100 if schema_count > 0 else 40
    }
    
    if schema_count == 0:
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Brak Schema Markup',
            'impact': 6,
            'description': 'Schema.org daje rich snippets w Google',
            'fix': 'Dodaj JSON-LD schema (Organization, Article, etc.)'
        })
    
    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0
    
    return results
```

### 6. **analyzers/content.py** - Analiza treści

```python
# analyzers/content.py
from bs4 import BeautifulSoup
import textstat
import re
from collections import Counter

def analyze_content(html_content):
    """Analiza jakości contentu"""
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Usuń script i style z analizy
    for script in soup(['script', 'style', 'nav', 'footer', 'header']):
        script.decompose()
    
    # Wyciągnij tekst
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)  # Normalizuj białe znaki
    
    # 1. Word count
    words = text.split()
    word_count = len(words)
    
    if word_count >= 1500:
        wc_score = 100
        wc_severity = None
    elif word_count >= 600:
        wc_score = 90
        wc_severity = None
    elif word_count >= 300:
        wc_score = 60
        wc_severity = 'recommendation'
    else:
        wc_score = 20
        wc_severity = 'important'
    
    results['checks']['word_count'] = {
        'value': f'{word_count} słów',
        'pass': word_count >= 300,
        'score': wc_score
    }
    
    if wc_severity:
        results['issues'].append({
            'severity': wc_severity,
            'title': f'{"Zbyt" if word_count < 300 else "Mało"} treści: {word_count} słów',
            'impact': 8 if word_count < 300 else 5,
            'description': f'Optimal: 600-1500+ słów. Thin content = słabe SEO.',
            'fix': 'Rozbuduj content do minimum 600 słów wartościowej treści'
        })
    
    # 2. Text-to-HTML ratio
    html_size = len(html_content)
    text_size = len(text)
    ratio = (text_size / html_size * 100) if html_size > 0 else 0
    
    results['checks']['text_html_ratio'] = {
        'value': f'{ratio:.1f}%',
        'pass': ratio >= 15,
        'score': 100 if ratio >= 15 else int(ratio / 15 * 100)
    }
    
    if ratio < 15:
        results['issues'].append({
            'severity': 'recommendation',
            'title': f'Niski text-to-HTML ratio: {ratio:.1f}%',
            'impact': 4,
            'description': 'Za dużo kodu, za mało tekstu (optimal >15%)',
            'fix': 'Dodaj więcej content lub uprość HTML'
        })
    
    # 3. Readability (Flesch Reading Ease dla angielskiego, approx dla PL)
    if word_count > 50:
        try:
            # textstat domyślnie dla EN, ale daje orientacyjną wartość
            reading_ease = textstat.flesch_reading_ease(text)
            
            # Interpretacja (im wyższy wynik tym łatwiejszy tekst)
            if reading_ease >= 60:
                read_score = 100
                read_label = 'Łatwy'
            elif reading_ease >= 50:
                read_score = 80
                read_label = 'Średni'
            else:
                read_score = 60
                read_label = 'Trudny'
            
            results['checks']['readability'] = {
                'value': f'{reading_ease:.0f} ({read_label})',
                'pass': reading_ease >= 50,
                'score': read_score
            }
            
            if reading_ease < 50:
                results['issues'].append({
                    'severity': 'recommendation',
                    'title': 'Tekst trudny w czytaniu',
                    'impact': 3,
                    'description': f'Readability score: {reading_ease:.0f} (im wyższy tym lepiej)',
                    'fix': 'Używaj krótszych zdań i prostszego języka'
                })
        except:
            results['checks']['readability'] = {'value': 'N/A', 'pass': True, 'score': 70}
    else:
        results['checks']['readability'] = {'value': 'Za mało tekstu', 'pass': False, 'score': 0}
    
    # 4. Keyword density (przykład - wykryj najpopularniejsze słowa)
    # Usuń stop words (uproszczona wersja)
    stop_words = {'i', 'w', 'z', 'na', 'do', 'się', 'to', 'że', 'po', 'jest', 'być', 'o', 'ale', 'dla', 'od', 'przez', 'oraz', 'jak', 'jako', 'więcej', 'też', 'już', 'tylko', 'bardzo', 'był', 'może', 'można', 'we', 'ze', 'and', 'the', 'a', 'an', 'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'is', 'are', 'was', 'were'}
    
    clean_words = [word.lower() for word in words if len(word) > 3 and word.lower() not in stop_words]
    
    if clean_words:
        word_freq = Counter(clean_words)
        top_keywords = word_freq.most_common(5)
        top_word, top_count = top_keywords[0] if top_keywords else ('N/A', 0)
        
        keyword_density = (top_count / len(words) * 100) if words else 0
        
        results['checks']['keyword_density'] = {
            'value': f'{keyword_density:.1f}% ("{top_word}")',
            'pass': 1 <= keyword_density <= 3,
            'score': 100 if 1 <= keyword_density <= 3 else (50 if keyword_density < 5 else 0),
            'top_keywords': [(kw, cnt) for kw, cnt in top_keywords]
        }
        
        if keyword_density > 5:
            results['issues'].append({
                'severity': 'important',
                'title': f'Keyword stuffing: "{top_word}" ({keyword_density:.1f}%)',
                'impact': 7,
                'description': 'Zbyt wysoka gęstość słowa kluczowego (>5% = spam)',
                'fix': 'Użyj synonimy i bardziej naturalnego języka'
            })
    else:
        results['checks']['keyword_density'] = {'value': 'N/A', 'pass': True, 'score': 70}
    
    # 5. Paragraph analysis
    paragraphs = soup.find_all('p')
    long_paragraphs = [p for p in paragraphs if len(p.get_text().split()) > 150]
    
    results['checks']['paragraphs'] = {
        'value': f'{len(paragraphs)} paragrafów',
        'pass': len(long_paragraphs) < len(paragraphs) * 0.3,
        'score': 100 if len(long_paragraphs) == 0 else 70
    }
    
    if len(long_paragraphs) > 0:
        results['issues'].append({
            'severity': 'recommendation',
            'title': f'{len(long_paragraphs)} długich paragrafów (>150 słów)',
            'impact': 3,
            'description': 'Długie paragrafy utrudniają czytanie',
            'fix': 'Podziel długie paragrafy na krótsze (50-100 słów)'
        })
    
    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0
    
    return results
```

### 7. **analyzers/pagespeed.py** - Google PSI API

```python
# analyzers/pagespeed.py
import requests
from config import GOOGLE_PSI_API_KEY, PSI_TIMEOUT

def analyze_pagespeed(url):
    """Analiza Core Web Vitals via Google PageSpeed Insights API"""
    results = {
        'score': 0,
        'checks': {},
        'issues': [],
        'mobile': {},
        'desktop': {}
    }
    
    # Sprawdź mobilną wersję
    try:
        mobile_data = fetch_psi_data(url, 'mobile')
        results['mobile'] = parse_psi_data(mobile_data)
        results['checks']['mobile_performance'] = {
            'value': f"{results['mobile']['performance_score']}/100",
            'pass': results['mobile']['performance_score'] >= 50,
            'score': results['mobile']['performance_score']
        }
        
        # Core Web Vitals issues
        cwv = results['mobile']['core_web_vitals']
        
        # LCP
        if cwv['lcp']['value'] > 2500:
            results['issues'].append({
                'severity': 'critical' if cwv['lcp']['value'] > 4000 else 'important',
                'title': f"Wolne LCP: {cwv['lcp']['value']/1000:.1f}s (mobile)",
                'impact': 9 if cwv['lcp']['value'] > 4000 else 7,
                'description': 'Largest Contentful Paint powinien być <2.5s',
                'fix': 'Optymalizuj obrazy, użyj CDN, zminifikuj CSS/JS'
            })
        
        # CLS
        if cwv['cls']['value'] > 0.1:
            results['issues'].append({
                'severity': 'important' if cwv['cls']['value'] > 0.25 else 'recommendation',
                'title': f"Problemy z CLS: {cwv['cls']['value']:.3f} (mobile)",
                'impact': 7 if cwv['cls']['value'] > 0.25 else 5,
                'description': 'Cumulative Layout Shift powinien być <0.1',
                'fix': 'Dodaj wymiary do obrazów, zarezerwuj miejsce dla ads'
            })
        
        # FID/INP
        if cwv['fid']['value'] > 100:
            results['issues'].append({
                'severity': 'important',
                'title': f"Wolna interaktywność: {cwv['fid']['value']}ms (mobile)",
                'impact': 6,
                'description': 'First Input Delay powinien być <100ms',
                'fix': 'Zmniejsz JavaScript, użyj code splitting, defer scripts'
            })
        
    except Exception as e:
        results['checks']['mobile_performance'] = {
            'value': 'Error',
            'pass': False,
            'score': 0,
            'error': str(e)
        }
        results['issues'].append({
            'severity': 'important',
            'title': 'Nie udało się pobrać danych PageSpeed',
            'impact': 5,
            'description': f'Error: {str(e)[:100]}',
            'fix': 'Sprawdź API key lub spróbuj ponownie'
        })
    
    # Oblicz score
    if results['mobile']:
        results['score'] = results['mobile']['performance_score']
    else:
        results['score'] = 0
    
    return results

def fetch_psi_data(url, strategy='mobile'):
    """Pobierz dane z PageSpeed Insights API"""
    endpoint = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    
    params = {
        'url': url,
        'key': GOOGLE_PSI_API_KEY,
        'strategy': strategy,  # mobile lub desktop
        'category': 'performance'
    }
    
    response = requests.get(endpoint, params=params, timeout=PSI_TIMEOUT)
    response.raise_for_status()
    
    return response.json()

def parse_psi_data(data):
    """Parsuj dane z PSI API"""
    lighthouse = data.get('lighthouseResult', {})
    audits = lighthouse.get('audits', {})
    
    # Performance score
    perf_score = int(lighthouse.get('categories', {}).get('performance', {}).get('score', 0) * 100)
    
    # Core Web Vitals
    lcp_audit = audits.get('largest-contentful-paint', {})
    fid_audit = audits.get('max-potential-fid', {})
    cls_audit = audits.get('cumulative-layout-shift', {})
    
    return {
        'performance_score': perf_score,
        'core_web_vitals': {
            'lcp': {
                'value': lcp_audit.get('numericValue', 0),
                'displayValue': lcp_audit.get('displayValue', 'N/A')
            },
            'fid': {
                'value': fid_audit.get('numericValue', 0),
                'displayValue': fid_audit.get('displayValue', 'N/A')
            },
            'cls': {
                'value': cls_audit.get('numericValue', 0),
                'displayValue': cls_audit.get('displayValue', 'N/A')
            }
        },
        'opportunities': [
            {
                'title': opp.get('title', ''),
                'description': opp.get('description', ''),
                'savings': opp.get('numericValue', 0)
            }
            for key, opp in audits.items()
            if opp.get('details', {}).get('type') == 'opportunity'
        ][:5]  # Top 5 opportunities
    }
```

### 8. **audit_engine.py** - Główna logika

```python
# audit_engine.py
from utils import validate_url, fetch_url
from analyzers.technical import analyze_technical
from analyzers.onpage import analyze_onpage
from analyzers.indexing import analyze_indexing
from analyzers.content import analyze_content
from analyzers.pagespeed import analyze_pagespeed
from config import WEIGHTS

def run_audit(url):
    """Uruchom pełny audyt SEO"""
    
    # 1. Walidacja URL
    url = validate_url(url)
    if not url:
        return {'error': 'Invalid URL'}
    
    # 2. Pobierz stronę
    print(f"Fetching {url}...")
    page_data = fetch_url(url)
    
    if not page_data['success']:
        return {
            'error': 'Cannot fetch page',
            'details': page_data.get('error')
        }
    
    html_content = page_data['content']
    
    # 3. Uruchom wszystkie analizatory
    print("Running analyzers...")
    
    results = {
        'url': url,
        'timestamp': datetime.datetime.now().isoformat(),
        'categories': {}
    }
    
    # Technical
    print("  - Technical analysis...")
    results['categories']['technical'] = analyze_technical(url, page_data)
    
    # On-Page
    print("  - On-page analysis...")
    results['categories']['onpage'] = analyze_onpage(url, html_content)
    
    # Indexing
    print("  - Indexing analysis...")
    results['categories']['indexing'] = analyze_indexing(url, html_content)
    
    # Content
    print("  - Content analysis...")
    results['categories']['content'] = analyze_content(html_content)
    
    # PageSpeed (może zająć chwilę)
    print("  - PageSpeed analysis (Google API)...")
    try:
        results['categories']['pagespeed'] = analyze_pagespeed(url)
        # Merge PageSpeed score do technical
        results['categories']['technical']['core_web_vitals'] = results['categories']['pagespeed']['mobile']['core_web_vitals']
    except Exception as e:
        print(f"    Warning: PageSpeed failed: {e}")
        results['categories']['pagespeed'] = {'score': 0, 'error': str(e)}
    
    # 4. Oblicz finalny score
    final_score = calculate_final_score(results['categories'])
    results['final_score'] = final_score
    results['grade'] = get_grade(final_score)
    
    # 5. Agreguj wszystkie issues
    all_issues = []
    for category in results['categories'].values():
        all_issues.extend(category.get('issues', []))
    
    # Sortuj po impact (descending)
    all_issues.sort(key=lambda x: x['impact'], reverse=True)
    results['all_issues'] = all_issues
    
    # 6. Quick wins (high impact, łatwe)
    results['quick_wins'] = [
        issue for issue in all_issues
        if issue['impact'] >= 6 and issue['severity'] in ['important', 'recommendation']
    ][:5]
    
    print("Audit complete!")
    return results

def calculate_final_score(categories):
    """Oblicz finalny wynik z wagami"""
    score = 0
    score += categories['technical']['score'] * WEIGHTS['technical']
    score += categories['onpage']['score'] * WEIGHTS['onpage']
    score += categories['indexing']['score'] * WEIGHTS['indexing']
    score += categories['content']['score'] * WEIGHTS['content']
    
    # PageSpeed jako część technical (już wliczone w technical)
    
    return round(score, 1)

def get_grade(score):
    """Określ ocenę literową"""
    if score >= 90:
        return {'label': 'EXCELLENT', 'color': 'green', 'emoji': '🟢'}
    elif score >= 75:
        return {'label': 'GOOD', 'color': 'lightgreen', 'emoji': '🟡'}
    elif score >= 60:
        return {'label': 'NEEDS IMPROVEMENT', 'color': 'yellow', 'emoji': '🟠'}
    elif score >= 40:
        return {'label': 'POOR', 'color': 'orange', 'emoji': '🔴'}
    else:
        return {'label': 'CRITICAL', 'color': 'red', 'emoji': '⛔'}

# Test
if __name__ == '__main__':
    import datetime
    
    test_url = "https://example.com"
    result = run_audit(test_url)
    
    print("\n=== AUDIT RESULTS ===")
    print(f"URL: {result['url']}")
    print(f"Final Score: {result['final_score']}/100 ({result['grade']['label']})")
    print(f"\nCategory Scores:")
    for cat_name, cat_data in result['categories'].items():
        print(f"  {cat_name}: {cat_data['score']:.1f}/100")
    
    print(f"\nTop Issues:")
    for issue in result['all_issues'][:5]:
        print(f"  [{issue['severity']}] {issue['title']} (Impact: {issue['impact']}/10)")
```

---

## 🚀 JAK URUCHOMIĆ

### Backend test (Python):

```bash
# 1. Zainstaluj dependencies
pip install requests beautifulsoup4 lxml textstat validators

# 2. Edytuj config.py - wstaw swój API key
# GOOGLE_PSI_API_KEY = "twój_klucz"

# 3. Uruchom test
python audit_engine.py
```

### Frontend (React Artifact):

W Claude.ai możesz wygenerować pełną aplikację React jako artifact, która będzie wywoływała backend przez API lub będzie działała standalone z fetching bezpośrednio z JavaScript (ograniczone CORS).

**Przykład minimalistyczny - React artifact standalone:**

```javascript
// W artifact React można zrobić uproszczoną wersję która:
// 1. Pobiera HTML przez proxy (cors-anywhere)
// 2. Parsuje w przeglądarce (DOMParser)
// 3. Wywołuje Google PSI API bezpośrednio
// 4. Pokazuje wyniki

// To da ci MVP działające w 100% w przeglądarce bez backendu!
```

---

## 💰 KOSZTY I LIMITY

### Google PageSpeed Insights API:
- ✅ **Darmowe**: 25,000 zapytań/dzień
- ✅ Wystarczy na ~800 audytów dziennie
- ✅ Nie wymaga karty kredytowej
- ✅ Brak kosztów ukrytych

### Pozostałe API/narzędzia:
- ✅ Wszystkie biblioteki Python: **darmowe** (open source)
- ✅ Requests, BeautifulSoup, textstat: **darmowe**
- ✅ Hosting: możesz zrobić static site (GitHub Pages, Netlify) - **darmowe**

**Total cost MVP: 0 PLN/miesiąc**

---

## ✅ CHECKLIST WDROŻENIA MVP

- [ ] Uzyskaj Google PSI API key
- [ ] Zainstaluj Python dependencies
- [ ] Edytuj config.py (API key)
- [ ] Przetestuj każdy analyzer osobno
- [ ] Uruchom audit_engine.py test
- [ ] Zbuduj React frontend (artifact)
- [ ] Połącz frontend z backendem (API lub standalone)
- [ ] Test na 5-10 różnych stronach
- [ ] Popraw błędy/edge cases
- [ ] Deploy (opcjonalnie)

---

To jest kompletny plan implementacji MVP w 100% za darmo. Wszystko oparte na open source i darmowych API. Gotowe do wdrożenia! 🚀