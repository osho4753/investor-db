# 1. Plán výzkumu a kritéria zařazení/vyloučení

## 1.1 Cíl

Vytvořit reprodukovatelný proces, který z bezplatných veřejných zdrojů najde, klasifikuje a ověří reálné investory. Měřítkem úspěchu je **spolehlivost** dat (precision, doložitelnost jednotlivých faktů), nikoli počet záznamů.

Pilot ověřuje proces na malém, ručně zkontrolovatelném vzorku **20–30 kandidátů** z jedné země a jednoho typu investora. Výsledky pilotu (precision, čas na záznam, dostupnost zdrojů) slouží jako vstup pro odhad globálního škálování.

## 1.2 Rozsah pilotu

| Dimenze | Rozhodnutí |
|---|---|
| Země | Česká republika |
| Typ investora | Venture kapitál (VC) |
| Jednotka záznamu | VC značka / investiční tým, který rozhoduje o investicích |
| Zdroje | Pouze bezplatné veřejné zdroje |
| Velikost | 20–30 kandidátů |

### Jednotka záznamu: VC značka, ne právní správce

Jeden záznam v `data/investors.csv` odpovídá **VC značce nebo týmu, který rozhoduje o investicích**. V ČR mnoho VC fondů formálně spravuje licencovaný třetí správce (tzv. white-label správce), takže v seznamech ČNB často figuruje právní správce, a ne samotná VC značka. Kdyby záznamem byl právní správce, jeden správce by sdružoval mnoho nesouvisejících investičních strategií a výsledná data by neodpovídala tomu, kdo skutečně investuje.

Právní správce či administrátor fondu se proto ukládá jako **fakt** (`pravni_spravce` v `data/facts.csv`), nikoli jako samostatný investor.

### Proč Česká republika

Výběr země je zdůvodněn dostupností bezplatných veřejných zdrojů a možností ruční kontroly:

- **Obchodní rejstřík a Sbírka listin** jsou veřejně a bezplatně dostupné online; sbírka listin obsahuje mimo jiné výroční zprávy a účetní závěrky, ze kterých lze doložit údaje o fondech. Webové rozhraní or.justice.cz však podle svého `robots.txt` automatizovaný přístup k cestě `/ias/` zakazuje; údaje rejstříku se proto čerpají z ARES.
- **ARES** poskytuje bezplatný přístup k identifikačním údajům právnických osob podle IČO.
- **Česká národní banka** zveřejňuje seznamy regulovaných subjektů včetně správců investičních fondů.
- Existuje národní asociace soukromého a rizikového kapitálu se seznamem členů.
- Trh je dost malý na to, aby pilot mohl pokrýt podstatnou část VC investorů, a zároveň dost velký na 20–30 kandidátů.
- Zadavatel ovládá jazyk zdrojů, takže je možná nezávislá ruční kontrola.

Skutečná dostupnost a užitečnost každého zdroje se ověřuje a zaznamenává při sběru dat v `data/search_log.csv`; tvrzení výše jsou do té doby **předpoklady**.

### Proč pouze VC

| Typ | Rozhodnutí | Zdůvodnění |
|---|---|---|
| VC fondy | **Zařazeny** | Mají právní formu a regulatorní stopu (rejstřík, ČNB, výroční zprávy) a veřejně komunikují portfolio – lze je doložit. |
| Business angels | Vyloučeny | Jde o fyzické osoby: zpracování jejich údajů naráží na GDPR a veřejná doložitelnost investic je slabá. |
| Family offices | Vyloučeny | Nemají povinnost zveřejňovat a veřejných dat je málo. |
| PE fondy | Vyloučeny, **budoucí rozšíření** | Metodicky odlišné (většinové podíly, buyout); smíchání s VC by rozmazalo definici. Evidují se jako vyloučené s důvodem `pe_budouci_rozsireni`. |
| Corporate VC (více než 50 % kapitálu fondu od jedné korporátní skupiny) | Vyloučeny, budoucí rozšíření | Investují převážně kapitál korporace; hranice vůči strategickým akvizicím je nejasná. Není-li rozložení kapitálu doloženo, zůstávají kandidáty. Důvod `cvc`. |
| Fondy fondů | Vyloučeny, budoucí rozšíření | Investují do fondů, ne přímo do firem; jejich zařazení by vedlo k dvojímu započtení kapitálu. Důvod `fond_fondu`. |
| Státní fondy a rozvojové instituce | Vyloučeny, budoucí rozšíření | Kombinují veřejné politiky, dotace a nástroje fondů fondů; vyžadují vlastní definici. Důvod `statni_fond`. |
| Dluhové fondy (direct lending, mezanin, venture debt jako hlavní strategie) | Vyloučeny, budoucí rozšíření | Poskytují úvěr, ne kapitál za podíl; patří do jiné kategorie investorů. Důvod `dluhovy_fond`. |
| Fondy digitálních aktiv a otevřené smíšené fondy | Vyloučeny | Nekupují (výhradně) podíly v nekótovaných firmách; jde o jinou třídu aktiv. Důvod `digitalni_aktiva`, resp. `otevreny_smiseny_fond`. |
| Zahraniční VC bez české právnické osoby | Vyloučeny, budoucí rozšíření | Nelze je doložit z českých registrů; patří do pilotu své domovské země. Důvod `zahranicni_subjekt`. |

