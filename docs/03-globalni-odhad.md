# 3. Globální odhad: počet investorů, spolehlivost a náklady škálování

Dokument pokrývá výstupy 3 (odhad globálního pokrytí, počtu investorů a spolehlivosti) a 7 (odhad nákladů a složitosti škálování). Každé číslo má buď zdroj otevřený 11. 10. 2026, nebo je výslovně označené jako **předpoklad**. Předpoklady jsou uvedené s rozsahem a se zdůvodněním. Kde zdroj nic neuvádí, hodnota zůstává neznámá a nedopočítává se.

## 3.1 Zdroje počtu investorů

| # | Zdroj | Typ | Údaj | Rozsah a omezení | Ověření |
|---|---|---|---|---|---|
| G1 | [NVCA 2026 Yearbook](https://nvca.org/?p=124853) | asociace | **2 984** VC firem v USA („Total VC firms in existence“), poprvé pokles z 3 054 | Rok 2025. Firmy, ne fondy. Metodika započtení je v plné zprávě, která otevřena nebyla. | surový text stránky |
| G2 | [NVCA, tisková zpráva k Yearbooku 2025](https://nvca.org/press_releases/nvca-releases-2025-yearbook-showcasing-2024-vc-trends/) | asociace | USA tvoří **57 %** celosvětové hodnoty VC transakcí | Rok 2024. Podíl na **hodnotě** transakcí, ne na počtu firem. | surový text stránky |
| G3 | [Tech.eu o zprávě Invest Europe](https://tech.eu/2025/07/24/invest-europe-european-private-capital-hits-eur125t-in-2024-growing-26x-over-the-decade/) | médium (cituje asociaci) | **3 095** aktivních firem PE a VC v Evropě, AUM 1,25 bil. EUR | Rok 2024. PE a VC dohromady, podíl VC článek neuvádí. Zpráva Invest Europe sama otevřena nebyla. | surový text stránky |
| G4 | [UK Private Capital (dříve BVCA)](https://www.ukprivatecapital.co.uk/resource/new-report-shows-domestic-fundraising-environment-for-venture-capital-remains-challenging-despite-strong-returns.html) | asociace | Více než **260** členských firem PE a VC | Listopad 2024. Jen členové asociace, PE a VC dohromady. | surový text stránky |
| G5 | [ESMA – registr fondů](https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_funds), veřejné API Solr | regulátor | **1 369** fondů EuVECA, z toho **970** aktivních. **415** správců s aktivním fondem EuVECA, **z ČR žádný**. Nejvíce ES 90, SE 71, DE 68, NL 55. | Stav 11. 10. 2026. Označení EuVECA je dobrovolné, registr proto zachycuje jen část trhu. Správci jsou počítaní podle národního jména a země, bez deduplikace napříč zeměmi. | JSON z API |
| G6 | [SEC – Private Fund Statistics, počet fondů a poradců](https://www.sec.gov/data-research/data-visualizations/private-fund-statistics/private-funds-number-funds-advisers) | regulátor | **4 392** VC fondů a **362** registrovaných poradců s VC fondem (2025Q4) | Jen poradci registrovaní u SEC, kteří podávají Form PF. Exempt reporting advisers (výjimka pro VC poradce) tu **nejsou**. | jen shrnutí nástroje: sec.gov vrátil surovému stahování HTTP 403 |
| G7 | [FCA – registrace malých AIFM](https://www.fca.org.uk/firms/aifmd/sef-rveca-managers) a [komentář Ocorian](https://www.ocorian.com/knowledge-hub/insights/beyond-registration-future-small-registered-uk-aifms-under-proposed-aifmd) | regulátor a odborný komentář | Registr malých registrovaných UK AIFM zahrnuje i správce RVECA. Komentář uvádí **145** firem v tomto režimu. | Registr FCA je aplikace vykreslovaná JavaScriptem, surový text neposkytl a počet správců RVECA z něj nešel zjistit. Číslo 145 je z komentáře, ne od regulátora, a nerozlišuje VC. | surový text stránek |
| P1 | Pilot ČR ([04-rucni-kontrola.md](04-rucni-kontrola.md)) | vlastní měření | 14 ověřených VC, 6 kandidátů (po kontrole R1-v2). Capture–recapture (Chapman) 9–29, jde o dolní mez. 17 subjektů vyloučeno jako PE. | Jedna země, 52 nalezených subjektů. | ruční kontrola R1 |
| P2 | [CVCA, řádní členové](https://cvca.cz/en/category/full-members/) (průchod s-002) | asociace | 27 řádných členů (PE a VC) | Stav 9. 10. 2026 | surový text stránky |

**SEC exempt reporting advisers (IAPD).** Počet poradců, kteří se opírají o výjimku pro VC fondy, se nepodařilo zjistit. sec.gov surovému stahování vrátil HTTP 403 a ochranu jsme neobcházeli podvrženou hlavičkou User-Agent, takže počet zůstává **neznámý**. Pro škálování jde o klíčový zdroj. Dalším krokem je zjistit podmínky strojového přístupu SEC a data stahovat v souladu s nimi.

**Národní registry.** Pilot ukázal, že rejstřík ČNB (JERRS) je za CAPTCHA a or.justice.cz zakazuje cestu `/ias/` v robots.txt. Použitelný byl až ARES (REST API). Dostupnost národních registrů se proto musí posoudit země po zemi a v odhadu se počítá s koeficientem obtížnosti (3.4).

## 3.2 Co z pilotu plyne pro odhad

- **Registry regulátorů VC podhodnocují.** V ČR je 14 ověřených VC, ale v registru EuVECA žádný. Opt-in registr tedy není použitelný jako výčet trhu, poslouží jen jako zdroj kandidátů a dolní mez.
- **Asociace mísí PE a VC.** V pilotu připadlo na 20 VC subjektů (14 ověřených a 6 kandidátů) 17 subjektů vyloučených jako PE, podíl VC tedy vychází 48–54 %. Odtud plyne předpoklad podílu VC mezi firmami PE a VC v Evropě 0,4–0,6.
- **Trychtýř:** na jednoho ověřeného investora připadá 52 / 14 = 3,7 zpracovaného subjektu.
- **Capture–recapture** dává jen dolní mez, protože zdroje nejsou nezávislé.

## 3.3 Odhad počtu VC investorů – scénáře

| Složka | Nízký | Základní | Vysoký | Zdroj nebo předpoklad |
|---|---|---|---|---|
| USA | 2 984 | 2 984 | 2 984 | G1 |
| Evropa: podíl VC mezi firmami PE a VC | 0,4 | 0,5 | 0,6 | **Předpoklad** z pilotu (48–54 %) |
| Evropa | 1 238 | 1 548 | 1 857 | G3 × podíl VC |
| Zbytek světa | 1 013 | 2 719 | 4 841 | Nízký: dopočet do celku USA / 0,57 (G2). Základní a vysoký: **předpoklad** 0,6×, resp. 1,0× součtu USA a Evropy. |
| **Svět celkem** | **5 235** | **7 251** | **9 682** | |

**Zdůvodnění scénářů:**
- **Nízký** předpokládá, že počet firem je úměrný hodnotě transakcí (G2). Fondy mimo USA jsou ale typicky menší, takže jejich počet je vůči hodnotě vyšší. Nízký scénář je proto spíš podhodnocený.
- **Základní a vysoký** scénář pro zbytek světa (Asie, Izrael, Latinská Amerika, Kanada, Austrálie, Afrika) **nemají přímý zdroj**. Násobek je předpoklad, který je třeba nahradit daty národních asociací nebo regulátorů v dalším kroku.
- Kontrolní dolní meze: v Evropě je nejméně 415 správců s aktivním fondem EuVECA (G5) a v USA 362 registrovaných poradců s VC fondem (G6). Obě čísla jsou výrazně nižší, protože registry zachycují jen část trhu.
- Počty jsou **firmy (značky)**, stejná jednotka jako v pilotu, ne fondy (SEC: 4 392 VC fondů).

## 3.4 Spolehlivost dat podle regionů

Výchozím bodem je pilot:
- precision z kola R1-v2: **11/16 = 68,8 %** přísně (95% Wilsonův interval 44,4–85,8 %) a **11/11** jen u rozhodnutých případů (74,1–100 %). Původní kolo 15/15 je jen historie (docs/04, 4.6 a 4.11);
- přesnost faktů **32/34 = 94,1 %** (80,9–98,4 %), pesimisticky 88,9 %.

Hodnoty pro ostatní regiony jsou **předpoklady**, které je nutné změřit ruční kontrolou vzorku v každém regionu.

| Úroveň | Regiony | Dostupnost zdrojů | Očekávaná přesnost faktů (předpoklad) | Koeficient obtížnosti (předpoklad) |
|---|---|---|---|---|
| 1 | USA, UK, Kanada, Austrálie | Angličtina, data SEC (strojový přístup je třeba vyřešit), silné asociace a média; dostupnost firemních registrů v pilotu neověřena | jako pilot, 90–98 % | 1,0–1,3 |
| 2 | EU a EHP | Registr ESMA (API), národní registry s různou dostupností (CAPTCHA, robots.txt), více jazyků | 85–95 % | 1,0–1,5 |
| 3 | Asie, Izrael, Latinská Amerika, Blízký východ, Afrika | Místní jazyky a písma, registry často placené nebo bez API, méně médií | 75–90 % | 2,0–3,0 |

Precision ve smyslu „ověřený záznam je skutečně aktivní VC“: kolo R1-v2 nenašlo žádný FP, ale u 5 z 16 záznamů nestačily doklady (Z1, Z3 nebo Z4), takže přísná precision je 11/16. Identitu (Z1) drželo hlavně zařazování jen s primárním dokladem z ARES. Kde takový registr chybí (úroveň 3), přibude kandidátů. V pilotu skončilo jako kandidát 4 z 20 VC subjektů, tedy 20 %.

## 3.5 Náklady škálování

### Naměřené vstupy z pilotu

| Vstup | Hodnota | Zdroj |
|---|---|---|
| Čas modelu na ověřeného investora (hledání, triáž, ověření, doplnění; sjednocená definice v 3.8) | (5,55 + 0,66 + 80,1 + 23,9) min / 14 = **7,9 min** | `effort_log.csv`, `search_log.csv` |
| Tokeny a cena API na ověřeného investora (opakované ověření, n = 3) | **363 690 tokenů, od 0,365 USD** (spíš dolní mez) | [ai-log/mereni-tokenu-2026-10-13.md](../ai-log/mereni-tokenu-2026-10-13.md) |
| Čas člověka na kontrolu investora | **15,5 min** | `reviews.csv` (první kontrola) |
| Čas člověka na kontrolu faktu | **0,96 min** | `fact_reviews.csv` |
| Vzorek na region | 25 investorů a 36 faktů (±15 p. b.) | Cochran, viz [04-rucni-kontrola.md](04-rucni-kontrola.md) |

Čas modelu je čas běhu nástrojů včetně čekání na stránky a omezení rychlosti.

### Výpočet

**Model.** Počet investorů × 7,9 min × koeficient regionu (USA 1,0–1,3, Evropa 1,0–1,5, zbytek světa 2,0–3,0):

| Scénář | Investorů | Čas modelu, první sběr | Roční aktualizace (**předpoklad** 50–100 % prvního sběru) |
|---|---|---|---|
| Nízký | 5 235 | 817–1 149 h | 408–1 149 h |
| Základní | 7 251 | 1 304–1 878 h | 653–1 878 h |
| Vysoký | 9 682 | 1 900–2 772 h | 950–2 772 h |

Čas běhu jde paralelizovat mezi domény. Omezení rychlosti platí pro každou doménu zvlášť, celková doba sběru tedy závisí na počtu souběžných pracovníků, ne na součtu hodin.

**API modelu [M].** Samostatná session Claude Code (Opus 5.5) znovu ověřila 3 ověřené investory podle metodiky: Soulmates (nejsnazší podle `effort_log`), Purple (medián) a Lighthouse (nejsložitější). Skript `python -m investor_db tokens` sečetl spotřebu z transkriptu session. Postup, výstup skriptu a porovnání s daty jsou v [ai-log/mereni-tokenu-2026-10-13.md](../ai-log/mereni-tokenu-2026-10-13.md).

| Model | Tokenů | Cena |
|---|---|---|
| Opus 5.5 (session): vstup 22, výstup 10 242, čtení cache 714 750, zápis cache 1h 79 620 | 804 634 | 0,985 USD |
| Haiku 5.5 (interně ve WebFetch a WebSearch) a 7 vyhledávání | 286 436 | 0,109 USD |
| **Celkem za 3 investory** | **1 091 070** | **1,094 USD** |
| **Na ověřeného investora** | **363 690** | **od 0,365 USD** |

Ceník: [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing), otevřeno 13. 10. 2026. Opus 5.5 stojí 4 USD za milion vstupních tokenů, 20 USD za výstup, 0,20 USD za čtení cache a 8 USD za zápis do hodinové cache; vyhledávání 0,01 USD. Session běžela 2 min 43 s. Dřívější předpoklad byl 100 000–400 000 tokenů a 0,30–6 USD na investora. Počet tokenů vyšel u horní hranice, cena u spodní, protože 66 % tokenů tvoří levné čtení z cache.

**Cena na záznam v databázi.** Měření pokrývá jen opakované ověření hotového investora. Při prvním sběru se navíc ověřují subjekty, které skončí jako kandidáti nebo vyloučení, a zapisují se fakta:

- **nízký:** 0,36 USD [M] – jen ověření jednoho investora;
- **základní:** 0,36 × 30 posouzených / 14 ověřených = **0,78 USD** [M] – ověření i subjektů, které se do databáze nedostanou (poměr z pilotu);
- **vysoký:** 0,78 × 2 = 1,56 USD [M+P] – zdvojnásobení za zápis dat, doplnění polí a opravy po kontrole je předpoklad.

| Scénář počtu VC | Investorů | API, první sběr (0,36 / 0,78 / 1,56 USD na záznam) |
|---|---|---|
| Nízký | 5 235 | 1 909 / 4 091 / 8 182 USD |
| Základní | 7 251 | 2 644 / 5 666 / 11 332 USD |
| Vysoký | 9 682 | 3 531 / 7 566 / 15 132 USD |

**Měření je spíš dolní mez.** Session jen četla a vyhledávala, nic nezapisovala (fakta, zdroje, status), neověřovala proti surovému textu stránek, trvala jen 2 min 43 s a u Lighthouse měla v docs/02 nápovědu domény (lhv.vc). Skutečný sběr s ověřením a zápisem dat bude dražší. Navíc jde o n = 3, jeden běh a jednu zemi.

**Člověk.** Ruční kontrola je výběrová, její rozsah proto závisí na počtu regionů, ne na počtu investorů:
- 25 × 15,5 + 36 × 0,96 = **422 min (7,0 h) na region a hodnotitele**;
- při 8–15 regionech to dává **56–106 h** na jednoho hodnotitele a jedno kolo; druhý hodnotitel (R2) čas zdvojnásobí;
- **hodinová sazba (předpoklad)** 25–60 EUR/h znamená 1 407–6 331 EUR za kolo;
- kolo se opakuje při každé roční aktualizaci;
- navíc je potřeba čas na rozhodnutí kandidátů (v pilotu 20 % VC subjektů), který pilot neměřil.

**Infrastruktura (předpoklady):**
- PostgreSQL místo CSV (CSV v Gitu stačí do jednotek tisíc řádků): spravovaná instance 20–200 USD měsíčně;
- cache surových stránek mimo repozitář: objektové úložiště v řádu jednotek USD měsíčně;
- plánovač úloh s omezením rychlosti na doménu a kontrolou robots.txt už existuje (`investor_db/rawtext.py`), je třeba ho jen rozšířit o frontu a souběh;
- přístup k datům regulátorů v souladu s jejich podmínkami (ESMA API fungovalo bez omezení, SEC vrátil 403).

Měny se nepřepočítávají, náklady na API a infrastrukturu jsou v USD, náklady na lidi v EUR.

### Složitost

| Oblast | Složitost | Proč |
|---|---|---|
| Hledání kandidátů | střední | Asociace a registry pokrývají jen část trhu (EuVECA v ČR 0 z 16), je nutné kombinovat zdroje a měřit překryv. |
| Z1 (právnická osoba) | vysoká mimo EU | Pilot stál na ARES. Bez bezplatného registru s API zůstává záznam kandidátem. |
| Pravidlo CVC | vysoká | Podíl korporace na kapitálu fondu veřejné zdroje obvykle neuvádějí (Inven, J&T). |
| Jazyky | vysoká pro úroveň 3 | Ověření proti surovému textu vyžaduje vzory částek a dat pro každý jazyk (`rawtext.money_patterns`, `date_patterns`). |
| Ruční kontrola | lineární s počtem regionů | Potřeba hodnotitelů znalých regionu a jazyka. |

## 3.6 Omezení veřejných zdrojů zjištěná v pilotu

| Omezení | Příklad z pilotu | Dopad na škálování |
|---|---|---|
| CAPTCHA | Rejstřík ČNB JERRS (s-004) nelze projít nástroji | Regulatorní seznamy správců nejsou vždy strojově dostupné. Je nutná náhrada (ARES, ESMA). |
| robots.txt | or.justice.cz zakazuje `/ias/`, sbírka listin se nečetla, doklady nahradil ARES | Část primárních dokladů (stanovy, výroční zprávy) je nedostupná. |
| HTTP 403 a 429 | businessinfo.cz a fundsforngos.org vrátily 403 (s-008, s-012, s-013), funding.tech.eu 429, sec.gov 403 | Ochranu se nesnažíme obejít. Hodnota zůstává ověřená jen přes shrnutí nebo neznámá. |
| Placené databáze | PitchBook, Dealroom, Crunchbase Pro se nepoužívají, agregátory slouží jen jako vodítko | Nižší úplnost (ticket 69–75 %, velikost fondu 12,5 %). |
| Shrnování stránek nástrojem | Nástroj pro čtení webu vrací shrnutí jazykovým modelem. Částky a data se proto ověřují proti surovému textu. | Stránky vykreslované JavaScriptem (registr FCA) surový text neposkytnou. |
| Nejednoznačné názvy | Gain Ventures, Nation1, Tachles | Identifikace podle domény a týmu, část záznamů zůstává kandidáty. |
| Paywall | Článek The Recursive o Tachles je jen pro předplatitele | Fakty z takových zdrojů se nezapisují. |
| Konflikt uvnitř zdroje | Reflex: citace zakladatele a text redakce uvádějí jiný ticket | Pole tiketu neumí zachytit „typicky X, výjimečně Y“. |

## 3.7 Zdroje pro další kategorie investorů

Zdroje byly otevřeny 12. 10. 2026. Čísla, která se nepodařilo otevřít ve zdroji, se nepoužívají.

| # | Zdroj | Typ | Údaj | Rozsah a omezení |
|---|---|---|---|---|
| E1 | [Vault – Private Equity: The Industry Today](https://legacy.vault.com/industries-professions/industries/private-equity/the-industry-today) | odborný přehled, cituje asociaci | „approximately **7,000** private equity firms worldwide (with **6,000** firms located in the United States), according to the American Investment Council“ | Sekundární zdroj. Údaj AIC jsme neotevřeli v originále. Celkový počet ve světě je menší než součet USA a Evropy (G3), definice se tedy zřejmě liší. |
| E2 | G3 a P2 ze 3.1, mini-pilot PE ([01](01-plan-a-kriteria.md), 1.11) | vlastní měření | 17 PE mezi řádnými členy CVCA. Z 5 náhodně vybraných jsou skutečnými PE všech 5/5, českou entitu mají 2/5. | n = 5, jen členové CVCA |
| E3 | [Deloitte Private – Family Office Insights Series, tisková zpráva](https://www.deloitte.com/in/en/about/press-room/global-edition-explores-the-rapid-expansion-family-offices-and-ffers-vision-of-the-future-landscape.html) | výzkumná zpráva | „an estimated **8,030** single family offices in the world today“ (2019: 6 130, projekce 2030: více než 10 720) | Jen single-family office. Odhad, ne registr. |
| E4 | [Dakota o zprávě Deloitte](https://www.dakota.com/fundraising-news/deloitte-number-of-family-offices-to-grow-75-by-2030) | médium (cituje E3) | Evropa **2 020**, Severní Amerika 3 180, Asie a Tichomoří 2 290 family office | Regionální rozpad z tabulky Deloitte |
| E5 | [EBAN – Statistics Compendium 2021](https://www.eban.org/2022/10/10/) | asociace | „approximately **39400** active business angel investors on the European continent“, investice 1 456 mil. EUR (2021) | Jen angelé organizovaní v sítích a asociacích. Shrnutí nástroje, surový text neotevřen. |
| E6 | [CBAA – databáze členů](https://www.cbaa.cz/clenstvi) | asociace | **11** zveřejněných členů, z toho 7 fyzických osob | Stav 12. 10. 2026; sonda v [01](01-plan-a-kriteria.md), 1.12 |
| E7 | [Forbes Česko o The Wealth Report (Knight Frank)](https://forbes.cz/pocet-ultrabohatych-roste-minuly-rok-jich-pribyvalo-sedmdesat-za-den/) | médium (cituje výzkumnou zprávu) | Lidí s majetkem nad 30 mil. USD je „přes **626 tisíc**“, meziročně +4,2 % | Článek z 19. 4. 2024. Českou hodnotu neuvádí. |
| E8 | [e15, 29. 9. 2015](https://www.e15.cz/byznys/finance-a-bankovnictvi/v-ceske-republice-je-pres-200-ultrabohacu-1231288) | médium | Capgemini Czech Republic: „Přesné číslo není známé, ale lze odvodit, že je to jedno procento z milionářské populace, což je zhruba **210** lidí“ s investičním majetkem nad 30 mil. USD | Starý a odvozený odhad |
| E9 | [Newstream (ČTK), 21. 6. 2022](https://www.newstream.cz/money/pocet-dolarovych-milionaru-v-cesku-prekonal-30-tisic-jsou-take-bohatsi) | médium (cituje Capgemini) | **32 200** dolarových milionářů v ČR (investovatelné jmění od 1 mil. USD), rok 2021 | Milionáři nejsou investoři do firem |
| E10 | Sonda family office ([01](01-plan-a-kriteria.md), 1.12) | vlastní měření | 0/5 lze doložit podle F1–F4, 3/5 kandidáti, 2/5 poskytovatelé služeb; kapitál zveřejněn 0/5 | n = 5, jen mediálně známé případy |

**Nepoužito.** Počet aktivních angel investorů v USA z UNH Center for Venture Research se nepodařilo otevřít: chyba certifikátu, PDF bez čitelného textu a stránka EBAN, která výsledky přebírá, vrátila 404. Údaj proto zůstává **neznámý**. Statistiky ČNB ani Knight Frank pro ČR v otevřených zdrojích nebyly.

## 3.8 Odhad pro jednotlivé kategorie

Typ každého údaje je uveden přímo u čísla:

- **[M]** změřeno v pilotu nebo mini-pilotu (data v repozitáři, ruční kontrola R1);
- **[Z]** převzato ze zdroje (E1–E10, G1–G7, P1–P2);
- **[P]** předpoklad.

Hodnocení sběrače (status, který přidělil model) není měření. Měřením je až ruční kontrola R1.

„Získatelné z veřejných zdrojů“ znamená záznam, který lze doložit podle pravidel kategorie ([01](01-plan-a-kriteria.md), 1.10). Neznamená to, že bude mít vyplněná všechna pole zadání.

### Sjednocená definice času modelu

Čas modelu se dělí na fáze. Všechny se berou z `effort_log.csv` (časové značky začátku a konce) a z průchodů hledání kandidátů v `search_log.csv`.

| Fáze | Co obsahuje | VC (pilot) | PE (mini-pilot) |
|---|---|---|---|
| Hledání kandidátů | průchody seznamů a registrů (`search_log` bez `investor_id`) | 5,55 min / 52 nalezených = **0,11 min** na nalezený subjekt [M] | vlastní hledání 0. Seznam převzat z průchodu s-002 VC pilotu, počítá se stejně 0,11 min [M] |
| Triáž | rychlé vyloučení podle zdroje hledání | 0,66 min / 22 = **0,03 min** [M] | proběhla ve VC pilotu, 0,03 min [M] |
| Ověření | doložení kritérií kategorie (Z1–Z4, resp. P1–P4) | 80,1 min / 30 posouzených = **2,67 min** na posouzený subjekt [M] | 5,03 min / 5 = **1,01 min** na posouzený subjekt [M]; pole zadání zapsána už při ověření |
| Doplnění | sektor, ticket a kapitál podle zadání | 23,9 min / 16 = **1,49 min** na ověřený záznam [M] | 0, je součástí ověření |
| **Celkem na záznam v databázi** | všechny fáze / počet záznamů, které se do databáze dostanou | (5,55 + 0,66 + 80,1 + 23,9) / 14 = **7,9 min** na ověřený VC [M] | 0,11 + 0,03 + 1,01 = **1,15 min** na pravého PE investora (5/5 podle R1) [M] |

Na 30 posouzených VC připadá 14 ověřených (po kontrole R1-v2, dříve 16 a 6,9 min), protože ověřování kandidátů a vyloučených také stojí čas. U PE se záznam vede v zemi sídla, takže se do databáze dostane každý pravý investor.

**Proč se dřívější hodnoty liší.** Dřívější hodnota 5,4 min u VC zahrnovala hledání, triáž a ověření, ale ne doplnění. Hodnota 1,0 min u PE zahrnovala jen ověření. Nově se obě kategorie počítají stejně.

**Proč je PE rychlejší:**

- weby PE fondů a profily CVCA uvádějí strategii, ticket a fondy přehledně;
- 3 z 5 subjektů rozhodlo P1 (zahraniční sídlo) už v první fázi;
- ve VC pilotu byly složité případy (CVC, kandidáti, konflikty zdrojů).

Při n = 5 je rozdíl orientační.

**Minuty cílených hledání** v `search_log.csv` (s-018 až s-035) se nezapočítávají. Nejsou změřené: jde o kulaté hodnoty, které při zápisu odhadl sběrač. Čas těchto hledání je obsažen ve změřeném čase ověření a doplnění.

### VC

| | Nízký | Základní | Vysoký |
|---|---|---|---|
| Svět, počet firem | 5 235 [Z+P] | 7 251 [Z+P] | 9 682 [Z+P] |
| ČR | 14 [M] | 20 [M] | 29 [M] |
| Získatelné z veřejných zdrojů | 70 % [M] | 70 % [M] | 70 % [M] |

Svět: USA 2 984 [Z: G1], Evropa = 3 095 [Z: G3] × podíl VC 0,4–0,6 [P], zbytek světa [P] (3.3). ČR: 14 ověřených, 14 + 6 kandidátů a nejvyšší Chapmanův odhad. Získatelné: 14 ověřených z 20 VC subjektů.

**Spolehlivost [M]:**

- precision R1-v2: 11/16 přísně, 11/11 rozhodnuté;
- přesnost faktů – vzorek 32/34, přísně 32/36;
- přesnost faktů – doplňování 42/44, přísně 42/49;
- opravy 7/7.

Pole zadání [M]: sektor 13/14, ticket 12/14, kapitál 11/14.

**Náklady [M]:** model 7,9 min na ověřený záznam (sjednocená definice). API 0,78 USD na záznam (0,36–1,56, viz 3.5). Člověk 15,5 min na kontrolu investora a 0,82–0,96 min na fakt.

### PE

| | Nízký | Základní | Vysoký |
|---|---|---|---|
| USA | 6 000 [Z: E1] | 6 000 [Z: E1] | 6 000 [Z: E1] |
| Evropa | 1 238 [Z: G3 × P] | 1 548 [Z: G3 × P] | 1 857 [Z: G3 × P] |
| Zbytek světa | – | 0,3 × (USA + Evropa) [P] | 0,6 × (USA + Evropa) [P] |
| **Svět celkem** | **7 000** [Z: E1] | **9 812** [Z+P] | **12 571** [Z+P] |
| ČR – skuteční PE investoři aktivní v ČR | 17 [M] | 22 [M+P] | 27 [M+P] |
| ČR – s českou právnickou osobou | 3 [M+P] | 9 [M+P] | 16 [M+P] |

- **Evropa:** G3 × podíl PE 0,4 / 0,5 / 0,6. Podíl PE = 1 − podíl VC z 3.3 a je to předpoklad.
- **Svět, nízký scénář:** číslo E1. Je menší než součet USA a Evropy, protože definice zdrojů se liší.
- **ČR, aktivní:** 17 PE členů CVCA (pravost 5/5 podle R1, viz níže). Nečlenové +30 % / +60 % jsou předpoklad.
- **ČR, s českou entitou:** 17 × podíl 0,2 / 0,4 / 0,6 (pilot 2/5 [M], rozpětí [P]) × nečlenové 1,0 / 1,3 / 1,6 [P].

**Kontrola R1 [M]** (`reviews.csv`, `category=pe`, 12. 10. 2026):

| | Počet |
|---|---|
| Verdikt TP celkem | 5/5 |
| Ověření v zemi pilotu potvrzeni | 2/2 |
| Správně vyloučeni z rámce země (zahraniční subjekt) | 3/3 |
| Pravost (skutečný PE investor) potvrzená R1 | 5/5 (u vyloučených R1 výslovně: „Skutečný PE investor: ano“) |
| V rámci země pilotu (česká právnická osoba) | 2/5 |

Při 5 záznamech jde o studii proveditelnosti, výsledek se proto neuvádí v procentech. Čas kontroly R1 [M]: 45 min za 5 záznamů, tedy **9 min na záznam** (5–15 min). Vyloučené zahraniční subjekty trvaly 5–15 min, ověřené 5–10 min.

**Pole zadání [M]:**

- sektor 5/5, ticket 5/5;
- získaný kapitál podle přísné definice 1/5, nějaký údaj o kapitálu 5/5;
- ticket se mezi webem a CVCA rozchází ve 3/5.

**Přesnost faktů:** kontrolou faktů neměřena. Očekává se 85–95 % jako u VC [P], protože jde o stejnou metodiku.

**Náklady [M]:** model 1,15 min na pravého PE investora (sjednocená definice, n = 5). API 0,11 USD na záznam [M+P]: cena VC × 1,15 / 7,9 min.

### Family office

| | Nízký | Základní | Vysoký |
|---|---|---|---|
| Svět, single-family office | 8 030 [Z: E3] | 8 030 [Z: E3] | 10 720 [Z: E3, projekce 2030] |
| z toho Evropa | 2 020 [Z: E4] | 2 020 [Z: E4] | – |
| Svět – přímí investoři do firem | 2 409 [Z × P 0,3] | 4 015 [Z × P 0,5] | 7 504 [Z × P 0,7] |
| ČR – family office celkem | 10 [P] | 30 [P] | 60 [P] |
| ČR – přímí investoři | 3 [P] | 15 [P] | 42 [P] |
| Získatelné z veřejných zdrojů | 0 % [M: sonda 0/5] | 15 % [P] | 30 % [P] |

**Proč základní scénář 15 %, když sonda dala 0/5.**

- 0/5 při tak malém vzorku nevylučuje ani poměrně vysoký skutečný podíl. 95% Wilsonův interval pro 0/5 je **0–43,4 %**.
- Nízký scénář bere bodový odhad sondy (0 %). Základní a vysoký leží uvnitř intervalu a jsou to předpoklady. 15 % je zhruba třetina horní meze. 30 % předpokládá, že hlubší hledání doloží část ze 3/5 kandidátů.
- Sonda četla jen jeden mediální článek na případ. Hledání tiskových zpráv o přímých investicích by mohlo F3 doložit u části kandidátů, ale doložitelnost by zůstala nízká.
- Hodnotu je potřeba nahradit sondou o 25 záznamech.

**Spolehlivost [P]:** 70–90 %. Hlavním rizikem je klasifikace: vlastní, nebo cizí kapitál; přímá investice, nebo LP. Stejný typ chyby převažoval v kole `po_doplneni` (6/7 nálezů [M]). Pole zadání: kapitál 0/5 [M], sektor a výše zřídka.

**Náklady [P]:** model 2–4× čas ověření a doplnění u VC, tedy 14–28 min na záznam (střed 21 min). Chybí registr i seznam kandidátů. API 2,08 USD na záznam [P]: cena VC × 21 / 7,9 min. Člověk 15–30 min.

### Angel investoři

| | Nízký | Základní | Vysoký |
|---|---|---|---|
| Evropa – aktivní angelé v sítích | 39 400 [Z: E5] | 39 400 [Z: E5] | 39 400 [Z: E5] |
| Svět | 118 200 [P: Evropa × 3] | 197 000 [P: Evropa × 5] | 394 000 [P: Evropa × 10] |
| ČR – angelé celkem | 100 [P] | 300 [P] | 1 000 [P] |
| ČR – sami se veřejně prezentují (A1) | 7 [M: CBAA, E6] | 30 [P] | 100 [P] |
| Získatelné z veřejných zdrojů | 5 % [P] | 10 % [P] | 20 % [P] |

Údaj za USA nebyl ověřen (3.7), proto je světový počet předpokladem, ne zdrojem.

**Spolehlivost [P]:** 80–95 % u identity a investice, pokud stojí na vlastním zveřejnění. Pole zadání [M]: sektor a ticket 2/11 profilů v CBAA, kapitál se neukládá.

**Náklady [P]:** model 14–28 min na záznam. Navíc informační povinnost podle čl. 14 GDPR, 5–10 min na osobu. API 2,83 USD na záznam [P]: cena VC × 28,5 / 7,9 min. Člověk 15–30 min.

**Omezení:** CBAA záměrně brání indexaci seznamu členů (1.12).

### Velcí soukromí investoři

| | Nízký | Základní | Vysoký |
|---|---|---|---|
| Svět – UHNWI (majetek nad 30 mil. USD) | 626 000 [Z: E7] | 626 000 [Z: E7] | 626 000 [Z: E7] |
| Svět – přímí investoři do firem | 31 300 [Z × P 5 %] | 62 600 [Z × P 10 %] | 125 200 [Z × P 20 %] |
| ČR – UHNWI | 210 [Z: E8, 2015] | 210 [Z: E8] | 210 [Z: E8] |
| ČR – přímí investoři | 11 [Z × P] | 21 [Z × P] | 42 [Z × P] |
| Získatelné z veřejných zdrojů | 10 % [P] | 20 % [P] | 30 % [P] |

Kategorie se částečně překrývá s family office.

**Spolehlivost [P]:** 70–90 %.

**Náklady [P]:** model 14–28 min a GDPR 5–10 min jako u angelů. API 2,83 USD na záznam [P] jako u angelů. Člověk 15–30 min.

### Souhrnná tabulka (základní scénář, v závorce nízký – vysoký)

Typ údaje: [M] změřeno, [Z] zdroj, [P] předpoklad; kombinace znamená výpočet z obou.

| Kategorie | ČR | Svět | Získatelné z veřejných zdrojů | Spolehlivost | Model na záznam | API na záznam | Člověk na kontrolu záznamu |
|---|---|---|---|---|---|---|---|
| VC | 20 (14–29) [M] | 7 251 (5 235–9 682) [Z: G1, G3 + P] | 70 % [M] | precision R1-v2 11/16 přísně, 11/11 rozhodnuté [M]; fakta 32/34 a 42/44, přísně 32/36 a 42/49 [M] | 7,9 min [M] | 0,78 USD (0,36–1,56) [M] | 15,5 min [M] |
| PE | 9 (3–16) s českou entitou [M+P]; 22 (17–27) aktivních v ČR [M+P] | 9 812 (7 000–12 571) [Z: E1, G3 + P] | pravost 5/5, v zemi pilotu 2/5 [M: kontrola R1] | status 5/5 TP [M: R1]; fakta 85–95 % [P] | 1,15 min [M, n = 5] | 0,11 USD (0,05–0,23) [M+P] | 9 min [M, n = 5] |
| Family office | 15 (3–42) přímých investorů [P] | 4 015 (2 409–7 504) [Z: E3 × P] | 15 % (0–30 %) [P; sonda 0/5 M] | 70–90 % [P] | 14–28 min [P] | 2,08 USD (0,97–4,17) [P] | 15–30 min [P] |
| Angel investor | 30 (7–100) s vlastním zveřejněním [P; 7 M] | 197 000 (118 200–394 000) [P: Evropa E5 × 3–10] | 10 % (5–20 %) [P] | 80–95 % [P] | 14–28 + GDPR 5–10 min [P] | 2,83 USD (1,32–5,66) [P] | 15–30 min [P] |
| Velký soukromý investor | 21 (11–42) [Z: E8 × P] | 62 600 (31 300–125 200) [Z: E7 × P] | 20 % (10–30 %) [P] | 70–90 % [P] | 14–28 + GDPR 5–10 min [P] | 2,83 USD (1,32–5,66) [P] | 15–30 min [P] |

**Čas modelu na získatelné záznamy ve světě, základní scénář** (bez koeficientů regionů z 3.4):

| Kategorie | Výpočet | Hodin |
|---|---|---|
| VC | 7 251 × 0,7 × 7,9 min [M] | 666 |
| PE | 9 812 × 1,15 min [M] | 188 |
| Family office | 4 015 × 0,15 × 21 min [P] | 211 |
| Angel investor | 197 000 × 0,1 × (21 + 7,5) min [P] | 9 358 |
| Velký soukromý investor | 62 600 × 0,2 × (21 + 7,5) min [P] | 5 947 |

**Náklady API na získatelné záznamy ve světě, základní scénář počtu** (bez koeficientů regionů z 3.4). Cena na záznam u kategorií mimo VC = měřená cena VC × poměr času modelu ke 7,9 min. Předpoklad [P] je, že tokeny rostou úměrně času modelu; u PE stojí na měřeném čase (n = 5), u family office, angelů a velkých soukromých investorů na předpokládaném čase.

| Kategorie | Záznamů | Poměr času k VC | USD na záznam (nízký / základní / vysoký) | API celkem, USD (nízký / základní / vysoký) |
|---|---|---|---|---|
| VC | 5 076 [Z+M] | 1,00 [M] | 0,36 / 0,78 / 1,56 [M] | 1 851 / 3 966 / 7 933 |
| PE | 9 812 [Z+P] | 0,15 [M] | 0,05 / 0,11 / 0,23 [M+P] | 523 / 1 120 / 2 240 |
| Family office | 602 [Z×P] | 2,67 [P] | 0,97 / 2,08 / 4,17 [P] | 586 / 1 255 / 2 511 |
| Angel investor | 19 700 [P] | 3,62 [P] | 1,32 / 2,83 / 5,66 [P] | 26 009 / 55 733 / 111 465 |
| Velký soukromý investor | 12 520 [Z×P] | 3,62 [P] | 1,32 / 2,83 / 5,66 [P] | 16 529 / 35 420 / 70 840 |
| **Celkem** | 47 710 | | | **45 497 / 97 494 / 194 988** |

Angelé a velcí soukromí investoři tvoří 94 % nákladu na API, ale jejich počty i čas na záznam jsou předpoklady. Spolehlivé jsou jen řádky VC a PE.

**Jak číst výsledek:**

- **VC a PE** stojí na měření a zdrojích. Rozdíl mezi nízkým a vysokým scénářem je do dvojnásobku.
- **Family office, angelé a velcí soukromí investoři** mají rozpětí v řádech. Většina vstupů je předpoklad [P].
- U fyzických osob převažují náklady na GDPR a ruční kontrolu nad časem modelu.
- Před rozšířením na tyto kategorie je potřeba nejdřív ověřit předpoklady sondou o 25 záznamech na kategorii.
