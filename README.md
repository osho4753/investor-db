# Investor Intelligence Database

Prezentační web: https://investor-db-woad.vercel.app/

## Shrnutí na jednu obrazovku

Výsledkem je reprodukovatelný proces a pilotní databáze VC investorů v Česku z bezplatných veřejných zdrojů. Každý údaj má zdroj, datum přístupu a popis důkazu a ruční kontrola R1 změřila přesnost.

- **14 ověřených VC investorů** z 52 nalezených subjektů (6 kandidátů, 32 vyloučených s důvodem); stav po opravách po kontrole R1-v2.
- **Precision (kolo R1-v2): 11/16** přísně, nejisté = nepotvrzeno (95% interval 44,4–85,8 %); **11/11** jen rozhodnuté případy (74,1–100 %).
- **Přesnost faktů 32/34** (94,1 %) na náhodném vzorku, přísně 32/36.

Tabulka 14 ověřených investorů: [web](https://investor-db-woad.vercel.app/data.html#overeni), data v [`data/investors.csv`](data/investors.csv). Jak data zkontrolovat: [Návod pro hodnotitele](#návod-pro-hodnotitele).

Reprodukovatelný proces, který z bezplatných veřejných zdrojů najde, zařadí a ověří investory do firem. Každý údaj je fakt se zdrojem, datem přístupu a popisem důkazu. Hlavním cílem je spolehlivost dat, ne počet záznamů. Pilot pokrývá **venture kapitál (VC) v Česku**. Pro PE proběhl mini-pilot, pro family office, angel investory a velké soukromé investory studie proveditelnosti. Zadání je v [docs/00-zadani.md](docs/00-zadani.md).

## Klíčové výsledky

- **Trychtýř:** pilot našel 52 subjektů.
  - 14 ověřených VC investorů;
  - 6 kandidátů, kterým chybí doklad některého kritéria (i&i Biotech a Tilia přešly mezi kandidáty po kontrole R1-v2);
  - 32 vyloučených s konkrétním důvodem, z toho 17 PE.
- **Precision (kolo R1-v2, 13. 10. 2026):** 11 TP, 0 FP, 5 nejistých ze 16 tehdy ověřených. Přísně (nejisté = nepotvrzeno) 11/16 = 68,8 % (95% interval 44,4–85,8 %), jen rozhodnuté případy 11/11 (74,1–100 %). Nejisté případy jsou vady dokladů, ne vyvrácené záznamy ([docs/04](docs/04-rucni-kontrola.md) 4.11).
- **Původní kolo R1 (historie):** 15/15 v době kontroly. Poznámky se ale opíraly o Crunchbase, LinkedIn a agregátory v rozporu s metodikou, časy byly zaokrouhlené a Springtide, Patero a Gain byly nejdřív TP a podle pravidel pak FP nebo nejisté.
- **Recall:** ze dvou nezávislých seznamů českých VC (Vestbee 2021/2023, AIN.UA 2022), které hledání nepoužilo, máme **14 z 18** subjektů, které seznamy uvádějí jako VC v ČR (bez Pale Fire Capital, který investuje vlastní peníze partnerů): 8 ověřených, 3 kandidáti, 3 vyloučení s důvodem). Chybí Longevitytech.fund, Y Soft Ventures, Koopeo Ventures a Air Ventures ([docs/04](docs/04-rucni-kontrola.md) 4.10).
- **Capture–recapture (doplňkový, málo informativní odhad):** Chapmanovy odhady 9–29 ověřitelných VC v ČR jsou jen dolní mez, protože zdroje hledání nejsou nezávislé. Pro samotné ověřené vychází 13,7, tedy méně, než kolik jich už je (14). Lepší představu o úplnosti dává recall proti nezávislým seznamům.
- **Kontrola vyloučených:** náhodný vzorek 10 z 32 dal 9 správných vyloučení a 1 nejistý případ. False negative se ve vzorku nenašel.
- **Přesnost faktů po kolech:**

  | Kolo | Výsledek | Přísně (neověřitelné = chybné) |
  |---|---|---|
  | Náhodný vzorek | 32/34 = 94,1 % | 32/36 = 88,9 % |
  | Všechna doplněná fakta | 42/44 = 95,5 % | 42/49 = 85,7 % |
  | Fakta změněná opravami | 7/7 | 7/7 |