Vyloučení platí pro **VC pilot**. Plán pro ostatní kategorie (PE, family office, angel investoři, velcí soukromí investoři) je v 1.10. PE je ověřeno mini-pilotem v 1.11.

## 1.3 Kritéria zařazení

Záznam může mít status `overeny`, jen pokud platí **všechna** kritéria a každé je doloženo faktem:

| Kód | Kritérium | Jak se dokládá |
|---|---|---|
| Z1 | VC značka má **českou právnickou osobu s IČO** – správcovskou společnost, poradenskou společnost nebo samotný fond. | Fakt `registry_id` z primárního zdroje (rejstřík, ARES, ČNB). |
| Z2 | Převažující strategií je **rizikový kapitál**: menšinové podíly v nekótovaných firmách ve fázích pre-seed až growth. | Popis strategie ve zdroji (web investora, výroční zpráva, profil v asociaci, médium) a `investor_type` `vc`. Doplňková pole `investment_stages` a `investment_sectors` nejsou povinná a nejsou podmínkou zařazení. |
| Z3 | Značka investuje prostřednictvím **alespoň jednoho fondu nebo vehiklu s kapitálem třetích osob**. | Alespoň jeden fakt s vyplněným `fund_name` (např. velikost fondu, právní správce, registrace u regulátora). |
| Z4 | Značka je **aktivní**: alespoň jedna doložená investice nebo nový fond za posledních 36 měsíců. | Fakt `dolozena_investice`, nebo fondový fakt (`informace_o_fondu`, `total_fund_size`, `cilova_velikost_fondu`) s `value_as_of` nejvýše 36 měsíců před `last_verified_at`. |

Hranice 36 měsíců je **předpoklad**: odpovídá typické investiční periodě, kdy VC fond aktivně vybírá nové investice. Lze ji změnit v `investor_db/schema.py`.

## 1.4 Kritéria vyloučení

Subjekt je vyloučen (`vyloucen`) s jedním z těchto důvodů (`exclusion_reason`):

| Kód | Význam |
|---|---|
| `cvc` | Corporate VC: více než 50 % kapitálu fondu pochází od jedné korporátní skupiny (pravidlo viz [02-metodika.md](02-metodika.md)). |
| `fond_fondu` | Fond fondů: investuje do jiných fondů, ne přímo do firem. |
| `statni_fond` | Státní fond, státní program nebo rozvojová instituce financovaná z veřejných prostředků. |
| `dluhovy_fond` | Dluhový fond: hlavní strategií jsou úvěry, mezanin nebo venture debt, ne kapitál za podíl. |
| `digitalni_aktiva` | Fond digitálních aktiv (tokeny, protokoly, kryptoměny), který nekupuje podíly ve firmách. |
| `otevreny_smiseny_fond` | Otevřený smíšený fond s průběžnou likviditou, který kombinuje podíly ve firmách s kotovanými akciemi. |
| `zahranicni_subjekt` | Zahraniční investor bez české právnické osoby. |
| `pe_budouci_rozsireni` | Private equity s převažujícími většinovými podíly; kandidát pro budoucí rozšíření. |
| `business_angel` | Business angel nebo angel síť. |
| `family_office` | Family office. |
| `bez_fondu` | Akcelerátor, inkubátor, crowdfundingová platforma nebo program bez fondu s kapitálem třetích osob. Akcelerátor, který investuje přes vehikl s kapitálem třetích osob, do pilotu patří a ověřuje se podle Z1–Z4. |
| `neaktivni` | Žádná doložená investice za posledních 36 měsíců. |
| `zanikly_subjekt` | Subjekt zanikl nebo je v likvidaci. |
| `duplicita` | Duplicitní záznam jiného investora. |

Vyloučené subjekty zůstávají v datech, aby bylo zřejmé, co bylo posouzeno a proč nebylo zařazeno. Kódy jsou konkrétní, aby hodnotitel u faktu `duvod_vylouceni` věděl, který znak má ve zdroji hledat. Dřívější souhrnný kód `mimo_definici_pilotu` byl rozdělen na kódy `cvc` až `otevreny_smiseny_fond` (viz [02-metodika.md](02-metodika.md), Incidenty a poučení) a validátor ho odmítá. Důvod vyloučení musí být doložen alespoň jedním faktem `duvod_vylouceni` se zdrojem (např. stránka, ze které plyne, že jde o corporate VC nebo zahraniční subjekt); kontroluje to validátor.

### Hraniční případy (rozhodnutí zadavatele)

