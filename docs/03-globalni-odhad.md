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