- **Pole zadání u 14 ověřených VC:**
  - sektor 13/14, fáze 14/14;
  - ticket 12/14 (obě meze 9/14);
  - kapitál 11/14: získaná částka fondu nebo AUM;
  - zdroj 14/14.

  Kapitál je ve [`funds.csv`](data/funds.csv) po fondech a s typem částky. Získaný kapitál je všude dolní mez. Cíl fondu se do kapitálu nepočítá a konflikty zdrojů jsou v reportu vidět.
- **PE mini-pilot (5 náhodných PE členů CVCA):**
  - pravost 5/5 a status správně 5/5 podle kontroly R1;
  - českou právnickou osobu mají 2/5;
  - sektor a ticket má 5/5, získaný kapitál jen 1/5.
- **Globální odhad VC:** 5 235 / 7 251 / 9 682 firem ve scénářích nízký / základní / vysoký.
- **Čas a cena:** model 7,9 min na ověřený VC záznam, API 0,365 USD na investora (měřeno, n = 3) a 0,78 USD na záznam v databázi. Člověk 15,5 min na kontrolu investora (u PE 9 min) a 0,8–1,0 min na fakt.

## Splnění zadání

| Požadavek zadání | Stav | Kde | Poznámka |
|---|---|---|---|
| Databáze investorů: VC, PE, family office, angelé, velcí soukromí investoři | **částečně** | [data/](data/), [docs/01](docs/01-plan-a-kriteria.md) 1.10–1.12 | Data: VC v ČR (pilot) a PE (mini-pilot n = 5). Ostatní kategorie mají plán, pravidla a studii proveditelnosti, ale ne data. |
| Každý záznam je skutečný investor, ne náhodná firma | splněno | [docs/04](docs/04-rucni-kontrola.md) 4.6, 4.8, 4.9 | precision R1-v2 11/16 přísně, 11/11 rozhodnuté; PE 5/5, vyloučení 9/9 + 1 nejisté |
| U investora: sektor, do čeho investuje a v jaké výši, celkový kapitál, zdroj | **částečně** | [docs/04](docs/04-rucni-kontrola.md) 4.7, report `metrics` | Vyplněno sektor 13/14, ticket 12/14, kapitál 11/14, zdroj 14/14. Co chybí, je zapsáno jako „hledáno, nenalezeno“. |
| Plán: kdo v databázi bude a kdo ne, pravidla zařazení a vyřazení | splněno | [docs/01](docs/01-plan-a-kriteria.md) | Z1–Z4 pro VC, P/F/A/S pro ostatní kategorie, kódy vyloučení |
| Jak se ověří pravost a správné zařazení | splněno | [docs/01](docs/01-plan-a-kriteria.md), [docs/02](docs/02-metodika.md), [docs/04](docs/04-rucni-kontrola.md) | validátor, primární zdroje, ruční kontrola R1 |
| Odhad dosažitelného okruhu, počtu a spolehlivosti s uvedením, z čeho vychází | splněno | [docs/03](docs/03-globalni-odhad.md) 3.1–3.4, 3.7–3.8 | Každé číslo má značku: změřeno, zdroj, nebo předpoklad. |
| Ověření na vzorku (VC v jedné zemi) | splněno | [data/](data/) | 52 subjektů v ČR |
| Zdroj a datum dokládající, že subjekt investuje | splněno | `facts.csv` (Z4), `investors.csv` (`evidence_urls`) | Doložená investice za 36 měsíců u 11/14, u ostatních nový fond nebo vehikl. |
| Přesnost změřená na ručně ověřeném vzorku | splněno | [docs/04](docs/04-rucni-kontrola.md) | Jen jeden hodnotitel (R1), shoda hodnotitelů se nepočítá. |
| Odhad nákladů na rozšíření na celý svět | splněno | [docs/03](docs/03-globalni-odhad.md) 3.5, 3.8 | Čas modelu a člověka je změřený. Tokeny a cena API jsou změřené na 3 investorech (0,365 USD na investora), přepočet na ostatní kategorie je předpoklad. |
| Jen veřejně dostupná data | splněno | [docs/02](docs/02-metodika.md) 2.2, 2.8 | Jedno porušení `robots.txt` bylo zjištěno a opraveno (níže). |
| Veřejný repozitář: plán, data se zdrojem u každého údaje, výsledek měření | splněno | tento repozitář | Validátor vynucuje fakt se zdrojem u každé vyplněné hodnoty. |
| Kód s průběžnou historií commitů | splněno | `investor_db/`, `tests/`, `git log` | 76+ commitů od 9. 10. 2026 |
| `ai-log` s exportem konverzací | **splněno** | [ai-log/](ai-log/) | Úplný export celé session bez `--detailed`, popis a mapování fází na commity. |
| README: práce s AI, rozhodnutí v nejasnostech, co chybí | splněno | níže | |