| Subjekt | Rozhodnutí | Zdůvodnění |
|---|---|---|
| Impulse Ventures, Patero | `vyloucen`, `bez_fondu` | Investují vlastní kapitál zakladatelů či společníků bez fondu a bez kapitálu třetích osob (Impulse podle článku z roku 2020, Patero s.r.o. podle ARES s pěti fyzickými osobami po 20 %). Patero bylo nejdřív zařazeno jako `business_angel`, sjednoceno s Impulse. Chybí fond (Z3). |
| Orbit Capital | `vyloucen`, `dluhovy_fond` | Nejnovější fond je dluhový (venture debt), profil CVCA uvádí i growth equity. Kandidát pro budoucí rozšíření definice o venture debt. |
| Springtide Ventures | `vyloucen`, `cvc` | Bez cizích peněz, kapitál od skupiny KKCG (Forbes 2018). |
| StartupYard | `overeny` | Akcelerátor, který investuje přes vehikl s kapitálem třetích osob. |
| Zaka VC | `vyloucen`, `family_office` | Kapitál třetích osob není doložen. |
| Inven Capital | `kandidat` | Vazba na ČEZ doložena, podíl ČEZ na kapitálu fondu nad 50 % ne (pravidlo CVC). |
| J&T Ventures | `kandidat` | J&T banka je podle webu fondu institucionálním investorem bez zvláštních práv, podíl neuveden (pravidlo CVC). Do 11. 10. 2026 `overeny`. |

## 1.5 Dvě úrovně zpracování a trychtýř

Po hledání se každý nalezený subjekt zpracuje jednou ze dvou úrovní:

| Úroveň | Pro koho | Co se dělá | Záznam v `effort_log.csv` |
|---|---|---|---|
| Rychlá triáž | Subjekty, které už podle zdroje hledání zjevně spadají pod důvod vyloučení (např. PE podle typu investic na webu asociace) | Jeden doložený fakt `duvod_vylouceni`, status `vyloucen` | `triaz` |
| Plné ověření | VC kandidáti a nejasné subjekty | Doložení Z1–Z4 a dalších polí; výsledkem je `overeny`, `kandidat` nebo `vyloucen` | `overeni` |

Trychtýř (nalezeno → triáž → ověřeno/vyloučeno) se počítá z `investors.csv` a `effort_log.csv` příkazem `python -m investor_db metrics`. Čas obou úrovní se měří zvlášť, aby odhad nákladů škálování mohl odlišit levnou triáž od drahého ověření.

## 1.6 Statusy

| Status | Kód | Podmínka |
|---|---|---|
| Ověřený investor | `overeny` | Platí Z1–Z4 a všechna vyplněná pole mají podpůrný fakt. Kontroluje validační skript. |
| Kandidát k dalšímu ověření | `kandidat` | Pravděpodobně splňuje kritéria, ale chybí důkaz pro některé z Z1–Z4. |
| Vyloučený subjekt | `vyloucen` | Spadá pod některý důvod vyloučení. |

Status nastavuje ten, kdo sbírá data. Ruční kontrola (viz `docs/04-rucni-kontrola.md`) pak nezávisle měří, zda byl status `overeny` přidělen správně – to je základ výpočtu precision.

## 1.7 Kritéria dokončení projektu

1. `python -m investor_db validate` projde bez chyb.
2. `python -m pytest` projde; každé validační pravidlo má pozitivní i negativní test.
3. Pilot obsahuje 20–30 posouzených subjektů; vyloučené mají důvod.
4. Každá vyplněná hodnota v `data/investors.csv` má podpůrný fakt se zdrojem, datem přístupu a popisem důkazu.
5. Ruční kontrolu vyplnil R1 (zadavatel), volitelně R2 (nezávislý hodnotitel); precision a další metriky se počítají skriptem reprodukovatelně.
6. Dokumentace pokrývá povinné výstupy 1–7 včetně předpokladů a rozsahu nejistoty.
7. Historie Gitu obsahuje malé logické commity; `ai-log/` obsahuje exporty dialogů.

## 1.8 Plán postupu

1. Kostra repozitáře, dokumentace kritérií a metodiky.
2. Datové schéma, validace a metriky včetně testů (bez reálných dat).
3. **Schválení zadavatelem před sběrem dat.**
4. Vyhledání kandidátů a protokol hledání (`search_log.csv`).
5. Ověření faktů a přidělení statusů.
6. **Ruční kontrola** záznamů a vzorku faktů (R1, volitelně R2).
7. Výpočet metrik, vyhodnocení a odhad globálního škálování.

## 1.9 Fakta, předpoklady a otevřené otázky

**Rozhodnutí zadavatele:** rozsah pilotu (VC, ČR), jednotka záznamu (VC značka), vyloučení CVC, fondů fondů, státních fondů a zahraničních subjektů, jedna měna na řádek bez přepočtů, ASCII kódy ve slovnících, ruční kontrola R1 povinně a R2 volitelně.

**Předpoklady:** dostupnost a obsah českých zdrojů uvedených v 1.2; dostatečný počet VC značek v ČR pro 20–30 kandidátů; hranice aktivity 36 měsíců; hranice aktuálnosti ověření 12 měsíců.

**Otevřené otázky:** řízené slovníky sektorů a fází se mohou při sběru dat ukázat jako nedostatečné – případná úprava proběhne samostatným commitem se zdůvodněním.

## 1.10 Plán pro všechny kategorie investorů

Zadání chce databázi VC fondů, private equity, family office, angel investorů a velkých soukromých investorů. Pilot (1.2–1.9) do hloubky zpracoval jen VC. Tento oddíl doplňuje plán pro ostatní kategorie: definici, pravidla zařazení a vyloučení, ověření, veřejné zdroje a dostupnost polí, která zadání žádá. PE je ověřeno mini-pilotem (1.11). Family office, angel a velcí soukromí investoři mají jen studii proveditelnosti ([03-globalni-odhad.md](03-globalni-odhad.md)) a data se o nich zatím nesbírají.

