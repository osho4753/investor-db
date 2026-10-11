# Investor Intelligence Database

Reprodukovatelný proces vyhledávání, klasifikace a ověřování reálných investorů z veřejně dostupných dat. Hlavní prioritou je spolehlivost dat, ne počet záznamů.

**Pilot:** venture kapitálové (VC) značky s českou právnickou osobou, 20–30 kandidátů.

## Principy

- Pouze bezplatné veřejné zdroje.
- CSV soubory v Gitu jsou jediným zdrojem pravdy; integritu hlídá validační skript a testy.
- Každá vyplněná hodnota je doložena faktem se zdrojem, datem přístupu a popisem důkazu.
- Neznámé hodnoty zůstávají prázdné; nic se neodhaduje ani nepřepočítává mezi měnami.
- Ruční kontrolu provádí člověk, ne model, který data sbíral.

## Klíčové výsledky

Pilot v ČR našel 52 subjektů: 16 je ověřených VC investorů, 4 zůstávají kandidáty a 32 je vyloučených s konkrétním důvodem. Ruční kontrola hodnotitele R1 dala precision **15/15 = 100 %** (95% Wilsonův interval 79,6–100 %) a přesnost vzorku faktů **32/34 = 94,1 %** (80,9–98,4 %, pesimisticky 88,9 %), obojí ze stavu dat v době kontroly. Kontrola odhalila dva false negatives, Lighthouse a Tachles, které jsou už opravené. Capture–recapture dává dolní mez nejméně 16 VC v ČR. Model potřeboval 5,4 min na ověřeného investora, člověk 15,5 min na kontrolu investora a 0,96 min na fakt. Globální odhad vychází na 5 235 / 7 251 / 9 682 VC firem (nízký, základní a vysoký scénář). Po doplnění podle požadavků zadání má z 16 ověřených investorů 15 sektor, 14 ticket a 13 získaný kapitál nebo AUM. Dva investoři mají doloženou jen cílovou velikost fondu, která se ke kapitálu nepřičítá. Kapitál je v [data/funds.csv](data/funds.csv) po fondech s typem částky. U všech investorů je získaný kapitál dolní mez. Bez ní by byl jen tehdy, kdyby byl doložen počet fondů, všechny fondy měly final close nebo uzavřenou částku, žádný ještě nesbíral peníze a nebyl u nich konflikt zdrojů. Konflikty zdrojů (Credo) jsou v tabulce kapitálu vidět. Chybějící údaje jsou zapsány jako „hledáno, nenalezeno“. Všech 49 faktů z doplňování čeká na samostatnou kontrolu „po doplnění“ (viz [docs/04](docs/04-rucni-kontrola.md), 4.7).

## Povinné výstupy

| # | Výstup | Kde ho najít |
|---|---|---|
| 1 | Plán výzkumu a kritéria zařazení a vyloučení | [docs/01-plan-a-kriteria.md](docs/01-plan-a-kriteria.md) |
| 2 | Metodika vyhledávání a ověřování | [docs/02-metodika.md](docs/02-metodika.md) |
| 3 | Odhad globálního pokrytí, počtu investorů a spolehlivosti | [docs/03-globalni-odhad.md](docs/03-globalni-odhad.md), oddíly 3.1–3.4 |
| 4 | Pilotní vzorek v ČR a zdůvodnění výběru země | [data/investors.csv](data/investors.csv), [docs/01-plan-a-kriteria.md](docs/01-plan-a-kriteria.md) |
| 5 | Zdroje a data ověření záznamů i faktů | [data/facts.csv](data/facts.csv), [data/funds.csv](data/funds.csv), [data/sources.csv](data/sources.csv), [data/search_log.csv](data/search_log.csv), [data/effort_log.csv](data/effort_log.csv) |
| 6 | Ruční kontrola vzorku a precision | [docs/04-rucni-kontrola.md](docs/04-rucni-kontrola.md), [review/kontrolni-list-faktu.md](review/kontrolni-list-faktu.md), [data/reviews.csv](data/reviews.csv), [data/fact_reviews.csv](data/fact_reviews.csv) |
| 7 | Odhad nákladů a složitosti globálního škálování | [docs/03-globalni-odhad.md](docs/03-globalni-odhad.md), oddíly 3.5–3.6 |
| 8 | Kód, testy, dokumentace, historie commitů, ai-log | `investor_db/`, `tests/`, `docs/`, `git log`, [ai-log/](ai-log/) |

## Hlavní omezení

- Jen bezplatné veřejné zdroje. Úplnost nepovinných polí je proto nízká: ticket má 69–75 % ověřených investorů, velikost fondu 12,5 %.
- Některé primární zdroje jsou nedostupné: JERRS ČNB je za CAPTCHA, or.justice.cz zakazuje `/ias/` v robots.txt a část webů vrací HTTP 403 nebo 429. Ochrany se neobcházejí.
- Nástroj pro čtení webu vrací shrnutí, proto se částky a data ověřují proti surovému textu. Stránky vykreslované JavaScriptem surový text neposkytnou.
- Pravidlo CVC často nejde rozhodnout, protože podíl korporace na kapitálu fondu zdroje neuvádějí (Inven, J&T).
- Precision vychází z 15 záznamů a jednoho hodnotitele, interval je široký a shoda hodnotitelů se nepočítá.
- Globální odhad stojí na předpokladech, hlavně na podílu VC mezi firmami PE a VC v Evropě a na zbytku světa. Ty jsou v [docs/03](docs/03-globalni-odhad.md) označené a mají rozsah.

## Návod pro hodnotitele

1. **Instalace.** Je potřeba Python 3.11 nebo novější. Kód používá jen standardní knihovnu, pytest je volitelná závislost `dev`.

   ```
   git clone git@github.com:osho4753/investor-db.git
   cd investor-db
   python -m pip install -e ".[dev]"      # jen kvůli testům (pytest)
   ```

2. **Kontrola integrity dat.** Příkaz musí skončit hláškou „Validace prošla bez chyb.“

   ```
   python -m investor_db validate
   ```

3. **Kontrolní list a šablony pro ruční kontrolu.** Postup je v [docs/04-rucni-kontrola.md](docs/04-rucni-kontrola.md), oddíl 4.2.

   ```
   python -m investor_db review-guide                          # review/kontrolni-list-faktu.md
   python -m investor_db review-template --reviewer R2         # řádky pro kontrolu investorů
   python -m investor_db fact-review-template --reviewer R2    # řádky pro kontrolu vzorku faktů
   python -m investor_db fact-review-template --reviewer R1 --round po_doplneni --from-fact f-00249  # kolo po doplnění
   ```

   CSV upravujte v textovém editoru (UTF-8), ne v Excelu. Excel mění kódování a ořezává úvodní nuly v IČO.

4. **Metriky** (precision, přesnost faktů, úplnost, trychtýř, pracnost, capture–recapture):

   ```
   python -m investor_db metrics
   ```

5. **Testy:**

   ```
   python -m pytest
   ```

## Struktura

```
data/          CSV tabulky (jediný zdroj pravdy)
docs/          plán, metodika, odhady, ruční kontrola
investor_db/   schéma, validace, metriky, CLI
review/        vygenerovaný kontrolní list faktů pro hodnotitele
tests/         testy nad fiktivními daty
ai-log/        exporty dialogů s AI
```

Pytest je zvolen místo `unittest`, protože parametrizované testy validačních pravidel a dočasné složky (`tmp_path`) jsou s ním výrazně kratší a čitelnější; samotný kód na něm nezávisí.