## Práce s AI

Data sbíral, kód psal a dokumentaci připravoval agent **Claude Code**. Pokyny pro Claude Code jsem připravoval s pomocí chatového asistenta. Rozhodoval jsem sám a výstupy jsem sám kontroloval. Ruční kontrolu dat dělal člověk (R1), ne model.

### Hlavní pokyny pro agenta

- Používat jen bezplatné veřejné zdroje. Respektovat `robots.txt`, omezovat rychlost požadavků a cachovat stažené stránky. Ochrany (CAPTCHA, 403) neobcházet.
- Každý fakt musí pocházet ze stránky, kterou agent v té session skutečně otevřel. Nic nedoplňovat z vlastních znalostí, nic neodhadovat. Co nejde doložit, zůstává „neznámé“ a hledání se zapíše do `search_log`.
- Nevymýšlet investory, odkazy, hodnoty ani domény. Web hledat přes zdroje.
- Agregátory (Crunchbase, Dealroom apod.) slouží jen jako vodítko, fakta stojí na primárních zdrojích nebo médiích.
- Konflikty zdrojů zapisovat viditelně, ne vybírat jednu verzi potichu. Chyby nalezené kontrolou jen navrhovat, ne opravovat potichu.
- Verdikty ruční kontroly mění jen hodnotitel. Pushnutou historii nepřepisovat.
- Kód bez komentářů, jen standardní knihovna Pythonu (pytest pro testy). Malé commity a push po úspěšných testech a validaci.

### Jak se kontroloval výstup

1. **Validátor** (`python -m investor_db validate`) kontroluje integritu:
   - každá vyplněná hodnota má podpůrný fakt a každý fakt zdroj a datum přístupu;
   - ověřený investor má doložena kritéria Z1–Z4;
   - vyloučený má důvod doložený faktem;
   - částky ve `funds.csv` odpovídají faktům;
   - zdroj z agregátoru se hlásí jako chyba.

   `metrics` nad nevalidními daty odmítne běžet.
2. **Kontrola proti surovému textu.** Nástroj pro čtení webu vrací shrnutí jazykovým modelem. Částky, data a citace se proto ověřovaly proti surovému textu stránky (`investor_db/rawtext.py`).
3. **Ruční kontroly R1 po kolech:**
   - investoři (precision);
   - náhodný vzorek faktů;
   - všechna doplněná fakta;
   - fakta změněná opravami;
   - mini-pilot PE;
   - náhodný vzorek vyloučených.

   Pro hodnotitele je vygenerovaný kontrolní list s tvrzením, tím, co ve zdroji hledat, a odkazem na zdroj. Přesnost se počítá pro každé kolo zvlášť a opravy po kontrole metriku zpětně nemění.
4. **Testy** (376) nad fiktivními daty, každé validační pravidlo má pozitivní i negativní test.

### Kde se agent (a zadání) mýlil

