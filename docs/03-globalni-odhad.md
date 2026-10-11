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
| P1 | Pilot ČR ([04-rucni-kontrola.md](04-rucni-kontrola.md)) | vlastní měření | 16 ověřených VC, 4 kandidáti. Capture–recapture (Chapman) 7–25, jde o dolní mez. 17 subjektů vyloučeno jako PE. | Jedna země, 52 nalezených subjektů. | ruční kontrola R1 |
| P2 | [CVCA, řádní členové](https://cvca.cz/en/category/full-members/) (průchod s-002) | asociace | 27 řádných členů (PE a VC) | Stav 9. 10. 2026 | surový text stránky |

**SEC exempt reporting advisers (IAPD).** Počet poradců, kteří se opírají o výjimku pro VC fondy, se nepodařilo zjistit. sec.gov surovému stahování vrátil HTTP 403 a ochranu jsme neobcházeli podvrženou hlavičkou User-Agent, takže počet zůstává **neznámý**. Pro škálování jde o klíčový zdroj. Dalším krokem je zjistit podmínky strojového přístupu SEC a data stahovat v souladu s nimi.

**Národní registry.** Pilot ukázal, že rejstřík ČNB (JERRS) je za CAPTCHA a or.justice.cz zakazuje cestu `/ias/` v robots.txt. Použitelný byl až ARES (REST API). Dostupnost národních registrů se proto musí posoudit země po zemi a v odhadu se počítá s koeficientem obtížnosti (3.4).

## 3.2 Co z pilotu plyne pro odhad

- **Registry regulátorů VC podhodnocují.** V ČR je 16 ověřených VC, ale v registru EuVECA žádný. Opt-in registr tedy není použitelný jako výčet trhu, poslouží jen jako zdroj kandidátů a dolní mez.
- **Asociace mísí PE a VC.** V pilotu připadlo na 20 VC subjektů (16 ověřených a 4 kandidáti) 17 subjektů vyloučených jako PE, podíl VC tedy vychází 48–54 %. Odtud plyne předpoklad podílu VC mezi firmami PE a VC v Evropě 0,4–0,6.
- **Trychtýř:** na jednoho ověřeného investora připadá 52 / 16 = 3,25 zpracovaného subjektu.
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
- precision **15/15 = 100 %** (95% Wilsonův interval 79,6–100 %);
- přesnost faktů **32/34 = 94,1 %** (80,9–98,4 %), pesimisticky 88,9 %.

Hodnoty pro ostatní regiony jsou **předpoklady**, které je nutné změřit ruční kontrolou vzorku v každém regionu.

| Úroveň | Regiony | Dostupnost zdrojů | Očekávaná přesnost faktů (předpoklad) | Koeficient obtížnosti (předpoklad) |
|---|---|---|---|---|
| 1 | USA, UK, Kanada, Austrálie | Angličtina, data SEC (strojový přístup je třeba vyřešit), silné asociace a média; dostupnost firemních registrů v pilotu neověřena | jako pilot, 90–98 % | 1,0–1,3 |
| 2 | EU a EHP | Registr ESMA (API), národní registry s různou dostupností (CAPTCHA, robots.txt), více jazyků | 85–95 % | 1,0–1,5 |
| 3 | Asie, Izrael, Latinská Amerika, Blízký východ, Afrika | Místní jazyky a písma, registry často placené nebo bez API, méně médií | 75–90 % | 2,0–3,0 |

Precision ve smyslu „ověřený záznam je skutečně aktivní VC“ byla v pilotu vysoká, protože se zařazovalo jen s primárním dokladem (ARES). Kde takový registr chybí (úroveň 3), přibude kandidátů. V pilotu skončilo jako kandidát 4 z 20 VC subjektů, tedy 20 %.

## 3.5 Náklady škálování

### Naměřené vstupy z pilotu

| Vstup | Hodnota | Zdroj |
|---|---|---|
| Čas modelu na ověřeného investora (hledání, triáž, ověření) | (5,6 + 0,7 + 80,1) min / 16 = **5,4 min** | `effort_log.csv`, `search_log.csv` |
| Čas člověka na kontrolu investora | **15,5 min** | `reviews.csv` (první kontrola) |
| Čas člověka na kontrolu faktu | **0,96 min** | `fact_reviews.csv` |
| Vzorek na region | 25 investorů a 36 faktů (±15 p. b.) | Cochran, viz [04-rucni-kontrola.md](04-rucni-kontrola.md) |

Čas modelu je čas běhu nástrojů včetně čekání na stránky a omezení rychlosti. Spotřebu tokenů pilot neměřil.

### Výpočet

**Model.** Počet investorů × 5,4 min × koeficient regionu (USA 1,0–1,3, Evropa 1,0–1,5, zbytek světa 2,0–3,0):

| Scénář | Investorů | Čas modelu, první sběr | Roční aktualizace (**předpoklad** 50–100 % prvního sběru) |
|---|---|---|---|
| Nízký | 5 235 | 562–790 h | 281–790 h |
| Základní | 7 251 | 897–1 292 h | 449–1 292 h |
| Vysoký | 9 682 | 1 307–1 907 h | 654–1 907 h |

Čas běhu jde paralelizovat mezi domény. Omezení rychlosti platí pro každou doménu zvlášť, celková doba sběru tedy závisí na počtu souběžných pracovníků, ne na součtu hodin.

**API modelu (předpoklad).** Odhad počítá se 100 000–400 000 tokenů na ověřeného investora a cenou 3–15 USD za milion tokenů. Pilot tokeny neměřil, proto jde o předpoklad, který je při škálování třeba měřit. Vychází to na 0,30–6 USD na investora:

| Scénář | API, první sběr |
|---|---|
| Nízký | 1 571–31 410 USD |
| Základní | 2 175–43 506 USD |
| Vysoký | 2 905–58 092 USD |

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

Každé číslo je buď ze zdroje (E1–E10, G1–G7, P1–P2), nebo je označeno jako **předpoklad**. „Získatelné z veřejných zdrojů“ znamená záznam, který lze doložit podle pravidel kategorie ([01](01-plan-a-kriteria.md), 1.10). Neznamená to, že bude mít vyplněná všechna pole zadání.

### VC (změřeno v pilotu)

| | Nízký | Základní | Vysoký | Zdroj |
|---|---|---|---|---|
| Svět, počet firem | 5 235 | 7 251 | 9 682 | 3.3 |
| ČR | 16 | 20 | 25 | 16 ověřených, 16 + 4 kandidáti, horní mez Chapmanova intervalu (P1) |
| Získatelné z veřejných zdrojů | 80 % | 80 % | 80 % | pilot: 16 ověřených z 20 VC subjektů, 4 kandidáti |

**Spolehlivost (změřeno):**

- precision 15/15;
- přesnost faktů – vzorek 32/34, přísně 88,9 %;
- přesnost faktů – doplňování 42/44, přísně 85,7 %;
- opravy 7/7.

Pole zadání: sektor 15/16, ticket 14/16, kapitál 13/16.

**Náklady (změřeno):** model 5,4 min na ověřeného investora. Člověk 15,5 min na kontrolu investora a 0,82–0,96 min na fakt.

### PE (změřeno v mini-pilotu, n = 5)

| | Nízký | Základní | Vysoký | Zdroj nebo předpoklad |
|---|---|---|---|---|
| USA | 6 000 | 6 000 | 6 000 | E1 |
| Evropa: firmy PE a VC × podíl PE | 3 095 × 0,4 = 1 238 | × 0,5 = 1 548 | × 0,6 = 1 857 | G3; podíl PE = 1 − podíl VC (3.3, **předpoklad** z pilotu) |
| Zbytek světa | – | 0,3 × (USA + Evropa) | 0,6 × (USA + Evropa) | **předpoklad**, bez zdroje |
| **Svět celkem** | **7 000** | **9 812** | **12 571** | Nízký = celosvětové číslo z E1. Je menší než součet USA a Evropy, protože definice zdrojů se liší. |
| ČR – skuteční PE investoři aktivní v ČR | 17 | 22 | 27 | 17 PE členů CVCA (E2), pravost 5/5; základní a vysoký scénář přičítají nečleny CVCA +30 %, resp. +60 % (**předpoklad**) |
| ČR – s českou právnickou osobou | 3 | 9 | 16 | 17 × podíl s českou entitou 0,2 / 0,4 / 0,6 (pilot 2/5, malý vzorek), × 1,0 / 1,3 / 1,6 za nečleny (**předpoklad**) |
| Získatelné z veřejných zdrojů | pravost 5/5, v zemi pilotu 2/5 | | | E2 |

**Spolehlivost:**

- Pravost 5/5.
- Ruční kontrola PE od R1 v době zápisu ještě není v `reviews.csv`, výsledek proto chybí.
- Přesnost faktů se očekává jako u VC, 85–95 % (**předpoklad**: stejná metodika).
- Ticket se mezi webem a CVCA rozchází u 3/5, takže u pole „typická výše“ je spolehlivost nižší.
- Pole zadání: sektor 5/5 a ticket 5/5. Získaný kapitál podle přísné definice má jen 1/5, nějaký údaj o kapitálu 5/5.

**Náklady:** model **1,0 min** na subjekt (změřeno, n = 5, bez hledání kandidátů, seznam pochází z CVCA). Pro hledání se přičítá 0,4 min jako u VC ((5,6 + 0,7) / 16). Čas člověka zatím změřen není, počítá se jako u VC 15,5 min (**předpoklad**).

### Family office

| | Nízký | Základní | Vysoký | Zdroj nebo předpoklad |
|---|---|---|---|---|
| Svět, single-family office | 8 030 | 8 030 | 10 720 | E3; vysoký scénář = projekce Deloitte pro rok 2030 jako horní mez |
| z toho Evropa | 2 020 | 2 020 | – | E4 |
| Svět – přímí investoři do firem (v rozsahu databáze) | 8 030 × 0,3 = 2 409 | 8 030 × 0,5 = 4 015 | 10 720 × 0,7 = 7 504 | Podíl přímých investorů je **předpoklad**. Sonda ukázala investice přes fondy jako LP (1/5) i poskytovatele služeb (2/5). |
| ČR – family office celkem | 10 | 30 | 60 | **předpoklad**; žádný zdroj počet neuvádí |
| ČR – přímí investoři | 3 | 15 | 42 | ČR × stejný podíl |
| Získatelné z veřejných zdrojů | 0 % | 15 % | 30 % | Sonda 0/5 `overeny`, 3/5 kandidáti; **předpoklad**, že část kandidátů doloží hlubší hledání |

**Spolehlivost (předpoklad):** přesnost faktů 70–90 %. Hlavním rizikem je klasifikace (vlastní, nebo cizí kapitál; přímá investice, nebo LP). Stejný typ chyby převažoval v kole `po_doplneni` (6/7 nálezů). Pole zadání: kapitál 0/5 v sondě, sektor a výše zřídka.

**Náklady (předpoklad):** model 2–4× VC, tedy 11–22 min na záznam, protože chybí registr a seznam kandidátů. Člověk 15–30 min.

### Angel investoři

| | Nízký | Základní | Vysoký | Zdroj nebo předpoklad |
|---|---|---|---|---|
| Evropa – aktivní angelé v sítích | 39 400 | 39 400 | 39 400 | E5 (jen organizovaní v sítích, skutečný počet je vyšší) |
| Svět | 118 200 | 197 000 | 394 000 | **Předpoklad**: Evropa × 3 / 5 / 10. Údaj za USA nebyl ověřen (3.7). |
| ČR – angelé celkem | 100 | 300 | 1 000 | **předpoklad**; žádný zdroj počet neuvádí, Světová banka (2018) popisuje málo sítí a koncentraci u „super angels“ |
| ČR – sami se veřejně prezentují (A1) | 7 | 30 | 100 | Nízký = 7 fyzických osob v databázi CBAA (E6); ostatní **předpoklad** |
| Svět – získatelné z veřejných zdrojů | 5 % | 10 % | 20 % | **předpoklad**; jen osoby s vlastním zveřejněním a doloženou investicí |

**Spolehlivost (předpoklad):** 80–95 % u identity a investice, pokud stojí na vlastním zveřejnění. Pole zadání: sektor a ticket 2/11 profilů v CBAA, kapitál se neukládá.

**Náklady (předpoklad):** model 11–22 min na záznam. Člověk 15–30 min. Navíc informační povinnost podle čl. 14 GDPR: 5–10 min na osobu na oznámení a evidenci námitek.

**Omezení:** CBAA záměrně brání indexaci seznamu členů (1.12). Sběr proto vyžaduje dohodu nebo souhlas a odhad počítá s nízkým podílem.

### Velcí soukromí investoři

| | Nízký | Základní | Vysoký | Zdroj nebo předpoklad |
|---|---|---|---|---|
| Svět – UHNWI (majetek nad 30 mil. USD) | 626 000 | 626 000 | 626 000 | E7 |
| Svět – přímí investoři do firem | 31 300 | 62 600 | 125 200 | Podíl 5 / 10 / 20 % je **předpoklad** |
| ČR – UHNWI | 210 | 210 | 210 | E8 (odvozený odhad z roku 2015); dolaroví milionáři 32 200 (E9) |
| ČR – přímí investoři | 11 | 21 | 42 | stejný podíl (**předpoklad**) |
| Získatelné z veřejných zdrojů (holding s doloženými investicemi) | 10 % | 20 % | 30 % | **předpoklad**; evidence skutečných majitelů je uzavřena, Sbírka listin jen ručně |

Kategorie se částečně překrývá s family office. Část UHNWI investuje přes vlastní kanceláře, takže součet obou kategorií by počítal některé subjekty dvakrát.

**Spolehlivost (předpoklad):** 70–90 %. Vazba osoby na holding se dokládá jen vlastním zveřejněním.

**Náklady (předpoklad):** model 11–22 min, člověk 15–30 min a GDPR jako u angelů.

### Souhrnná tabulka (základní scénář, v závorce nízký – vysoký)

| Kategorie | ČR | Svět | Získatelné z veřejných zdrojů | Spolehlivost | Model na záznam | Člověk na kontrolu záznamu |
|---|---|---|---|---|---|---|
| VC | 20 (16–25) | 7 251 (5 235–9 682) | 80 % (změřeno) | precision 15/15; fakta 94,1 %, přísně 85,7–88,9 % (změřeno) | 5,4 min (změřeno) | 15,5 min (změřeno) |
| PE | 9 (3–16) s českou entitou; 22 (17–27) aktivních v ČR | 9 812 (7 000–12 571) | pravost 5/5, v zemi pilotu 2/5 (změřeno, n = 5) | kontrola R1 chybí; fakta 85–95 % (předpoklad) | 1,0 min + 0,4 min hledání (změřeno, n = 5) | 15,5 min (předpoklad) |
| Family office | 15 (3–42) přímých investorů | 4 015 (2 409–7 504) přímých investorů | 15 % (0–30 %; sonda 0/5) | 70–90 % (předpoklad) | 11–22 min (předpoklad) | 15–30 min (předpoklad) |
| Angel investor | 30 (7–100) s vlastním zveřejněním | 197 000 (118 200–394 000), z toho získatelné 10 % (5–20 %) | 10 % (předpoklad) | 80–95 % (předpoklad) | 11–22 min + GDPR 5–10 min (předpoklad) | 15–30 min (předpoklad) |
| Velký soukromý investor | 21 (11–42) | 62 600 (31 300–125 200) | 20 % (10–30 %) | 70–90 % (předpoklad) | 11–22 min + GDPR 5–10 min (předpoklad) | 15–30 min (předpoklad) |

**Čas modelu na získatelné záznamy ve světě, základní scénář** (počet × čas na záznam, bez koeficientů regionů z 3.4):

| Kategorie | Výpočet | Hodin |
|---|---|---|
| VC | 7 251 × 0,8 × 5,4 min | 522 |
| PE | 9 812 × 1,4 min | 229 |
| Family office | 4 015 × 0,15 × 16,5 min | 166 |
| Angel investor | 197 000 × 0,1 × (16,5 + 7,5) min | 7 880 |
| Velký soukromý investor | 62 600 × 0,2 × (16,5 + 7,5) min | 5 008 |

U PE je celý počet, protože pravost byla 5/5 a záznam se vede v zemi sídla.

**Jak číst výsledek:**

- **VC a PE** jsou dobře proveditelné: existují seznamy a registry a pole zadání jsou dostupná. Rozdíl mezi nízkým a vysokým scénářem je do dvojnásobku.
- **Family office, angelé a velcí soukromí investoři** mají rozpětí v řádech. Většina vstupů je předpoklad a podíl získatelných záznamů je nízký.
- U fyzických osob převažují náklady na GDPR a ruční kontrolu nad časem modelu.
- Před rozšířením na tyto kategorie je potřeba nejdřív ověřit předpoklady **sondou o 25 záznamech na kategorii**, stejně velkou jako regionální vzorek v 3.5.