Zdroje v tomto oddílu byly otevřeny 12. 10. 2026. Pokud tvrzení stojí na vlastní úvaze, a ne na zdroji, je označeno jako **předpoklad**.

### Společná pravidla pro všechny kategorie

- Jednotkou záznamu je **subjekt, který rozhoduje o investici vlastních nebo svěřených peněz**. U fondů je to značka nebo tým (jako u VC), u fyzických osob osoba sama, případně její investiční vehikl.
- Platí pravidla dokládání z pilotu: každý údaj má fakt se zdrojem, datem přístupu a popisem důkazu, primární zdroje mají přednost a agregátory slouží jen jako vodítko.
- Kategorie se zapisuje do `investor_type` (`pe`, `family_office`, `business_angel`, `jiny` pro velkého soukromého investora). Status se posuzuje **podle pravidel dané kategorie**. Záznam vyloučený z VC pilotu (např. `pe_budouci_rozsireni`) tím nemění svůj VC status. Hodnocení v jiné kategorii se ukládá zvlášť (1.11).
- Aktivita: doložená investice nebo nový fond za posledních 36 měsíců. U všech kategorií jde o **předpoklad** převzatý z VC.
- Hraniční případy mezi kategoriemi se rozhodují podle toho, **čí peníze** subjekt investuje a **jakou formou**:

| Znak | Kategorie |
|---|---|
| Fond s kapitálem třetích osob, menšinové podíly v rané fázi | VC |
| Fond s kapitálem třetích osob, většinové nebo významné podíly ve zralých firmách (buyout, growth, recapitalization) | PE |
| Vlastní kapitál jedné nebo několika rodin spravovaný vlastní organizací (kancelář, holding) | family office |
| Vlastní peníze fyzické osoby, přímo nebo přes syndikát či angel síť, převážně raná fáze | angel |
| Vlastní peníze fyzické osoby přes vlastní holding, bez kanceláře, větší tikety nebo pozdější fáze | velký soukromý investor |

### Private equity (PE)