| # | Chyba | Jak se našla | Oprava |
|---|---|---|---|
| 1 | **`robots.txt`:** obchodní rejstřík se četl přes cestu `/ias/` na or.justice.cz, kterou `robots.txt` zakazuje. | Kontrola surového textu odmítla stažení. | 23 faktů nahrazeno ARES; kontrola `robots.txt` v kódu před každým požadavkem |
| 2 | **Pravidlo (c):** shoda obchodní firmy s názvem značky stačila k přiřazení IČO. | Při ověřování Techstars by pravidlo přiřadilo nesouvisející firmu stejného jména. | Pravidlo zrušeno, platí jen doložená spojení (a), (b), (d). |
| 3 | **CVC:** J&T Ventures byl ověřen, ačkoli vazba na skupinu J&T existuje a podíl skupiny doložen nebyl. Springtide (kapitál jen od KKCG) dostal od R1 nejdřív `TP`. | Poznámka R1 „fond patřící pod J&T“ a souhrn rozporů | J&T přeřazen mezi kandidáty (fakt z webu fondu), Springtide vyloučen jako `cvc`. Pravidlo CVC (> 50 % kapitálu od jedné skupiny) se uplatňuje i u ověřených. |
| 4 | **Lighthouse:** „poslední investice 2019“ převzata z jediného článku, novější se nehledaly. | R1: false negative | Doplněny investice z roku 2025. Absenci aktivity tvrdit jen po cíleném hledání. |
| 5 | **Tachles:** validátor vyžadoval nepovinné pole `investment_stages`, subjekt zůstal kandidátem. | R1: false negative | Požadavek odstraněn a pokryt testem. Validátor vynucuje jen Z1–Z4. |
| 6 | **Obecný kód vyloučení** `mimo_definici_pilotu`: konkrétní důvod byl jen v poznámce, hodnotitel ho nemohl ověřit. | Při přípravě kontrolního listu | Rozdělen na 6 konkrétních kódů (`cvc`, `fond_fondu`, …). Validátor starý kód odmítá. |
| 7 | **Agregátory:** fakt Startguide stál na Caplight. Gain Ventures dostal od R1 `TP` na základě databází transakcí. | Kontrola zdrojů a souhrn rozporů | Zdroj nahrazen CzechCrunch, Gain přeřazen na `nejiste`. Validátor hlásí agregátor jako zdroj. |
| 8 | **Cíl fondu započítaný jako kapitál** – chyba v mém zadání, ne agenta. | Při revizi tabulky kapitálu | Nová definice: získaný kapitál × cíl × investováno × AUM zvlášť. Kapitál klesl z 15/16 na 13/16. Přísnější pravidlo pro dolní mez. |
| 9 | **Typ částky odvozený z kontextu:** cíl odvozen z pozdějšího zdroje, „první kolo“ zapsané jako uzavřený fond, plán investic jako cíl. | Kontrola R1 všech doplněných faktů: 6 ze 7 nálezů | Opraveno 7 faktů (kolo po opravě 7/7). Nové typy `oznamena_velikost_fondu` a `fond_investovano_za_obdobi`. Pravidlo: typ jen z formulace zdroje. |
| 10 | **Odhadnuté minuty:** u 18 cílených hledání agent zapsal kulaté odhady času jako měření. | Agent sám, při sjednocování definice času | Hodnoty smazány s poznámkou „čas nebyl měřen“. Minuty jsou povinné jen tam, kde se měří. |
| 11 | **Odhadnuté domény:** při sondě angel sítí agent zkusil uhodnout adresy webů (jedna patřila nesouvisejícímu e-shopu). | Agent sám, výsledek nepoužil | Do dat ani dokumentace se nic nedostalo. Agent chybu nahlásil. |
| 12 | **Credo Stage 5:** můj pokyn „first close → dolní mez“ agent ověřil proti zdrojům. | Agent: Wikipedie cituje Tech.eu, který first close neuvádí; TNW píše „single closing“. | Pokyn provedl konzervativně, konflikt označil a upozornil na něj. Kontrola R1 Wikipedii vyřadila, fond je teď final close. |
| 13 | **Nereprodukovatelný doklad:** zánik subjektu doložen dotazem na vyhledávací API ARES (POST), který hodnotitel nemůže zopakovat. | Kontrola vyloučených: 1 nejistý | Zapsáno jako omezení. Doklad „nic nenalezeno“ potřebuje otevíratelný zdroj. |

