# ai-log

# Claude Conversation Log

Session ID: d385e1f5-0229-46e8-8649-3f0ea24e7385
Date: 2026-10-09 11:15:22

---

## 👤 User

hi are u ready?

---

## 🤖 Claude

Hi, I'm ready. I'm in your `investor-db` repo on `main`, and it has one commit so far. What would you like to work on?

---

## 👤 User

<pasted_content id="2b08">
Kontext: Začínáme testový projekt „Investor Intelligence Database“. Repozitář: git@github.com:osho4753/investor-db.git – je prázdný a naklonovaný lokálně, pracujeme v jeho kořeni (kořen repozitáře nahrazuje složku investor-intelligence/ z návrhu struktury). Nic nepushuj bez mého souhlasu. Komunikuj se mnou výhradně v češtině. Veškeré výstupy (dokumentace, README, názvy v datech, kde to dává smysl) budou v češtině. Do kódu nepiš komentáře – kód má být čitelný sám o sobě (jasné názvy, type hints, malé funkce).

Cíl projektu: Vytvořit reprodukovatelný proces vyhledávání, klasifikace a ověřování reálných investorů z veřejně dostupných dat. Hlavní priorita je spolehlivost dat, ne počet záznamů. Pilot: venture kapitálové fondy se správcovskou společností v ČR, 20–30 kandidátů.

Přijatá rozhodnutí:

- Pouze bezplatné veřejné zdroje. Placené databáze (Dealroom, Crunchbase Pro, PitchBook) nepoužíváme. Scraping je povolen, ale s respektem k robots.txt a podmínkám webů, s omezením rychlosti a cachováním – zatím ho ale neimplementuj.
- Pilot zahrnuje pouze VC fondy. Business angely (GDPR, slabá veřejná doložitelnost) a family offices (málo veřejných dat) vylučujeme; PE fondy jen jako kandidáty pro budoucí rozšíření. Toto rozhodnutí musí být zdůvodněno v dokumentaci.
- Úložiště dat: CSV soubory v Gitu jako jediný zdroj pravdy; integritu (unikátní ID, povinná pole, vazby mezi tabulkami, duplicity, formáty dat a měn) zajišťuje validační skript a testy. SQLite zvažuj jen jako odvozenou vrstvu, PostgreSQL pouze jako součást odhadu globálního škálování.
- Ruční kontrolu provádím já a nezávislý hodnotitel, ne model, který data sbíral.
- Cíl: nejdřív MVP, pak případně automatizace. Chci ukázat dobré inženýrské postupy.

Povinné výstupy projektu:

1. Plán výzkumu a kritéria zařazení/vyloučení.
2. Metodika vyhledávání a ověřování.
3. Odhad globálního pokrytí, přibližného počtu investorů a spolehlivosti dat s vysvětlením předpokladů.
4. Pilotní vzorek v jedné zemi (ČR, výběr země zdůvodnit dostupností zdrojů).
5. Zdroje a data ověření pro každý záznam i jednotlivá fakta.
6. Ruční kontrola vzorku a výpočet precision = TP / (TP + FP).
7. Odhad nákladů a složitosti globálního škálování (metoda, předpoklady, rozsah nejistoty).
8. Funkční kód, testy, dokumentace, historie Git commitů a export dialogů do ai-log.

Minimální pole: investor_id, name, investor_type, country, website, investment_sectors, investment_stages, typical_ticket_min, typical_ticket_max, currency, total_fund_size, assets_under_management, invested_capital, verification_status, evidence_urls, last_verified_at. Velikost fondu, AUM, investovaný kapitál a velikost jednotlivé transakce se nesmí směšovat. Neznámé hodnoty zůstávají neznámé. Pro každý ověřovaný fakt potřebujeme zdroj, datum přístupu a stručný popis důkazu – zvaž, zda fakta neukládat v samostatné tabulce (jeden řádek = jeden fakt) místo pouhého seznamu URL.

Statusy: ověřený investor / kandidát k dalšímu ověření / vyloučený subjekt.

Úkol pro tento krok – POUZE PLÁN, žádná implementace:

1. Prohlédni repozitář.
2. Připrav: požadavky a kritéria dokončení; pravidla zařazení/vyloučení; metodiku vyhledávání (konkrétní typy veřejných zdrojů pro ČR); datové schéma včetně evidence faktů; způsob výpočtu precision a doplňkových metrik (úplnost polí, podíl záznamů s primárními zdroji, doložení investiční činnosti, duplicity); přístup k odhadu globálního rozsahu; strukturu repozitáře (ověř, které soubory jsou opravdu potřeba pro minimální dostatečné řešení); plán implementace po krocích s Git commity.
3. Jasně odděl ověřená fakta, předpoklady a otevřené otázky.

Omezení: Nesbírej data, nevymýšlej investory, odkazy ani hodnoty. Neinstaluj závislosti a nedělej destruktivní změny bez vysvětlení a mého souhlasu. Preferuj standardní knihovnu Pythonu; pytest navrhni s odůvodněním. Plán mi předlož ke schválení a počkej.
</pasted_content id="2b08">

---

## 🤖 Claude

# Plán: Investor Intelligence Database (pilot ČR, VC fondy)

Zatím jsem nic nezměnil ani nenainstaloval. Projekt má jen jeden commit s README a v Pythonu jsou dostupné verze 3.11.0 a pytest 9.0.2.

---

## 0. Stav repozitáře (ověřeno)

| Co          | Zjištění                                                                                                                                                                                                                 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Obsah       | Jen `README.md` a jeden commit `d191549 first commit`                                                                                                                                                                    |
| `README.md` | Je uložený v kódování UTF-16 LE s BOM, proto ho Git bere jako binární soubor. Obsahuje jen `# investor-db`. **Navrhuji ho přepsat do UTF-8.** Jinak v něm nebudou fungovat diffy. Ztratí se jen kódování, obsah zůstane. |
| Remote      | `origin` = `git@github.com:osho4753/investor-db.git`                                                                                                                                                                     |
| Prostředí   | Windows 11, Python 3.11.0, pytest 9.0.2 je už nainstalovaný                                                                                                                                                              |
| Riziko      | Repozitář leží v OneDrive a v cestě je cyrilice. Synchronizace OneDrive se může dostat do konfliktu se složkou `.git`. Doporučuji ho přesunout mimo OneDrive (rozhodnutí je na tobě).                                    |

---

## 1. Požadavky a kritéria dokončení (DoD)

Projekt je hotový, když platí všechno z tohoto seznamu:

1. `data/*.csv` projdou validačním skriptem bez chyb (`python -m investor_db validate`).
2. `pytest` projde. Testy pokrývají každé validační pravidlo pozitivním i negativním případem a všechny metriky.
3. Pilot má 20–30 subjektů se statusem a vyloučené subjekty mají uvedený důvod.
4. Každá vyplněná hodnota v `investors.csv` má v `facts.csv` aspoň jeden fakt. Ten obsahuje zdroj, datum přístupu a popis důkazu.
5. Ruční kontrolu vyplníš ty a nezávislý hodnotitel. Precision i doplňkové metriky se z ní počítají skriptem a jsou reprodukovatelné.
6. Dokumentace pokrývá povinné výstupy 1–7. Odhady obsahují předpoklady a rozsah nejistoty.
7. Historie Gitu má malé logické commity. V `ai-log/` je export dialogů.
8. Kód používá jen standardní knihovnu, nemá komentáře, má type hints a malé funkce.

---

## 2. Pravidla zařazení a vyloučení

**Jednotka záznamu (návrh):** Jeden záznam je jeden _VC investor_, tedy správce nebo značka VC fondů. Konkrétní fondy se v MVP ukládají jako fakta, ne do samostatné tabulky (viz otevřená otázka Q1).

**Zařazení – musí platit všechno:**

- Z1: Správcovská společnost je zapsaná v českém obchodním rejstříku (má IČO).
- Z2: Převažuje strategie rizikového kapitálu: menšinové podíly v nekótovaných firmách ve fázi pre-seed až growth. Podkladem je deklarace investora a skladba portfolia.
- Z3: Spravuje aspoň jeden fond nebo investiční vehikl, který investuje kapitál třetích osob.
- Z4: Je doložená investiční činnost, tj. aspoň jedna investice nebo nový fond za posledních 36 měsíců. Hranice 36 měsíců je předpoklad.

**Vyloučení, s uvedením důvodu v `exclusion_reason`:** business angel a angel síť (GDPR, slabá doložitelnost), family office (málo veřejných dat), PE/buyout s převažujícími většinovými podíly (zapíše se jako kandidát pro budoucí rozšíření), crowdfundingová platforma, akcelerátor nebo inkubátor bez fondu, dotační program bez kapitálové investice, zaniklý nebo likvidovaný subjekt, duplicita jiného záznamu.

**Statusy:**

- `overeny`: platí Z1–Z4, Z1 je doložené primárním zdrojem a všechna vyplněná pole mají fakt.
- `kandidat`: pravděpodobně splňuje kritéria, ale chybí důkaz pro některé z Z1–Z4.
- `vyloucen`: spadá pod pravidlo vyloučení.

Status nastavuje ten, kdo data sbírá. Ruční kontrola pak měří, jestli bylo `overeny` přiděleno správně, a právě to vyjadřuje precision.

**Zdůvodnění pro dokumentaci:** VC fondy v ČR mají právní formu a regulatorní stopu (ČNB, obchodní rejstřík, sbírka listin), takže se dají ověřit. U business angelů jde o fyzické osoby, takže hrozí GDPR riziko a chybí veřejné registry. Family offices nemají povinnost zveřejňovat. PE se metodicky liší a kdyby se smíchalo s VC, rozmazalo by definici.

---

## 3. Metodika vyhledávání a ověřování (ČR)

**Typy veřejných zdrojů.** U každého zdroje před použitím ověřím, že je dostupný a že ho podmínky webu dovolují použít.

| Úroveň               | Zdroj                                                                                              | K čemu slouží                                                         |
| -------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Primární – regulátor | Seznamy ČNB: správci investičních fondů s povolením a registrovaní správci podle §15 ZISIF         | Existence a regulatorní status (Z1, Z3)                               |
| Primární – registr   | Obchodní rejstřík a sbírka listin (justice.cz), ARES                                               | IČO, sídlo, výroční zprávy s velikostí fondu a investovaným kapitálem |
| Primární – EU        | Registr ESMA (EuVECA / AIFM)                                                                       | Doplňková identifikace fondů                                          |
| Primární – vlastní   | Web investora, jeho tiskové zprávy                                                                 | Sektory, fáze, ticket, portfolio                                      |
| Sekundární           | Seznam členů CzVCA, Invest Europe, oznámení EIF a Národní rozvojové banky o fondech, odborná média | Hledání kandidátů a potvrzení investic                                |

**Postup:**

1. **Hledání kandidátů.** Projdu seznamy (ČNB, CzVCA, ESMA). Každý průchod zapíšu do `search_log.csv`: zdroj, datum, dotaz nebo filtr, počet nálezů.
2. **Deduplikace** podle IČO, normalizovaného názvu a domény webu.
3. **Triáž** podle pravidel zařazení. Výsledkem je `kandidat` nebo `vyloucen`.
4. **Ověření.** Každý fakt dostane zdroj, datum přístupu a popis důkazu. Primární zdroj má přednost.
5. **Konflikty mezi zdroji.** Vítězí novější primární zdroj a konflikt se zapíše do faktu. Nic se neprůměruje ani nepřepočítává mezi měnami.
6. **Ruční kontrola.** Dělá ji člověk, ne model (viz bod 5).

---

## 4. Datové schéma (CSV v UTF-8, oddělovač `,`, data v ISO 8601)

**`data/investors.csv`** obsahuje minimální pole a navíc `registry_id` (IČO, kvůli deduplikaci) a `exclusion_reason`.

| Pole                                      | Pravidlo                                                                                 |
| ----------------------------------------- | ---------------------------------------------------------------------------------------- |
| `investor_id`                             | `inv-cz-0001`, unikátní                                                                  |
| `investor_type`                           | Řízený slovník: `vc` nebo `pe_kandidat`                                                  |
| `investment_sectors`, `investment_stages` | Více hodnot oddělených `;` z řízeného slovníku                                           |
| `typical_ticket_min/max`                  | Velikost **jedné investice**                                                             |
| `total_fund_size`                         | Velikost **fondu**, definice podle Q1                                                    |
| `assets_under_management`                 | Celkový majetek spravovaný **správcem**                                                  |
| `invested_capital`                        | Kumulativně **investovaný** kapitál                                                      |
| `currency`                                | ISO 4217. Platí pro všechny částky v řádku (viz Q3)                                      |
| `evidence_urls`                           | **Odvozené** z `facts.csv`, ne ručně zadané. Validátor kontroluje, že sedí.              |
| `last_verified_at`                        | Datum. Musí být stejné nebo pozdější než nejnovější `accessed_at` faktů daného investora |

Prázdná buňka znamená _neznámé_. Nula ani odhad se nesmí použít místo neznámé hodnoty.

**`data/facts.csv`** – jeden řádek je jeden fakt (doporučuji). Sloupce: `fact_id, investor_id, field, value, currency, value_as_of, source_id, accessed_at, evidence_note`.

- `field` je buď pole z `investors.csv`, nebo doplňkový typ (`registrace_cnb`, `dolozena_investice`, `nazev_fondu`).
- Validátor kontroluje, že každá vyplněná hodnota v `investors.csv` má fakt se shodnou hodnotou.

**`data/sources.csv`**: `source_id, url, publisher, source_type, is_primary`. Jedna URL je v tabulce jen jednou.

**`data/reviews.csv`**: `investor_id, reviewer (R1/R2), reviewed_at, verdict (TP/FP/nejiste), note`. Model sem nic nezapisuje. Skript vygeneruje jen prázdnou šablonu.

**`data/search_log.csv`**: protokol hledání, kvůli reprodukovatelnosti.

**Validace:** unikátní ID, povinná pole podle statusu, platnost cizích klíčů (fakt → investor, fakt → zdroj), hodnoty ze slovníků, formáty dat a částek (`Decimal`, nesmí být záporné, min ≤ max), kód měny, duplicity (IČO, doména, normalizovaný název), shoda mezi `investors.csv` a `facts.csv`, u `vyloucen` povinný `exclusion_reason`.

---

## 5. Precision a doplňkové metriky

- **Precision = TP / (TP + FP)** pro záznamy se statusem `overeny`. V pilotu se kontrolují všechny, protože jich je málo. Kdyby se kontroloval jen vzorek, vybere se náhodně s pevným seedem.
  - Verdikt `nejiste` se vykazuje zvlášť a k tomu citlivostní varianta, která ho počítá jako FP.
  - Precision se uvádí s 95% Wilsonovým intervalem, protože vzorek je malý.
- **Shoda hodnotitelů:** Cohenovo κ mezi R1 a R2. Neshody se rozhodnou a zdokumentují.
- **Úplnost polí:** podíl vyplněných hodnot u každého pole, počítaný ze záznamů `overeny`.
- **Primární zdroje:** podíl záznamů, které mají existenci (Z1) doloženou primárním zdrojem, a podíl faktů z primárních zdrojů.
- **Doložení investiční činnosti:** podíl záznamů s faktem `dolozena_investice` za posledních 36 měsíců.
- **Duplicity:** počet nalezených kandidátů na duplicitu a počet potvrzených.
- **Aktuálnost:** podíl záznamů s `last_verified_at` mladším než 12 měsíců.

Všechno se počítá standardní knihovnou (`csv`, `decimal`, `math`, `statistics`).

---

## 6. Odhad globálního rozsahu a škálování

**Počet investorů.** Kombinace tří postupů:

1. **Podle regulátorů:** spočítat VC správce v registrech, které jdou filtrovat (EU: ESMA a národní regulátoři; USA: SEC IAPD, kam se jako _exempt reporting advisers_ hlásí i poradci VC fondů; UK: FCA).
2. **Podle asociací:** počty členů národních VC asociací.
3. **Extrapolace z pilotu:** poměr „počet nalezených v ČR ÷ objem VC investic v ČR“ přenesený na další země.

Výsledek se uvede jako rozsah nízký / základní / vysoký. Konkrétní čísla teď **nevymýšlím**, vzniknou až z citovaných zdrojů.

**Spolehlivost dat.** Regiony se rozdělí do úrovní podle kvality registrů (např. EU/US/UK = vysoká, ostatní = nižší). Pilotní precision se pro ně upraví podle úrovně a předpoklady se zdokumentují.

**Náklady a složitost.** V pilotu se bude u každého záznamu měřit čas na vyhledání, ověření a kontrolu. Odhad pak bude čas na záznam × počet investorů × koeficient obtížnosti regionu (jazyk, registry), k tomu náklady na opakované ověřování (roční cyklus) a infrastrukturu. V globálním měřítku jde o PostgreSQL a scraping s cache.

Výstup bude ve třech scénářích. Monte Carlo s trojúhelníkovým rozdělením přes `random` je volitelné a doporučuji ho až po pilotu.

---

## 7. Struktura repozitáře (minimální)

```
README.md                  přehled, jak spustit, odkazy na dokumenty (UTF-8)
.gitignore, .gitattributes  .gitattributes kvůli koncům řádků (CSV/MD jako LF)
pyproject.toml             metadata, Python ≥3.11, pytest jako jediná dev závislost
docs/
  01-plan-a-kriteria.md    výstup 1 + zdůvodnění rozsahu pilotu a výběru ČR
  02-metodika.md           výstup 2 + datové schéma
  03-globalni-odhad.md     výstupy 3 a 7
  04-rucni-kontrola.md     výstup 6 + postup pro hodnotitele
data/  investors.csv, facts.csv, sources.csv, reviews.csv, search_log.csv
investor_db/  __main__.py (CLI: validate, metrics, review-template),
              schema.py, io.py, validation.py, metrics.py
tests/  test_validation.py, test_metrics.py (syntetické fixtures v kódu testů, jasně fiktivní)
ai-log/  exporty dialogů
```

U vynechaných souborů:

- **SQLite** jen jako volitelný odvozený export, až bude potřeba.
- Výstupy 4 a 5 jsou přímo `data/`, samostatný dokument nepotřebují.
- `requirements*.txt` nahrazuje `pyproject.toml`.

**Proč pytest:** je už nainstalovaný, takže se nic neinstaluje. Validátor potřebuje hodně parametrizovaných testů a `@pytest.mark.parametrize` spolu s `tmp_path` je dělají kratší a čitelnější než `unittest`. Samotný kód na pytestu nezávisí.

---

## 8. Plán implementace po commitech

| #   | Commit                                                       | Obsah                                                            |
| --- | ------------------------------------------------------------ | ---------------------------------------------------------------- |
| 1   | `chore: kostra repozitáře`                                   | README v UTF-8, `.gitignore`, `.gitattributes`, `pyproject.toml` |
| 2   | `docs: plán výzkumu a kritéria`                              | `01-plan-a-kriteria.md`                                          |
| 3   | `docs: metodika a datové schéma`                             | `02-metodika.md`                                                 |
| 4   | `feat: schéma a načítání CSV`                                | `schema.py`, `io.py`, prázdné CSV s hlavičkami a testy           |
| 5   | `feat: validace dat`                                         | `validation.py` a testy                                          |
| 6   | `feat: metriky a šablona kontroly`                           | `metrics.py`, CLI a testy                                        |
| —   | **⏸ Schválení před sběrem dat**                              |                                                                  |
| 7–8 | `data: protokol hledání a kandidáti`, `data: fakta a zdroje` | Sběr dat po malých dávkách                                       |
| —   | **⏸ Ruční kontrola: ty a R2**                                |                                                                  |
| 9   | `data: výsledky ruční kontroly`                              |                                                                  |
| 10  | `docs: výsledky kontroly a metriky`                          |                                                                  |
| 11  | `docs: globální odhad a škálování`                           |                                                                  |
| 12  | `docs: ai-log a finální README`                              |                                                                  |

Nic nepushuji, dokud to neschválíš.

---

## 9. Ověřená fakta, předpoklady, otevřené otázky

**Ověřená fakta:**

- Stav repozitáře, kódování README a verze Pythonu a pytestu (viz bod 0).

**Předpoklady, které je potřeba ověřit:**

- Že zdroje v bodě 3 jsou dostupné, obsahují uvedené údaje a jejich podmínky použití sběr dovolují. To platí hlavně pro seznamy ČNB a pro to, jestli se v nich dají VC správci odlišit od ostatních.
- Že v ČR je dost VC investorů na pilot s 20–30 kandidáty.
- Hranice aktivity 36 měsíců a hranice aktuálnosti 12 měsíců.
- Kategorie regionů pro globální odhad.

**Otevřené otázky – potřebuji tvé rozhodnutí:**

