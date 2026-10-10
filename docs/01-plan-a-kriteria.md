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