Další incidenty (soubor zamčený Excelem, nesoulad popisu commitu, data v nesouvisejícím commitu) jsou v [docs/02](docs/02-metodika.md), 2.8.

## Rozhodnutí v nejasných bodech zadání

| Bod | Rozhodnutí | Proč |
|---|---|---|
| Typ investora pro pilot | VC | Má právní formu a regulatorní stopu a veřejně komunikuje portfolio. Doložitelnost je nejlepší. PE se míchá s jinou strategií (většinové podíly). |
| Země | Česká republika | Bezplatný ARES s API, asociace CVCA se seznamem členů, malý trh vhodný pro ruční kontrolu, jazyk, který hodnotitel ovládá |
| Jednotka záznamu | VC značka (tým, který rozhoduje), ne právní správce | Jeden licencovaný správce často spravuje mnoho nesouvisejících strategií. Správce se ukládá jako fakt. |
| Corporate VC | Vyloučeno při > 50 % kapitálu fondu od jedné skupiny. Bez doloženého podílu kandidát. | Takový fond investuje převážně peníze korporace. |
| Aktivita | Investice nebo nový fond za 36 měsíců | Odpovídá investiční periodě VC fondu. Hodnota je předpoklad nastavitelný v `schema.py`. |
| Celkový investiční kapitál | Získaný kapitál po fondech podle typu částky. Cíl, investováno a AUM zvlášť. Měny se nesčítají ani nepřepočítávají. | „Kapitál“ v zadání je nejednoznačný. Sčítat cíle a získané částky by výsledek nadsadilo (chyba 8). |
| Hodnotitelé | Jeden hodnotitel R1, R2 nebyl k dispozici | Přesnost má proto široké intervaly a shoda hodnotitelů se nepočítá. Proces R2 podporuje (šablony, Cohenovo κ). |
| Úložiště | CSV v Gitu | Data jsou čitelná a verzovaná s historií, kterou hodnotitel zkontroluje. Pro tisíce záznamů by bylo potřeba přejít na databázi (docs/03). |
| Jazyk | Čeština, kódy slovníků ASCII | Jazyk zadavatele a zdrojů. ASCII kódy jsou stabilní pro strojové zpracování. |
| Osobní údaje | Fyzické osoby (angelé, soukromí investoři) se do dat neukládají | GDPR: v plánu je popsán oprávněný zájem, minimalizace a informační povinnost (docs/01 1.10). |

## Co v řešení chybí

- **Spotřeba tokenů je změřená jen na 3 investorech** (opakované ověření, jeden běh). Cena API pro family office, angely a velké soukromé investory je předpoklad odvozený z času modelu.
- **Family office, angel investoři a velcí soukromí investoři** mají jen pravidla a studii proveditelnosti se sondou v počtech, žádná data. Odhady jejich počtu jsou z velké části předpoklady.
- **PE jen jako mini-pilot (n = 5).** Výsledky jsou orientační a uvádějí se v počtech.
- **6 kandidátů** (Inven, J&T, Nation1, Gain Ventures, i&i Biotech, Tilia) zůstává nerozhodnutých. Chybí doklad podílu korporace (CVC), identifikace české entity nebo primární zdroj investice.
- **Jeden hodnotitel.** Chybí nezávislý R2 a shoda hodnotitelů.

## Reprodukovatelnost

Ověřeno 12. 10. 2026 na čistém klonu z GitHubu (commit `190e7e6`) v dočasné složce:

| Krok | Výsledek |
|---|---|
| `python -m pytest` | 364 testů prošlo |
| `python -m investor_db validate` | „Validace prošla bez chyb.“ |
| `python -m investor_db metrics` | výstup **shodný** s výstupem v pracovním repozitáři (`diff` bez rozdílů) |

Čísla z reportu odpovídají README:

| Ukazatel | Výsledek |
|---|---|
| Nalezeno subjektů | 52 |
| Přesnost faktů po kolech | 32/34, 42/44, 7/7 |
| Pole zadání | sektor 15/16, ticket 14/16, kapitál 13/16, zdroj 16/16 |
| Kontrola vyloučených | 9 TP a 1 nejisté |
| PE | pravost 5/5, v zemi 2/5, R1 2/2 a 3/3 TP |

Hlavní precision je z kola R1-v2 (11/16 přísně, 11/11 rozhodnuté) ze stavu v době kontroly. Původní kolo R1 report počítá ze současných statusů (14/14), hodnota 15/15 z doby kontroly je v [docs/04](docs/04-rucni-kontrola.md), 4.6, a v historii Gitu (commit `18877a1`). Instalace `pip install -e ".[dev]"` se v klonu nespouštěla, protože pytest byl v prostředí už nainstalovaný.

## Návod pro hodnotitele

1. **Instalace.** Je potřeba Python 3.11 nebo novější. Kód používá jen standardní knihovnu, pytest je jen pro testy.

   ```
   git clone https://github.com/osho4753/investor-db.git
   cd investor-db
   python -m pip install -e ".[dev]"
   ```

2. **Kontrola integrity.** Musí skončit hláškou „Validace prošla bez chyb.“

   ```
   python -m investor_db validate
   ```

3. **Metriky:** precision, přesnost faktů po kolech, úplnost, kapitál, trychtýř, pracnost a kategorie.

   ```
   python -m investor_db metrics
   ```

4. **Testy:**

   ```
   python -m pytest
   ```

5. **Ruční kontrola.** Návod je v [docs/04](docs/04-rucni-kontrola.md) a kontrolní list v [review/kontrolni-list-faktu.md](review/kontrolni-list-faktu.md) (`python -m investor_db review-guide`). Šablony se zakládají příkazy `review-template` a `fact-review-template` (parametry v docs/04 4.4, 4.8, 4.9).

> **Neupravujte CSV v Excelu.** Excel mění kódování (Windows-1250), formát dat a ořezává úvodní nuly v IČO. CSV upravujte v textovém editoru v UTF-8. Validátor takové poškození zachytí a `metrics` pak neběží.

## Prezentační web

Statický web s výsledky, daty a příběhy chyb je ve složce [`site/`](site/). Generuje ho příkaz:

```
python -m investor_db site
```

- **Zdroj dat:** čísla a záznamy počítají stejné funkce jako `metrics` z `data/*.csv`.
- **Převzaté tabulky:** souhrnná tabulka odhadů se načítá z docs/03, příběhy chyb z tabulky v tomto README.
- **Krátké texty:** jsou v [`site_texts/`](site_texts/) a dají se upravit bez zásahu do kódu.
- **Kontrola:** test ověřuje, že commitnutý `site/` odpovídá novému vygenerování a že odkazy na soubory v repozitáři existují. Po změně dat nebo textů je proto potřeba web přegenerovat a commitnout.

**Nasazení na Vercel:**

1. Na vercel.com zvolte Add New → Project a importujte repozitář `osho4753/investor-db`.
2. Nic dalšího nenastavujte. [`vercel.json`](vercel.json) vypíná instalaci i build a jako výstup používá složku `site`.
3. Deploy. Každý push do `main` web znovu nasadí ze commitnutého `site/`.

Bez Vercelu stačí otevřít `site/index.html` v prohlížeči.

## Struktura

```
docs/00-zadani.md         zadání
docs/01-plan-a-kriteria   plán, kritéria, kategorie, PE mini-pilot, studie proveditelnosti
docs/02-metodika          zdroje, postup, datové schéma, validace, incidenty
docs/03-globalni-odhad    globální odhad, spolehlivost, náklady, odhad po kategoriích
docs/04-rucni-kontrola    návod pro hodnotitele a výsledky všech kol kontroly
data/                     CSV tabulky (jediný zdroj pravdy)
investor_db/              schéma, validace, metriky, CLI
review/                   vygenerovaný kontrolní list
site/                     vygenerovaný prezentační web (python -m investor_db site)
site_texts/               krátké texty webu k úpravě
tests/                    testy nad fiktivními daty
ai-log/                   exporty konverzací s Claude Code
```