- **Q1 – Jednotka záznamu:** Investor bude správce nebo značka a `total_fund_size` bude velikost _posledního uzavřeného fondu`?_ Alternativou je samostatná tabulka `funds.csv` (přesnější, ale složitější).
- **Q2 – Hraniční subjekty:**
  - Corporate VC, fondy fondů a státní fondy (např. NRB): zařadit, nebo vyloučit?
  - Zahraniční správce s pobočkou v ČR: zařadit, nebo vyloučit?
- **Q3 – Měny:** Souhlasíš s jednou měnou na řádek a zákazem přepočtů? Částky v jiné měně by zůstaly jen ve `facts.csv`.
- **Q4 – Hodnoty ve slovnících:** ASCII kódy (`overeny`, `kandidat`, `vyloucen`) s českými popisy v dokumentaci, nebo hodnoty s diakritikou? Doporučuji ASCII kvůli robustnosti.
- **Q5 – Commity:** prefixy Conventional Commits (`feat:`, `docs:`) a popis česky – souhlasíš?
- **Q6 – ai-log:** stačí ti `/export` z Claude Code, nebo chceš skript, který převede transkripty JSONL na Markdown?
- **Q7:** Mám přepsat README do UTF-8? A přesuneš repozitář mimo OneDrive?

Čekám na schválení nebo úpravy. Dokud neodpovíš, nic neimplementuji.

---

## 👤 User

presunul jsem repo

---

## 🤖 Claude

Repozitář je teď v `C:\Users\ramazan\investor-db` a po přesunu je v pořádku:

- větev `main` je čistá a obsahuje jen commit `d191549 first commit`,
- `origin` je beze změny a Git hlásí, že je lokální větev aktuální s `origin/main`, takže ten commit už je na GitHubu,
- `README.md` je pořád v kódování UTF-16.

Pravidla spolupráce (čeština, žádné komentáře v kódu, bez pushe a instalací bez tvého souhlasu) jsem si uložil do paměti, aby platila i v dalších sezeních.

Na původní plán jsi zatím nereagoval. Než začnu s prvním commitem (`chore: kostra repozitáře`), potřebuji, abys plán schválil a odpověděl na otázky Q1–Q7. Stručně je opakuji i s mým doporučením:

| Otázka                       | Moje doporučení                                                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Q1** Co je jeden záznam    | Jeden záznam = správce nebo značka; `total_fund_size` = velikost posledního uzavřeného fondu; bez samostatné tabulky `funds.csv` |
| **Q2** Hraniční subjekty     | Corporate VC, fondy fondů, státní fondy (např. NRB) a zahraniční správci jen s pobočkou v ČR = `kandidat`; rozhodneme po pilotu  |
| **Q3** Měny                  | Jedna měna na řádek, nic nepřepočítávat; částky v jiné měně zůstanou jen ve `facts.csv`                                          |
| **Q4** Hodnoty ve slovnících | ASCII kódy (`overeny`, `kandidat`, `vyloucen`), české popisy v dokumentaci                                                       |
| **Q5** Commity               | Prefixy `feat:`/`docs:`, zbytek zprávy česky                                                                                     |
| **Q6** ai-log                | Tvůj `/export` a k tomu krátký `ai-log/README.md` s přehledem dialogů                                                            |
| **Q7** README                | Převést do UTF-8 v prvním commitu                                                                                                |

Stačí napsat „souhlasím“ a začnu podle těchto doporučení, nebo uveď, co chceš změnit.

---

## 👤 User

<pasted_content id="2b08">
Plán schvaluji s následujícími úpravami:

1. Jednotka záznamu: VC značka/tým, který rozhoduje o investicích – ne nutně právní správce. V ČR mnoho VC fondů formálně spravují licencovaní třetí správci (např. AMISTA, REDSIDE, Conseq), v seznamech ČNB tedy figuruje správce, ne VC značka. Právního správce/administrátora ukládej jako fakt. Z1 přeformuluj: VC značka má českou právnickou osobu s IČO (správcovská, poradenská společnost nebo samotný fond).

2. Q1: total_fund_size = velikost posledního fondu při final close, ne cílová velikost. Je-li známa jen cílová velikost, pole zůstává prázdné a cíl jde jen do facts.csv. Do facts.csv přidej volitelný sloupec fund_name. Samostatná funds.csv zatím ne.

3. Q2: Corporate VC, fondy fondů a státní fondy (NRB apod.) vyloučit s důvodem „mimo definici pilotu“. Zahraniční správce bez české právnické osoby vyloučit s důvodem „zahraniční subjekt“. Obojí zdůvodnit v dokumentaci jako budoucí rozšíření.

4. Q3: Souhlasím (jedna měna na řádek, žádné přepočty). Přidej metriku: počet hodnot, které zůstaly jen ve facts.csv kvůli jiné měně – patří do omezení dat.

5. Ruční kontrola: R1 jsem já, R2 je volitelný (nezávislý hodnotitel nemusí šablonu vyplnit). Cohenovo κ počítej jen pokud existují data R2 a vždy vedle něj uveď prosté procento shody (při malém vzorku a vysokém podílu TP je κ nestabilní).

6. Přidej kontrolu na úrovni faktů: šablona fact_reviews.csv (fact_id, reviewer, reviewed_at, verdict správně/chybně/nelze_ověřit, note) a metriku „přesnost faktů“. Pokud bude faktů příliš mnoho, kontroluje se náhodný vzorek s pevným seedem – velikost vzorku navrhni.

7. Q4: ASCII kódy. Q5: Conventional Commits s českým popisem – ano. Q6: stačí /export, skript nedělej.

8. Q7: README převeď do UTF-8. Repozitář přesunu mimo OneDrive sám – nejdřív vyexportuji tuto session. Zatím nic needituj, dokud ti nedám vědět, že pracujeme v nové cestě.

9. Do README přidej tabulku mapující povinné výstupy 1–8 na konkrétní soubory, aby je hodnotitel snadno našel.

Po přesunu repozitáře začni commity 1–6. Zastav se na plánovaném schválení před sběrem dat.
</pasted_content id="2b08">

---

## 🤖 Claude

Repozitář jsem už ověřil v nové cestě `C:\Users\ramazan\investor-db`, takže začínám commity 1–6. Tvé úpravy zapracuji do dokumentace i kódu.

---

## 🤖 Claude

Nástroj pro zápis zachoval původní kódování UTF-16. Soubor proto smažu, vytvořím ho znovu v UTF-8 a opravím lokální commit, který ještě nebyl pushnutý.

---

## 🤖 Claude

README je teď v UTF-8. Diff ho ukazuje jako „Bin“ jen proto, že původní verze byla binární. Pokračuji commitem 2, plánem a kritérii.

---

## 🤖 Claude

Commit 4: schéma, načítání CSV a parsování hodnot.

---

## 🤖 Claude

Validátor je hotový a teď píšu jeho testy, pozitivní i negativní případ ke každému pravidlu.

---

## 🤖 Claude

Commit 6: metriky, šablony pro ruční kontrolu, CLI a dokumentace postupu kontroly.

---

## 🤖 Claude

Všech 152 testů prochází a CLI funguje nad prázdnými daty. Doplním dokument o ruční kontrole a návod v README.

---

## 🤖 Claude

Commity 1–6 jsou hotové. Všech 152 testů prochází, `validate` i `metrics` nad prázdnými daty proběhnou bez chyb a nic jsem nepushnul. Na GitHubu je pořád jen původní `first commit`. Začal jsem hned, protože jsi mezitím napsal „přesunul jsem repo“ a pracuji už v `C:\Users\ramazan\investor-db`.

```
26322b6 feat: metriky, šablony ruční kontroly a CLI
defa85d feat: validace integrity dat
5d0d872 feat: datové schéma a načítání CSV
b073bae docs: metodika vyhledávání, ověřování a datové schéma
8cef2f3 docs: plán výzkumu a kritéria zařazení/vyloučení
60e877a chore: kostra repozitáře
```

Všech devět tvých úprav je zapracovaných:

- **Jednotka záznamu:** VC značka. Právního správce ukládám jako fakt `pravni_spravce`. Kritérium Z1 je přeformulované tak, jak jsi chtěl.
- **Velikost fondu:** do `total_fund_size` patří jen velikost při final close. Cílová velikost jde do faktu `cilova_velikost_fondu`. Ve `facts.csv` je nový sloupec `fund_name`.
- **Vyloučení:** corporate VC, fondy fondů a státní fondy mají důvod `mimo_definici_pilotu`, zahraniční subjekty bez české osoby `zahranicni_subjekt`. V dokumentaci jsou popsané jako budoucí rozšíření.
- **Kontrola:** R2 je volitelný. κ se počítá jen tehdy, když existují data R2, a vždy vedle procenta shody.
- **Kontrola faktů:** šablona `fact_reviews.csv` a metrika přesnosti faktů jsou hotové. Velikost vzorku navrhuji podle Cochranova vzorce (95 %, ±10 p. b.) s pevným seedem 2026. Při 150 faktech to vychází na 59, při 300 na 73 a maximum je 96.
- **Metrika měn:** počítá hodnoty, které zůstaly jen ve `facts.csv`, protože jsou v jiné měně než řádek.
- **README:** je v UTF-8 a obsahuje tabulku výstupů 1–8 s odkazy na soubory.

**Co jsem rozhodl sám** (vše lze snadno změnit):

- **IČO třetího správce:** `registry_id` nesmí být IČO licencovaného třetího správce, jinak by validátor označil různé značky jednoho správce jako duplicity. Pravidlo je v metodice.
- **Název kandidáta bez faktu:** u statusů `kandidat` a `vyloucen` nevyžaduji fakt pro `name`, jeho původ je v protokolu hledání. Pro všechna ostatní vyplněná pole fakt vyžaduji vždy.
- **Formát ID:** `inv-0001` místo `inv-cz-0001`, protože vyloučené zahraniční subjekty nejsou z ČR.
- **Metriky jen nad platnými daty:** `metrics` odmítne výpočet, dokud data neprojdou validací.
- **Primárnost zdroje:** neukládám ji ve zvláštním sloupci, odvozuje se z `source_type`, aby se dva údaje nemohly rozcházet.

Při prvním commitu nástroj pro zápis zachoval kódování UTF-16. Převedl jsem soubor znovu a opravil lokální commit přes `--amend`. Stejně jsem doplnil poslední commit o opravu README, kde jsem odstranil neověřený příkaz `pip install -e`.

**⏸ Zastavuji se před sběrem dat.** K pokračování potřebuji tvé schválení:

1. Můžu pro sběr používat webové nástroje (vyhledávání a čtení stránek)? Šlo by jen o ruční čtení jednotlivých stránek, ne o scraping.
2. Můžu sbírat po dávkách? Nejdřív protokol hledání a seznam kandidátů jako jeden commit, pak ověřování faktů po 5–10 investorech na commit.

---

## 👤 User

<pasted_content id="2b08">
Schvaluji s těmito podmínkami:

1. Webové nástroje: ano, pouze ruční čtení jednotlivých stránek, žádný scraping. Zásadní pravidlo: každý fakt musí pocházet ze stránky, kterou jsi v této session skutečně otevřel. Nic nedoplňuj z vlastních znalostí ani odhadem. Pokud se stránka nenačte nebo údaj neobsahuje, hodnota zůstává neznámá a do protokolu zapiš, co se nepodařilo. accessed_at je skutečné datum přístupu. evidence_note stručně parafrázuje, co a kde na stránce je – necituj delší pasáže.

2. Vyloučené subjekty: exclusion_reason musí být doložen aspoň jedním faktem se zdrojem (např. že jde o corporate VC nebo zahraniční subjekt). Doplň do validátoru a testů.

3. Měření času: pro každého investora zaznamenej čas strávený hledáním a ověřováním (v minutách, např. v search_log.csv nebo samostatném souboru – navrhni). Potřebujeme to pro odhad nákladů globálního škálování.

4. Dávky: ano. Nejdřív protokol hledání a seznam kandidátů jako jeden commit. Pak se zastav a ukaž mi souhrn: které zdroje byly dostupné a co obsahovaly (hlavně seznamy ČNB a CzVCA), počet kandidátů podle zdroje a předběžnou triáž. Po mém schválení ověřování po 5–10 investorech na commit.

5. Push: commity 1–6 pushni na origin teď. Od této chvíle už žádné --amend ani přepisování historie u pushnutých commitů.
   </pasted_content id="2b08">

---

## 🤖 Claude

Nejdřív pushnu commity 1–6, jak jsi schválil.

---

## 🤖 Claude

Teď validace: důvod vyloučení musí mít podpůrný fakt, `minutes` v protokolu hledání a kontrola `effort_log`.

---

## 🤖 Claude

Validátor je hotový. Přidám metriku pracnosti a do reportu sekci „Pracnost“.

---

## 🤖 Claude

Upravím testovací data a doplním testy pro nová pravidla.

---

## 🤖 Claude

Test čekal pevný počet řádků, který dřív vycházel jen náhodou. Upravím ho, aby ověřoval skutečné chování: vzorek je celý v šabloně a žádný řádek se nezdvojí.

---

## 🤖 Claude

Testy procházejí (166). Doplním dokumentaci: pravidla sběru, fakt `duvod_vylouceni` a měření času.

---

## 🤖 Claude

Commit `ca2e602` je hotový. Varování o CRLF jsou neškodná: v repozitáři se soubory díky `.gitattributes` ukládají s LF. Teď začínám hledat kandidáty.

---

## 🤖 Claude

Teď otevřu přímo web asociace CzVCA a seznamy ČNB, včetně jejich `robots.txt`.

---

## 🤖 Claude

Doména `czvca.cz` neexistuje. Dohledám správnou adresu asociace.

---

## 🤖 Claude

Asociace se jmenuje CVCA a sídlí na `cvca.cz`. Otevřu `robots.txt` a stránku řádných členů.

---

## 🤖 Claude

ARES funguje: vrací JSON s obchodním jménem, IČO a sídlem. Bude tedy primárním zdrojem pro kritérium Z1. Teď otevřu přehledový článek CzechCrunch o fondech.

---

## 🤖 Claude

Teď zapíšu protokol hledání a seznam kandidátů. Názvy přebírám tak, jak je uvádějí otevřené stránky. Typ a zemi vyplňuji jen tam, kde je zdroj uvádí.

---

## 🤖 Claude

Chyba se týkala jen závěrečného výpisu do konzole: Windows ho zkoušel zakódovat v cp1252. Soubory se zapsaly a validace prošla. Zkontroluji jejich obsah.

---

## 🤖 Claude

Řádek `inv-0031` je v CSV správně v uvozovkách, posun sloupců je jen artefakt výpisu. Commituji.

---

## 🤖 Claude

Protokol hledání a seznam 50 kandidátů jsou v commitu `fbd0803`. Před tím přibyly dva menší commity: `ca2e602` doplnil validaci a měření času podle tvých podmínek 2 a 3, `a3265f6` uvolnil povinnost vyplnit typ a zemi u kandidátů. Lokálně jsem 3 commity napřed před `origin` a bez tvého souhlasu je nepushnu. Testy procházejí (169) a `validate` je bez chyb.

## Dostupnost zdrojů

| Zdroj                                                                                                                                                                                                         | Výsledek                                 | Co obsahuje                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **CVCA** ([cvca.cz – full members](https://cvca.cz/en/category/full-members/))                                                                                                                                | ✅ dostupné, `robots.txt` nic nezakazuje | 27 řádných členů. U každého typ investic, objem fondů a sektory, bez IČO. Převažují PE fondy (buyout, growth).                      |
| `czvca.cz`                                                                                                                                                                                                    | ❌ doména neexistuje                     | Asociace vystupuje jako CVCA na `cvca.cz`.                                                                                          |
| **ČNB – popis § 15** ([stránka ČNB](https://www.cnb.cz/cs/dohled-financni-trh/vykon-dohledu/upozorneni-pro-verejnost/Role-CNB-u-spravcu-podle-15-zakona-o-investicnich-spolecnostech-a-investicnich-fondech)) | ✅ dostupné                              | Seznam § 15 je součástí JERRS. Zápis není licencí a ČNB údaje neověřuje. Investiční strategie v seznamu podle stránky uvedena není. |
| **ČNB – JERRS**                                                                                                                                                                                               | ❌ za CAPTCHA                            | Nástroji se nedá projít a export stránka nezmiňuje. Půjde použít jen při tvé ruční kontrole.                                        |
| **ARES REST API**                                                                                                                                                                                             | ✅ funguje                               | JSON s obchodním jménem, IČO a sídlem. Bude to primární zdroj pro kritérium Z1.                                                     |
| [Wikipedie – VC in the Czech Republic](https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic)                                                                                                   | ✅ sekundární                            | 16 kandidátů                                                                                                                        |
| [CzechCrunch, 2. 4. 2024](https://cc.cz/purple-presto-kaya-a-dalsi-investori-maji-apetit-startupove-fondy-nabiraji-dalsi-miliardy-korun/)                                                                     | ✅ médium                                | 19 kandidátů, z toho část jsou investoři v seed kolech                                                                              |
| BusinessInfo (CEE Funding Map)                                                                                                                                                                                | ❌ HTTP 403                              | —                                                                                                                                   |

**Hlavní zjištění:** seznamy ČNB nejdou použít k hledání kandidátů. Neobsahují strategii a JERRS je za CAPTCHA. Primárním zdrojem pro identitu (Z1) bude ARES. Kandidáty jsem získal z CVCA a ze sekundárních zdrojů.

## Kandidáti podle zdroje

Celkem jde o 50 unikátních subjektů: 27 z CVCA, 11 nových z Wikipedie a 12 nových z CzechCrunch. Duplicity mezi zdroji jsem sloučil, například Credo, KAYA, Depo, Inven, Orbit, Tilia, Presto, Purple a Reflex.

## Předběžná triáž (jen návrh, v datech jsou zatím všichni `kandidat`)

| Skupina                               | Počet | Subjekty                                                                                                                                                                                                                 |
| ------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **VC – k ověření**                    | 21    | Credo, KAYA, Depo, Nation1, Tensor, i&i Biotech, Orbit, Tilia, Presto, Rockaway Ventures, J&T Ventures, Purple, Impulse, Lighthouse, Reflex, Tachles, IVBF, Zaka VC, Inven Capital, Fond rizikového kapitálu, Springtide |
| **Nejasné (investoři v seed kolech)** | 7     | Techstars, Soulmates Ventures, 10X, Patero, Startguide VC, Gain Ventures, StartupYard                                                                                                                                    |
| **Pravděpodobně vyloučit – PE**       | 17    | Členové CVCA s buyout/growth strategií (Stratum, Thein, Espira, EVERITA, Abris, ARX, Integral, MAM, Enterprise, Genesis, Innova, Jet, Mid Europa, SkyLimit, Versute, V4C, Sandberg)                                      |
| **Pravděpodobně vyloučit – ostatní**  | 5     | CVI (dluhové financování), Miton (podle Wikipedie investuje jen vlastní kapitál), Seed Fund (státní program), EIF (fond fondů), OTB Ventures (článek ho označuje za polský fond)                                         |

U Inven Capital a Springtide budu teprve dokládat případnou vazbu na korporaci, z paměti ji nedoplňuji. U Springtide článek uvádí, že spadá pod KKCG.

Čas: 8 průchodů zabralo 8 minut běhu modelu. Měřil jsem ho jen souhrnně, což je uvedeno v poznámkách. Od další dávky budu měřit každého investora zvlášť.

## Potřebuji rozhodnout

1. **Rozsah ověřování:** Mám ověřovat všech 50 (PE a ostatní by šli rychle jako vyloučení s faktem z CVCA), nebo jen 28 VC a nejasných kandidátů? Doporučuji všech 50, protože to ukáže celý trychtýř od nalezených po ověřené.
2. **CVI (dluhový fond):** Mám pro něj použít důvod `mimo_definici_pilotu` a doplnit dluhové fondy do jeho definice v dokumentaci?
3. **Push:** Mám pushnout 3 nové commity?

Webové vyhledávání jsem používal jen k nalezení zdrojů. Do dat jde jen to, co jsem přečetl na otevřených stránkách. Dotaz na seznam fondů EIF nenašel žádnou stránku se seznamem, takže z EIF zatím nemám nic.

Zdroje:

- [CVCA – Full members](https://cvca.cz/en/category/full-members/)
- [ČNB – Role ČNB u správců podle § 15](https://www.cnb.cz/cs/dohled-financni-trh/vykon-dohledu/upozorneni-pro-verejnost/Role-CNB-u-spravcu-podle-15-zakona-o-investicnich-spolecnostech-a-investicnich-fondech)
- [ČNB – JERRS](https://www.cnb.cz/cs/dohled-financni-trh/seznamy/jerrs)
- [Wikipedia – Venture capital in the Czech Republic](https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic)
- [CzechCrunch – Purple, Presto, Kaya a další…](https://cc.cz/purple-presto-kaya-a-dalsi-investori-maji-apetit-startupove-fondy-nabiraji-dalsi-miliardy-korun/)
- [EIF – RRF Czech Republic](https://www.eif.org/products/all/rrf-czech-republic)
- [BusinessInfo – CEE Funding Map](https://www.businessinfo.cz/clanky/cee-funding-map-prinasi-prehled-aktivnich-investoru-ve-stredni-a-vychodni-evrope/)

---

## 👤 User

<pasted_content id="2b08">
Rozhodnutí:

1. Ověřuj všech 50, ale ve dvou úrovních: 28 kandidátů (VC + nejasní) plné ověření Z1–Z4; 22 pravděpodobně vyloučených jen rychlé vyloučení s jedním doloženým faktem. Čas měř zvlášť pro obě úrovně – v odhadu nákladů ukážeme, že triáž je levná a ověření drahé. Trychtýř (nalezeno → triáž → ověřeno/vyloučeno) uveď v dokumentaci.

2. CVI: ano, mimo_definici_pilotu a dluhové fondy doplň do definice v dokumentaci.

3. Push: ano. Od teď pushuj po každém commitu, u kterého projdou testy i validate – už se neptej.

4. Doplnění hledání: CVCA je převážně PE asociace a VC kandidáti pochází hlavně ze sekundárních zdrojů, takže hrozí, že méně viditelné VC fondy chybí. Před ověřováním zkus další zdroj kandidátů: veřejné seznamy fondů, do kterých investovaly fondy fondů (Národní rozvojová banka / Národní rozvojový fond, EIF – RRF Czech Republic, případně tiskové zprávy o výběru fondů). Ověř také, zda CVCA nemá i jiné kategorie členů než full members. Každý průchod zapiš do search_log.csv, nové kandidáty přidej a sjednoť duplicity. Pokud zdroj nic neposkytne, zapiš to a pokračuj.

5. Odhad pokrytí: protože máme několik částečně se překrývajících seznamů kandidátů, připrav v metrics odhad celkového počtu VC v ČR metodou capture–recapture (Lincoln–Petersen, případně Chapmanova korekce) z překryvů zdrojů. V dokumentaci uveď, že zdroje nejsou nezávislé a odhad je tedy spíše dolní mez. Pro výpočet bude potřeba zaznamenat, ve kterých zdrojích byl každý kandidát nalezen – pokud to search_log neumožňuje, navrhni úpravu.

6. Čas ruční kontroly: do šablon reviews.csv a fact_reviews.csv přidej sloupec review_minutes. Čas modelu a čas člověka se v odhadu nákladů vykazují zvlášť.

Pak pokračuj ověřováním po 5–10 investorech na commit. Zastav se, až budou všichni ověřeni, a ukaž mi souhrn.
</pasted_content id="2b08">

---

## 🤖 Claude

Začnu pushem tří čekajících commitů. Pak doplním kód (původ kandidátů ve zdrojích, capture–recapture, trychtýř, `review_minutes`), rozšířím hledání a pustím se do ověřování.

---

## 🤖 Claude

Push proběhl. Teď úpravy kódu. Než je začnu psát, projdu si aktuální stav dotčených souborů.

---

## 🤖 Claude

Teď metriky: capture–recapture (Lincoln–Petersen a Chapman), trychtýř a čas ruční kontroly.

---

## 🤖 Claude

Schéma se změnilo, takže přegeneruji hlavičky prázdných tabulek kontrol. Zároveň vytvořím `candidate_sources.csv`, kde je u každého kandidáta zapsaný průchod, ve kterém byl nalezen.

---

## 🤖 Claude

Shell heredoc tak dlouhý skript nezpracoval. Uložím ho do souboru v scratchpadu a spustím odtud.

---

## 🤖 Claude

Testovací případ měnil špatné pole. Chybějící vazbu vyvolá jen to, když řádek patří jinému investorovi.

---

## 🤖 Claude

Testy procházejí (183) a validace je bez chyb. Teď dokumentace: dluhové fondy, dvě úrovně zpracování, trychtýř, `candidate_sources`, capture–recapture a `review_minutes`.

---

## 🤖 Claude

Nejslibnější je článek CzechCrunch o 17 českých fondech, do kterých vložil peníze EIF. Otevřu ho, spolu se zprávou o NRI a zprávou o IP Lab Ventures.

---

## 🤖 Claude

Na webu NRB jsou dvě relevantní zprávy, o výběru fondu pro program Fond Ukrajina a o DeepTech fondu. Otevřu je.

---

## 🤖 Claude

Dvojice s velmi malým zdrojem (n = 1–2) dávají nesmyslné odhady. Do výpočtu proto zahrnu jen průchody, které našly aspoň 5 subjektů dané populace, a hranici uvedu v dokumentaci.

---

## 🤖 Claude

Typy investic na CVCA sedí s prvním čtením. Zapíšu rychlou triáž 22 subjektů.

---

## 🤖 Claude

Rychlá triáž trvala necelou minutu na všech 22 subjektů. Zápis 1 minuty na subjekt (nejmenší celé číslo) skutečný čas nadhodnocuje a v souhrnu to uvedu. Commit a push:

---

## 🤖 Claude

Web ani profil CVCA IČO neuvádějí. Zkusím vyhledávání podle názvu v obchodním rejstříku (justice.cz) a otevřu newsroom kvůli datované investici.

---

## 🤖 Claude

Pro zápis ověření si připravím pomocný skript ve scratchpadu. Zdroje, ID faktů a odvozená pole (`evidence_urls`, `last_verified_at`) bude generovat sám, aby se nedala ručně splést.

---

## 🤖 Claude

Omylem jsem spustil `cat`, který čeká na vstup. Zastavím ho. Soubor `sources.py` se zapsal dřív.

---

## 🤖 Claude

Credo Ventures je ověřený: 9 faktů, 5 minut, validace prošla. Pokračuji s KAYA VC.

---

## 🤖 Claude

V rejstříku je víc subjektů Kaya na adrese z profilu CVCA (Thámova 183/11). Správnou entitu značky musí určit web, ne můj odhad.

---

## 🤖 Claude

Hledám pro KAYA datovanou investici. Agregátory (Seedtable, Techleap) vracejí 403, takže zkouším tiskové zprávy startupů.

---

## 🤖 Claude

Pro KAYA je doložená investice: pre-seed kolo Riptides z 23. 4. 2025, kde KAYA podle článku Vestbee spoluinvestovala. Zapisuji.

---

## 🤖 Claude

KAYA je ověřená. Další je Depo Ventures. NRB jeho správce popisuje jako lucemburský, takže rozhodující bude, jestli značka má i českou entitu.

---

## 🤖 Claude

Depo Ventures je ověřený. Teď Nation1 a s ním i kandidát „N1“ z článku o EIF.

---

## 🤖 Claude

Dávka 1 je pushnutá (`acb91c9`). Dávka 2: Tensor Ventures, i&i Biotech, Tilia, Orbit Capital a Inven Capital. Začínám profily CVCA a rejstříkem.

---

## 🤖 Claude

Tensor má doloženou investici do DYNANIC z 28. 11. 2024, první z druhého fondu. To je v rámci 36 měsíců. Zapisuji.

---

## 🤖 Claude

Zápis selhal: `data/investors.csv` je zamčený jiným procesem. Na Windows to bývá soubor otevřený v Excelu. Zkontroluji, jestli se nic nezapsalo napůl.

---

## 🤖 Claude

Excel je zavřený. Zkontroluji, že ho soubor neuložil změněný, a pak zopakuji zápis i&i.

---

## 🤖 Claude

i&i trval od 14:23:58 do selhání zápisu asi 2 minuty, Tilia od té doby asi 3 minuty. Zapíšu obě.

---

## 🤖 Claude

Tensor, i&i a Tilia jsou ověřené. Než dávku 2 uložím, dodělám ještě Orbit Capital a Inven Capital. Do metodiky mezitím doplním pravidlo (c).

---

## 🤖 Claude

Orbit je zapsaný jako kandidát. Dalším je Inven Capital, kde ověřuji, jestli jde o corporate VC.

---

## 🤖 Claude

Dávka 2 je pushnutá (`eb10da4`). Dávka 3: Presto, Rockaway Ventures, Fond rizikového kapitálu, J&T Ventures, Purple a Impulse.

---

## 🤖 Claude

Doménu presto.vc jsem odhadl a je zaparkovaná, tu nepoužiji. Správný web dohledám vyhledáváním.

---

## 🤖 Claude

Presto je ověřený. Teď Rockaway Ventures.

---

## 🤖 Claude

Rockaway Ventures je ověřený. Fond rizikového kapitálu, s.r.o. zmiňuje Wikipedie jen historicky (výnosy do roku 2000). Ověřím v rejstříku, jestli subjekt ještě existuje.

---

## 🤖 Claude

Pravidlu (b) odpovídají dva fondy SICAV na adrese z webu. Zásady zpracování osobních údajů by mohly jmenovat správce údajů, a tím spor rozhodnout podle pravidla (a).

---

## 🤖 Claude

Web jmenuje správce údajů J&T Ventures CG SICAV a.s., IČO 08220867. Platí tedy pravidlo (a). Pro Z4 otevřu blog.

---

## 🤖 Claude

Pro Purple platí pravidlo (c): Purple Ventures s.r.o. je jediný subjekt s přesným názvem značky. Pro Z4 otevřu zprávu o investici do Kilde (říjen 2025) a web značky.

---

## 🤖 Claude

Dávka 3 je pushnutá (`fe42afb`): dalších 4 ověření a 2 vyloučení. Zbývá 14 subjektů. Pokračuji dávkou 4: Lighthouse, Reflex, Tachles, IVBF, Springtide a IP Lab Ventures.

---

## 🤖 Claude

Lighthouse zůstává kandidátem. Teď Reflex Capital. Doloženou investici z blogu J&T (grid.online, 3. 3. 2025) už mám, potřebuji web a entitu.

---

## 🤖 Claude

Pro Reflex Capital platí pravidlo (c): Reflex Capital SE, IČO 24269158. Otevřu článek o třetím fondu a zkusím web.

---

## 🤖 Claude

Tachles VC: web tachles.vc neexistuje a s českou entitou žádné pravidlo nepracuje. Tachles VC Management s.r.o. má v názvu slovo navíc a adresu značky neznám. Zůstává `kandidat`.

---

## 🤖 Claude

Zápis se zastavil uprostřed: `investors.csv` se uložil, ale `facts.csv` je zamčený, takže data jsou teď nekonzistentní a validace to správně hlásí. Zjistím, co soubor drží.

---

## 🤖 Claude

Teď IP Lab Ventures, nový fond ze září 2026. Podle zpráv výběr projektů teprve začíná, takže doloženou investici nejspíš mít nebude.

---

## 🤖 Claude

Dávka 4 je pushnutá (`c2fae0a`). Poslední dávka 5 obsahuje 8 nejasných investorů ze seed kol: Techstars, Soulmates, 10X, Patero, Startguide VC, Gain Ventures, StartupYard a Zaka VC.

---

## 🤖 Claude

Soulmates je ověřený. 10X a Patero jsou zmínění jen jako investoři v seed kole Flowpay. Najdu, o koho jde.

---

## 🤖 Claude

Data se zapsala správně. Úprava dokumentace ale neprošla kontrolou shody textu. Podívám se, jak řádek teď vypadá.

---

## 🤖 Claude

Startguide je ověřený. Zbývají poslední 3 subjekty: Gain Ventures, StartupYard a Zaka VC.

---

## 🤖 Claude

Všech 52 subjektů je zpracovaných a dávka 5 je pushnutá (`c94022f`). Spustím metriky pro souhrn.

---

## 🤖 Claude

Všech 52 nalezených subjektů je zpracovaných: 14 ověřených investorů, 9 kandidátů, kteří potřebují tvé rozhodnutí nebo další zdroj, a 29 vyloučených, každý s doloženým důvodem. Validace i 185 testů procházejí a vše je pushnuté (poslední commit `c94022f`). Ruční kontrola R1 zatím chybí, takže precision ještě nemáme.

## Trychtýř

| Úroveň       | Celkem | Ověřeno | Kandidát | Vyloučeno |
| ------------ | ------ | ------- | -------- | --------- |
| Rychlá triáž | 22     | –       | –        | 22        |
| Plné ověření | 30     | 14      | 9        | 7         |

**Ověření investoři (14):** Credo Ventures, KAYA VC, Depo Ventures, Tensor Ventures, i&i Biotech, Tilia Impact Ventures, Inven Capital, Presto Ventures, Rockaway Ventures, J&T Ventures, Purple Ventures, Reflex Capital, Soulmates Ventures, Startguide VC.

**Vyloučení při plném ověření (7):**

- N1: duplicita Nation1.
- Fond rizikového kapitálu: subjekt je vymazaný z rejstříku.
- Impulse Ventures: investuje jen vlastní peníze.
- IVBF: fond digitálních aktiv.
- Springtide Ventures: corporate VC skupiny KKCG.
- Techstars: zahraniční subjekt.
- 10X: otevřený smíšený fond.

**Data:** 181 faktů ze 70 zdrojů. U všech 14 ověřených je IČO doložené z primárního zdroje a investice za posledních 36 měsíců je doložená. Z primárních zdrojů ale pochází jen 55,8 % faktů, zbytek jsou média a agregátory.

## Co bys měl vědět, než začneš kontrolu

1. **Nástroj na čtení stránek vrací shrnutí od menšího modelu, ne surový text.** Pravidlo „jen ze skutečně otevřené stránky“ jsem dodržel, ale chyba v přečtení je možná. Právě proto je kontrola faktů s otevřením zdroje důležitá.
2. **Přiřazení české entity ke značce (Z1)** jsem musel formalizovat třemi pravidly (a/b/c v `docs/02-metodika.md`).
   - Pravidlo (c), tedy jediný subjekt přesně s názvem značky, je slabé. Případ Techstars ukázal, že by přiřadilo nesouvisející firmu z Třince.
   - Pouze na (c) stojí Rockaway Ventures a u Tensoru je to (c) plus stejná ulice. Doporučuji tyto dva zkontrolovat přednostně.
   - Návrh: pravidlo (c) zrušit, nebo ho povolit jen s doplňkovým důkazem.
3. **Data s měsíční přesností:** u 5 investic znám jen měsíc, proto `value_as_of` = 1. den měsíce a evidence_note to uvádí.
4. **`total_fund_size` je vyplněno u 0 ze 14.** Zdroje píšou „uzavřel fond“, ale nikdy výslovně „final close“. Podle tvého pravidla jsem pole nechal prázdné a údaj je jen ve faktu `informace_o_fondu`.

## Rozhodnutí, která potřebuji

1. **Hraniční kandidáti:**
   - **Orbit Capital:** většina aktivity je venture debt. Vyloučit jako dluhový fond?
   - **StartupYard:** akcelerátor s kapitálem investorů ve vehiklech pro každý ročník. Patří do pilotu?
   - **Zaka VC:** zdroj ho označuje za family office, ale později vznikla osoba rizikového kapitálu. Vyloučit?
   - **Inven Capital (ČEZ) a Rockaway Ventures (asi 25 % kapitálu od Rockaway Capital):** nechávám jako VC, protože převažuje kapitál třetích osob. Souhlasíš?
2. **Kandidáti s nedoloženou entitou nebo aktivitou:** Nation1, Lighthouse, Tachles, IP Lab Ventures (nový fond bez investic), Patero, Gain Ventures. Ponechat jako `kandidat`, nebo u Lighthouse použít `neaktivni` (poslední doložená investice je z roku 2019)?
3. **Slovník sektorů:** chybí obrana/bezpečnost, cestování a logistika. U Presta proto sektory zůstaly prázdné. Mám je přidat?
4. **Měření času:** celé minuty jsou moc hrubé. Triáž vychází na 1,0 min a ověření na 1,5 min na investora, přitom skutečná triáž trvala asi 2 s na subjekt. Mám povolit desetinné minuty? Pro odhad nákladů je ale stejně podstatnější tvůj čas kontroly.

## Capture–recapture

Ověřených VC vychází podle dvojic zdrojů zhruba 13–19 (Chapman). Zdroje jsou ale silně závislé: článek o EIF je téměř celý obsažený v seznamu CVCA, takže tato dvojice dává degenerovaný odhad 7. Odhad je proto jen dolní mez.

## Incidenty

- **Zamčený soubor:** zápis dvakrát selhal na zamčeném CSV. Poprvé ho držel otevřený Excel, podruhé neznámý proces. Při druhém selhání zůstala data krátce nekonzistentní. Pomocný skript teď zapisuje přes dočasné soubory a selhání opakuje. Čas u i&i a Tilie je proto odhad z časových značek a je tak označený.
- **Commit `c2fae0a`:** v popisu uvádí rozšíření definice, které se kvůli selhání tehdy neprovedlo. Napravil jsem to a výslovně uvedl v `c94022f`. Historii jsem nepřepisoval.
- **Domény:** domény presto.vc a tachles.vc jsem zkusil odhadnout. První je na prodej, druhá neexistuje. Do dat jsem z nich nic nevzal.

## Další krok: tvoje kontrola

```
python -m investor_db review-template --reviewer R1
python -m investor_db fact-review-template --reviewer R1
```

První příkaz připraví 14 záznamů ke kontrole, druhý náhodný vzorek 63 ze 181 faktů. Do `review_minutes` prosím zapisuj čas. Až budeš hotový, napiš a dopočítám precision a připravím `docs/03-globalni-odhad.md`.

Zdroje (výběr; úplný seznam je v `data/sources.csv`):

- [CVCA – full members](https://cvca.cz/en/category/full-members/)
- [Obchodní rejstřík](https://or.justice.cz/)
- [Wikipedia – VC in the Czech Republic](https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic)
- [CzechCrunch – fondy s EIF](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/)
- [NRB – Fond Ukrajina](https://www.nrb.cz/nri-dokoncila-vyber-venture-kapitaloveho-fondu-pro-program-fond-ukrajina/)
- [Vestbee – Riptides](https://www.vestbee.com/blog/articles/riptides-secures-3-3-m)
- [Brno Tech Region – DYNANIC](https://brnotechregion.eu/en/news/cipova-revoluce-z-univerzitniho-brna-tensor-ventur)
- [Tech.eu – Orbit Capital](https://tech.eu/2026/07/02/orbit-capital-closes-eur107m-venture-debt-fund-for-cee-scaleups/)
- [Seznam Zprávy – Impulse Ventures](https://www.seznamzpravy.cz/clanek/novy-cesky-fond-nabizi-ctyri-miliardy-pro-technologicke-nadsence-118740)
- [E15 – IVBF](https://www.e15.cz/kryptomeny/do-sveta-kryptomen-vstupuje-dalsi-cesky-miliardar-ondrej-tomek-rozjizdi-novy-fond-1411749)
- [AIN.UA – Zaka VC](https://en.ain.ua/2024/03/11/zaka-vc-invests-in-eigen-therapeutics)

---

## 👤 User

<pasted_content id="2b08">
Než začnu kontrolu, zapracuj prosím tato rozhodnutí. Pak přegeneruj šablony kontroly.

1. Corporate VC – jednotné pravidlo: CVC = více než 50 % kapitálu fondu od jedné korporátní skupiny. Aplikuj stejně na Inven Capital i Springtide (i na ostatní). Pokud rozložení kapitálu není doloženo, status je kandidat. Rockaway (~25 % od skupiny) tedy podle pravidla zůstává VC, pokud je to doloženo. Pravidlo zapiš do metodiky.

2. Pravidlo (c) pro přiřazení entity zruš. Rockaway Ventures a Tensor Ventures dolož silnějším důkazem (IČO v impresu/kontaktech webu, shoda adresy se zdrojem investora, shoda osob ve statutárním orgánu s týmem). Pokud se nepodaří, status kandidat.

3. total_fund_size: pravidlo „final close“ bylo příliš přísné. Přijímej výslovné tvrzení v minulém čase, že fond byl uzavřen s danou velikostí (z webu investora, tiskové zprávy nebo spolehlivého média). Nepřijímej first close, cílovou velikost ani formulace „až X“. Projdi znovu fakty informace_o_fondu a podle toho doplň. Pravidlo uprav v metodice.

4. Shrnutí od nástroje: u všech peněžních částek a dat investic ověř hodnotu proti surovému textu stránky (urllib ze standardní knihovny, s ohledem na robots.txt). Stažené stránky neukládej do repozitáře. Výsledek zapiš do evidence_note (ověřeno proti surovému textu ano/ne). Omezení popiš v dokumentaci.

5. Hraniční kandidáti:
   - Orbit Capital: vyloucen jako dluhový fond (stejně jako CVI).
   - StartupYard: akcelerátor s vehiklem s kapitálem třetích osob spadá do definice. Ověř Z1–Z4, a pokud platí, overeny. Model akcelerátoru uveď v poznámce.
   - Zaka VC: bez doložení kapitálu třetích osob vyloucen jako family office.
   - Lighthouse: žádný nový status nezavádíme. Zůstává kandidat s poznámkou o poslední doložené investici v roce 2019.
   - IP Lab Ventures: podle Z4 se nový fond za posledních 36 měsíců počítá jako aktivita. Pokud je doložená entita, může být overeny.
   - Nation1, Tachles, Patero, Gain Ventures: zůstávají kandidat, pokud nenajdeš primární doklad.

6. Slovník sektorů: přidej obrana_bezpecnost, cestovani, logistika a jine. Doplň sektory u Presta.

7. Čas: povol desetinné minuty.

8. Domény neodhaduj. Web investora hledej jen přes zdroje.

Po zapracování spusť testy a validate, pushni a pošli mi krátký souhrn změn statusů. Pak teprve přegeneruj šablony R1.
</pasted_content id="2b08">

---

## 🤖 Claude

Začnu kódem a dokumentací. Pak data znovu projdu podle nových pravidel a nakonec ověřím peněžní částky a data investic proti surovému textu stránek.

---

## 🤖 Claude

Teď úpravy kódu: desetinné minuty, nové sektory a Z4 s novým fondem jako aktivitou.

---

## 🤖 Claude

Testy selhávají jen kvůli očekávanému novému chování: nové znění chyby u minut a Z4 s novým fondem. Upravím je a přidám testy na desetinné minuty a nový fond.

---

## 🤖 Claude

Upravím ještě jednotku milionů, aby „mil…“ nezachytilo i „miliardy“. Pak přidám příkaz do CLI a testy s falešným openerem, takže testy nepotřebují síť.

---

## 🤖 Claude

Pravidla jsou pushnutá (`b7737ff`). Teď data. Začnu přepočtem časů na desetinné minuty ze skutečných časových značek v logu.

---

## 🤖 Claude

Teď přepracování jednotlivých subjektů podle tvých rozhodnutí. Pomocný zápis nejdřív upravím, aby i nové řádky měřil v desetinných minutách.

---

## 🤖 Claude

Výsledky naznačují, že většinu kapitálu Inven Capital tvoří ČEZ. Otevřu článek z července 2026, abych podíl doložil z otevřené stránky.

---

## 🤖 Claude

Springtide Ventures podle stejného pravidla: hledám, kolik kapitálu dává KKCG.

---

## 🤖 Claude

Ani u Springtide žádný zdroj neuvádí podíl KKCG na kapitálu, jen že fond je součástí skupiny. Podle pravidla vracím Springtide mezi kandidáty a ruším vyloučení.

---

## 🤖 Claude

Orbit a Zaka jsou vyloučené. U Lighthouse doplním poslední doloženou investici (Pekat Vision, červen 2019) jako fakt.

---

## 🤖 Claude

Hledám českou entitu IP Lab Ventures. Zakladatele jmenuje CzechCrunch (Navrátil, Fingl, Hladký), takže když najdu subjekt v rejstříku, zkusím pravidlo (d).

---

## 🤖 Claude

Výsledek: 15 ověřených, 7 kandidátů, 30 vyloučených. Ukládám commit.

---

## 🤖 Claude

Heuristika dat je rozšířená a 218 testů prochází. Teď nahrazení faktů z obchodního rejstříku. Nejdřív si vypíšu, kterých faktů se to týká a jaká IČO dokládají.

---

## 🤖 Claude

Vyhledávací API ARES vrací pro „Fond rizikového kapitálu“ 0 subjektů. To bude nový doklad zániku. Upravím skript, aby tento fakt zpracoval zvlášť, a spustím ho znovu.

---

## 🤖 Claude

V datech už žádný odkaz na justice.cz nezůstal. Doplním metodiku (rejstřík jen přes ARES a důvod) a uložím commit.

---

## 🤖 Claude

Commit `2fc5ece` je pushnutý. Spustím znovu kontrolu surového textu: ID faktů se změnila, heuristika je rozšířená a Tech.eu dřív vrátil HTTP 429.

---

## 🤖 Claude

Všechny změny jsou pushnuté. Jako poslední krok vygeneruji šablony kontroly pro R1 nad finálními daty.

---

## 🤖 Claude

Šablona kontroly investorů hlásí jen 2 přidané řádky, přitom ověřených je 15. To nesedí, podívám se, co v `reviews.csv` je.

---

## 🤖 Claude

Všechna rozhodnutí jsou zapracovaná a šablony pro R1 jsou připravené. Testy (218) i validace procházejí a vše je pushnuté (poslední commit `e9c570d`).

## Změny statusů

| Subjekt             | Před     | Po           | Důvod                                                                                                                                               |
| ------------------- | -------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inven Capital       | overeny  | **kandidat** | Podíl ČEZ na aktuálním kapitálu není doložen. Článek z roku 2017 jmenuje jako investory ČEZ a EIB, ale zmiňuje i další peníze z neuvedených zdrojů. |
| Springtide Ventures | vyloucen | **kandidat** | Příslušnost ke KKCG je doložená, podíl skupiny na kapitálu ne.                                                                                      |
| StartupYard         | kandidat | **overeny**  | Z1 podle shody adresy (StartupYard Services s.r.o.). Z4 jen přes nový vehikl Batch 15 z 11/2024, datovanou investici jsem nenašel.                  |
| IP Lab Ventures     | kandidat | **overeny**  | Z1: jednatelé IP Lab Services s.r.o. jsou zakladatelé IP Lab. Z4: nový fond z 9/2026.                                                               |
| Orbit Capital       | kandidat | **vyloucen** | Dluhový fond                                                                                                                                        |
| Zaka VC             | kandidat | **vyloucen** | Family office                                                                                                                                       |

- **Rockaway a Tensor:** zůstávají ověřené, Z1 je teď doložené shodou statutárního orgánu s týmem.
- **Tachles:** má nově doloženou entitu, ale zůstává kandidátem, protože žádný zdroj neuvádí fázi investic.
- **Ostatní:** Nation1 (jednatelé se neshodují se správcem fondu), Lighthouse (poslední investice 2019), Patero a Gain zůstávají kandidáty.

**Výsledek:** 15 ověřených, 7 kandidátů, 30 vyloučených.

## Další změny

- **`total_fund_size`:** doplněno u Reflexu (22 mil. EUR) a Presta (30 mil. EUR). U ostatních zdroje uvádějí jen first close, cíl nebo přibližné částky.
- **Sektory:** u Presta, Depa a Rockaway podle rozšířeného slovníku.
- **Časy:** jsou v desetinných minutách podle časových značek. Triáž vychází na 0,03 min na subjekt, plné ověření v průměru zhruba na 1 min.
- **Surový text:** zkontroloval jsem 72 částek a dat investic. 69 se potvrdilo, z toho 7 jsem posoudil ručně, protože jsou zapsané slovy. 3 se nepotvrdily:
  - Tilia: Tech.eu vrací HTTP 429.
  - Inven: datum je jen v adrese odkazu.
  - Zaka: částka ve faktu pochází z jiného zdroje.

## Co bys měl vědět

**Porušil jsem `robots.txt` obchodního rejstříku.** or.justice.cz zakazuje cestu `/ias/` a já ji při prvním sběru používal. Odhalila to až kontrola surového textu. Všech 23 faktů odtud jsem nahradil ověřením v ARES a obchodní jména se shodují. Sbírku listin kvůli tomu nelze v pilotu používat; je to uvedené v metodice.

**Šablony pro tebe:**

- `data/reviews.csv`: 15 řádků, jeden pro každého ověřeného investora.
- `data/fact_reviews.csv`: náhodný vzorek 66 z 205 faktů.

Do sloupce `review_minutes` prosím zapisuj čas, který kontrolou strávíš.

---

## 👤 User

<pasted_content id="2b08">
Před mou kontrolou ještě tři drobnosti, pak už na data nesahej, dokud ti nedám vědět:

1. Potvrď, odkud teď pochází údaje o statutárních orgánech, na kterých stojí Z1 u Rockaway Ventures, Tensor Ventures, IP Lab Ventures a porovnání u Nation1. Pokud pocházely z or.justice.cz/ias/, nahraď je údaji z povoleného zdroje (např. ARES – endpoint veřejného rejstříku se statutárními orgány). Pokud to nejde, status kandidat.

2. Zaka VC: fakt s částkou odkazuje na nesprávný zdroj. Oprav přiřazení zdroje, nebo fakt odstraň.

3. Tilia: zkus Tech.eu znovu později s prodlevou. Inven: datum jen z URL označ v evidence_note jako slabý doklad.

4. Do dokumentace přidej sekci „Incidenty a poučení“ (porušení robots.txt u or.justice.cz/ias/ a náprava, zamčené CSV a atomický zápis, nesoulad popisu commitu c2fae0a). Do procesu sběru přidej kontrolu robots.txt před každým požadavkem (urllib.robotparser) a pokryj ji testem.

Pak testy, validate, push a krátké potvrzení. Šablony reviews.csv a fact_reviews.csv přegeneruj jen pokud se změnily ověřené záznamy nebo vzorek faktů.
</pasted_content id="2b08">

---

## 🤖 Claude

Začnu kódem: kontrolu `robots.txt` udělám povinnou pro každý síťový požadavek, ne jen pro `fetch_raw_text`. Potom ověřím statutární orgány proti surovému JSON z ARES a opravím fakty u Zaka VC, Tilie a Invenu.

---

## 🤖 Claude

Teď testy: povolená stránka se stáhne až po přečtení `robots.txt`, zakázaná nevyvolá žádný požadavek na stránku a totéž platí pro POST.

---

## 🤖 Claude

Řídicí znak `\n` se při zápisu přes heredoc proměnil ve skutečný konec řádku. Opravím to v nově přidaných testech.

---

## 🤖 Claude

Surový JSON z ARES potvrzuje všechny pět statutárních orgánů. U pravidla (d) ověřím proti surovému textu i druhou stranu shody, tedy jména týmu na webech a v článcích.

---

## 🤖 Claude

Teď dokumentace: sekce „Incidenty a poučení“ a zmínka o povinné kontrole `robots.txt` v pravidlech sběru.

---

## 🤖 Claude

Uložím commit a soubory přidám výslovně, podle poučení z incidentu. Potom naposledy zkusím Tech.eu.

---

## 🤖 Claude

Všechny čtyři body jsou hotové. Testy (222) i validace procházejí, vše je pushnuté (poslední commit `de4b18e`) a na data už nesahám.

1. **Statutární orgány nepocházely z or.justice.cz.** Byly z endpointu veřejného rejstříku ARES (`ekonomicke-subjekty-vr`), který `robots.txt` povoluje. Četl jsem je ale přes shrnovací nástroj, proto jsem je teď ověřil v surovém JSON:
   - Rockaway, Tensor, IP Lab a Tachles: shoda statutárního orgánu s týmem se potvrdila, a to i v surovém textu webů a článků, které tým jmenují. Statusy se nemění a fakty mají poznámku o ověření.
   - Nation1: neshoda se potvrdila (jednatelé Ton a Jiříček proti správci fondu Moravcovi), zůstává kandidátem.
2. **Zaka VC:** z hodnoty faktu se zdrojem ARES jsem odstranil částku 12–15 mil. EUR, protože ji dokládá jen článek AIN.UA. Fakt teď obsahuje jen to, co ARES dokládá (vznik 25. 4. 2024), a změna je v poznámce.
3. **Tilia a Inven:**
   - **Tilia:** Tech.eu vrátil HTTP 429 při čtyřech pokusech, naposledy po prodlevách 1 a 4 minuty. Omezení jsem neobcházel. Fakt o investici do Flox Intelligence zůstává ověřený jen ze shrnutí a Tilia je ověřená právě na jeho základě, doporučuji tenhle fakt při kontrole otevřít.
   - **Inven:** datum, které vyplývá jen z URL, je v evidence_note označené jako slabý doklad.
4. **Dokumentace a kód:**
   - V `docs/02-metodika.md` přibyla sekce „Incidenty a poučení“: porušení `robots.txt` a náprava přes ARES, zamčené CSV a atomický zápis, nesoulad popisu commitu `c2fae0a` a navíc přimíchaná šablona v `b7737ff`.
   - V kódu teď každý požadavek (`download`, `post_json`, `fetch_raw_text`) nejdřív přečte `robots.txt` přes `urllib.robotparser` a zakázanou cestu odmítne. Pokrývají to 4 nové testy.

Šablony jsem nepřegeneroval. Ověřené záznamy se nezměnily (15) a počet faktů zůstal 205, takže vzorek 66 faktů je stejný.

Můžeš začít s kontrolou.

---

## 👤 User

This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:

1. Primary Request and Intent:

**Projekt.** Testový projekt „Investor Intelligence Database“. Repozitář je `git@github.com:osho4753/investor-db.git`, lokálně `C:\Users\ramazan\investor-db` (přesunut z OneDrive). Cílem je reprodukovatelný proces vyhledávání, klasifikace a ověřování reálných investorů z bezplatných veřejných zdrojů. Prioritou je spolehlivost, ne počet. Pilot tvoří VC fondy / VC značky s českou právnickou osobou, 20–30 kandidátů.

**Povinné výstupy 1–8:**

1. plán a kritéria,
2. metodika,
3. globální odhad,
4. pilot ČR,
5. zdroje a data ověření,
6. ruční kontrola a precision,
7. odhad nákladů škálování,
8. kód, testy, dokumentace, Git historie a ai-log.

**Trvalá omezení a pravidla od uživatele (zachovat doslovně v platnosti):**

- „Komunikuj se mnou výhradně v češtině.“ Výstupy a dokumentace jsou česky.
- „Do kódu nepiš komentáře – kód má být čitelný sám o sobě (jasné názvy, type hints, malé funkce).“
- „Nesbírej data, nevymýšlej investory, odkazy ani hodnoty.“
- „Neinstaluj závislosti a nedělej destruktivní změny bez vysvětlení a mého souhlasu. Preferuj standardní knihovnu Pythonu“ (pytest je dev závislost).
- Pouze bezplatné veřejné zdroje. Placené databáze (Dealroom, Crunchbase Pro, PitchBook) nepoužívat.
- Scraping je povolen s respektem k `robots.txt` a podmínkám, s omezením rychlosti a cachováním. Jen ruční čtení jednotlivých stránek.
- „Každý fakt musí pocházet ze stránky, kterou jsi v této session skutečně otevřel. Nic nedoplňuj z vlastních znalostí ani odhadem. Pokud se stránka nenačte nebo údaj neobsahuje, hodnota zůstává neznámá a do protokolu zapiš, co se nepodařilo. accessed_at je skutečné datum přístupu. evidence_note stručně parafrázuje… necituj delší pasáže.“
- Ruční kontrolu dělá uživatel (R1) a volitelně nezávislý hodnotitel (R2), ne model.
- Push: „Od teď pushuj po každém commitu, u kterého projdou testy i validate – už se neptej.“ „Od této chvíle už žádné --amend ani přepisování historie u pushnutých commitů.“
- „Domény neodhaduj. Web investora hledej jen přes zdroje.“
- „Stažené stránky neukládej do repozitáře.“
- Poslední pokyn: „pak už na data nesahej, dokud ti nedám vědět“. Šablony `reviews.csv` a `fact_reviews.csv` přegenerovat jen tehdy, když se změní ověřené záznamy nebo vzorek faktů.

**Rozhodnutí uživatele:**

- **Jednotka záznamu:** VC značka. Právní správce se ukládá jako fakt.
- **Z1:** česká právnická osoba s IČO (správcovská, poradenská společnost nebo fond).
- **`total_fund_size`:** výslovné tvrzení v minulém čase, že fond byl uzavřen s danou velikostí. Nepřijímá se first close, cíl ani „až X“.
- **Fakty:** sloupec `fund_name` v `facts.csv`, bez `funds.csv`.
- **Vyloučení:** CVC, fondy fondů, státní a dluhové fondy jako `mimo_definici_pilotu`; zahraniční subjekt bez české osoby jako `zahranicni_subjekt`.
- **CVC:** více než 50 % kapitálu fondu od jedné korporátní skupiny. Pokud podíl není doložen, status je `kandidat`.
- **Měny:** jedna měna na řádek, bez přepočtů, metrika hodnot ponechaných jen ve `facts.csv`.
- **Kontrola:** R1 povinně, R2 volitelně. κ jen s daty R2 a vždy s procentem shody. `fact_reviews` se vzorkem (Cochran, seed 2026). Sloupec `review_minutes`.
- **Formáty:** ASCII kódy, Conventional Commits s českým popisem, ai-log přes `/export`.
- **Zpracování:** dvě úrovně (rychlá triáž s jedním faktem, plné ověření Z1–Z4), čas se měří zvlášť, trychtýř je v dokumentaci.
- **Capture–recapture:** Lincoln–Petersen a Chapman, s poznámkou o závislosti zdrojů.
- **Pravidla Z1:** pravidlo (c) zrušeno; přidáno pravidlo (d) shody statutárního orgánu s týmem.
- **Hraniční případy:** Orbit je dluhový fond (vyloučen). StartupYard s vehiklem spadá do definice. Zaka bez doložení kapitálu třetích osob je family office. Lighthouse zůstává kandidátem s poznámkou o roce 2019. U IP Lab se nový fond počítá jako aktivita Z4. Nation1, Tachles, Patero a Gain zůstávají kandidáty bez primárního dokladu.
- **Sektory:** přidány `obrana_bezpecnost`, `cestovani`, `logistika`, `jine`. Minuty jsou desetinné.

2. Key Technical Concepts:

- Python 3.11, jen standardní knihovna, pytest 9.0.2 (dev).
- CSV v Gitu jako jediný zdroj pravdy, UTF-8, LF.
- Validační skript plus pytest. Windows a Git Bash. `.gitattributes` s `eol=lf`.
- Tabulky: `investors`, `facts` (jeden řádek = jeden fakt), `sources`, `search_log`, `reviews`, `fact_reviews`, `effort_log`, `candidate_sources`.
- Kritéria Z1–Z4. Z4 = investice nebo nový fond za 36 měsíců (1096 dní).
- Pravidla Z1:
  - (a) web nebo profil jmenuje entitu nebo IČO,
  - (b) název obsahuje značku a sídlo se shoduje s adresou,
  - (d) statutární orgán se shoduje s týmem.
- Precision TP/(TP+FP) s Wilsonovým intervalem, pesimistická varianta, Cohenovo κ, procento shody.
- Cochranova velikost vzorku s korekcí na konečný soubor (p 0,5, e 0,10, z 1,96).
- Capture–recapture se započítávají jen průchody s alespoň 5 subjekty (`MIN_SEARCH_SIZE`).
- Ověření proti surovému textu: `urllib`, `urllib.robotparser`, `User-Agent`, prodleva 1 s, cache mimo repozitář, heuristiky regex pro částky a data.
- ARES REST API:
  - `/ekonomicke-subjekty/{ico}`,
  - `/ekonomicke-subjekty-vr/{ico}` (statutární orgány),
  - POST `/ekonomicke-subjekty/vyhledat`.
  - `robots.txt` zakazuje jen `/cms/`.
- or.justice.cz `robots.txt` zakazuje `/ias/`, takže se nepoužívá.
- Atomický zápis přes `*.tmp` a `os.replace` s opakováním.
- Konvence měsíční přesnosti: `value_as_of` = 1. den měsíce.

3. Files and Code Sections:

- **README.md** (UTF-8): mapa výstupů 1–8 na soubory, použití CLI, struktura repozitáře, zdůvodnění pytestu.
- **.gitignore**: `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.venv/`, `*.sqlite`, `*.db`, `*.tmp`.
- **.gitattributes**: `* text=auto eol=lf` a totéž pro csv, md, py.
- **pyproject.toml**: `requires-python >=3.11`, `dependencies = []`, `dev = ["pytest>=8"]`, pytest `testpaths=["tests"]`, `pythonpath=["."]`.
- **ai-log/README.md**: popis exportů (`RRRR-MM-DD-tema.md`).
- **docs/01-plan-a-kriteria.md**:
  - cíl a rozsah, jednotka záznamu, zdůvodnění ČR (s poznámkou, že or.justice.cz zakazuje `/ias/` a data se čerpají z ARES),
  - tabulka typů investorů,
  - Z1–Z4 (Z4 včetně nového fondu),
  - kódy vyloučení (`mimo_definici_pilotu` = CVC >50 %, fond fondů, státní, rozvojová instituce, dluhový fond, fond digitálních aktiv, otevřený smíšený fond; `bez_fondu` s výjimkou akcelerátoru s vehiklem),
  - 1.5 dvě úrovně a trychtýř, 1.6 statusy, 1.7 DoD, 1.8 plán, 1.9 fakta, předpoklady a otázky.
- **docs/02-metodika.md**:
  - zdroje (`rejstrik` = ARES), pravidla sběru faktů, pravidla scrapingu včetně kontroly `robots.txt` před každým požadavkem,
  - zákaz or.justice.cz,
  - postup a pravidlo výběru kandidátů z médií,
  - Z1 pravidla a/b/d (c zrušeno), CVC, `total_fund_size`, Z4, ověření proti surovému textu a jeho omezení, měsíční přesnost, konflikty,
  - 2.4 schéma všech tabulek (včetně `candidate_sources`, `effort_log`, doplňkových faktů `informace_o_fondu`, `pravni_spravce`, `cilova_velikost_fondu`, `registrace_regulator`, `dolozena_investice`, `duvod_vylouceni`) a slovník sektorů,
  - 2.5 validace, 2.6 metriky, 2.7 capture–recapture s omezením,
  - **2.8 Incidenty a poučení** (tabulka: robots.txt justice.cz, zamčené CSV a atomický zápis, nesoulad `c2fae0a`, šablona v `b7737ff` přes `git add -A`).
- **docs/04-rucni-kontrola.md**: R1/R2, verdikty TP/FP/nejiste, `fact_reviews` (spravne/chybne/nelze_overit), `review_minutes`, velikost vzorku, shoda, výsledky „budou doplněny“.
- **investor_db/schema.py**:
  - sloupce tabulek (`SEARCH_LOG` obsahuje `minutes`; `REVIEW` a `FACT_REVIEW` obsahují `review_minutes`; `EFFORT_COLUMNS`; `CANDIDATE_SOURCE_COLUMNS`),
  - `STATUSES`, `INVESTOR_TYPES`, `EXCLUSION_REASONS` (`EXCLUSION_DUPLICATE`, `EXCLUSION_FOREIGN`), stádia,
  - `INVESTMENT_SECTORS` (včetně `obrana_bezpecnost`, `cestovani`, `logistika`, `jine`), `PRIMARY_SOURCE_TYPES`, `CURRENCIES`, `REVIEWERS`, verdikty,
  - `EFFORT_TRIAGE`/`EFFORT_VERIFICATION`, `EFFORT_ACTORS`, `MONEY_FIELDS`, `EVIDENCED_FIELDS`,
  - `FACT_FUND_INFO` a doplňková pole, `FUND_ACTIVITY_FACT_FIELDS`, `FUND_SCOPED_FACT_FIELDS`,
  - `ID_PATTERNS` (`inv-\d{4}`, `f-\d{5}`, `src-\d{4}`, `s-\d{3}`),
  - `ACTIVITY_WINDOW_DAYS=1096`, `FRESHNESS_WINDOW_DAYS=365`.
- **investor_db/values.py**: `parse_date`, `parse_money`, `parse_minutes` (regex `\d+(\.\d{1,2})?`, >0), `split_list`, `is_valid_url`, `website_domain`, `is_valid_ico` (mod 11), `normalize_name`.
- **investor_db/io.py**: `Row`, `TABLE_COLUMNS` (8 tabulek), `SchemaError`, `Dataset`, `read_table`, `write_table`, `load_dataset`.
- **investor_db/validation.py**:
  - `Issue`, `DuplicateGroup`, `validate_dataset`,
  - kontroly identifikátorů, investorů (povinné jen `name` a status; `vyloucen` vyžaduje `investor_type`; `zahranicni_subjekt` vyžaduje zemi jinou než CZ; `overeny` vyžaduje vc, CZ, IČO, stádia, evidence a datum),
  - zdroje, fakty, podpora hodnot fakty (bez `name` u nevěřených), `evidence_urls`, data ověření,
  - `inclusion_criteria_issues` (Z1 primární registr, Z3 `fund_name`, Z4 `has_recent_activity`), `exclusion_evidence_issues`,
  - `has_recent_fact`, `has_recent_investment`, `has_recent_activity`,
  - `find_duplicate_groups` (IČO, doména, normalizovaný název), `check_search_log`, `minutes_issues` (`parse_minutes`), `check_effort_log`, review kontroly, `check_candidate_sources`.
- **investor_db/metrics.py**: `Proportion` (Wilson), `PrecisionResult`, `FactAccuracyResult`, `AgreementResult`, precision, `cohen_kappa`, `reviewer_agreement`, `fact_accuracy`, úplnost, podíly primárních zdrojů, aktivita, aktuálnost, duplicity, `values_only_in_facts_due_to_currency`, `EffortSummary` (Decimal), `effort_summaries`, `total_parsed_minutes`, `search_minutes`, `PopulationEstimate` (Lincoln–Petersen, Chapman, rozptyl, interval), `population_estimates` (`MIN_SEARCH_SIZE=5`), `funnel`, `ReviewEffort`, `review_efforts`.
- **investor_db/report.py**: `render_report`. Sekce: stav, trychtýř, precision, shoda, přesnost faktů, úplnost, doložení, pracnost (zvlášť model a člověk), capture–recapture, omezení. Formátování přes `format_decimal`.
- **investor_db/review.py**: `fact_sample_size`, `sample_fact_ids` (seed 2026), `add_pending_reviews`.
- **investor_db/**main**.py**: CLI `validate`, `metrics` (odmítne nevalidní data), `review-template --reviewer`, `fact-review-template --reviewer`, `raw-text URL --grep --cache-dir` (výchozí tempdir/investor-db-raw), `sys.stdout.reconfigure(utf-8)`.
- **investor_db/rawtext.py** (poslední úpravy jsou klíčové):

  ```python
  class RobotsDisallowedError(Exception):
      pass

  def read_request(request, opener) -> str: ...  # bez kontroly, použito jen pro robots.txt
  def robots_url(url) -> str
  def is_allowed_by_robots(url, opener) -> bool:  # RobotFileParser.parse(read_request(robots)); chyba => True
  def polite_request(request, opener) -> str:
      if not is_allowed_by_robots(request.full_url, opener):
          raise RobotsDisallowedError(request.full_url)
      try:
          return read_request(request, opener)
      finally:
          time.sleep(REQUEST_DELAY_SECONDS)
  def download(url, opener=default_opener) -> str
  def post_json(url, payload, opener=default_opener) -> object
  def fetch_raw_text(url, cache_dir, opener=default_opener) -> RawPage
      # cache; RobotsDisallowedError -> "zakázáno v robots.txt"; HTTP chyby
  ```

  Dále `html_to_text` (`TextExtractor` vynechává script, style, noscript a template), `money_patterns` (seskupené varianty a měřítka mld/mil(?!iard)/tis s `RANGE_TAIL`), `date_patterns` (ISO, „5. 11. 2025“, lomítka, anglické a české měsíce, „28. November 2024“, „27/11/24“; měsíční přesnost) a `find_first`.

- **tests/**:
  - `conftest.py`: `build_valid_dataset`, fiktivní data, IČO 12345679, fakt f-00011 `duvod_vylouceni` pro inv-0003, `effort_log`, `candidate_sources`, reviews s `review_minutes`.
  - `test_values.py`, `test_io.py`, `test_validation.py` (parametrizované negativní případy a nová pravidla), `test_metrics.py`, `test_review.py`, `test_cli.py`.
  - `test_rawtext.py`: `FakeResponse`, `fake_opener` zaznamenávající `requested`; testy pořadí robots.txt před každým požadavkem, odmítnutí zakázané cesty bez požadavku, `post_json` s robots a parsováním.
  - Celkem **222 testů prochází.**
- **data/**:
  - `investors.csv`: 52 subjektů, **15 overeny, 7 kandidat, 30 vyloucen**.
  - `facts.csv`: 205 faktů.
  - `sources.csv`, `search_log.csv` (17 průchodů, desetinné minuty), `candidate_sources.csv`, `effort_log.csv` (desetinné minuty).
  - `reviews.csv`: 15 prázdných řádků R1.
  - `fact_reviews.csv`: 66 prázdných řádků R1, vzorek z 205.
- **Scratchpad** (`C:\Users\ramazan\AppData\Local\Temp\claude\C--Users-ramazan-investor-db\d385e1f5-0229-46e8-8649-3f0ea24e7385\scratchpad`), mimo repozitář:
  - `record.py` (`record(investor_id, status, updates, facts, effort_note, activity, minutes_override)`, `save_atomically`, `source_id_for`, `TIMING_LOG`),
  - `sources.py`, `timing.log`, skripty `v_*.py` a `r_*.py`, `rawcheck.py`, `rawcheck.json`, `annotate_raw.py`, `replace_justice.py`, `fix_notes.py`,
  - `raw-cache/`, `ares-cache/`.
  - Spouštět s `PYTHONPATH=".;C:\...scratchpad"` (cesta ve formátu Windows).

4. Errors and fixes:

- **README v UTF-16:** nástroj Write zachoval kódování. Převedeno přes Python (`utf-16-le` na UTF-8) a amend před pushem.
- **Dlouhý heredoc v Bashi** selhal na „unexpected EOF“. Skripty se proto zapisují jako soubory ve scratchpadu.
- **`cat > /tmp/x`** čekal na vstup. Úloha zastavena přes TaskStop a soubor smazán.
- **Excel zamkl `investors.csv`.** Uživatel byl upozorněn a soubor po uzavření zkontrolován (UTF-8 beze změn). Časy odhadnuty a označeny.
- **Částečný zápis** (`facts.csv` zamčený) vedl k nekonzistenci. Zavedeno `save_atomically` s `*.tmp`, `os.replace` a opakováním.
- **Nesoulad popisu commitu `c2fae0a`:** úprava dokumentace se neprovedla, protože příkaz byl v řetězci za selhaným zápisem. Opraveno a uvedeno v `c94022f`.
- **Pravidlo (c)** by přiřadilo nesouvisející techstars s.r.o. Uživatel pravidlo zrušil a zavedl (d).
- **robots.txt na or.justice.cz zakazuje `/ias/`.** Odhaleno při kontrole surového textu. Všech 23 faktů nahrazeno ARES (`2fc5ece`). Zánik FRK doložen vyhledáváním v ARES (0 výsledků). Zaznamenáno v incidentech.
- **ARES vrací 404 pro vymazaný subjekt.** Použito vyhledávací POST API.
- **PYTHONPATH s `/c/` cestou** nefunguje. Použita cesta ve formátu Windows.
- **`\n` v heredocu** se změnil na skutečný konec řádku v testech. Opraveno náhradou.
- **`reviews.csv` z dřívějšího běhu `review-template`** se omylem dostal do `b7737ff` přes `git add -A`. Řádek pro Inven odstraněn (`e9c570d`). Od té doby přidávám soubory výslovně.
- **Odhadnuté domény:** presto.vc je zaparkovaná, tachles.vc neexistuje. Uživatel řekl: „Domény neodhaduj.“
- **Testy po změnách pravidel** (minuty, Z4) aktualizovány.
- **Tech.eu (Tilia)** vrací HTTP 429 i po prodlevě 1 a 4 minuty. Neobcházeno a označeno.

5. Problem Solving:

- Kompletní pipeline: hledání, triáž, ověření, metriky, šablony.
- Seznamy ČNB (JERRS) jsou za CAPTCHA, ARES funguje. Zdroje kandidátů: CVCA, Wikipedie, CzechCrunch, EIF a NRB.
- Kontrola proti surovému textu: 72 faktů, 69 potvrzeno (7 ručně, hodnoty zapsané slovy), 3 nepotvrzené:
  - Tilia Flox: HTTP 429,
  - Inven Ember: datum jen z URL, slabý doklad,
  - Zaka: dřívější chybný zdroj.
- Fakt Zaka f-00226 opraven. Hodnota je teď jen „osoba rizikového kapitálu zapsaná 25. 4. 2024“, ověřeno v JSON ARES.
- Statutární orgány Rockaway, Tensor, IP Lab, Tachles a neshoda u Nation1 pochází z ARES VR endpointu (povolený zdroj). Teď jsou potvrzené surovým JSON a jména týmů surovým textem zdrojů (fakty f-00182, f-00184, f-00197, f-00200 mají poznámku „ano“).
- **Ověření (15):** Credo, KAYA, Depo, Tensor, i&i, Tilia, Presto, Rockaway, J&T, Purple, Reflex, Soulmates, Startguide, StartupYard, IP Lab.
- **Kandidáti (7):** Nation1, Lighthouse, Tachles, Patero, Gain, Inven, Springtide.
- **Capture–recapture:** ověřených VC zhruba 13–19 (Chapman); zdroje jsou závislé, takže jde o dolní mez.

6. All user messages:

- „hi are u ready?“
- Velké zadání (Kontext, Cíl projektu, Přijatá rozhodnutí, Povinné výstupy, Minimální pole, Statusy, Úkol: POUZE PLÁN…, Omezení: Nesbírej data, nevymýšlej investory, odkazy ani hodnoty. Neinstaluj závislosti a nedělej destruktivní změny bez vysvětlení a mého souhlasu. Preferuj standardní knihovnu Pythonu; pytest navrhni s odůvodněním. Plán mi předlož ke schválení a počkej. Nic nepushuj bez mého souhlasu. Komunikuj se mnou výhradně v češtině… Do kódu nepiš komentáře…).
- „presunul jsem repo“
- Schválení plánu s 9 úpravami: jednotka = VC značka; Q1 final close a `fund_name`; Q2 vyloučení CVC, fondů fondů a státních fondů a zahraničních; Q3 měny a metrika; R2 volitelný s κ a procentem shody; `fact_reviews`; Q4 ASCII, Q5 Conventional Commits, Q6 `/export`; Q7 README UTF-8; mapa výstupů v README; „Po přesunu repozitáře začni commity 1–6. Zastav se na plánovaném schválení před sběrem dat.“
- Schválení sběru: 1. webové nástroje jen ruční čtení a „každý fakt musí pocházet ze stránky, kterou jsi v této session skutečně otevřel…“; 2. `exclusion_reason` doložit faktem; 3. měření času; 4. dávky a souhrn po seznamu kandidátů; 5. push commitů 1–6 a „žádné --amend“.
- Rozhodnutí: 1. dvě úrovně a trychtýř; 2. CVI `mimo_definici_pilotu`; 3. „Push: ano. Od teď pushuj po každém commitu, u kterého projdou testy i validate – už se neptej.“; 4. doplnit hledání (NRB/NRF, EIF RRF, kategorie CVCA); 5. capture–recapture; 6. `review_minutes`; „Zastav se, až budou všichni ověřeni, a ukaž mi souhrn.“
- Rozhodnutí před kontrolou: 1. CVC >50 %; 2. zrušit (c), doložit Rockaway a Tensor silněji; 3. `total_fund_size` v minulém čase; 4. ověření proti surovému textu (urllib, robots.txt), „Stažené stránky neukládej do repozitáře.“; 5. hraniční kandidáti (Orbit vyloučen, StartupYard ověřit, Zaka family office, Lighthouse kandidat, IP Lab nový fond, Nation1, Tachles, Patero a Gain kandidat bez primárního dokladu); 6. sektory; 7. desetinné minuty; 8. „Domény neodhaduj. Web investora hledej jen přes zdroje.“; „Po zapracování spusť testy a validate, pushni a pošli mi krátký souhrn změn statusů. Pak teprve přegeneruj šablony R1.“
- Poslední zpráva: „Před mou kontrolou ještě tři drobnosti, pak už na data nesahej, dokud ti nedám vědět: 1. Potvrď, odkud teď pochází údaje o statutárních orgánech… Pokud pocházely z or.justice.cz/ias/, nahraď je údaji z povoleného zdroje… Pokud to nejde, status kandidat. 2. Zaka VC: fakt s částkou odkazuje na nesprávný zdroj. Oprav přiřazení zdroje, nebo fakt odstraň. 3. Tilia: zkus Tech.eu znovu později s prodlevou. Inven: datum jen z URL označ v evidence_note jako slabý doklad. 4. Do dokumentace přidej sekci „Incidenty a poučení“ (porušení robots.txt u or.justice.cz/ias/ a náprava, zamčené CSV a atomický zápis, nesoulad popisu commitu c2fae0a). Do procesu sběru přidej kontrolu robots.txt před každým požadavkem (urllib.robotparser) a pokryj ji testem. Pak testy, validate, push a krátké potvrzení. Šablony reviews.csv a fact_reviews.csv přegeneruj jen pokud se změnily ověřené záznamy nebo vzorek faktů.“

7. Pending Tasks:

- Poslat uživateli krátké potvrzení v češtině, že všechny čtyři body jsou hotové.
- Pak čekat na ruční kontrolu R1. **Na data nesahat**, dokud uživatel nedá vědět.
- Později, až uživatel dá vědět: dopočítat precision a připravit `docs/03-globalni-odhad.md` (výstupy 3 a 7), výsledky v `docs/04`, README mapu a ai-log.

8. Current Work:

Všechny čtyři body poslední zprávy jsou dokončené a pushnuté. Commity:

- `b7a11f1` „fix: robots.txt před každým požadavkem, opravy faktů a incidenty“,
- `de4b18e` „data: opakované ověření zdroje u Tilie zapsáno“.

`main` je synchronní s `origin`. 222 testů prochází a validace je bez chyb.

Detaily ke každému bodu:

- **Bod 1:** statutární orgány pochází z ARES endpointu veřejného rejstříku (`ekonomicke-subjekty-vr`), ne z justice.cz. Teď jsou potvrzené surovým JSON (Rockaway: Havrlant, Fischer; Tensor: Drdúl, Smola; IP Lab Services: Fingl, Hladký, Navrátil; Tachles: Tušek, Marek; Nation1: Ton, Jiříček, kteří se neshodují s Moravcem). Jména týmů jsou potvrzená v surovém textu zdrojů. Statusy beze změny.
- **Bod 2:** Zaka f-00226 opraven odstraněním částky z jiného zdroje.
- **Bod 3:** Tilia: Tech.eu vrací 429 i po prodlevě, poznámka zapsána, neobcházeno; Tilia zůstává ověřená, ale Z4 stojí na tomto neověřeném faktu. Inven f-00100 označen jako „Slabý doklad“.
- **Bod 4:** sekce 2.8 Incidenty a poučení a pravidlo robots v metodice přidány. `rawtext.py` má `polite_request`, `download`, `post_json` a `RobotsDisallowedError` s testy.

Šablony se nepřegenerovávaly, protože se nezměnily ověřené záznamy ani počet faktů (vzorek je stejný).

9. Optional Next Step:

Poslat uživateli pouze krátké potvrzení v češtině, jak požadoval („Pak testy, validate, push a krátké potvrzení“). Shrnout v něm:

- statutární orgány jsou z ARES VR endpointu, potvrzené surovým JSON, statusy beze změny;
- Zaka fakt opraven;
- Tilia stále HTTP 429, neobcházeno, Z4 Tilie stojí na tomto faktu;
- Inven označen jako slabý doklad;
- incidenty zdokumentovány a kontrola robots.txt testovaná;
- šablony nebylo třeba přegenerovat;
- commity `b7a11f1` a `de4b18e` jsou pushnuté.

Poté na data nesahat: „pak už na data nesahej, dokud ti nedám vědět“.

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: C:\Users\ramazan\.claude\projects\C--Users-ramazan-OneDrive--------------projects-investor-db\d385e1f5-0229-46e8-8649-3f0ea24e7385.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.

The messages after this summary are the most recent messages from before compaction, kept verbatim. The summary was written without seeing them, so something it says has not happened yet may already have happened in them.

---

## 👤 User

<local-command-caveat>The command below was run directly in Claude Code, not sent to you as a request, and its output goes straight to the user. It's recorded here as context for later messages.</local-command-caveat>

---

## 👤 User

<command-name>/export</command-name>
<command-message>export</command-message>
<command-args></command-args>

---

## 👤 User

<local-command-stdout>Conversation exported to: C:\Users\ramazan\investor-db\ai-log\README.md</local-command-stdout>

---

## 👤 User

<local-command-caveat>The command below was run directly in Claude Code, not sent to you as a request, and its output goes straight to the user. It's recorded here as context for later messages.</local-command-caveat>

---

## 👤 User

<command-name>/export</command-name>
<command-message>export</command-message>
<command-args>ai-log/02-implementace.md</command-args>

---

## 👤 User

<local-command-stdout>Conversation exported to: C:\Users\ramazan\investor-db\ai-log\02-implementace.md</local-command-stdout>

---

## 👤 User

<local-command-caveat>The command below was run directly in Claude Code, not sent to you as a request, and its output goes straight to the user. It's recorded here as context for later messages.</local-command-caveat>

---

## 👤 User

<command-name>/export</command-name>
<command-message>export</command-message>
<command-args>ai-log/02-implementace.md</command-args>

---

## 👤 User

<local-command-stdout>Conversation exported to: C:\Users\ramazan\investor-db\ai-log\02-implementace.md</local-command-stdout>

---

## 👤 User

Zmenši vzorek fact_reviews.csv na přesnost ±15 p. b. (95 %), stejný seed 2026, a uprav to v metodice včetně důvodu (časová kapacita hodnotitele). Na reviews.csv nesahej.

---

## 🤖 Claude

Kód má přípustnou chybu ±15 p. b. Teď upravuju metodiku.

---

## 🤖 Claude

Nový vzorek je podmnožinou původního (36 ze 66 se shoduje), takže větu v dokumentaci opravuji.

---

## 🤖 Claude

Vzorek faktů ke kontrole je teď 36 místo 66, při přesnosti ±15 p. b. a 95% spolehlivosti se stejným seedem 2026. Změna je v commitu `74ea856` a je pushnutá. Testy (223) procházejí a validace commitnutého stavu je bez chyb.

- **Kód:** `investor_db/review.py` počítá s přípustnou chybou 0,15 místo 0,10. Testy velikosti vzorku jsem upravil na nové hodnoty a přidal případ pro 205 faktů z pilotu.
- **Metodika:** v `docs/04-rucni-kontrola.md` je nový výpočet, tabulka velikostí vzorku a důvod změny. Důvodem je časová kapacita hodnotitele R1, který kontroluje i všechny ověřené investory. Uvádím tam i důsledek: interval přesnosti faktů bude širší a výsledek je třeba brát jako orientační. Zmínil jsem také, že vzorek změnil ještě před prvním verdiktem faktu. V `docs/02-metodika.md` jsem doplnil řádek o přesnosti faktů s odkazem na toto zdůvodnění.
- **`fact_reviews.csv`:** šablonu jsem vygeneroval znovu. Všech 36 faktů bylo už v původním vzorku, takže nově nic nepřibylo.

`reviews.csv` ani `investors.csv` jsem nezměnil ani necommitnul, tvoje rozpracované změny zůstaly jen v pracovní kopii. Validace téhle pracovní kopie ale teď hlásí chybu u inv-0044 a inv-0049: IČO v `investors.csv` nemá podpůrný fakt z primárního zdroje. Vzniklo to tvou úpravou `investors.csv`. Než budeš úpravy commitovat, bude potřeba to vyřešit, já na to bez pokynu nesahám.

---

## 👤 User

<pasted_content id="2b08">
Chci, aby hodnotitel u každého faktu bez dalšího kontextu rozuměl, co přesně ověřuje. Připrav návod a kontrolní list pro ruční kontrolu.

1. Nový příkaz CLI (např. python -m investor_db review-guide), který z dat vygeneruje soubor review/kontrolni-list-faktu.md (nebo .html, pokud je čitelnější) pro aktuální vzorek fact_reviews.csv. U každého faktu:
   - fact_id, název investora (z investors.csv, ne jen ID) a jeho status;
   - „Tvrzení“ – jedna srozumitelná věta, co fakt říká. Generuj ji deterministicky ze šablony podle typu pole (field) a hodnoty, NE volným textem modelu. Příklad: duvod_vylouceni = pe_budouci_rozsireni → „Stratum Partners investuje hlavně formou buyoutů a většinových podílů (PE), proto není VC a je odložen pro budoucí rozšíření.“;
   - „Co hledat ve zdroji“ – šablona podle typu pole (např. u částek: stejné číslo, stejná měna, a že jde o velikost fondu, ne o cíl ani o velikost kola);
   - odkaz na zdroj (URL) a typ zdroje;
   - evidence_note NEuváděj – hodnotitel má hledat nezávisle.
2. Šablony pro všechny typy polí, které se ve facts.csv vyskytují (registry_id, název, pravni_spravce, total_fund_size, cilova_velikost_fondu, informace_o_fondu, typical_ticket_min/max, investment_sectors, investment_stages, dolozena_investice, duvod_vylouceni a další). Typ pole bez šablony = chyba (pokryj testem), aby žádný fakt nezůstal bez vysvětlení. Text šablon pro duvod_vylouceni rozliš podle hodnoty (pe_budouci_rozsireni, mimo_definici_pilotu, zahranicni_subjekt, family office…).
3. Do docs/04-rucni-kontrola.md přidej sekci „Návod pro hodnotitele“:
   - princip: hodnotitel neposuzuje metodiku, ale jen to, zda uvedený zdroj podporuje uvedenou hodnotu;
   - definice verdiktů (správně / chybně / nelze ověřit) s jedním příkladem každého;
   - tabulka typů polí: co otevřít a co porovnat;
   - typické chyby, kvůli kterým kontrola existuje (cíl fondu místo velikosti, velikost kola místo vkladu fondu, záměna měny, jiná firma s podobným názvem);
   - podobný stručný návod pro kontrolu investorů v reviews.csv (co znamená TP, FP, nejiste vzhledem ke kritériím Z1–Z4).
4. Šablony pokryj testy (každý typ pole má text, výstup je deterministický).
5. Neměň data ani vzorek. Commit, push a pošli mi ukázku 3 vygenerovaných řádků (jeden finanční údaj, jeden ARES, jeden duvod_vylouceni).
   </pasted_content id="2b08">

---

## 🤖 Claude

Píšu modul se šablonami tvrzení. Předtím si ještě rychle ověřuju, co se změnilo ve tvé pracovní kopii `investors.csv`.

---

## 🤖 Claude

Mezitím jsi `investors.csv` vrátil do stavu z commitu a validace pracovní kopie teď prochází. Pokračuju modulem.

---

## 🤖 Claude

Kontrolní list se generuje (36 faktů). Píšu testy šablon a pak sekci „Návod pro hodnotitele“.

---

## 🤖 Claude

Návod v dokumentaci je hotový. Zbývá doplnit README a pak testy, validace, commit a push.

---

## 🤖 Claude

Kontrolní list a návod pro hodnotitele jsou v commitu `e82b854` a jsou pushnuté. Testy (260) i validace procházejí. Data ani vzorek jsem neměnil a tvůj rozpracovaný `reviews.csv` jsem do commitu nezahrnul.

**Co přibylo:**

- **Příkaz `python -m investor_db review-guide`** vytvoří ze vzorku v `fact_reviews.csv` soubor `review/kontrolni-list-faktu.md` (36 faktů). Zvolil jsem Markdown, protože se na GitHubu dobře čte. `evidence_note` v něm není.
- **Šablony v `investor_db/review_guide.py`:**
  - pokrývají všechny typy polí ze schématu, všech 9 důvodů vyloučení s vlastním textem a české popisy kódů sektorů, fází a typů zdrojů;
  - k datu na 1. den měsíce přidají upozornění, že může jít o přesnost na měsíc;
  - k odkazům na ARES přidají nápovědu, jak číst JSON.
- **Chybějící šablona** pro typ pole, důvod vyloučení nebo kód sektoru je chyba a generování se zastaví. Hlídají to testy, stejně jako to, že výstup je pokaždé stejný.
- **Sekce 4.2 „Návod pro hodnotitele“ v `docs/04-rucni-kontrola.md`** obsahuje vše z tvého zadání. Příklady u verdiktů jsou obecné, nejsou to fakty z dat. Další sekce se tím posunuly na 4.3–4.6.

Mimochodem jsem opravil v dokumentaci zastaralou větu „`review_minutes` je kladné celé číslo“, minuty už mohou být desetinné.

**Ukázka tří vygenerovaných položek:**

> **5. `f-00028` – Credo Ventures (status: overeny)**
> **Tvrzení:** Typická investice investora Credo Ventures do jednoho startupu začíná na 1 000 000 USD.
> **Co hledat ve zdroji:** Najdi ve zdroji částku 1 000 000 USD: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o dolní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.
> **Zdroj:** https://www.credoventures.com/ – web investora (primární), vydavatel: Credo Ventures

> **35. `f-00211` – i&i Biotech Investments (status: overeny)**
> **Tvrzení:** i&i Biotech Investments má českou právnickou osobu s IČO 10885978.
> **Co hledat ve zdroji:** Najdi ve zdroji subjekt s IČO 10885978. Zkontroluj, že IČO sedí číslice po číslici a že název nebo sídlo subjektu odpovídá investorovi i&i Biotech Investments, ne jiné firmě. Odkaz vede na rozhraní ARES a prohlížeč zobrazí data ve formátu JSON: IČO je v poli „ico“, název v „obchodniJmeno“, sídlo v „sidlo“…
> **Zdroj:** https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/10885978 – veřejný rejstřík (primární), vydavatel: Ministerstvo financí ČR – ARES

> **1. `f-00001` – Stratum Partners (status: vyloucen)**
> **Tvrzení:** Stratum Partners investuje hlavně formou buyoutů a většinových podílů (PE), proto není VC a je odložen pro budoucí rozšíření.
> **Co hledat ve zdroji:** Zdroj popisuje subjekt jako private equity (buyout, většinové podíly, zralé firmy), nebo ho do private equity zařazuje.
> **Zdroj:** https://cvca.cz/en/category/full-members/ – asociace (sekundární), vydavatel: CVCA

**Na co narazíš při kontrole:**

- **Důvod `mimo_definici_pilotu`:** fakt obsahuje jen kód, takže tvrzení vyjmenovává všechny možné znaky a hodnotitel zapíše do `note`, který z nich zdroj dokládá. Konkrétní znak je zatím jen v `evidence_note`, kterou list záměrně neukazuje.
- **Ve tvém rozpracovaném `reviews.csv`** se v několika poznámkách jako opora uvádí Crunchbase, LinkedIn nebo TechCrunch. Podle nového návodu rozhodují zdroje uvedené v záznamu a jiný zdroj se jen zapíše do `note`. Je to tvoje rozhodnutí, upozorňuju jen na nesoulad s návodem.

---

## 👤 User

Důvod mimo_definici_pilotu je příliš obecný – konkrétní znak je jen v evidence_note, takže fakt nejde nezávisle ověřit. Rozděl ho na konkrétní kódy podle skutečného důvodu, např. cvc, dluhovy_fond (vč. venture debt), fond_fondu, statni_fond, digitalni_aktiva (případně další podle dat). U každého dotčeného faktu a investora přiřaď kód podle již doloženého evidence_note – nic nově nedohledávej. Doplň šablony v review_guide.py, slovník, validátor, testy a metodiku. Vzorek fact_reviews.csv neměň (stejná fact_id). Pak přegeneruj kontrolní list, commit a push.

---

## 🤖 Claude

Slovník a validátor jsou upravené. Teď píšu šablony pro nové kódy.

---

## 🤖 Claude

Data a dokumentace jsou upravené. Do tabulky incidentů přidávám poslední řádek a pak testy, list, commit a push.

---

## 🤖 Claude

Kód `mimo_definici_pilotu` jsem rozdělil na konkrétní kódy podle už zapsaného `evidence_note`, nic jsem nově nedohledával. Je to v commitu `fb2f330` a je to pushnuté. Testy (274) i validace procházejí.

**Přiřazení kódů:**

| Fakt    | Investor              | Nový kód                | Opora v evidence_note                              |
| ------- | --------------------- | ----------------------- | -------------------------------------------------- |
| f-00003 | CVI                   | `dluhovy_fond`          | přímé úvěry, seniorní dluh, mezanin                |
| f-00187 | Orbit Capital         | `dluhovy_fond`          | Growth Debt Fund II, venture debt                  |
| f-00020 | Seed Fund             | `statni_fond`           | program ministerstva financovaný z fondů EU        |
| f-00021 | EIF                   | `fond_fondu`            | fondy fondů, neinvestuje přímo do firem            |
| f-00150 | IVBF                  | `digitalni_aktiva`      | blockchainy, zastakovaný ether                     |
| f-00164 | 10X                   | `otevreny_smiseny_fond` | otevřený fond s měsíční likviditou, kotované akcie |
| f-00151 | Springtide (kandidát) | `cvc`                   | vazba na skupinu KKCG, podíl nad 50 % nedoložen    |

Šest vyloučených investorů má stejný kód v `exclusion_reason`. Fact_id se nezměnila a `fact_reviews.csv` zůstal stejný.

- **Slovník a validátor:** nové kódy jsou v `schema.py`. Starý kód validátor odmítne se zprávou, které konkrétní kódy použít místo něj.
- **Šablony a testy:** každý nový kód má vlastní tvrzení a vlastní pokyn, co hledat ve zdroji. U `dluhovy_fond` šablona výslovně zmiňuje venture debt. Testy pokrývají nové kódy i odmítnutí starého.
- **Metodika:** tabulky v `01` mají místo souhrnného kódu konkrétní, pravidlo pro CVC v `02` odkazuje na `cvc` a do „Incidentů a poučení“ přibyl řádek o příliš obecném kódu.
- **Kontrolní list:** přegenerovaný, změnily se 4 položky ve vzorku (f-00003, f-00021, f-00164, f-00187).

**Na co narazíš při kontrole:**

- **Springtide (f-00151):** kód `cvc` dostal fakt u kandidáta, u kterého bylo vyloučení zrušeno, protože podíl KKCG nad 50 % není doložen. Šablona `cvc` proto netvrdí, že podíl přes 50 % platí. Říká jen, že fond je napojený na korporátní skupinu, a podíl nad 50 % hodnotitel poznamená do `note`, jen pokud ho zdroj dokládá.
- **Orbit (f-00187, ve vzorku):** profil CVCA uvádí growth equity i venture debt. Tvrzení „hlavně dluhové financování“ proto hodnotitel nemusí ve zdroji potvrdit jednoznačně. Výsledný verdikt `chybne` by byl oprávněný signál, protože vyloučení stálo na tvém rozhodnutí.

Historická poznámka v `effort_log.csv` (inv-0040) starý kód stále zmiňuje. Je to záznam o tehdejší práci, proto jsem ji nepřepisoval.

---

## 👤 User

<pasted_content id="2b08">
Pravidla: agregátory (CB Insights, PitchBook, Caplight, Altss, Seedtable, Superscout) jen jako vodítko, fakta z primárních zdrojů nebo spolehlivých médií. Nejednoznačné názvy identifikuj podle domény a týmu. Konflikty zdrojů zapiš do evidence_note. Nepovinná pole (investment_stages apod.) nejsou kritérium zařazení – pokud je validátor nebo metodika vyžadují pro overeny, oprav to a pokryj testem.

1. Lighthouse Ventures (chyba hledání): „poslední investice 2019“ je chybně, fond vznikl 2019. Investice 2025–2026 (Ranketta 11/2025 jako lead – Tech.eu, DecisionRules 2025, Merchantee a BeatpulseLabs 6/2026). Identifikace lhv.vc, Michal Zálešák. Z3: Forbes (forbes.cz/stat-pomuze-startupum-penize-budou-rozdelovat-dva-nove-fondy/) 23 mil. EUR, fond s EIF / Czech ESIF FoF. Ověř Z1–Z4.
2. Tachles VC (chybné pravidlo): fáze doložena v The Recursive (therecursive.com/?p=39551, převážně pre-seed a seed). Z3/Z4: CzechCrunch – uzavřená první fáze kolem půl miliardy Kč, sedm investic za rok. Konflikt Superscout (2015, Tel Aviv) vs. česká média (nový fond od 2023) zapiš.
3. Springtide Ventures: vyloucen s kódem cvc. Forbes (forbes.cz/pocitame-s-uspechem-kazde-nasi-firmy-rika-manazer-komarkova-vc-fondu/): fond nemá cizí peníze; CzechCrunch: plně spadá do KKCG. Uveď stáří článku Forbes.
4. Patero: ověř na patero.cz a v ARES typ subjektu (fond s kapitálem třetích osob / vlastní kapitál → vyloucen / syndikát → kandidat jako hraniční případ). Pozor na záměnu s jiným subjektem Patero v CB Insights.
5. Gain Ventures: identifikuj subjekt z původního článku CzechCrunch. Pokud jde o gainventures.com (Web3 bez české vazby), vyloucen. Jinak kandidat s poznámkou o nejednoznačném názvu.
6. Orbit Capital: vyloučení jako dluhovy_fond dolož primárně článkem Tech.eu o Growth Debt Fund II (src-0031), profil CVCA uvádí growth equity i venture debt.
7. Nové overeny přidej do reviews.csv jako prázdné řádky k mé kontrole. Vzorek fact_reviews.csv neměň.

Testy, validate, commit, push. Pak se ZASTAV a napiš mi: změny statusů, nové řádky k mé kontrole, nová čísla trychtýře.
</pasted_content id="2b08">

---

## 🤖 Claude

Lighthouse má Z1 (ARES: Lighthouse Ventures GP s.r.o. se sídlem na adrese z lhv.vc, jednatel Zálešák) i Z3 (Forbes 2019, EIF) doložené. Teď hledám investice pro Z4.

---

## 🤖 Claude

Odkaz na The Recursive (`?p=39551`) se otevírá jen jako titulní stránka bez článku. Hledám skutečnou adresu článku o Tachles.

---

## 🤖 Claude

Springtide: Forbes z 26. 7. 2018 píše „žádné cizí peníze“ a fond řadí do investičního ramene KKCG. To dokládá CVC nad 50 %, Springtide proto vyloučím. Teď ověřuji Patero.

---

## 🤖 Claude

Všechno potřebné mám otevřené. Zapisuji změny do dat jedním atomickým skriptem.

---

## 🤖 Claude

Data jsou teď zapsaná správně. Zbývají dvě věci u Tachles: oprava pravidla pro stádia ve validátoru a fakt pro `name`. Ten doložím článkem CzechCrunch, který znovu otevřu.

---

## 🤖 Claude

Testy procházejí (281). Teď validace dat.

---

## 🤖 Claude

Všech sedm bodů je hotových v commitu `a63c885` a je pushnutý. Testy (281) i validace procházejí. Vzorek `fact_reviews.csv` jsem neměnil a tvoje rozpracované `reviews.csv` a `fact_reviews.csv` zůstaly jen v pracovní kopii.

## Změny statusů

| Investor            | Před     | Po                              | Doklad                                                                                                                                                                                                                                                                                                         |
| ------------------- | -------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lighthouse Ventures | kandidat | **overeny**                     | Z1: ARES, Lighthouse Ventures GP s.r.o. (IČO 07500912), sídlo stejné jako na lhv.vc a jednatel Zálešák je managing partner. Z3: Czech ESIF Fund of Funds podle lhv.vc a 23 mil. EUR od EIF podle Forbesu z 8. 4. 2019. Z4: DecisionRules (Tech.eu, 8. 5. 2025, lead) a Ranketta (Tech.eu, 27. 11. 2025, lead). |
| Tachles             | kandidat | **overeny**                     | Z1–Z4 už byly doložené, blokoval ho jen chybný požadavek na `investment_stages`. Konflikt se Superscoutem je zapsaný u faktu o fondu.                                                                                                                                                                          |
| Springtide Ventures | kandidat | **vyloucen** (`cvc`)            | Forbes z 26. 7. 2018 (8 let starý) píše „žádné cizí peníze“ a řadí fond pod investiční rameno KKCG. CzechCrunch z roku 2024 to potvrzuje.                                                                                                                                                                      |
| Patero              | kandidat | **vyloucen** (`business_angel`) | ARES uvádí Patero s.r.o. (dříve Logio Holding) se sídlem shodným s patero.cz a pěti fyzickými osobami po 20 %. Web nezmiňuje žádný fond ani externí kapitál.                                                                                                                                                   |
| Gain Ventures       | kandidat | kandidat                        | Článek CzechCrunch subjekt blíž neurčuje a gainventures.com se nenačetl (vypršel časový limit, spojení odmítnuto). ARES zná GAIN Ventures s.r.o. (Praha 4), vazbu na článek ale nelze doložit. Poznámku o nejednoznačném názvu jsem zapsal.                                                                    |
| Orbit Capital       | vyloucen | vyloucen                        | Primárním dokladem `dluhovy_fond` je teď Tech.eu (src-0031). Konflikt s profilem CVCA (growth equity i venture debt) je zapsaný.                                                                                                                                                                               |

## Co se nepodařilo a co jsem změnil navíc

- **The Recursive (Tachles):** odkaz `?p=39551` vede jen na titulní stránku. Skutečný článek z 26. 2. 2025 je jen pro předplatitele, takže fázi pre-seed/seed jsem nezapsal.
- **Superscout:** profil Tachles jsem nedohledal. Konflikt je proto zapsaný jako tvoje upozornění, ne jako fakt z otevřené stránky.
- **Merchantee a BeatpulseLabs (Lighthouse):** našel jsem je jen v agregátorech (PitchBook, Caplight), proto nejsou zapsané.
- **Patero:** jde o hraniční případ. Že investují vlastní kapitál, odvozuji ze struktury společníků a z toho, že web žádný fond nezmiňuje. Pokud to vyhodnotíš jako syndikát, vrátím ho na kandidáta.
- **Pravidlo pro agregátory:** v datech byly dva fakty z Caplightu.
  - **Startguide:** Z4 stálo jen na nich. Fakt f-00173 jsem ponechal se stejným ID a změnil mu zdroj na CzechCrunch z 2. 4. 2024 (Carebot).
  - **Depo:** fakt f-00050 (Tapaya) jsem nahradil investicí do Flowpay ze stejného článku. Depo mělo Z4 doložené i jinak a f-00050 nebyl ve vzorku.
  - **Validátor** teď zdroj z domény agregátoru odmítne.
- **Nepovinná pole:** validátor u statusu `overeny` už nevyžaduje `investment_stages`. Pokrývají to testy a upravil jsem i Z2 v metodice. Do „Incidentů a poučení“ přibyly dva řádky: stádia jako podmínka a chyba hledání u Lighthouse.
- **Chyba při zápisu dat:** pomocná funkce přidělila nové zdroje pod ID, která už existovala. Validace to zachytila před commitem. Moje změny jsem vrátil na HEAD (`git checkout` jen u `investors`, `facts`, `sources` a `effort_log`, které jsi lokálně neměnil) a zapsal je znovu s opraveným přidělováním ID.
- **Čas:** minuty v `effort_log` jsou tentokrát odhad, ne měření. V poznámkách je to uvedené.

## Nové řádky k tvé kontrole

V `reviews.csv` jsou commitnuté dva prázdné řádky R1: **inv-0037 Lighthouse Ventures** a **inv-0039 Tachles**. Ve tvé pracovní kopii už pro oba máš řádky s verdiktem TP, ty jsem nechal beze změny.

**Musíš znovu otevřít f-00173 (Startguide – Carebot).** Ohodnotil jsi ho jako `spravne` 10. 10., tedy proti původnímu zdroji z Caplightu. Teď má nový zdroj (CzechCrunch) a nové datum. U f-00187 (Orbit) se změnila jen poznámka, tvrzení i zdroj zůstaly stejné. Kontrolní list jsem přegeneroval.

## Trychtýř

|              | Celkem | overeny          | kandidat       | vyloucen         |
| ------------ | ------ | ---------------- | -------------- | ---------------- |
| Nalezeno     | 52     | **17** (bylo 15) | **3** (bylo 7) | **32** (bylo 30) |
| Rychlá triáž | 22     | 0                | 0              | 22               |
| Plné ověření | 30     | 17               | 3              | 10               |

Zbývající kandidáti jsou Nation1, Inven a Gain Ventures. Zastavuji se a čekám na tvůj pokyn.

---

## 👤 User

Patero je s.r.o., která investuje vlastní kapitál společníků bez fondu, stejně jako Impulse Ventures. Použij bez_fondu (nebo kód, který má Impulse), uprav fakt a exclusion_reason a zmiň to jako hraniční případ v dokumentaci. f-00173 jsem znovu ohodnotil proti novému zdroji. Řádky pro Lighthouse (inv-0037) a Tachles (inv-0039) v reviews.csv jsou vyplněné. ted delame

<pasted_content id="2b08">

1. Spusť validate a metrics.
2. Precision počítej jen z řádků pro záznamy se statusem overeny. Řádky pro kandidat/vyloucen do precision nezahrnuj – zpracuj je zvlášť jako můj nesouhlas se statusem (možné false negatives) s mými poznámkami.
3. Upozorni, pokud můj verdikt odporuje pravidlům zařazení (např. CVC nebo family office jako TP), a navrhni řešení. Sám verdikty neměň.
4. Do docs/04-rucni-kontrola.md zapiš: precision s 95% Wilsonovým intervalem (zvlášť nejiste jako FP); přesnost faktů a seznam všech chybně a nelze_ověřit s mými poznámkami; úplnost polí, podíl primárních zdrojů, doložení aktivity, duplicity, metriku měn; capture–recapture jako dolní mez; čas modelu (triáž/ověření) a člověka (na záznam a na fakt); tabulku kandidátů (chybějící kritérium, typ problému: slabé hledání / chybné pravidlo / nejednoznačný název / data chybí); false negatives Lighthouse a Tachles; Orbit jako vyloučení z definice (venture debt), kandidát pro rozšíření.
5. Uveď, jaké zdroje jsem při kontrole investorů použil (podle poznámek často Crunchbase, LinkedIn, média místo evidence_urls): kontrola investorů tedy ověřuje existenci a aktivitu nezávisle, nikoli evidence_urls; kontrola faktů naopak ověřuje přímo uvedené zdroje.
6. Do „Incidenty a poučení“ doplň: reviews.csv a investors.csv jsem omylem uložil v Excelu (kódování Windows-1250, formát dat, ořezané nuly v IČO); validátor to zachytil před výpočtem metrik.
7. Pokud kontrola odhalila chybná data, navrhni opravy v samostatném seznamu, neopravuj potichu. Precision se počítá z dat v době kontroly.
   </pasted_content id="2b08">

---

## 🤖 Claude

Validace prochází a metriky jsou spočítané. Teď si projdu tvoje verdikty po řádcích.

---

## 🤖 Claude

Mám spočítané hodnoty: precision v době kontroly je 15/15, přesnost faktů 32/34 a časy hodnotitele. Teď dopočítám intervaly a píšu výsledky do `docs/04`.

---

## 🤖 Claude

Dlouhý heredoc v Bashi opět selhal. Text proto zapíšu do souboru ve scratchpadu a vložím ho do dokumentu skriptem.

---

## 🤖 Claude

Výsledky kontroly jsou v `docs/04-rucni-kontrola.md` (sekce 4.6) a vše je pushnuté. Testy (281) i validace procházejí. Tvoje verdikty jsem nijak neměnil.

**Patero:** změnil jsem kód na `bez_fondu` u faktu f-00245 i v `exclusion_reason`. Typ investora je teď `jiny` jako u Impulse. V `docs/01` přibyla tabulka hraničních případů: Impulse a Patero, Orbit, Springtide, StartupYard, Zaka a Inven.

**Precision a fakty:**

- **Precision** se počítá ze stavu dat v době tvé kontroly, kdy bylo ověřených 15 investorů: **15/15 = 100 %, 95% interval 79,6–100 %**. Bez verdiktů `nejiste` je pesimistická varianta stejná. `metrics` z dnešních dat ukazuje 17/17, v dokumentu je to jen pro informaci.
- **Přesnost faktů:** **32/34 = 94,1 %, interval 80,9–98,4 %**. Když se `nelze_overit` počítá jako chyba, vychází 32/36 = 88,9 %.
  - Chybně: f-00071 (sektory i&i) a f-00145 (ticket Reflex).
  - Nelze ověřit: f-00003 (CVI) a f-00081 (Tilia).

**Tvoje TP u neověřených záznamů** (do precision nejsou započtené):

- Lighthouse a Tachles jsou potvrzené false negatives. U Lighthouse šlo o slabé hledání, u Tachles o chybné pravidlo.
- Inven a Nation1 jsou možné false negatives.
- Gain je nejasný.

**Verdikty v rozporu s pravidly** (v dokumentu je u každého návrh řešení):

- **Springtide:** TP, ale podle tvé poznámky jde o „VC křídlo KKCG“ a podle Forbesu nemá cizí peníze, tedy CVC.
- **Patero:** TP s poznámkou „family office“, přitom family office i investice bez fondu pravidla vylučují.
- **Gain:** TP opřený o databáze transakcí, tedy agregátory. Z1 ani Z3 nejsou doložená.
- **J&T:** TP odpovídá statusu, ale tvoje poznámka „patří pod J&T“ naznačuje vazbu na korporátní skupinu a podíl skupiny na kapitálu v datech doložený není.

**Navržené opravy dat** (nic jsem neopravil, čekají na tvé schválení):

1. **i&i (f-00071):** web uvádí fond „výhradně“ jako life science a AI je jedna z jeho vertikál. Navrhuji `ai` odebrat, nebo v metodice upřesnit, co se počítá jako sektor.
2. **Reflex (f-00145, f-00144):** 2 mil. EUR je výjimečné maximum, ne typická horní mez, a 1 mil. EUR je typická hodnota, ne dolní mez. Navrhuji upravit ticket v `investors.csv`.
3. **Tilia (f-00081):** dnes jsem tilia.vc otevřel znovu a titulní stránka uvádí „0.3 - 1.2m EUR initial ticket“. Stálo by za to, abys stránku otevřel ještě jednou.
4. **CVI (f-00003):** text, který v poznámce cituješ, dluhovou strategii spíš potvrzuje. Zvaž verdikt `spravne`.
5. **J&T:** dohledat strukturu kapitálu fondu. Pokud se doloží vazba na skupinu bez podílu, status by byl `kandidat`; při podílu nad 50 % `cvc`.

**Další doplněné body:**

- **Zdroje při kontrole investorů:** ve 4.6 je rozepsáno, že jsi použil hlavně Crunchbase, web investora, LinkedIn a média, u 4 záznamů zdroj chybí. Je tam i rozlišení, že kontrola investorů ověřuje existenci a aktivitu nezávisle na `evidence_urls`, kdežto kontrola faktů ověřuje přímo uvedené zdroje.
- **Kandidáti:** zbývají Inven (data chybí, podíl ČEZ), Nation1 (Z1, nejednoznačný název nebo chybějící data) a Gain (Z1 a Z3, nejednoznačný název). Orbit je v dokumentu jako vyloučení z definice pilotu (venture debt) a kandidát pro rozšíření.
- **Pracnost:** model potřeboval 2,4 min na ověření jednoho investora a méně než 0,1 min na triáž. Ty jsi strávil 15,5 min na záznam a 0,94 min na fakt.
- **Capture–recapture:** Chapmanovy odhady vycházejí 7–25, ověřených je 17, takže jde o dolní mez.
- **Incident s Excelem:** zapsaný v „Incidentech a poučení“.

U f-00173 je v řádku pořád datum 10. 10. bez poznámky, i když píšeš, že jsi ho ohodnotil znovu. V dokumentu to tak uvádím. Pokud se datum změnit má, oprav ho.

Commity jsou dva: `fefffe1` obsahuje dokumentaci a změnu u Patero, `18877a1` tvoje vyplněné `reviews.csv` a `fact_reviews.csv`. Ty jsem commitnul i bez výslovného pokynu, protože z nich výsledky v dokumentu vycházejí. Pokud jsi je chtěl commitnout sám, `18877a1` můžu vrátit samostatným revert commitem, historii nepřepisuji.

---

## 👤 User

This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:

1. Primary Request and Intent:

   **Project.** Testový projekt „Investor Intelligence Database“. Repozitář je `git@github.com:osho4753/investor-db.git`, lokálně `C:\Users\ramazan\investor-db`. Cílem je reprodukovatelný proces vyhledávání, klasifikace a ověřování reálných investorů z bezplatných veřejných zdrojů. Pilot tvoří VC značky s českou právnickou osobou.

   **Povinné výstupy 1–8:**
   1. plán a kritéria,
   2. metodika,
   3. globální odhad,
   4. pilot ČR,
   5. zdroje a data ověření,
   6. ruční kontrola a precision,
   7. odhad nákladů škálování,
   8. kód, testy, dokumentace, Git historie a ai-log.

   **Trvalá omezení (doslovně v platnosti):**
   - „Komunikuj se mnou výhradně v češtině.“
   - „Do kódu nepiš komentáře – kód má být čitelný sám o sobě (jasné názvy, type hints, malé funkce).“
   - „Nesbírej data, nevymýšlej investory, odkazy ani hodnoty.“
   - „Neinstaluj závislosti a nedělej destruktivní změny bez vysvětlení a mého souhlasu. Preferuj standardní knihovnu Pythonu“ (pytest je dev závislost).
   - Pouze bezplatné veřejné zdroje, žádné placené databáze. Scraping jen s respektem k `robots.txt`, s omezením rychlosti a cachováním.
   - „Každý fakt musí pocházet ze stránky, kterou jsi v této session skutečně otevřel. Nic nedoplňuj z vlastních znalostí ani odhadem. Pokud se stránka nenačte nebo údaj neobsahuje, hodnota zůstává neznámá… accessed_at je skutečné datum přístupu. evidence_note stručně parafrázuje… necituj delší pasáže.“
   - Ruční kontrolu dělá uživatel (R1) a volitelně R2, ne model. Verdikty hodnotitele sám neměň.
   - „Od teď pushuj po každém commitu, u kterého projdou testy i validate – už se neptej.“
   - „Od této chvíle už žádné --amend ani přepisování historie u pushnutých commitů.“
   - „Domény neodhaduj. Web investora hledej jen přes zdroje.“
   - „Stažené stránky neukládej do repozitáře.“
   - Agregátory (CB Insights, PitchBook, Caplight, Altss, Seedtable, Superscout) slouží jen jako vodítko. Fakta pochází z primárních zdrojů nebo spolehlivých médií.
   - Nejednoznačné názvy identifikuj podle domény a týmu. Konflikty zdrojů zapiš do evidence_note.
   - Vzorek fact_reviews.csv neměnit.
   - Chybná data odhalená kontrolou neopravuj potichu, jen navrhni opravy. Precision se počítá z dat v době kontroly.

   **Requests in this segment, in order:**
   1. Zmenšit vzorek faktů na ±15 p. b. se seedem 2026, na reviews.csv nesahat. Hotovo.
   2. Příkaz review-guide a kontrolní list, šablony, návod pro hodnotitele, testy, ukázka tří řádků. Hotovo.
   3. Rozdělit `mimo_definici_pilotu` na konkrétní kódy. Hotovo.
   4. Velký úkol: Lighthouse, Tachles, Springtide, Patero, Gain, Orbit, agregátory, nepovinná pole, nové řádky v reviews. Hotovo, poté se zastavit a reportovat.
   5. Nejnovější úkol:
      - Patero → bez_fondu jako Impulse a zmínit jako hraniční případ.
      - Body 1–7: validate a metrics; precision jen pro overeny; řádky kandidat/vyloucen zvlášť jako nesouhlas; upozornit na rozpory verdiktů s pravidly; výsledky v docs/04 (precision s Wilsonem a nejiste jako FP, přesnost faktů se seznamem chybne/nelze_overit, úplnost, primární zdroje, aktivita, duplicity, měny, capture–recapture jako dolní mez, čas modelu a člověka, tabulka kandidátů s typem problému, FN Lighthouse a Tachles, Orbit jako vyloučení z definice); zdroje použité hodnotitelem; incident s Excelem; samostatný seznam návrhů oprav.

2. Key Technical Concepts:
   - Python 3.11, jen standardní knihovna, pytest. CSV v Gitu jako zdroj pravdy (UTF-8, LF).
   - Kritéria Z1–Z4:
     - Z1: česká právnická osoba s IČO, pravidla a/b/d;
     - Z2: strategie VC; stádia už nejsou povinná;
     - Z3: fond s kapitálem třetích osob, fakt s `fund_name`;
     - Z4: investice nebo nový fond za 36 měsíců.
   - Pravidlo CVC: více než 50 % kapitálu od jedné skupiny.
   - Wilsonův interval, Cochranův vzorek (e = 0,15), capture–recapture (Chapman).
   - `rawtext` (`download`, `post_json`, `fetch_raw_text`) kontroluje robots.txt před každým požadavkem.
   - ARES REST: `/ekonomicke-subjekty/{ico}`, `/ekonomicke-subjekty-vr/{ico}`, POST `/vyhledat`.
   - Atomický zápis přes `save_atomically` ve scratchpad `record.py`.
   - Staging jen vlastních řádků přes `git hash-object -w` a `git update-index --cacheinfo`.

3. Files and Code Sections:
   - **investor_db/review.py:** `FACT_SAMPLE_MARGIN = 0.15`, seed 2026.
   - **investor_db/review_guide.py** (nový):
     - `GuideTemplateError`, `FieldGuide(claim, look_for)`, `FactGuide`;
     - `FIELD_GUIDES` pro všechna `FACT_FIELDS` kromě `duvod_vylouceni`;
     - `EXCLUSION_GUIDES` pro všechny `EXCLUSION_REASONS` (cvc, fond_fondu, statni_fond, dluhovy_fond, digitalni_aktiva, otevreny_smiseny_fond, zahranicni_subjekt, pe_budouci_rozsireni, business_angel, family_office, bez_fondu, neaktivni, zanikly_subjekt, duplicita);
     - `STAGE_LABELS`, `SECTOR_LABELS`, `SOURCE_TYPE_LABELS`, `ARES_JSON_HINT`, `ARES_SEARCH_HINT`, `MONTH_PRECISION_HINT`;
     - funkce `format_money`, `list_labels`, `field_guide`, `template_values` (placeholdery investor, value, fund, as_of_clause, announced_clause, money, labels), `build_fact_guide`, `sampled_fact_ids`, `build_fact_guides`, `missing_templates`, `render_checklist`.
   - **investor_db/**main**.py:**
     - příkaz `review-guide --output` (výchozí `review/kontrolni-list-faktu.md`);
     - `run_review_guide` zachytí `GuideTemplateError`, zapisuje UTF-8 s LF.
   - **investor_db/schema.py:**
     - `OUT_OF_SCOPE_EXCLUSION_REASONS` (cvc, fond_fondu, statni_fond, dluhovy_fond, digitalni_aktiva, otevreny_smiseny_fond) na začátku `EXCLUSION_REASONS`;
     - `RETIRED_EXCLUSION_REASONS = {"mimo_definici_pilotu": OUT_OF_SCOPE_EXCLUSION_REASONS}`;
     - `AGGREGATOR_NAMES` (altss, caplight, cbinsights, crunchbase, dealroom, pitchbook, seedtable, superscout).
   - **investor_db/values.py:** `is_aggregator_url(url)` porovnává popisky domény s `AGGREGATOR_NAMES`.
   - **investor_db/validation.py:**
     - `exclusion_reason_issues(table, row_id, column, reason)` odmítne vyřazený kód s nápovědou;
     - `check_sources` hlásí „zdroj je agregátor; slouží jen jako vodítko…“;
     - `verified_row_issues` vyžaduje jen `("registry_id", "evidence_urls", "last_verified_at")`, `investment_stages` odstraněno.
   - **tests:**
     - test_review.py: nové velikosti vzorku;
     - test_review_guide.py: nový, pokrývá všechny šablony, chybové stavy, determinismus a CLI, plus test venture debt;
     - test_validation.py: retired kód, nové kódy vyloučení jsou platné, agregátory, nepovinná pole u overeny, název agregátoru uvnitř jiné domény se nehlásí.
     - Celkem **281 testů prochází**.
   - **review/kontrolni-list-faktu.md:** generovaný kontrolní list, 36 faktů.
   - **docs/01-plan-a-kriteria.md:**
     - tabulka nových kódů vyloučení a odstavec o rozdělení;
     - Z2 už nevyžaduje stádia;
     - nová sekce „Hraniční případy (rozhodnutí zadavatele)“: Impulse a Patero bez_fondu, Orbit, Springtide, StartupYard, Zaka, Inven.
   - **docs/02-metodika.md:**
     - odstavce o agregátorech a nejednoznačných názvech;
     - `investment_stages` nepovinné, rozšířené pravidlo konfliktů, pravidlo CVC s kódem `cvc`;
     - 2.8 Incidenty: příliš obecný důvod vyloučení, nepovinné pole jako podmínka, chyba hledání u Lighthouse, uložení CSV v Excelu.
   - **docs/04-rucni-kontrola.md:**
     - 4.2 Návod pro hodnotitele, 4.4 vzorek ±15 p. b. se zdůvodněním;
     - 4.6 Výsledky: precision 15/15 (79,6–100 %) v době kontroly, 17/17 informativně; nesouhlasy a FN; rozpory verdiktů s pravidly (Springtide, Patero, Gain, J&T); přesnost faktů 32/34 a 32/36 se seznamem f-00071, f-00145, f-00003, f-00081; použité zdroje; úplnost; capture–recapture Chapman 7–25 jako dolní mez (≥17); pracnost; zbývající kandidáti; Orbit; návrhy oprav 1–6.
   - **data/:**
     - Lighthouse a Tachles overeny; Springtide vyloucen cvc; Patero vyloucen bez_fondu (f-00245, investor_type jiny); Gain kandidat s poznámkou;
     - f-00173 přepojen na cc.cz, f-00050 smazán a nahrazen Depo Flowpay;
     - nové zdroje (forbes, tech.eu, lhv.vc, patero.cz, ARES VR), effort_log s odhadnutými minutami;
     - reviews.csv a fact_reviews.csv s verdikty R1 commitnuty.
   - **README.md:** příkaz review-guide a složka review/.
   - **Scratchpad** (`C:\Users\ramazan\AppData\Local\Temp\claude\C--Users-ramazan-investor-db\d385e1f5-0229-46e8-8649-3f0ea24e7385\scratchpad`):
     - `peek.py` (cache `raw-cache-20261011`), `apply_20261011.py`, `tachles_name.py`, `patero_fix.py`, `results_section.md`, `clean-data/`, `record.py`;
     - spouštět s `PYTHONPATH=".;<scratchpad ve Windows formátu>"`.

4. Errors and fixes:
   - Věta v dokumentaci, že nový vzorek není podmnožinou původního, byla chybná: všech 36 faktů bylo v původních 66. Opraveno.
   - Chybějící newline v `__main__` (`newline="\n"` rozbité heredocem) jsem opravil přes Edit.
   - `record.source_id_for` přiděloval ID jako `len+1` a po dřívějším mazání zdrojů kolidoval s existujícími ID. Validace to odhalila, soubory investors, facts, sources a effort_log jsem vrátil přes `git checkout` (neměly lokální změny) a skript předělal na `max+1`.
   - Odkaz na The Recursive `?p=39551` vedl na titulní stránku a skutečný článek je jen pro předplatitele, stádia Tachles se proto nezapsala.
   - gainventures.com vrátil timeout a ECONNREFUSED.
   - Dlouhý heredoc v Bashi znovu selhal („unexpected EOF“). Text výsledků jsem zapsal přes Write do scratchpadu a vložil Pythonem.
   - Excel uložil uživatelovy CSV ve Windows-1250 s ořezanými nulami v IČO. Validace na tom selhala (inv-0044, inv-0049), uživatel soubory obnovil. Zdokumentováno jako incident.
   - Rozhodnutí uživatele: Patero použít `bez_fondu` jako Impulse, ne `business_angel`.

5. Problem Solving:
   - Precision se počítá podle statusů v době kontroly (commit `fb2f330`, 15 overeny). Nástroj `metrics` počítá z aktuálních 17.
   - Hodnotitel ověřoval investory nezávisle (Crunchbase, LinkedIn a další), kontrola faktů ověřovala uvedené zdroje.
   - Návrhy oprav dat jsou zapsané v dokumentaci, nic se neopravovalo potichu:
     - i&i AI sektor,
     - Reflex ticket max i min,
     - Tilia: dnes stránka hodnotu ukazuje,
     - CVI: poznámka R1 tvrzení podporuje,
     - J&T: možné CVC,
     - Springtide, Patero, Gain: rozpory verdiktů s pravidly.
   - Stav dat: 17 overeny, 3 kandidat (Inven, Nation1, Gain), 32 vyloucen. Trychtýř: triáž 22 (vše vyloucen), plné ověření 30 (17/3/10).

6. All user messages:
   - (/export příkazy do ai-log/README.md a ai-log/02-implementace.md, spuštěné uživatelem lokálně)
   - „Zmenši vzorek fact_reviews.csv na přesnost ±15 p. b. (95 %), stejný seed 2026, a uprav to v metodice včetně důvodu (časová kapacita hodnotitele). Na reviews.csv nesahej.“
   - Vložený text: „Chci, aby hodnotitel u každého faktu bez dalšího kontextu rozuměl, co přesně ověřuje. Připrav návod a kontrolní list pro ruční kontrolu.“ Body 1–5: CLI review-guide; tvrzení generované deterministicky ze šablon; „Co hledat ve zdroji“; URL a typ zdroje; bez evidence_note; šablony pro všechna pole a chybějící šablona = chyba; sekce „Návod pro hodnotitele“ v docs/04; testy; „Neměň data ani vzorek. Commit, push a pošli mi ukázku 3 vygenerovaných řádků (jeden finanční údaj, jeden ARES, jeden duvod_vylouceni).“
   - „Důvod mimo_definici_pilotu je příliš obecný – konkrétní znak je jen v evidence_note, takže fakt nejde nezávisle ověřit. Rozděl ho na konkrétní kódy podle skutečného důvodu, např. cvc, dluhovy_fond (vč. venture debt), fond_fondu, statni_fond, digitalni_aktiva (případně další podle dat). U každého dotčeného faktu a investora přiřaď kód podle již doloženého evidence_note – nic nově nedohledávej. Doplň šablony v review_guide.py, slovník, validátor, testy a metodiku. Vzorek fact_reviews.csv neměň (stejná fact_id). Pak přegeneruj kontrolní list, commit a push.“
   - Vložený text s pravidly („agregátory … jen jako vodítko, fakta z primárních zdrojů nebo spolehlivých médií. Nejednoznačné názvy identifikuj podle domény a týmu. Konflikty zdrojů zapiš do evidence_note. Nepovinná pole … nejsou kritérium zařazení – pokud je validátor nebo metodika vyžadují pro overeny, oprav to a pokryj testem.“) a body 1–7: Lighthouse, Tachles, Springtide, Patero, Gain, Orbit, nové overeny do reviews.csv jako prázdné řádky; „Vzorek fact_reviews.csv neměň. Testy, validate, commit, push. Pak se ZASTAV a napiš mi: změny statusů, nové řádky k mé kontrole, nová čísla trychtýře.“
   - Poslední zpráva: „Patero je s.r.o., která investuje vlastní kapitál společníků bez fondu, stejně jako Impulse Ventures. Použij bez_fondu (nebo kód, který má Impulse), uprav fakt a exclusion_reason a zmiň to jako hraniční případ v dokumentaci. f-00173 jsem znovu ohodnotil proti novému zdroji. Řádky pro Lighthouse (inv-0037) a Tachles (inv-0039) v reviews.csv jsou vyplněné. ted delame“ plus vložené body 1–7:
     1. Spusť validate a metrics.
     2. Precision jen z řádků overeny; kandidat/vyloucen zvlášť jako nesouhlas (možné FN) s poznámkami.
     3. Upozorni na verdikty odporující pravidlům a navrhni řešení; „Sám verdikty neměň.“
     4. Do docs/04 zapsat výsledky (vyjmenované metriky, tabulka kandidátů, FN Lighthouse a Tachles, Orbit).
     5. Uveď zdroje, které hodnotitel použil (kontrola investorů ověřuje nezávisle, kontrola faktů ověřuje uvedené zdroje).
     6. Incident: reviews.csv a investors.csv uložené v Excelu (Windows-1250, formát dat, ořezané nuly v IČO); validátor to zachytil.
     7. „Pokud kontrola odhalila chybná data, navrhni opravy v samostatném seznamu, neopravuj potichu. Precision se počítá z dat v době kontroly.“

7. Pending Tasks:
   - Poslat uživateli česky závěrečný report k poslední zprávě (vše je hotové a pushnuté).
   - Pak čekat. Navržené opravy dat nedělat bez souhlasu a verdikty neměnit.
   - Později podle pokynu uživatele: `docs/03-globalni-odhad.md` (výstupy 3 a 7), README mapa, ai-log.

8. Current Work:
   Poslední zpráva je zpracovaná a pushnutá:
   - `fefffe1` „docs: výsledky ruční kontroly R1, Patero jako bez_fondu a incident s Excelem“ (data/investors.csv, data/facts.csv, docs/01, 02, 04);
   - `18877a1` „data: verdikty ruční kontroly R1 (investoři a vzorek faktů)“ (uživatelovy reviews.csv a fact_reviews.csv). Commitnul jsem je bez výslovného pokynu, protože výsledky v dokumentaci na nich stojí, a uživateli to musím zmínit.

   Testy (281) a validate prochází. Neověřený zůstává jen `ai-log/claude-conversation-2026-10-09-d385e1f5.md`.

   Klíčová čísla pro report:
   - precision v době kontroly 15/15 = 100 % (Wilson 79,6–100 %), nejiste jako FP stejné; aktuální stav 17/17 (81,6–100 %);
   - přesnost faktů 32/34 = 94,1 % (80,9–98,4 %); s nelze_overit jako chybně 32/36 = 88,9 % (74,7–95,6 %);
   - chybne: f-00071 i&i sektory, f-00145 Reflex ticket max; nelze_overit: f-00003 CVI, f-00081 Tilia;
   - primární zdroje 127/223 = 57,0 %; aktivita 14/17; duplicity 0 skupin a 1 vyloučená; měny 0;
   - capture–recapture Chapman 7–25, dolní mez ≥17;
   - čas R1: 22 záznamů za 340 min (průměr 15,5 min) a 36 faktů za 34 min (0,94 min); model: ověření 71,1 min/30, triáž 0,7 min/22, hledání 5,6 min/17 průchodů.

   Rozpory verdiktů:
   - Springtide TP proti pravidlu CVC;
   - Patero TP s poznámkou „family office“;
   - Gain TP opřený o databáze (agregátory);
   - J&T poznámka „patřící pod J&T“ naznačuje možné CVC bez doloženého podílu.

   FN: Lighthouse (slabé hledání) a Tachles (chybné pravidlo). Možné FN: Inven (data chybí, CVC) a Nation1 (Z1). f-00173 má stále reviewed_at 2026-10-10, což dokumentace uvádí.

9. Optional Next Step:
   Poslat uživateli stručný český report podle bodů 1–7 poslední zprávy: výsledky validate a metrics, precision 15/15 v době kontroly, nesouhlasy a FN, rozpory verdiktů s pravidly a návrhy řešení, přesnost faktů a seznam chybných, zdroje použité hodnotitelem, doplněný incident s Excelem, seznam navržených oprav dat (neprovedených) a commity `fefffe1` a `18877a1`. Výslovně uvést, že jsem commitnul jeho verdikty R1 v reviews.csv a fact_reviews.csv. Pak čekat na pokyn a data ani verdikty bez souhlasu neměnit („Sám verdikty neměň.“, „navrhni opravy v samostatném seznamu, neopravuj potichu“).

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: C:\Users\ramazan\.claude\projects\C--Users-ramazan-OneDrive--------------projects-investor-db\d385e1f5-0229-46e8-8649-3f0ea24e7385.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.

The messages after this summary are the most recent messages from before compaction, kept verbatim. The summary was written without seeing them, so something it says has not happened yet may already have happened in them.

---

## 👤 User

<pasted_content id="2b08">

1. Opravil jsem své verdikty u neověřených záznamů: Springtide FP (CVC), Patero FP (bez fondu), Gain nejiste (jen agregátory). Opravy jsem udělal po zveřejnění souhrnu rozporů s pravidly – v dokumentu to uveď (původní a opravený verdikt, důvod). Do precision se tyto řádky stále nezapočítávají.
2. f-00173 jsem znovu ohodnotil proti novému zdroji (CzechCrunch) s datem 2026-10-11.
3. Opravy dat schvaluji jako „opravy po kontrole“: i&i – odeber ai ze sektorů; Reflex – uprav ticket podle zdroje. Precision a přesnost faktů zůstávají vypočtené ze stavu v době kontroly, opravy uveď zvlášť.
4. Tilia (f-00081) a CVI (f-00003): verdikty NEměním. Opakovanou kontrolu podnítil sběrač, takže by už nebyla nezávislá. Zapiš to v dokumentu jako „možná přísnost hodnotitele“ s tvým zjištěním, metriky ponech.
5. J&T Ventures: dohledej strukturu kapitálu z primárních zdrojů. Status měň jen při doloženém důkazu podle pravidla CVC; jinak zapiš jako otevřenou otázku.
   </pasted_content id="2b08">

---

## 🤖 Claude

Úpravy tvých verdiktů (body 1–2) zatím nejsou na disku: `reviews.csv` i `fact_reviews.csv` jsou beze změny. Pokračuji body 3–5 a pak se k tomu vrátím.

---

## 🤖 Claude

Znovu otevírám zdroje pro i&i a Reflex, abych opravy opřel o text stránek.

---

## 🤖 Claude

Teď hledám strukturu kapitálu J&T Ventures na webu značky a v ARES.

---

## 🤖 Claude

Procházím stránky „Přístup“ a „Tým“ na webu J&T Ventures. Hledám, kdo do fondů vkládá kapitál.

---

## 🤖 Claude

Na stránce /pristup je přímo FAQ o vztahu k J&T bance. Čtu celou odpověď.

---

## 🤖 Claude

Data jsou opravená a validace prošla. Teď zapisuji změny do `docs/04` (sekce 4.6).

---

## 🤖 Claude

Teď nahrazuji seznam návrhů sekcí „Opravy po kontrole“, „Možná přísnost hodnotitele“ a „Otevřené otázky“.

---

## 🤖 Claude

Body 3–5 jsou hotové a pushnuté v commitu `e328721`. Testy (281) i validace procházejí. U bodů 1 a 2 jsem se zastavil, protože tvoje úpravy nejsou na disku.

**Body 1 a 2 – zatím nic nezapsáno.** `data/reviews.csv` i `data/fact_reviews.csv` jsou stejné jako v commitu `18877a1`:

- Springtide, Patero i Gain mají pořád `TP`.
- f-00173 má pořád datum 2026-10-10.

Jinou kopii těch souborů jsem na disku nenašel, nejspíš zůstaly neuložené v editoru. Až je uložíš (v UTF-8, ne z Excelu), commitnu je a doplním do `docs/04` původní a opravený verdikt s důvodem. Sám je nezapisuji, protože jde o tvoje verdikty.

**Bod 3 – opravy po kontrole** (v `docs/04` mají vlastní tabulku, precision i přesnost faktů zůstávají ze stavu v době kontroly):

- **i&i:** `ai` jsem odebral z faktu f-00071 i z `investors.csv`.
- **Reflex: hodnoty jsem nezměnil, jen opravil `evidence_note`.** Při opětovném otevření článku jsem zjistil, že si zdroj sám odporuje:
  - zakladatel v přímé citaci říká „typické investici mezi jedním až dvěma miliony eur“;
  - redakce o odstavec níže píše „kolem jednoho milionu eur, někdy ke hranici dvou milionů“.

  Ticket 1–2 mil. EUR tedy odpovídá přímé citaci a můj původní návrh tu citaci přehlédl. Konflikt jsem zapsal do `evidence_note` f-00144 a f-00145 a v dokumentu je vysvětlený. Tvůj verdikt `chybne` zůstává. Jestli chceš ticket přesto upravit podle textu redakce, řekni a udělám to.

**Bod 4 – Tilia a CVI:** jsou v nové sekci „Možná přísnost hodnotitele“ i s mým zjištěním. Verdikty ani metriky jsem neměnil.

**Bod 5 – J&T Ventures: status jsem změnil z `overeny` na `kandidat`.**

- Web fondu na stránce /pristup výslovně píše, že nejde o korporátní fond J&T banky a že banka je ve fondu „pouze institucionálním investorem bez speciálních práv“. Jaký podíl má, neuvádí.
- ARES u obou SICAV (08220867 a 22175903) uvádí jen zakladatelské akcie, akcionáře neuvádí.
- Pravidlo CVC v `docs/02` pro tuto situaci (vazba doložená, podíl ne) předepisuje `kandidat`, stejně jako u Invenu. Zjištění je zapsané jako nový fakt f-00248.
- Podíl banky zůstává v dokumentu jako otevřená otázka.

Precision v době kontroly se tím nemění, J&T byl tehdy `overeny` a tvoje `TP` se započítalo. Aktuální stav je teď 16 ověřených a 4 kandidáti, informativní precision vychází 16/16 (interval 80,6–100 %). Úplnost, capture–recapture a pracnost modelu jsem v dokumentu přepočítal na 16 ověřených. Pokud chceš J&T nechat ověřený, stačí to vrátit dalším commitem, ale pak by se pravidlo CVC uplatňovalo jinak než u Invenu.

Kontrolní list faktů jsem nepřegeneroval, aby odpovídal stavu, podle kterého jsi kontroloval.

---

## 👤 User

reviews.csv a fact_reviews.csv jsou uložené (UTF-8, z VS Code). Commitni je a doplň do docs/04 původní a opravený verdikt s důvodem.

Rozhodnutí: J&T jako kandidat přijímám (stejné pravidlo jako Inven). Reflex: ticket ponech 1–2 mil. EUR podle přímé citace zakladatele, můj verdikt chybne zůstává a konflikt ve zdroji uveď jako příklad v omezeních dat.

---

## 🤖 Claude

Do `docs/04` teď zapisuji opravené verdikty, f-00173, pracnost, omezení dat a rozhodnutí k Reflex a J&T.

---

## 🤖 Claude

Commitnul jsem a pushnul `reviews.csv`, `fact_reviews.csv` i doplněný `docs/04`. Testy (281) i validace procházejí.

**Commity:**

- `47bf0df`: tvoje `reviews.csv` a `fact_reviews.csv` beze změn obsahu. Při commitu Git převedl konce řádků z CRLF na LF podle `.gitattributes` a na konec `reviews.csv` jsem přidal chybějící nový řádek.
- `d5232eb`: doplnění v `docs/04`.

**Co přibylo v `docs/04`, sekce 4.6:**

- **Opravené verdikty:** tabulka s původním verdiktem z 9. 10., opraveným z 11. 10. a tvým důvodem:
  - Springtide `TP` → `FP`,
  - Patero `TP` → `FP`,
  - Gain `TP` → `nejiste`.

  Je tam i poznámka, že opravy přišly až po zveřejnění souhrnu rozporů, takže nebyly nezávislé na sběrači, rozhodnutí ale bylo tvoje. Do precision se tyto řádky nezapočítávají, precision v době kontroly zůstává 15/15.

- **f-00173:** opakovaná kontrola 11. 10. 2026 proti CzechCrunch, verdikt zůstal `spravne`.
- **Omezení dat:** nová podsekce s Reflexem jako příkladem konfliktu uvnitř jednoho zdroje. Citace zakladatele uvádí 1–2 mil. EUR, text redakce „kolem 1 mil., někdy až 2“. Data se drží citace, tvůj verdikt `chybne` zůstává. Přidal jsem dvě související poznámky:
  - pole `typical_ticket_min/max` neumí zachytit „typicky X, výjimečně Y“;
  - podíl korporace na kapitálu fondu zdroje obvykle neuvádějí (Inven, J&T).
- **Rozhodnutí zadavatele:** u Reflexu (ticket ponechán) a u J&T (`kandidat` přijat) je to v tabulce „Opravy po kontrole“.
- **Otevřené otázky:** zůstal podíl J&T banky na kapitálu fondu a identifikace Gain Ventures.

**Pracnost:** v opravených řádcích je teď jen čas opravy (5 min), původní časy 10, 20 a 20 min se přepsaly. `metrics` proto ukazuje 305 min místo 340. V dokumentu uvádím obojí: první kontrolu 340 min podle commitu `18877a1` a opravu 15 min zvlášť.

Nezacommitovaný zůstává jen `ai-log/claude-conversation-2026-10-09-d385e1f5.md`, který jsem zatím nečetl.

---

## 👤 User

Dobre ted projdeme dalsi body

<pasted_content id="2b08">

1. docs/03-globalni-odhad.md (výstupy 3 a 7): počet investorů z regulátorů (ESMA, národní registry, SEC IAPD exempt reporting advisers, FCA), asociací (Invest Europe, národní VC asociace) a extrapolace z pilotu; každé číslo se zdrojem, nedoložitelné jako předpoklad, nic nevymýšlej; scénáře nízký/základní/vysoký. Spolehlivost dat po úrovních regionů s pilotní precision jako výchozím bodem. Náklady: změřený čas modelu a člověka × počet investorů × koeficient obtížnosti regionu, roční aktualizace, infrastruktura (PostgreSQL, scraping s cache a robots.txt); hodinová sazba a ceny API jako explicitní předpoklady s rozsahem. Omezení veřejných zdrojů z pilotu (JERRS za CAPTCHA, robots.txt or.justice.cz, HTTP 403/429, placené databáze, shrnování stránek nástrojem, nejednoznačné názvy).
2. README: návod pro hodnotitele (instalace, validate, metrics, review-guide, pytest), tabulka výstupů 1–8 → soubory, klíčové výsledky v jednom odstavci, hlavní omezení.
   </pasted_content id="2b08">

---

## 🤖 Claude

Hledám primární zdroje a čísla ověřuji v surovém textu stránek (rawtext s robots.txt a cache), ne jen ve shrnutí nástroje.

---

## 🤖 Claude

Mám čísla NVCA, Invest Europe a UK Private Capital ověřená v surovém textu. Teď zkouším data SEC a registr ESMA.

---

## 🤖 Claude

Registr ESMA má veřejné API: 970 aktivních fondů EuVECA a 415 správců s aktivním fondem, z ČR žádný. Teď zkouším FCA a pak sepíšu `docs/03`.

---

## 🤖 Claude

Zdroje mám pohromadě. Výpočty scénářů a nákladů dělám skriptem, aby v nich nebyly aritmetické chyby.

---

## 🤖 Claude

Teď přepisuji README.

---

## 🤖 Claude

Oba body jsou hotové v commitu `3282965` a pushnuté. Testy (281) i validace procházejí.

**1. `docs/03-globalni-odhad.md`**

Všechny zdroje jsem otevřel dnes. Čísla jsou ověřená v surovém textu stránky nebo v JSON z API, jedinou výjimkou je SEC.

| Zdroj                        | Údaj                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| NVCA 2026 Yearbook           | 2 984 VC firem v USA (2025)                                                           |
| NVCA, tisková zpráva 2025    | USA tvoří 57 % světové hodnoty VC transakcí                                           |
| Invest Europe (přes Tech.eu) | 3 095 aktivních firem PE a VC v Evropě                                                |
| UK Private Capital           | více než 260 členských firem PE a VC                                                  |
| ESMA, veřejné API registru   | 970 aktivních fondů EuVECA, 415 správců, z ČR žádný (pilot přitom má 16 ověřených VC) |
| SEC                          | 362 registrovaných poradců s VC fondem a 4 392 VC fondů                               |
| FCA                          | počet správců RVECA nezjištěn                                                         |

- **SEC:** sec.gov surovému stahování vrátil HTTP 403, čísla jsou tedy ověřená **jen přes shrnutí nástroje**. Počet exempt reporting advisers zůstává neznámý.
- **FCA:** registr je vykreslovaný JavaScriptem, takže počet správců RVECA nešel zjistit. K dispozici je jen číslo 145 z komentáře Ocorian, ne od regulátora, a VC nerozlišuje.

**Scénáře:** 5 235 / 7 251 / 9 682 VC firem.

- Podíl VC mezi firmami PE a VC v Evropě (0,4–0,6) je předpoklad opřený o pilot, kde vyšel 48–54 %.
- Zbytek světa nemá přímý zdroj, jeho násobek je označený jako předpoklad.

**Spolehlivost:** výchozím bodem je pilotní precision. Pro tři úrovně regionů jsou očekávaná přesnost faktů a koeficient obtížnosti uvedené jako předpoklady.

**Náklady:**

- Model: 5,4 min na ověřeného investora (naměřeno) × počet investorů × koeficient regionu. Vychází 897–1 292 h běhu v základním scénáři.
- Člověk: kontrola se dělá na vzorku, takže nezáleží na počtu investorů, ale na počtu regionů. Vychází 7 h na region a hodnotitele.
- Jako předpoklady s rozsahem jsou vedené: hodinová sazba 25–60 EUR, 100–400 tis. tokenů na investora, 3–15 USD za milion tokenů, PostgreSQL a roční aktualizace. Spotřebu tokenů pilot neměřil, to je potřeba doplnit.

**Omezení z pilotu:** JERRS za CAPTCHA, robots.txt u or.justice.cz, HTTP 403 a 429, placené databáze, shrnování stránek nástrojem, nejednoznačné názvy, paywall a konflikt uvnitř zdroje (Reflex).

**2. README**

- Klíčové výsledky jsou shrnuté v jednom odstavci.
- Tabulka výstupů 1–8 odkazuje na skutečné soubory.
- Je tam sekce s hlavními omezeními.
- Návod pro hodnotitele obsahuje instalaci, validate, review-guide a šablony, metrics a pytest, plus upozornění, ať CSV neupravují v Excelu.

Příkaz `pip install -e ".[dev]"` jsem nespouštěl, protože bez tvého souhlasu nic neinstaluju. Funkčnost instalace tedy ověřená není.

Nezacommitovaný zůstává jen soubor v `ai-log/`.

---