**Definice.** Správce nebo poradce fondu, který z kapitálu třetích osob kupuje většinové nebo významné menšinové podíly v nekótovaných zralých firmách. Typické formy jsou buyout (LBO), growth a expansion kapitál a recapitalization. Profily členů CVCA uvádějí u PE typ investic například jako „Growth equity investments, buyouts or recapitalization“ (Stratum Partners) nebo „LBO, Growth capital“ (Thein) ([CVCA – full members](https://cvca.cz/en/category/full-members/)).

**Kritéria zařazení (obdoba Z1–Z4)** – status `overeny` v hodnocení PE vyžaduje všechna:

| Kód | Kritérium | Doklad |
|---|---|---|
| P1 | Česká právnická osoba s IČO (správce, poradce, fond nebo odštěpný závod zahraniční společnosti). | Fakt `registry_id` z ARES. |
| P2 | Převažující strategií je PE: buyout, growth nebo recapitalization ve zralých nekótovaných firmách, většinové nebo významné menšinové podíly. | Popis strategie na webu investora nebo v profilu asociace. |
| P3 | Investuje přes fond nebo vehikl s kapitálem třetích osob. | Fakt s `fund_name` (velikost fondu, správce, „Volume of Funds Managed“). |
| P4 | Aktivní: investice nebo nový fond za 36 měsíců. | `dolozena_investice` nebo fondový fakt s `value_as_of`. |

**Vyloučení v hodnocení PE.** Platí důvody vyloučení z 1.4 (`zahranicni_subjekt`, `fond_fondu`, `dluhovy_fond`, `cvc`, `neaktivni`, `zanikly_subjekt`, `family_office`). Přibývají dva:

- `vc_ne_pe`: převažuje rizikový kapitál v rané fázi, subjekt patří do VC;
- `realitni_fond`: převažují nemovitosti nebo infrastruktura, ne podíly ve firmách.

**Jak ověřit pravost a zařazení.** IČO a název z ARES. Strategie z vlastního webu (primární), profil CVCA je sekundární vodítko. Fond z webu, ze zprávy o uzavření fondu, ze seznamu ČNB nebo z registrů ESMA. Aktivita z tiskové zprávy o investici nebo exitu. Rozdíl PE a VC se posuzuje podle fáze a velikosti podílu, ne podle názvu („Capital“, „Partners“).

**Veřejné zdroje.**

| Oblast | Zdroj | Co dává | Omezení |
|---|---|---|---|
| ČR | [CVCA – full members](https://cvca.cz/en/category/full-members/) | Seznam PE a VC členů; v profilu objem spravovaných fondů, typ investic, preferovaná výše investice, sektory | Sekundární zdroj, vyplňuje člen sám, ne každý PE je členem |
| ČR | ARES | IČO, sídlo, vznik, statutární orgán | Bez finančních údajů |
| ČR | Seznam ČNB (JERRS) | Správci a fondy kvalifikovaných investorů | Za CAPTCHA, nástroji neprojde (s-004) |
| ČR | Sbírka listin (or.justice.cz) | Výroční zprávy fondů s velikostí a portfoliem | `robots.txt` zakazuje cestu `/ias/` (1.2), ručně dostupná |
| EU | Registry ESMA (EuVECA a další), národní regulátoři | Registrace správců a fondů | Jen část fondů, bez portfolia |
| Svět | [SEC – Form ADV data](https://www.sec.gov/data-research/sec-markets-data/information-about-registered-investment-advisers-exempt-reporting-advisers) | Měsíční soubory Form ADV (Items 1–11) za registrované a „exempt reporting“ poradce včetně soukromých fondů | Jen poradci s vazbou na USA; SEC správnost údajů negarantuje |
| Svět | Národní asociace (Invest Europe a členské asociace) | Seznamy členů, statistiky trhu | Členství dobrovolné |

**Dostupnost polí zadání (očekávaná, ověřuje mini-pilot 1.11).** Sektor: dobrá (web, CVCA). Typická investice a výše: dobrá, CVCA uvádí „Preferred Amount of Investment“, často jako výši equity. Celkový kapitál: dobrá, „Volume of Funds Managed“ v CVCA a zprávy o uzavření fondů, ovšem jako AUM nebo velikost fondu, s typy podle [02-metodika.md](02-metodika.md). Zdroj: vždy.

### Family office

**Definice.** Organizace, která spravuje a investuje majetek jedné rodiny (single-family office) nebo několika rodin (multi-family office). Investuje vlastní kapitál rodiny, ne kapitál cizích investorů. Pojem nemá v Česku právní definici ani přesný český ekvivalent ([e15, 31. 10. 2024](https://www.e15.cz/byznys/superholding-amalar-prevzal-skupinu-ppf-bohate-rodiny-v-cesku-nasedly-na-trend-rodinnych-kancelari-1417807)). V USA family office vymezuje pravidlo SEC 202(a)(11)(G)-1. Family office podle něj radí jen „family clients“, je jimi zcela vlastněn a ovládán a nevystupuje veřejně jako investiční poradce. Takový subjekt je z regulace Advisers Act vyňat a neregistruje se ([SEC, průvodce pravidlem](https://www.sec.gov/files/rules/final/2011/ia-3220-secg.htm)). Ve Form ADV ho proto nenajdeme.

**Kritéria zařazení:**

| Kód | Kritérium | Doklad |
|---|---|---|
| F1 | Právnická osoba s IČO (holding, s.r.o., a.s., fond kvalifikovaných investorů rodiny). | ARES |
| F2 | Spravuje vlastní kapitál rodiny, ne kapitál cizích klientů. | Vlastní prohlášení subjektu (web, výroční zpráva) nebo rozhovor se zástupcem; ARES jen u právnických osob ve vlastnické struktuře |
| F3 | Přímo investuje do podílů ve firmách, nejen do nemovitostí, kotovaných cenných papírů nebo vkladů. | Doložená investice (tisková zpráva, web) |
| F4 | Aktivní: investice za 36 měsíců. | `dolozena_investice` |

**Vyloučení:**

- multi-family office, který jen poskytuje služby správy majetku klientům a sám neinvestuje (`jiny`, poskytovatel služeb);
- privátní bankovnictví a správci aktiv;
- rodinné holdingy, které drží jen vlastní provozní firmy a nové investice nedělají (`neaktivni`);
- subjekt, který investuje kapitál třetích osob přes fond (to je VC nebo PE).

**Ověření pravosti a zařazení.** Rozhodující je F2. Označení „family office“ v médiích nestačí, protože ho používají i poradenské firmy. Pokud subjekt sám neuvádí, že spravuje majetek rodiny, zůstává `kandidat`.

**Veřejné zdroje.** Neexistuje registr ani asociace family office, která by zveřejňovala seznam (ČR: vyhledávání 12. 10. 2026 nenašlo; USA: family office jsou z registrace vyňaty, viz výše). Zbývají vlastní weby a tiskové zprávy, média (např. e15 o Amalar Holding), ARES a výroční zprávy holdingů ve Sbírce listin. Ty jsou dostupné ručně, ne automatizovaně.

**Dostupnost polí.** Sektor: částečně (portfolio ze zpráv o investicích). Typická výše investice: zřídka. Celkový kapitál: zřídka. Family office hodnotu spravovaných aktiv obvykle nezveřejňují. U Amalar Holding „celková hodnota spravovaných aktiv a akcií nebyla zveřejněna“ a médium uvádí jen vlastní odhad jmění rodiny (e15). Odhad jmění od třetí strany není kapitál family office a nezapisuje se. Zdroj: vždy.

### Angel investoři

**Definice.** Fyzická osoba, která investuje vlastní peníze do nekótovaných firem, převážně v rané fázi, přímo nebo přes syndikát či angel síť. Angel sítě a kluby jsou samostatné záznamy, pokud mají vlastní právnickou osobu.

**Kritéria zařazení:**

| Kód | Kritérium | Doklad |
|---|---|---|
| A1 | Osoba se **sama veřejně prezentuje** jako angel investor. | Profil v členské databázi angel asociace, vlastní web nebo profesní profil, rozhovor |
| A2 | Investuje vlastní peníze, ne jako zaměstnanec nebo partner fondu za fond. | Vlastní prohlášení nebo tisková zpráva cílové firmy |
| A3 | Aktivní: doložená investice za 36 měsíců. | Tisková zpráva firmy nebo vlastní zveřejnění osoby |

Angel síť nebo syndikát (právnická osoba) se ověřuje podle A2–A3 a navíc Z1 (IČO).

**Vyloučení:** osoba, která se jako investor veřejně neprezentuje (údaje jen ze zprávy třetí strany), osoba bez doložené investice, a crowdfundingová platforma (`bez_fondu`, platformy jsou v registru ESMA podle nařízení (EU) 2020/1503, [FMA – odkaz na registr ESMA](https://www.fma.gv.at/en/financial-service-providers/crowdfunding-service-providers/authorised-crowdfunding-services-providers-in-europe/)).

**Ověření.** Totožnost se ověřuje shodou jména napříč vlastním zveřejněním a zprávou o investici, ne z registrů fyzických osob. Pokud se shoda nedá potvrdit, záznam zůstává `kandidat`.

**Veřejné zdroje.**

| Oblast | Zdroj | Poznámka |
|---|---|---|
| ČR | [CBAA – Czech Business Angel Association](https://www.cbaa.cz/) | Národní asociace. Na webu zveřejňuje „databázi členů“ (sekce Členství), členové se zavazují etickým kodexem. |
| ČR | Angel sítě a kluby | Konkrétní sítě je třeba dohledat; viz studie v [03](03-globalni-odhad.md) |
| ČR | [Světová banka, 2018](https://blogs.worldbank.org/en/psd/how-can-czech-republic-activate-its-business-angels-market) | Analýza trhu: kapitál soustředěný u malého počtu „super angels“, v Praze a v ICT. Ve srovnání s vyspělými trhy „very little business angel networks or syndication“. |
| Evropa | EBAN (European Business Angels Network) | Statistiky trhu podle národních sítí (čísla v [03](03-globalni-odhad.md)) |
| Média | Tiskové zprávy o kolech | Uvádějí jména angelů jako spoluinvestorů |

**Dostupnost polí.** Sektor: částečně, pokud ho osoba sama uvádí. Typická výše investice: zřídka. Celkový kapitál: **neukládá se** (osobní majetek, viz GDPR). Zdroj: vždy.

### Velcí soukromí investoři

**Definice.** Fyzická osoba s velkým majetkem, která investuje vlastní peníze přímo do firem, obvykle přes vlastní investiční holding a bez samostatné kanceláře (jinak jde o family office). Větší tikety a pozdější fáze než u angelů.

**Jednotka záznamu.** Investiční **holding** jako právnická osoba, ne fyzická osoba. Osoba se k němu uvádí jen tehdy, když se sama veřejně prezentuje jako jeho vlastník nebo investor (rozhovor, vlastní web, výroční zpráva holdingu).

**Kritéria zařazení:**

| Kód | Kritérium | Doklad |
|---|---|---|
| S1 | Investiční vehikl s IČO. | ARES |
| S2 | Investuje vlastní kapitál jedné osoby, ne kapitál třetích osob. | Vlastní prohlášení, výroční zpráva |
| S3 | Doložené přímé investice do nekótovaných firem za 36 měsíců. | Tiskové zprávy, web holdingu |
| S4 | „Velký“: doložené investice nebo vlastní kapitál holdingu nad prahem. | Výroční zpráva nebo součet doložených investic; výše prahu je **předpoklad** k rozhodnutí zadavatele |

**Vyloučení:** holding, který drží jen vlastní provozní firmy (`neaktivni`); subjekt, který spravuje cizí kapitál (VC, PE); osoba, u níž by záznam stál jen na odhadu majetku z žebříčku třetí strany.

**Veřejné zdroje.** ARES a výroční zprávy holdingů ve Sbírce listin (ručně), tiskové zprávy o investicích, vlastní weby holdingů. Žebříčky nejbohatších slouží jen jako **vodítko** k hledání holdingů, nezapisují se. Evidenci skutečných majitelů nelze použít. Soudní dvůr EU v roce 2022 zrušil plošný přístup veřejnosti k registrům skutečných majitelů (věci C-37/20 a C-601/20). Ministerstvo spravedlnosti podle epravo.cz (23. 12. 2025) českou evidenci veřejnosti znepřístupní a přístup zůstane jen osobám s prokázaným oprávněným zájmem ([epravo.cz](https://www.epravo.cz/top/clanky/evidence-skutecnych-majitelu-se-uzavira-verejnosti-120450.html)).

**Dostupnost polí.** Sektor: částečně (z portfolia holdingu). Typická výše investice: zřídka, jen z jednotlivých zpráv o investicích. Celkový kapitál: částečně, jako vlastní kapitál holdingu z výroční zprávy (ne majetek osoby). Zdroj: vždy.

### Dostupnost polí zadání – souhrn

| Kategorie | Sektor | Typická investice a výše | Celkový kapitál | Zdroj |
|---|---|---|---|---|
| VC (pilot, změřeno) | 15/16 | 14/16 alespoň jedna mez | 13/16 (získaný nebo AUM) | 16/16 |
| PE | změří mini-pilot 1.11 | | | |
| Family office | částečně | zřídka | zřídka (hodnota aktiv se obvykle nezveřejňuje) | ano |
| Angel | částečně (jen vlastní zveřejnění) | zřídka | neukládá se | ano |
| Velký soukromý investor | částečně | zřídka | částečně (vlastní kapitál holdingu) | ano |

Hodnoty u family office, angelů a velkých soukromých investorů jsou **předpoklady** odvozené z popsaných zdrojů, ne měření. Studie proveditelnosti v [03](03-globalni-odhad.md) je upřesní.

### GDPR u fyzických osob (angel, velký soukromý investor)

Angel investoři a velcí soukromí investoři jsou fyzické osoby, takže jejich údaje jsou osobní údaje podle obecného nařízení (EU) 2016/679 (GDPR). Citace článků jsou z českého znění na [gdpr-text.com](https://gdpr-text.com/cs/read/article-6/). Jde o zrcadlo textu, závazné je znění v Úředním věstníku; EUR-Lex se 12. 10. 2026 nástroji nenačetl.

- **Právní základ: oprávněný zájem, čl. 6 odst. 1 písm. f).** Zpracování je možné, je-li „nezbytné pro účely oprávněných zájmů příslušného správce či třetí strany, kromě případů, kdy před těmito zájmy mají přednost zájmy nebo základní práva a svobody subjektu údajů“. Před sběrem je třeba sepsat test vyvážení (účel, nezbytnost, dopad na osobu). Souhlas jako základ nepřichází v úvahu, protože osoby se před zápisem neoslovují.
- **Minimalizace, čl. 5 odst. 1 písm. c).** Údaje musí být „přiměřené, relevantní a omezené na nezbytný rozsah ve vztahu k účelu“. Ukládá se jen to, co zadání žádá: jméno, jak ho osoba sama zveřejňuje, role (angel, vlastník holdingu), sektory, typická výše investice a doložené investice, pokud je osoba sama zveřejnila, a zdroj s datem přístupu.
- **Jen informace, které osoba sama zveřejnila.** Pravidlo zadavatele. Zdrojem údajů o osobě může být jen její vlastní zveřejnění (profil v databázi členů asociace, vlastní web, rozhovor, tisková zpráva, kterou spoluvydala). Zpráva třetí strany může doložit investici, ne další osobní údaje.
- **Zvláštní kategorie, čl. 9.** Politické názory, náboženství, zdraví a podobné údaje se neukládají vůbec. Výjimka čl. 9 odst. 2 písm. e) pro údaje „zjevně zveřejněné subjektem údajů“ se nevyužívá, protože pro investiční databázi nejsou potřeba.
- **Informační povinnost, čl. 14.** Údaje nezískané od osoby samé vyžadují informovat ji do jednoho měsíce. Výjimku čl. 14 odst. 5 písm. b), kdy by informování „vyžadovalo nepřiměřené úsilí“, nelze předpokládat. Před ostrým sběrem osobních údajů je třeba připravit oznámení a kontaktní kanál.
- **Námitka, čl. 21.** Osoba může vznést námitku proti zpracování na základě oprávněného zájmu. Databáze musí umět záznam na žádost odstranit a evidovat, že se nemá znovu přidat.
- **Co se do databáze neukládá:**
  - adresa bydliště, datum narození, rodné číslo;
  - soukromé kontakty (telefon, e-mail), fotografie;
  - rodinní příslušníci;
  - odhad osobního majetku (žebříčky bohatství), údaje z evidence skutečných majitelů;
  - podíly ve firmách, které osoba sama jako investici neuvádí;
  - zvláštní kategorie údajů.
- **Pilot osobní údaje nesbírá.** Studie proveditelnosti pro angely a velké soukromé investory pracuje jen se souhrnnými počty (např. kolik profilů zveřejňuje asociace) a jména neukládá.

## 1.11 Mini-pilot PE

**Cíl.** Ověřit, zda pravidla PE z 1.10 (P1–P4) fungují na skutečných subjektech, a změřit čas a úplnost polí zadání. Data se sbírají stejnou metodikou jako u VC: jen otevřené stránky, primární zdroje přednostně, každý údaj jako fakt se zdrojem a datem přístupu.

**Výběr.** VC pilot vyřadil 17 PE členů CVCA s důvodem `pe_budouci_rozsireni`. Z nich bylo náhodně vybráno 5 příkazem `random.Random(2026).sample(sorted(ids), 5)`. Seed 2026 je stejný jako u vzorku faktů. Vybráni byli EVERITA Capital (inv-0007), Enterprise Investors (inv-0015), Innova Capital (inv-0018), Versute Investments (inv-0023) a V4C / Value4Capital (inv-0024).

### Jak je PE uloženo, aby se nerozbil VC pilot

| Volba | Proč ne / proč ano |
|---|---|
| Změnit status v `investors.csv` na `overeny` | **Ne.** Status v `investors.csv` je status VC pilotu. Změna by posunula trychtýř, precision i úplnost VC a přepsala historii, ke které se váže kontrola R1. Tyto subjekty do VC pilotu opravdu nepatří. |
| Samostatná kopie tabulek pro PE | **Ne.** Zdvojila by schéma a validaci, fakta a zdroje by se rozdělily. |
| **Samostatné hodnocení v kategorii: tabulka `category_assessments.csv`** | **Ano.** Řádek určuje investora, kategorii (`pe`), status podle pravidel kategorie, důvod vyloučení, datum a poznámku. Fakta, zdroje a fondy zůstávají ve společných tabulkách, takže platí stejná validace dokladů. VC status v `investors.csv` zůstává (`vyloucen`, `pe_budouci_rozsireni`). |

Co k tomu patří:

- **Validace kategorie `pe`:**
  - `investor_type` musí odpovídat kategorii;
  - u `overeny` platí P1 (IČO z primárního zdroje), P3 (fakt s fondem) a P4 (aktivita za 36 měsíců vůči datu hodnocení);
  - u `vyloucen` musí být důvod doložen faktem `duvod_vylouceni`;
  - slovník důvodů je rozšířený o `vc_ne_pe` a `realitni_fond`.
- **Ruční kontrola:** sloupec `category` v `reviews.csv` (`vc`, `pe`), precision se počítá pro každou kategorii zvlášť. Řádky zakládá `python -m investor_db review-template --reviewer R1 --category pe`.
- **Pracnost:** činnost `overeni_kategorie` v `effort_log.csv`, oddělená od `overeni` VC.
- **Metriky:** VC metriky počítají jen VC pilot. U investorů hodnocených v jiné kategorii se do VC počítá jen jejich původní fakt `duvod_vylouceni` z triáže. Report má oddíl „Hodnocení v dalších kategoriích“. Kontrola, že se VC čísla nezměnila: výstup `metrics` před a po zápisu PE se liší jen novým oddílem.
- **Pole `investors.csv`** (sektor, ticket, kapitál, země) se u hodnocených subjektů vyplňují. VC metriky je nečtou, protože počítají jen ověřené VC.

### Výsledek

| Investor | Status PE | Důvod | IČO | Sektor | Ticket | Kapitál podle zdroje | Aktivita |
|---|---|---|---|---|---|---|---|
| EVERITA Capital | `overeny` | – | 19067097 (ARES) | ✓ web | 2–5 mil. EUR (CVCA) | jen cíl Everita Fund I 40 mil. EUR | Clintrial 8/2026, Pekarna Hrstić 3/2026 (51 %) |
| Versute Investments | `overeny` | – | 03965953 (ARES) | ✓ web („všechna odvětví“) | 1–5 mil. EUR equity (CVCA) | jen cílová hodnota aktiv podfondu 1,5–2 mld. Kč | Unipap 9/2025 (50 %) |
| Enterprise Investors | `vyloucen` | `zahranicni_subjekt` | v ARES nenalezeno | ✓ web | 20–75 mil. EUR (web) | investováno 2,5 mld. EUR za celou historii, 10 fondů | – |
| Innova Capital | `vyloucen` | `zahranicni_subjekt` | v ARES nenalezeno | ✓ CVCA (2020) | 25–40 mil. EUR (web) | Innova/7 uzavřen 407 mil. EUR (4/2024), 7 fondů | – |
| Value4Capital (V4C) | `vyloucen` | `zahranicni_subjekt` | v ARES jen nesouvisející V4C, s.r.o. | ✓ web | 7–15 mil. EUR (web) | velikosti fondů 91 mil. a „128M+“ EUR bez typu | – |

**Zjištění:**

- **P1 vyřadilo 3 z 5.** Regionální PE fondy jsou členy CVCA a uvádějí Česko jako cílový trh, ale nemají českou právnickou osobu (Varšava, Lucemburk). Pro databázi světa to znamená, že se mají evidovat v zemi sídla. Česká mutace webu (ei.com.pl/cz) neexistuje (HTTP 404).
- **Pole zadání jsou u PE dostupnější než u VC:**
  - sektor 5/5, ticket 5/5 (obě meze);
  - nějaký údaj o kapitálu 5/5;
  - získaný kapitál podle přísné definice ale jen 1/5 (Innova). Ostatní zdroje uvádějí cíl, „size“ bez typu nebo investovanou částku za celou historii.
- **Konflikty ticketu web × CVCA** u 3 z 5 (EI, Innova, V4C). Profily CVCA jsou starší a vyplňuje je člen. Zapsán je web.
- **Mapování sektorů.** Slovník sektorů je stavěný na VC. Tradiční odvětví PE (služby, stavebnictví, zdravotnictví) se mapují přibližně na `jine`, `prumysl` a `healthtech`. Pro rozšíření na PE by slovník potřeboval kategorie jako služby nebo zdravotnictví.
- **Fáze.** Slovník fází má pro PE jen `growth`; buyout a growth nerozlišuje.
- **Čas modelu:** 5,0 min celkem, průměr 1,0 min a medián 1,1 min na subjekt. VC pilot měl 5,4 min na ověřeného investora. Vyloučení podle P1 je rychlé (0,5–1,3 min), ověřené PE trvalo 1,1–1,6 min.
- Hledání bez výsledku (česká entita) je v `search_log` jako s-033 až s-035.

Ruční kontrolu PE záznamů dělá zadavatel, viz [04-rucni-kontrola.md](04-rucni-kontrola.md), 4.8.
