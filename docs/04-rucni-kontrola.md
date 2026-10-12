# 4. Ruční kontrola a precision

Ruční kontrolu provádí výhradně člověk. Model, který data sbíral, kontrolní tabulky nevyplňuje – generuje jen prázdné šablony.

## 4.1 Hodnotitelé

| Kód | Kdo | Povinnost |
|---|---|---|
| `R1` | Zadavatel projektu | Povinná kontrola všech ověřených investorů a vzorku faktů |
| `R2` | Nezávislý hodnotitel | Volitelná; pokud data R2 chybí, metriky shody se nepočítají |

Aby byla kontrola R2 nezávislá, R2 vyplňuje svou šablonu bez znalosti verdiktů R1 (např. na samostatné větvi, která se sloučí až po dokončení obou kontrol).

## 4.2 Návod pro hodnotitele

### Princip

Hodnotitel **neposuzuje metodiku** (např. zda je správné vylučovat PE nebo jak je nastavena hranice 36 měsíců). Posuzuje jen jednu věc: **podporuje uvedený zdroj uvedenou hodnotu?** Pokud metodika vede k výsledku, se kterým hodnotitel nesouhlasí, zapíše to do `note`, ale verdikt podle toho nemění.

Hodnotitel hledá ve zdroji nezávisle. Kontrolní list proto neobsahuje `evidence_note` (poznámku, kde a jak údaj našel model), aby hodnotitele nenavedl k jednomu místu ani výkladu. Údaje z jiných zdrojů, než je ten uvedený, verdikt neovlivňují: fakt je správně jen tehdy, když ho podporuje právě jeho zdroj.

### Kontrolní list faktů

```
python -m investor_db review-guide
```

Příkaz z `data/fact_reviews.csv` vygeneruje `review/kontrolni-list-faktu.md`, zvlášť pro kolo `vzorek` a kolo `po_doplneni`. U každého faktu uvádí:

- `fact_id`, název investora a jeho status,
- **tvrzení**: jednu větu, co fakt říká,
- **co hledat ve zdroji**: na co se při porovnání zaměřit,
- odkaz na zdroj a typ zdroje (primární nebo sekundární).

Věty se skládají deterministicky ze šablon podle typu pole (`investor_db/review_guide.py`), nepíše je model volným textem. Typ pole nebo důvod vyloučení bez šablony je chyba, takže generování selže a žádný fakt nezůstane bez vysvětlení. Verdikty se zapisují do `data/fact_reviews.csv`, kontrolní list se jen čte.

### Verdikty faktů

| Verdikt | Kdy | Příklad |
|---|---|---|
| `spravne` | Zdroj uvádí stejnou hodnotu ve stejném významu (číslo, měna, fond, datum). | Tvrzení: typická investice začíná na 1 000 000 USD. Web investora uvádí „Typical check: $1–5M“. |
| `chybne` | Zdroj uvádí jinou hodnotu, jiný význam, jiný subjekt, nebo hodnotu neuvádí vůbec. | Tvrzení: fond byl uzavřen s velikostí 50 000 000 EUR. Článek píše, že fond „cílí na 50 milionů eur“, jde tedy o cíl, ne o uzavřenou velikost. |
| `nelze_overit` | Zdroj se nenačte, je za placenou zdí, vyžaduje přihlášení nebo byl odstraněn. | Odkaz vrací chybu 404 nebo 429, článek je dostupný jen předplatitelům. |

Pokud zdroj potvrzuje jen část tvrzení (např. dva ze tří sektorů), verdikt je `chybne` a do `note` se zapíše, co chybí.

### Co otevřít a co porovnat podle typu pole

| Pole | Co otevřít | Co porovnat |
|---|---|---|
| `name` | Odkaz ve faktu (web, profil v asociaci, článek) | Název značky; rozdíl jen ve velkých písmenech nebo v právní formě nevadí. Musí jít o stejný subjekt. |
| `registry_id` | Obvykle ARES (JSON v prohlížeči), případně web investora | IČO číslici po číslici; název nebo sídlo subjektu odpovídá investorovi. |
| `website` | Samotný web, nebo stránka, která na něj odkazuje | Doména; web patří investorovi, ne firmě s podobným názvem. |
| `investment_sectors`, `investment_stages` | Web investora, profil, článek | Každý uvedený sektor nebo fáze je ve zdroji jmenován (obdobné označení stačí). |
| `typical_ticket_min`, `typical_ticket_max` | Web investora, profil v asociaci, článek | Číslo, měna a to, že jde o investici fondu do jedné firmy (dolní, resp. horní mez). |
| `total_fund_size` | Článek nebo web o uzavření fondu | Číslo, měna, název fondu a minulý čas („uzavřel“, „final close“). |
| `cilova_velikost_fondu` | Článek nebo web o fondu | Číslo, měna, název fondu a to, že jde o cíl nebo plán. |
| `assets_under_management`, `invested_capital` | Web investora, výroční zpráva | Číslo, měna a to, že jde o celková spravovaná aktiva, resp. skutečně investovaný kapitál. |
| `informace_o_fondu` | Zdroj ve faktu | Každá část věty: název fondu, částky, data, role (správce, GP, AIFM). |
| `pravni_spravce` | Rejstřík, web fondu | Přesný název správcovské entity a její vztah k fondu. |
| `registrace_regulator` | Seznam regulátora | Název a IČO entity, typ registrace. |
| `dolozena_investice` | Článek, tisková zpráva, portfolio | Investovala právě tato značka (nebo její fond) a datum oznámení odpovídá. U data na 1. den měsíce stačí shoda měsíce. |
| `duvod_vylouceni` | Zdroj ve faktu | Zdroj dokládá důvod uvedený v tvrzení (např. PE strategie, dluhové financování, fond fondů, zahraniční sídlo, family office, zánik subjektu). Každý kód má vlastní tvrzení. |

### Typické chyby, kvůli kterým kontrola existuje

- **Cíl fondu místo velikosti fondu.** „Fond cílí na 50 mil. EUR“ nebo „first close 30 mil. EUR“ není uzavřený fond s velikostí 50, resp. 30 mil. EUR.
- **Velikost kola místo vkladu fondu.** „Startup získal 5 mil. EUR v kole, které vedl investor X“ neříká, kolik vložil investor X.
- **Záměna měny.** Částka v USD zapsaná jako EUR nebo přepočtená z korun. Hodnota a měna musí odpovídat zdroji bez přepočtu.
- **Jiná firma s podobným názvem.** Stejný nebo podobný název u jiného IČO, jiný web, nebo investice jiného investora se shodným slovem v názvu.
- **Jiný fond téže značky.** Údaj patří k jinému fondu značky (např. k prvnímu místo ke třetímu).
- **Datum.** Datum oznámení investice se liší, nebo jde o starší investici do téže firmy.

### Kontrola investorů v `reviews.csv`

U investora hodnotitel posuzuje, zda záznam jako celek splňuje kritéria pilotu Z1–Z4 (viz [01-plan-a-kriteria.md](01-plan-a-kriteria.md)). Vychází přitom z odkazů v `evidence_urls`:

| Kritérium | Co ověřit |
|---|---|
| Z1 | Existuje česká právnická osoba s IČO a patří k této značce (název, sídlo nebo statutární orgán odpovídá). |
| Z2 | Převažující strategií je rizikový kapitál: menšinové podíly v nekótovaných firmách, fáze pre-seed až growth. |
| Z3 | Značka investuje přes fond nebo vehikl s kapitálem třetích osob (ne jen vlastní peníze majitele). |
| Z4 | Za posledních 36 měsíců je doložena investice nebo nový fond. |

| Verdikt | Význam |
|---|---|
| `TP` | Všechna kritéria Z1–Z4 platí a záznam popisuje skutečně ten subjekt, kterého se týká. |
| `FP` | Aspoň jedno kritérium neplatí (např. jde o PE, family office nebo neaktivní subjekt), nebo záznam popisuje jiný či neexistující subjekt. Které kritérium neplatí, se zapíše do `note`. |
| `nejiste` | Z uvedených zdrojů nelze rozhodnout, např. Z3 nebo Z4 stojí na zdroji, který se nenačte. Důvod se zapíše do `note`. |

Stejně jako u faktů platí, že rozhodují uvedené zdroje. Pokud hodnotitel ověří kritérium z jiného zdroje (např. z databáze, kterou projekt nepoužívá), zapíše to do `note`. Takový zdroj ale nenahrazuje chybějící doklad v záznamu.

## 4.3 Kontrola investorů → precision

**Kdo se kontroluje:** všichni investoři se statusem `overeny`. V pilotu (20–30 kandidátů) je to celý soubor, takže není třeba vzorkovat.

```
python -m investor_db review-template --reviewer R1
```

Příkaz doplní do `data/reviews.csv` řádek pro každého ověřeného investora, který ještě nemá řádek daného hodnotitele. Hodnotitel vyplní `reviewed_at`, `verdict` a případně `note`.

| Verdikt | Význam |
|---|---|
| `TP` | Hodnotitel z uvedených zdrojů potvrdil, že subjekt splňuje kritéria Z1–Z4 a je to skutečně ten subjekt, kterého se záznam týká (správné IČO a web). |
| `FP` | Některé z kritérií Z1–Z4 neplatí, nebo záznam popisuje jiný či neexistující subjekt. |
| `nejiste` | Z dostupných zdrojů nelze rozhodnout. Důvod uveďte v `note`. |

Čas strávený kontrolou záznamu zapište v minutách do sloupce `review_minutes` (kladné číslo, nejvýše dvě desetinná místa); slouží k odhadu nákladů škálování a vykazuje se odděleně od času modelu.

Chyby v doplňkových polích (např. špatný ticket) se nepromítají do precision záznamu – zachytí je kontrola faktů.

**Výpočet:**

- precision = TP / (TP + FP),
- pesimistická varianta = TP / (TP + FP + nejisté),
- 95% Wilsonův interval, protože u malého vzorku je normální aproximace nepřesná.

## 4.4 Kontrola faktů → přesnost faktů

```
python -m investor_db fact-review-template --reviewer R1
python -m investor_db fact-review-template --reviewer R1 --round po_doplneni --from-fact f-00249
python -m investor_db fact-review-template --reviewer R1 --round po_oprave --facts f-00262,f-00267,f-00270,f-00273,f-00282,f-00285,f-00298
```

První příkaz založí kolo `vzorek`, tedy náhodný vzorek faktů z původního sběru. Pokud už hodnotitel vzorek má, nepřidá nic. Druhý příkaz založí kolo `po_doplneni` se všemi fakty od zadaného `fact_id`. Třetí založí kolo `po_oprave` s fakty, které se po kontrole změnily nebo při opravě přibyly. Fakt tak může mít více řádků, jeden v každém kole. Verdikt v kole `po_oprave` posuzuje současný stav faktu. Kolo je uvedeno ve sloupci `review_round` a přesnost se počítá pro každé kolo zvlášť. Hodnotitel otevře zdroj faktu a vyplní verdikt:

| Verdikt | Význam |
|---|---|
| `spravne` | Zdroj hodnotu uvádí tak, jak je zapsána, včetně měny, fondu a data. |
| `chybne` | Zdroj uvádí jinou hodnotu, nebo hodnotu neuvádí. |
| `nelze_overit` | Zdroj není dostupný nebo jej nelze otevřít. |

I zde se čas kontroly faktu zapisuje do `review_minutes`.

Přesnost faktů = správně / (správně + chybně); `nelze_overit` se vykazuje zvlášť.

### Velikost vzorku faktů

Velikost vzorku se počítá Cochranovým vzorcem s korekcí na konečný soubor: 95% spolehlivost (z = 1,96), přípustná chyba ±15 procentních bodů a konzervativní p = 0,5:

n₀ = z² · p · (1 − p) / e² ≈ 42,68, n = ⌈n₀ / (1 + (n₀ − 1) / N)⌉

| Počet faktů N | Velikost vzorku n |
|---|---|
| 20 | 14 |
| 150 | 34 |
| 205 (pilot) | 36 |
| 300 | 38 |
| velmi mnoho | 43 |

**Proč ±15 p. b. a ne ±10 p. b.:** původní návrh s přípustnou chybou ±10 p. b. vedl v pilotu k 66 faktům z 205. Kontrola jednoho faktu znamená otevřít zdroj, najít v něm hodnotu a porovnat měnu, fond a datum. Při 66 faktech by to přesahovalo časovou kapacitu hodnotitele R1, který kontroluje ještě i všechny ověřené investory. Přípustná chyba proto byla zvětšena na ±15 p. b. a vzorek se zmenšil na 36 faktů. Odhad přesnosti faktů je tím méně přesný: Wilsonův interval ve výsledcích bude širší a výsledek je třeba číst jako orientační. Pokud kapacita dovolí, lze vzorek zpětně rozšířit dalším losováním (nebo přidat R2).

Změna proběhla dřív, než hodnotitel vyplnil jediný verdikt faktu, takže výběr vzorku nemohl ovlivnit znalost výsledků. Šablona `fact_reviews.csv` byla vygenerována znovu se stejným seedem `2026`. Všech 36 faktů nového vzorku bylo i v původním vzorku 66 faktů. `random.sample` se stejným seedem losuje stejnou posloupnost, takže menší vzorek je jejím začátkem.

Vzorek se losuje s pevným seedem `2026` (`investor_db/review.py`), takže je reprodukovatelný. Losuje se až po uzavření sběru dat, protože přidání faktů vzorek změní.

## 4.5 Shoda hodnotitelů

Pokud existují verdikty R2, počítá se pro investory zkontrolované oběma hodnoteli:

- **prosté procento shody**, které se uvádí vždy,
- **Cohenovo κ**. Při malém vzorku a vysokém podílu TP je κ nestabilní (paradox kappa), proto se interpretuje jen spolu s procentem shody a rozborem jednotlivých neshod.

Neshody se rozeberou a rozhodnutí se zapíše do `note`; verdikty se zpětně nepřepisují.

## 4.6 Výsledky

Kontrolu provedl hodnotitel R1 9. a 10. 10. 2026. R2 se kontroly neúčastnil, shoda hodnotitelů se proto nepočítá. Metriky vycházejí z výstupu `python -m investor_db metrics` ke dni 11. 10. 2026. Precision se počítá ze stavu dat **v době kontroly** (commit `fb2f330`, 15 ověřených investorů).

### Precision ověřených záznamů

| Varianta | Výsledek | 95% Wilsonův interval |
|---|---|---|
| TP / (TP + FP), v době kontroly | 15/15 = 100,0 % | 79,6 % – 100,0 % |
| `nejiste` počítáno jako FP | 15/15 = 100,0 % (žádný verdikt `nejiste`) | 79,6 % – 100,0 % |
| Pro informaci: aktuální stav (16 ověřených: přibyli Lighthouse a Tachles, J&T Ventures přešel po kontrole do kandidátů) | 16/16 = 100,0 % | 80,6 % – 100,0 % |

**Historie.** Toto kolo nahradilo kolo R1-v2 (4.11): poznámky se opíraly o Crunchbase, LinkedIn a agregátory v rozporu s metodikou, časy byly zaokrouhlené a Springtide, Patero a Gain byly nejdřív TP a podle pravidel pak FP nebo nejisté.

Do precision vstupují jen řádky investorů, kteří měli v době kontroly status `overeny`. Při 15 záznamech je interval široký. Spodní mez 79,6 % je pesimistický odhad, ne naměřená chybovost.

### Nesouhlas hodnotitele se statusem (možné false negatives)

R1 ohodnotil i sedm záznamů, které v době kontroly neměly status `overeny`, a všechny původně jako `TP`. U tří z nich verdikt později opravil (viz níže). Do precision se nepočítají.

| Investor | Status v době kontroly | Status nyní | Poznámka R1 (zkráceně) | Posouzení |
|---|---|---|---|---|
| Lighthouse Ventures | `kandidat` | `overeny` | Pražský VC fond podporovaný EIF, mnoho investic v posledních letech | **False negative** – chyba hledání: „poslední investice 2019“ byla převzata z jediného článku. Opraveno 11. 10. 2026. |
| Tachles | `kandidat` | `overeny` | Investiční společnost aktivní ve VC poslední tři roky | **False negative** – chybné pravidlo: validátor vyžadoval nepovinné `investment_stages`. Opraveno 11. 10. 2026. |
| Inven Capital | `kandidat` | `kandidat` | Kapitál institucionálních investorů, zejména ČEZ a EIB; investice 2024–2026 | Možný false negative. Z1–Z4 jsou doložena, brání jen pravidlo CVC (podíl ČEZ nad 50 % není doložen). |
| Nation1 | `kandidat` | `kandidat` | Fond s kapitálem EIF; druhý fond 2023, investice 2024 a 2026 | Možný false negative. Chybí doklad Z1 (česká entita značky). |
| Gain Ventures | `kandidat` | `kandidat` | Původně: existují a investují podle databází transakcí | Verdikt opraven na `nejiste`, subjekt z článku není identifikován. |
| Springtide Ventures | `kandidat` | `vyloucen` (`cvc`) | Původně: VC křídlo skupiny KKCG | Verdikt opraven na `FP`, shoda se statusem. |
| Patero | `kandidat` | `vyloucen` (`bez_fondu`) | Původně: reálná společnost („family office“), která dělá VC investice | Verdikt opraven na `FP`, shoda se statusem. |

### Verdikty v rozporu s pravidly zařazení

Sběrač verdikty neměnil. Níže jsou rozpory a návrh řešení, jak byly zveřejněny 11. 10. 2026.

| Investor | Rozpor | Návrh |
|---|---|---|
| Springtide Ventures | `TP` u subjektu, který R1 sám popisuje jako „VC křídlo skupiny KKCG“. Podle Forbesu nemá cizí peníze, celý kapitál tedy dává jedna skupina, což je CVC mimo definici pilotu. | R1 verdikt buď potvrdí jako nesouhlas s pravidlem CVC (pak jde o návrh změny definice, ne o false negative), nebo ho změní na `FP`. |
| Patero | `TP` s poznámkou „family office“. Family office i investice vlastního kapitálu bez fondu jsou podle 1.4 vyloučeny (Z3). | Stejně jako u Springtide: buď nesouhlas s pravidlem, nebo změna verdiktu. |
| Gain Ventures | `TP` stojí na „databázích startupových transakcí“, tedy na agregátorech, které podle metodiky slouží jen jako vodítko. Z1 a Z3 nejsou doložena. | Změnit na `nejiste`, dokud nebude subjekt identifikován. |
| J&T Ventures | `TP` odpovídá statusu, ale poznámka R1 „VC fond patřící pod J&T“ naznačuje vazbu na korporátní skupinu. Podíl skupiny J&T na kapitálu fondu v datech doložen není. Podle pravidla CVC by doložená vazba bez doloženého podílu znamenala status `kandidat`. | Vyřešeno po kontrole, viz Opravy po kontrole. |

R1 po zveřejnění tohoto souhrnu 11. 10. 2026 opravil tři verdikty. Oprava tedy nebyla nezávislá na sběrači: podnítil ji souhrn rozporů, rozhodnutí ale udělal hodnotitel. Do precision se tyto řádky nezapočítávají, protože žádný z nich neměl v době kontroly status `overeny`.

| Investor | Původní verdikt (9. 10.) | Opravený verdikt (11. 10.) | Důvod podle R1 |
|---|---|---|---|
| Springtide Ventures | `TP` | `FP` | CVC – fond nemá cizí kapitál, investuje jen peníze skupiny KKCG (Forbes). |
| Patero | `TP` | `FP` | Investuje vlastní kapitál společníků bez fondu, nespadá do definice VC. |
| Gain Ventures | `TP` | `nejiste` | Doloženo jen agregátory, Z1 a Z3 nejsou doloženy primárním zdrojem. |

Původní verdikty a poznámky jsou v historii Gitu (commit `18877a1`). V `reviews.csv` je u opravených řádků jen čas opravy (5 min), původní čas (10, 20 a 20 min) se přepsal. U J&T Ventures zůstává `TP` z doby kontroly, status se změnil až po kontrole (viz Opravy po kontrole).

### Přesnost faktů

| Varianta | Výsledek | 95% Wilsonův interval |
|---|---|---|
| správně / (správně + chybně) | 32/34 = 94,1 % | 80,9 % – 98,4 % |
| `nelze_overit` počítáno jako chybně | 32/36 = 88,9 % | 74,7 % – 95,6 % |

Jde o kolo `vzorek`: 36 faktů z 205 (Cochran, ±15 p. b.). Kolo `po_doplneni` (49 faktů, viz 4.7) se vykazuje zvlášť. Fakty s verdiktem `chybne` a `nelze_overit`:

| Fakt | Investor | Pole a hodnota | Verdikt | Poznámka R1 |
|---|---|---|---|---|
| f-00071 | i&i Biotech Investments | `investment_sectors` = biotech; healthtech; ai | `chybne` | Fond se podle webu zaměřuje výhradně na life science. |
| f-00145 | Reflex Capital | `typical_ticket_max` = 2 000 000 EUR | `chybne` | Fond obecně investuje kolem 1 mil. EUR, někdy ke hranici 2 mil. EUR (25–50 mil. Kč). |
| f-00003 | CVI | `duvod_vylouceni` = dluhovy_fond | `nelze_overit` | „Direct Lending, Senior Debt, Mezzanine, exceptionally Minority Equity Investments“ |
| f-00081 | Tilia Impact Ventures | `typical_ticket_min` = 300 000 EUR | `nelze_overit` | Žádné informace na webu. |

Fakt f-00173 (Startguide – Carebot) R1 11. 10. 2026 ohodnotil znovu, protože jeho zdroj se po kontrole změnil z agregátoru Caplight na CzechCrunch. Verdikt zůstal `spravne`. Přesnost faktů se tím nemění.

### Jaké zdroje hodnotitel použil

Kontrola investorů a kontrola faktů měří různé věci.

- **Kontrola investorů** podle poznámek R1 ověřovala existenci a aktivitu subjektu **nezávisle na `evidence_urls`**. R1 použil tyto zdroje:
  - Crunchbase (6 záznamů),
  - web investora (5),
  - LinkedIn (3),
  - CzechCrunch (3),
  - Forbes CZ (2),
  - obchodní rejstřík (2),
  - nespecifikované „databáze“ (2),
  - TechCrunch a Sifted (1),
  - registry EIF (1).

  U 4 záznamů zdroj uvedený není. Precision tedy vyjadřuje, zda jsou ověření investoři skutečně aktivní VC, ne zda je správný každý doklad v `evidence_urls`. Pro hodnotitele jsou agregátory legitimní nezávislá kontrola, přestože pro sběr faktů slouží jen jako vodítko.
- **Kontrola faktů** naopak ověřovala přímo zdroj uvedený u faktu podle kontrolního listu. Měří tedy spolehlivost samotných dokladů.

### Úplnost a doložení (ověření investoři, aktuální stav po opravách, n = 16)

| Pole | Vyplněno |
|---|---|
| `name`, `investor_type`, `country`, `registry_id`, `evidence_urls`, `last_verified_at` | 16/16 (100,0 %) |
| `investment_stages` | 15/16 (93,8 %) |
| `website` | 14/16 (87,5 %) |
| `investment_sectors` | 13/16 (81,2 %) |
| `typical_ticket_max`, `currency` | 12/16 (75,0 %) |
| `typical_ticket_min` | 11/16 (68,8 %) |
| `total_fund_size`, `assets_under_management` | 2/16 (12,5 %) |
| `invested_capital` | 0/16 (0,0 %) |

| Metrika | Výsledek | 95% Wilsonův interval |
|---|---|---|
| Ověření investoři s IČO z primárního zdroje | 16/16 = 100,0 % | 80,6 % – 100,0 % |
| Fakty z primárních zdrojů | 128/224 = 57,1 % | 50,6 % – 63,4 % |
| Ověření investoři s doloženou investicí za 36 měsíců (u ostatních je Z4 doloženo novým fondem) | 13/16 = 81,2 % | 57,0 % – 93,4 % |
| Ověření investoři ověření za posledních 12 měsíců | 16/16 = 100,0 % | 80,6 % – 100,0 % |

- **Duplicity:** žádná skupina možných duplicit; 1 záznam je vyloučen jako duplicita.
- **Měny:** 0 peněžních hodnot ponechaných jen ve `facts.csv` kvůli jiné měně, než má řádek.

### Odhad celkového počtu (capture–recapture)

Chapmanovy odhady počtu ověřitelných VC v ČR vycházejí podle dvojice průchodů od 7 do 25 a jejich intervaly od 7 do 41. U dvojic s velkým překryvem jsou odhady nižší než počet skutečně nalezených investorů. Ověřených investorů je 16. Zdroje hledání nejsou nezávislé (sekundární zdroje přebírají viditelné fondy), proto je odhad **dolní mezí**. V ČR je tedy nejméně 16 VC splňujících Z1–Z4, pravděpodobně více.

### Pracnost

| Kdo | Činnost | Rozsah | Celkem | Na položku |
|---|---|---|---|---|
| Model | Hledání kandidátů | 17 průchodů | 5,6 min | 0,3 min na průchod |
| Model | Rychlá triáž | 22 subjektů | 0,7 min | méně než 0,1 min |
| Model | Plné ověření včetně oprav po kontrole | 30 subjektů | 80,1 min | průměr 2,7 min, medián 1,9 min |
| Člověk (R1) | Kontrola investorů | 22 záznamů | 340 min | průměr 15,5 min, medián 15 min (ověření investoři 14,7 min, ostatní 17,1 min) |
| Člověk (R1) | Oprava tří verdiktů | 3 záznamy | 15 min | 5 min |
| Člověk (R1) | Kontrola faktů včetně opakované kontroly f-00173 | 36 faktů | 34,5 min | průměr 0,96 min, medián 0,5 min |

Časy první kontroly investorů jsou z commitu `18877a1`. `metrics` z aktuálních dat ukazuje 305 min, protože u opravených řádků se původní čas nahradil časem opravy. Čas modelu je čas běhu nástrojů a s časem člověka není přímo srovnatelný. Část časů modelu z 11. 10. 2026 je odhad, což je uvedeno v `effort_log`.

### Zbývající kandidáti

| Kandidát | Chybějící kritérium | Typ problému | Co by rozhodlo |
|---|---|---|---|
| Inven Capital | Žádné z Z1–Z4; nerozhodnuto pravidlo CVC | Data chybí | Doklad o podílu ČEZ na současném kapitálu fondu. V roce 2017 dal ČEZ asi 50 z 240 mil. EUR, původ zbytku není uveden; v roce 2021 dostal fond od ČEZ a EIB 6,3 mld. Kč bez rozpadu. |
| Nation1 | Z1 | Nejednoznačný název / data chybí | Česká entita spojená se značkou. Jediná nalezená Nation1 Investment s.r.o. má jiné sídlo a jiné jednatele než tým fondu, web je nedostupný. |
| Gain Ventures | Z1, Z3 | Nejednoznačný název | Identifikace subjektu z článku (web, tým). ARES zná GAIN Ventures s.r.o., vazba na článek ale není doložena. |
| J&T Ventures | Žádné z Z1–Z4; nerozhodnuto pravidlo CVC | Data chybí | Podíl J&T banky na kapitálu fondu. Web uvádí banku jen jako institucionálního investora bez zvláštních práv, podíl neuvádí. |

Opravené případy pro úplnost: Lighthouse Ventures (slabé hledání) a Tachles (chybné pravidlo). Oba byly false negatives a teď mají status `overeny`.

### Orbit Capital

Orbit Capital je vyloučen jako `dluhovy_fond`, protože jeho nejnovější fond Growth Debt Fund II (107 mil. EUR, 2026) poskytuje venture debt. Nejde o chybu klasifikace, ale o **vyloučení z definice pilotu**. Profil CVCA uvádí i growth equity, proto je Orbit kandidátem pro budoucí rozšíření definice o venture debt.

### Omezení dat

- **Konflikt uvnitř jednoho zdroje (Reflex Capital).** Článek CzechCrunch z 22. 12. 2023 uvádí ticket dvakrát a pokaždé jinak. Zakladatel v přímé citaci mluví o „typické investici mezi jedním až dvěma miliony eur“, redakce o odstavec níže o částkách „kolem jednoho milionu eur, někdy ke hranici dvou milionů“. Data se drží přímé citace (1–2 mil. EUR), konflikt je zapsán v `evidence_note`. Hodnotitel vycházel z textu redakce a fakt f-00145 ohodnotil jako `chybne`, verdikt zůstává. Rozpětí ticketu z médií tak může být nepřesné i u jednoho zdroje. Pole `typical_ticket_min` a `typical_ticket_max` neumí zachytit „typicky X, výjimečně Y“.
- **Měny:** 0 peněžních hodnot ponechaných jen ve `facts.csv`.
- **Podíl korporace na kapitálu fondu** veřejné zdroje obvykle neuvádějí (Inven, J&T). Pravidlo CVC proto často končí stavem `kandidat`.

### Opravy po kontrole

Opravy schválil zadavatel 11. 10. 2026 po zveřejnění výsledků. Provedly se až po kontrole, takže **precision a přesnost faktů výše se nemění** a platí pro data v době kontroly. Fakty ve vzorku si ponechávají své `fact_id` a verdikty R1 se vztahují k původní hodnotě (historie v Gitu).

| Záznam | Před opravou | Po opravě | Zdroj a důvod |
|---|---|---|---|
| i&i Biotech Investments (f-00071, `investors.csv`) | `investment_sectors` = biotech; healthtech; ai | biotech; healthtech | Web fondu uvádí zaměření výhradně na life science. AI je tam jedna z vertikál v rámci life science, ne samostatný sektor. Verdikt R1 `chybne` se potvrdil. |
| Reflex Capital (f-00144, f-00145) | ticket 1–2 mil. EUR | **beze změny hodnot** (rozhodnutí zadavatele), do `evidence_note` zapsán konflikt | Po opětovném otevření článku se ukázalo, že zdroj si odporuje. Zakladatel v přímé citaci uvádí „typickou investici mezi jedním až dvěma miliony eur“, redakce o odstavec níže píše „kolem jednoho milionu eur, někdy ke hranici dvou milionů“. Zadavatel rozhodl ponechat ticket podle přímé citace zakladatele. Původní návrh odebrat horní mez vycházel z textu redakce a citaci přehlédl. Verdikt R1 zůstává `chybne`, viz Omezení dat. |
| J&T Ventures (nový fakt f-00248, zdroj jtventures.cz/pristup) | `overeny` | `kandidat` | Web uvádí, že fond není korporátním fondem J&T banky a banka je v něm „pouze institucionálním investorem bez speciálních práv“. Podíl banky na kapitálu neuvádí. ARES u J&T Ventures CG SICAV (08220867) a J&T Ventures III SICAV (22175903) uvádí jen zakladatelské akcie, akcionáře neuvádí. Vazba na skupinu je tedy doložena, podíl ne, a podle pravidla CVC z [02-metodika.md](02-metodika.md) to znamená `kandidat` (stejně jako Inven). Zadavatel změnu přijal. V době kontroly byl J&T `overeny` a verdikt R1 `TP` se do precision započítal. |

### Možná přísnost hodnotitele

R1 verdikty u dvou faktů ponechává. Opakovanou kontrolu by podnítil sběrač dat, takže by už nebyla nezávislá. Metriky zůstávají beze změny a níže je jen zjištění sběrače pro čtenáře.

| Fakt | Verdikt R1 | Zjištění sběrače |
|---|---|---|
| f-00081 Tilia – `typical_ticket_min` 300 000 EUR | `nelze_overit` („žádné info na webu“) | Při opětovném otevření 11. 10. 2026 titulní stránka tilia.vc uváděla „0.3 - 1.2m EUR initial ticket“. Nelze vyloučit, že se obsah stránky liší podle verze nebo načtení skriptů. |
| f-00003 CVI – `duvod_vylouceni` = dluhovy_fond | `nelze_overit` | Text, který R1 v poznámce cituje („Direct Lending, Senior Debt, Mezzanine, exceptionally Minority Equity Investments“), dluhovou strategii spíše podporuje. |

Přesnost faktů 32/34 tedy může být mírně podhodnocená. Pesimistická varianta 32/36 tento případ pokrývá.

### Otevřené otázky

1. **J&T Ventures – podíl J&T banky na kapitálu fondu.** Rozhoduje mezi `overeny` (podíl do 50 %) a `vyloucen` s důvodem `cvc` (nad 50 %). Veřejné primární zdroje (web, ARES) podíl neuvádějí.
2. **Gain Ventures – identifikace subjektu.** Verdikt R1 je `nejiste`, status `kandidat`. Rozhodla by identifikace subjektu z článku (web, tým).

## 4.7 Doplnění údajů požadovaných zadáním (11. 10. 2026)

Zadání ([00-zadani.md](00-zadani.md)) u každého investora žádá sektor, do čeho běžně investuje a v jaké výši, celkový investiční kapitál a zdroj. Audit 16 ověřených investorů ukázal mezery hlavně u kapitálu, který byl většinou jen volným textem ve faktu `informace_o_fondu`. Doplňování proběhlo ve čtyřech dávkách po čtyřech investorech. Druhá fáze opravila definici kapitálu a doplnila fondy Credo, počty fondů, investované částky a sektory Reflexu hledané přímo na webu. Platila stejná pravidla jako při sběru: jen otevřené stránky, primární zdroje přednostně, agregátory jen jako vodítko, robots.txt, ověření proti surovému textu a zápis konfliktů do `evidence_note`. Kapitál se zapisuje do nové tabulky `funds.csv` s typem částky (viz [02-metodika.md](02-metodika.md)). Údaj, který se ani po hledání nenašel, je v `search_log.csv` s `investor_id` a `target_field`.

### Úplnost podle požadavků zadání – před a po

„Před“ je stav dat v commitu `25fff4c` (nový kód, data beze změny). „Po“ je stav po opravě definice kapitálu, třetím kole oprav (`ab775d8`) a opravách po kontrole kola `po_doplneni` (12. 10. 2026). Opravy po kontrole čísla úplnosti nezměnily. Kapitál se počítá podle opravené definice v [02-metodika.md](02-metodika.md): získaná částka fondu nebo AUM, cíl se nezapočítává.

| Požadavek (ověření investoři, n = 16) | Před | Po | Chybí, hledáno a nenalezeno |
|---|---|---|---|
| Sektor | 13/16 | 15/16 | 1 (Reflex, hledáno i přímo na webu) |
| Fáze | 15/16 | 16/16 | 0 |
| Ticket (alespoň jedna mez) | 12/16 | 14/16 | 2 (Rockaway, Tachles) |
| Ticket (obě meze) | 11/16 | 11/16 | dolní mez chybí u Soulmates, Startguide, IP Lab |
| Kapitál (získaná částka fondu nebo AUM) | 2/16 strukturovaně, 13/16 alespoň jako text | 13/16 | 1 (StartupYard) |
| Kapitál – jen cílová velikost, získaný neznámý | – | 2/16 (Startguide, IP Lab) | – |
| Zdroj | 16/16 | 16/16 | – |

**Oprava definice (11. 10. 2026).** První verze této tabulky uváděla u kapitálu 15/16, protože cílovou velikost fondu počítala jako kapitál a přičítala ji k získaným částkám. Cíl ale není kapitál. Podle opravené definice jsou Startguide a IP Lab vedeni zvlášť jako „jen cíl“ a u Presto a Depo se cíl k získanému kapitálu nepřičítá.

Investorů podle typu částky (po opravách po kontrole): uzavřený fond bez upřesnění 11, cílová velikost 4, first close 3, final close 2, závazek jednoho LP 1, investováno ve `funds.csv` 2 (Purple, i&i), investováno jen za období 1 (Tachles), AUM 2, `invested_capital` v `investors.csv` 2 (Depo, Reflex).

### Přehled po investorech

Po zpřísnění pravidla (11. 10. 2026) je získaný kapitál u všech investorů dolní mez. Tensor má doložené oba fondy, ale fundraising druhého fondu pokračuje (plán navýšení na 1,5 mld. Kč). Credo má doloženo všech pět fondů, ale u Stage 3 zůstává nevyřešený konflikt měny. Stage 5 je po kontrole final close (Wikipedie vyřazena jako zdroj typu uzavření).

| Investor | Sektor | Ticket před → po | Získaný kapitál | Cíl (nezapočten) | Investováno / AUM | Hledáno, nenalezeno |
|---|---|---|---|---|---|---|
| Tensor Ventures | ✓ | beze změny | 20 mil. EUR + 1 mld. Kč, dolní mez (2 ze 2 fondů, fundraising Co-investment Fund pokračuje) | – | – | – |
| KAYA VC | – → ✓ | beze změny | 142 mil. EUR, dolní mez (ET3 bez částky, počet fondů nedoložen) | – | AUM 500 mil. USD | – |
| Depo Ventures | ✓ | beze změny | 129 mil. Kč, dolní mez; **z toho 94 mil. Kč závazek jednoho LP (NRI)**, uzavřený Grouport 35 mil. Kč | 545 mil. Kč | investováno 9 mil. EUR | – |
| i&i Biotech | ✓ | beze změny | 47 mil. EUR, dolní mez (přibližně; **konflikt** s 50 mil. EUR v oznámení EIF) | – | investováno asi 7,4 mil. EUR | – |
| Credo Ventures | ✓ | beze změny | 146 mil. EUR + 188 mil. USD, dolní mez (5 z 5 fondů; **konflikt**: měna Stage 3; Stage 5 final close) | – | – | primární zdroj ke Stage 3 |
| Tilia Impact | ✓ | beze změny | 26 mil. EUR + 43 mil. Kč, dolní mez (první fond jen first close) | – | – | druhé kolo prvního fondu |
| Presto Ventures | ✓ | beze změny | 30 mil. EUR, dolní mez | 150 mil. EUR (Tech Horizons) | – | uzavření Tech Horizons |
| Rockaway Ventures | ✓ | – → – | 55 mil. EUR, dolní mez („necelých“) | – | – | ticket |
| Purple Ventures | – → ✓ | beze změny | 700 mil. Kč, dolní mez („přes“) | – | investováno čtvrt mld. Kč | – |
| Lighthouse Ventures | ✓ | beze změny | 23 mil. EUR, dolní mez (Fund II bez částky) | – | – | velikost Fund II |
| Reflex Capital | – → – | beze změny | 22 mil. EUR, dolní mez (fondy 1–2 neznámé) | – | investováno 150 mil. EUR za celého správce, **rozsah neznámý** (web: „€150M již investováno“) | sektor, rozsah 150 mil. EUR |
| Tachles | ✓ | – → – | 500 mil. Kč, dolní mez (first close, přibližně) | – | investováno 30 mil. Kč jen za rok 2024 (dolní mez) | ticket |
| Soulmates Ventures | ✓ | ?–3 mil. EUR beze změny | 50 mil. EUR, dolní mez (počet fondů nedoložen) | – | AUM 62 mil. EUR | dolní mez ticketu |
| Startguide VC | ✓ | – → ?–2 mil. EUR | neznámý | 6 mil. EUR (SG One; SG Two má jen plán investic 20 mil. EUR) | – | dolní mez ticketu |
| StartupYard | ✓ | beze změny | neznámý | – | – | kapitál |
| IP Lab Ventures | ✓ | – → ?–1 mil. EUR | neznámý | 1,2 mld. Kč | – | dolní mez ticketu |

### Konflikty a rozhodnutí při doplňování

- **KAYA – AUM 500 mil. USD.** Web neuvádí, co AUM zahrnuje. Vestbee (2025) uvádí hodnotu portfolia 350 mil. EUR, což je jiná veličina. AUM zůstává jako údaj správce a k získanému kapitálu se nepřičítá. Web dál uvádí „$85M Current Fund“, kdežto Vestbee first close Fund V 70 mil. EUR. Ticket je na webu v USD, ve Vestbee v EUR.
- **Tensor – druhý fond.** Ověřeno znovu: „více než miliardou korun“ v CzechCrunch (15. 5. 2024) je plán před získáním peněz, tedy cíl, vedle cíle „až 50 mil. EUR“. Forbes (18. 9. 2025) uvádí closing 1 mld. Kč („dokázal naraisovat miliardu korun během pěti měsíců“) s plánem navýšení na 1,5 mld. Kč. 1 mld. Kč je tedy získaný kapitál typu „uzavřen bez upřesnění“, ne final close. Fond Forbes nejmenuje, ztotožnění proběhlo podle pořadí („druhý fond“).
- **Credo – fondy 1–3.** Credo 1 má 18 mil. EUR, ale CzechCrunch (2019) uvádí start v roce 2011 a TechCrunch (2015) v roce 2010. Credo 2 mělo podle TechCrunch při uzavření v roce 2015 34 mil. EUR s cílem 40 mil. EUR, CzechCrunch (2019) uvádí 53 mil. EUR. Zapsán je pozdější údaj. Credo Stage 3 má podle money.pl (2020) 100 mil. USD, CzechCrunch a Vestbee uvádějí 100 mil. EUR. Zapsáno je USD, protože money.pl píše o získaných penězích, kdežto CzechCrunch o otevření fondu. Počet fondů 5 dokládá Tech.eu („their 5th fund“).
- **Credo Stage 5 – typ uzavření.** Wikipedie (f-00030, f-00295) uvádí „first closing“ 88 mil. USD, ale zdroj, který cituje (Tech.eu, f-00266), first close neuvádí. TNW (23. 3. 2026, f-00296) píše o fondu „raised in a single closing“, tedy o jediném uzavření. Zadavatel nejdřív rozhodl zapsat first close jako konzervativní variantu s konfliktem. Po kontrole R1 (12. 10. 2026) je Wikipedie pro tento údaj vyřazena a fond je zapsán jako final close podle TNW (viz Opravy po kontrole kola `po_doplneni`). Zadavatel změnu 12. 10. 2026 potvrdil, protože jeho dřívější rozhodnutí stálo na Wikipedii.
- **Credo Stage 3 – měna (konflikt).** USD uvádějí money.pl (10. 3. 2020, f-00291; partner Habermann v citované tiskové zprávě „blisko 100 mln USD“) a Silicon Canals. EUR uvádějí CzechCrunch (8. 11. 2019), partner Andrej Kiska v rozhovoru (11. 11. 2019, f-00297) a Vestbee (2. 4. 2020). Primární zdroj (web Credo, newsroom, EIF) se nenašel a vyhledávání vrátilo jen norský Credo III, což je jiný subjekt (s-030). Rozpor je ve `funds.csv` označený a zapsána je nižší varianta 100 mil. USD. Součet Creda proto obsahuje sporný fond.
- **Lighthouse – první fond.** Článek uvádí 23 mil. EUR, rozpis vkladů ve stejném článku ale dává 20 mil. EUR.
- **IP Lab – velikost fondu.** CzechCrunch a MPO uvádějí cíl 1,2 mld. Kč, Lupa „až 40 mil. EUR (necelá miliarda Kč)“.
- **i&i – 50 mil. EUR.** EIF fond popisuje jako „€50 million fund“, ÚOCHB uvádí start s více než 45 mil. EUR a později přibližně 47 mil. EUR. 50 mil. EUR bylo původně vedeno jako cílová velikost. Po kontrole R1 je to oznámená velikost bez rozlišení cíle a rozpor je označen jako konflikt.
- **Investovaný kapitál Purple** (čtvrt miliardy Kč) je ve `funds.csv` jako `investovano` v CZK, protože tam má měnu každá částka. V `investors.csv` zůstává prázdný, protože řádek je v EUR. Stejně je zapsána investovaná částka i&i (přibližně 7,4 mil. EUR).
- **Sektory Purple** jsou mapované na slovník: creator economy → `media`, security → `kyberbezpecnost`. Mapování je v `evidence_note`.
- **Reflex – sektory.** Sektory byly hledány přímo na reflexcapital.com (úvodní stránka cs i en, portfolio, kontakt). Web je neuvádí a píše jen „Investujeme zejména do lidí“. Sektorovou neomezenost výslovně neuvádí, proto se `sektorove_agnosticky` nezapisuje a hledání je v `search_log` (s-029). Na úvodní stránce je doslovně „€150M již investováno“ (anglicky „€150M invested“), doplněno jako `invested_capital` (f-00294). Žádný zdroj neuvádí, co částka zahrnuje (s-031). Forbes uvádí, že Reflex začal jako family office, kde Ondřej Fryc investoval vlastní prostředky. Částka je řádově vyšší než získaný kapitál známých fondů (třetí fond 22 mil. EUR, druhý „podobný“), takže pravděpodobně nejde jen o fondy. Zdroj to ale neříká, proto je v tabulce kapitálu uvedena jako údaj za celého správce s nejasným rozsahem.

### Pracnost

Doplňování trvalo modelu 13,0 min běhu nástrojů v první fázi (16 investorů, medián 0,8 min) 7,6 min ve druhé fázi (Credo, Tensor, Reflex, Purple, i&i; společný čas rozdělen rovnoměrně po 1,51 min) a 3,3 min ve třetí fázi (Tensor, Credo, Reflex; po 1,10 min). Je evidováno v `effort_log` jako činnost `doplneni`, odděleně od původního ověření (80,1 min). Cílená hledání bez výsledku jsou v `search_log` jako s-018 až s-032 (s-032 po kontrole).

### Nové fakty ke kontrole

Doplňování přidalo 49 faktů (f-00249 až f-00297). Všechny jsou v `fact_reviews.csv` jako samostatné kolo `po_doplneni`, kontroluje se každý fakt, ne vzorek. Původní vzorek 36 faktů (kolo `vzorek`) zůstal beze změny, přibyl mu jen sloupec `review_round`. Přesnost faktů se vykazuje zvlášť pro obě kola. Hodnoty v 4.6 platí pro kolo `vzorek`, výsledek kola `po_doplneni` je v následujícím oddílu. U f-00036, f-00037 a f-00038 (KAYA, původní sběr) přibyla jen poznámka v `evidence_note`. U f-00252 (Tensor) přibyla poznámka o ověření, že jde o získaný kapitál.

### Přesnost faktů – kolo `po_doplneni`

Kontrolu provedl R1 12. 10. 2026 na stavu dat v commitu `50b0205`. Zkontrolováno bylo všech 49 faktů z doplňování, ne vzorek. Interval proto nevyjadřuje výběrovou chybu, ale nejistotu odhadu chybovosti procesu doplňování.

| Varianta | Výsledek | 95% Wilsonův interval |
|---|---|---|
| správně / (správně + chybně) | 42/44 = 95,5 % | 84,9 % – 98,7 % |
| přísná: `nelze_overit` počítáno jako chybně | 42/49 = 85,7 % | 73,3 % – 92,9 % |

Pro srovnání kolo `vzorek`: 94,1 %, v přísné variantě 88,9 %. R1 potřeboval 40 min, tedy 0,82 min na fakt.

| Fakt | Investor | Pole a hodnota | Verdikt | Nález R1 (zkráceně) |
|---|---|---|---|---|
| f-00270 | Tilia Impact Ventures | `fond_uzavren` 43 mil. Kč (první fond) | `chybne` | Zdroj říká „první kolo jsme uzavřeli na 43 milionech“, jde o first close. |
| f-00295 | Credo Ventures | `fond_first_close` 88 mil. USD (Stage 5) | `chybne` | Wikipedie first close uvádí, ale citovaný Tech.eu ne a TNW píše „single closing“. Totéž platí pro dříve schválený f-00030. |
| f-00262 | i&i Biotech | `cilova_velikost_fondu` 50 mil. EUR | `nelze_overit` | EIF uvádí 50 mil. EUR jako velikost fondu, ne jako cíl. Cíl byl odvozen z pozdějšího údaje ÚOCHB. |
| f-00267 | Credo Ventures | `fond_uzavren` 75 mil. EUR (Stage 4) | `nelze_overit` | Sifted se nenačetl. AIN.UA částku potvrzuje, název „Credo Stage 4“ ne. |
| f-00273 | Purple Ventures | `cilova_velikost_fondu` 40 mil. EUR | `nelze_overit` | Tech.eu „launched a €40 million fund“ nerozlišuje cíl a získanou částku. |
| f-00282 | Tachles | `invested_capital` 30 mil. Kč | `nelze_overit` | Jde o investice „během minulého roku“ (2024), ne o celkový investovaný kapitál. |
| f-00285 | Startguide VC | `cilova_velikost_fondu` 20 mil. EUR (SG Two) | `nelze_overit` | „Plánujeme investovat 20 M EUR do 15 projektů“ je plánovaný objem investic, ne cílová velikost fondu. |

**Co z kontroly plyne.** Šest ze sedmi nálezů se netýká částky, ale jejího **typu**: cíl, získaná částka, first close, investice za období. Částky samotné odpovídaly zdrojům. Doplňování tedy chybovalo hlavně v klasifikaci. Agent přiřadil typ podle kontextu nebo pozdějšího zdroje („je vedeno jako cíl, protože…“), ne podle formulace zdroje. Jen f-00267 je `nelze_overit` kvůli nedostupnému zdroji. U zbylých čtyř R1 zdroj otevřel, ale zdroj typ údaje nedokládá. Proto je pro toto kolo výstižnější přísná varianta (85,7 %). Verdikty zůstávají, jak je R1 zapsal. Opravy, které R1 navrhl, jsou v oddílu „Opravy po kontrole kola `po_doplneni`“. Metrika výše platí pro data v době kontroly.

### Opravy po kontrole kola `po_doplneni`

Opravy navrhl R1 a schválil je zadavatel 12. 10. 2026. Provedly se až po kontrole, takže **přesnost kola `po_doplneni` výše se nemění** a platí pro data v době kontroly (`5fdc535`). Opravené fakty si ponechávají `fact_id`. Verdikty R1 se vztahují k původní hodnotě (historie v Gitu). Všechny dotčené zdroje sběrač 12. 10. 2026 znovu otevřel a ověřil proti surovému textu.

| Fakt | Před opravou | Po opravě | Zdroj a důvod |
|---|---|---|---|
| f-00270 Tilia | `fond_uzavren` 43 mil. Kč, přibližně | `fond_first_close` 43 mil. Kč; `funds.csv` `first_close` | Rozhovor 28. 11. 2018: „První kolo jsme uzavřeli na 43 milionech korun“, druhé kolo mělo fond navýšit na necelých 60 mil. Kč. Druhé kolo **nedoloženo**: CzechCrunch 21. 9. 2023 píše jen „přes 43 milionů“, Newstream 15. 9. 2023 popisuje až druhý fond (search_log s-032). |
| f-00262 i&i | `cilova_velikost_fondu` 50 mil. EUR | `oznamena_velikost_fondu` 50 mil. EUR; `conflict_note` u fondu | EIF 24. 9. 2021: „a €50 million tech transfer fund“, velikost v době závazku EIF, ne cíl. Rozpor s ÚOCHB (přibližně 47 mil. EUR, f-00264) je vidět v tabulce kapitálu. Zapsán zůstává pozdější údaj o získaném kapitálu. |
| f-00267 Credo | zdroj Sifted, fond „Credo Stage 4“ | zdroj AIN.UA 11. 10. 2022, fond „CS4“; nový fakt f-00298 (Podim) | AIN.UA: „closed its €75 million fourth fund“. Název „Credo Stage 4“ žádný zdroj neuvádí. Podim uvádí „fourth flagship fund, CS4, at €75 million“ a first close dříve v roce 2022. Sifted (src-0122) už žádný fakt nedokládá. |
| f-00273 Purple | `cilova_velikost_fondu` 40 mil. EUR | `oznamena_velikost_fondu` 40 mil. EUR | Tech.eu: „has launched a €40 million fund“ nerozlišuje cíl a získanou částku. Kapitál Purple se nemění (700 mil. Kč, f-00275). |
| f-00282 Tachles | `invested_capital` 30 mil. Kč v `investors.csv` | `fond_investovano_za_obdobi` 30 mil. Kč v `funds.csv`; `invested_capital` prázdné | „Jen během minulého roku podpořili sedm startupů dohromady částkou třicet milionů korun“. Jde o rok 2024, ne o celkovou částku, proto je to v tabulce kapitálu dolní mez. |
| f-00285 Startguide | `cilova_velikost_fondu` 20 mil. EUR (SG Two) | `informace_o_fondu` „plánovaný objem investic 20 mil. EUR do 15 projektů“; SG Two ve `funds.csv` bez částky | „Plánujeme investovat 20 M EUR do 15 projektů“ je plán investic, ne cílová velikost fondu. Cíl Startguide klesá z 26 na 6 mil. EUR (jen SG One). |
| f-00295, f-00030 Credo | Wikipedie jako zdroj first close Stage 5; `funds.csv` `first_close` s konfliktem | Wikipedie označena v `evidence_note` jako **vyřazený zdroj pro typ uzavření**; `funds.csv` `final_close` podle TNW (f-00296), konflikt odstraněn | Citovaný Tech.eu typ uzavření neuvádí a TNW píše „raised in a single closing“. Po vyřazení Wikipedie žádný zdroj first close nedokládá, proto řádek fondu nese typ podle TNW. f-00030 (kolo `vzorek`, verdikt `spravne`) zůstává beze změny verdiktu. |

**Dopad na metriky.** Úplnost podle požadavků zadání se nemění: kapitál 13/16, jen cíl 2/16 (Startguide, IP Lab). Získaný kapitál zůstává u všech investorů dolní mezí. U Creda je to už jen kvůli konfliktu měny Stage 3. Změnilo se:

- cíl Startguide z 26 na 6 mil. EUR,
- Tachles: investovaný kapitál je dolní mez za období,
- i&i: konflikt zdrojů je vidět v tabulce kapitálu,
- Tilia: první fond je first close.

**Nové typy faktů.** Kvůli opravám přibyly `oznamena_velikost_fondu` a `fond_investovano_za_obdobi` (s typem částky `investovano_za_obdobi`), viz [02-metodika.md](02-metodika.md). Metodika nově výslovně říká, že typ částky se určuje jen z formulace zdroje.

**Opakovaná kontrola (kolo `po_oprave`).** Fakty f-00262, f-00267, f-00270, f-00273, f-00282, f-00285 a nový f-00298 mají po opravě jiný typ, zdroj nebo hodnotu. Jsou v `fact_reviews.csv` jako samostatné kolo `po_oprave` a v kontrolním listu jako třetí oddíl. Jejich verdikty v kole `po_doplneni` se vztahují k původnímu stavu a zůstávají. Přesnost kola `po_oprave` se vykazuje zvlášť a do přesnosti ostatních kol se nezapočítává.

### Přesnost faktů – kolo `po_oprave`

Kontrolu provedl R1 12. 10. 2026 na stavu dat v commitu `5d895a9`. Všech 7 opravených a nových faktů je `spravne`: **7/7**. Interval 64,6–100 % je při 7 faktech široký, proto jde hlavně o potvrzení, že opravy odpovídají zdrojům, ne o odhad chybovosti. R1 potřeboval 3,5 min (0,5 min na fakt). Výsledek platí pro opravený stav. Přesnost kola `po_doplneni` (42/44, přísně 42/49) se tím nemění, protože popisuje kvalitu doplňování v době kontroly.

## 4.8 Kontrola mini-pilotu PE

Mini-pilot PE ([01](01-plan-a-kriteria.md), 1.11) má vlastní řádky v `reviews.csv` se sloupcem `category` = `pe`. Založil je příkaz `python -m investor_db review-template --reviewer R1 --category pe`. Posuzuje se **status podle pravidel PE** (P1–P4 v [01](01-plan-a-kriteria.md), 1.10), ne podle pravidel VC. Precision PE se počítá jen z řádků `pe` u subjektů se statusem PE `overeny`. VC precision se nemění.

| Verdikt | Význam v kategorii PE |
|---|---|
| `TP` | Subjekt je skutečný PE investor, který splňuje P1–P4 (u `overeny`), nebo je správně vyloučen (u `vyloucen`). |
| `FP` | Status je chybný: ověřený subjekt P1–P4 nesplňuje nebo nejde o PE, případně vyloučený subjekt kritéria splňuje. |
| `nejiste` | Zdroje nestačí k rozhodnutí. |

Výsledky se vykazují **v počtech, ne v procentech**. Při 5 záznamech jde o studii proveditelnosti, ne o měření precision. Vykazují se dvě oddělené otázky:

- **(a) Pravost:** jde o skutečného PE investora? Sem patří i subjekty vyloučené jen kvůli zemi (`zahranicni_subjekt`).
- **(b) Rámec pilotu:** má subjekt českou právnickou osobu (P1) a splňuje P2–P4?

Verdikt u vyloučených slouží jako kontrola false negatives, stejně jako u VC.

### Záznamy ke kontrole

| # | Investor | Status PE | Co ověřit | Klíčové fakty |
|---|---|---|---|---|
| 1 | EVERITA Capital (inv-0007) | `overeny` | IČO 19067097 v ARES; growth a většinové podíly; Everita Fund I; investice za 36 měsíců | f-00299 (ARES), f-00303 (fáze), f-00306 (cíl fondu 40 mil. EUR), f-00307 (EIF schválil 20 mil. EUR), f-00308 Clintrial 31. 8. 2026, f-00309 Pekarna Hrstić 31. 3. 2026 |
| 2 | Enterprise Investors (inv-0015) | `vyloucen`, `zahranicni_subjekt` | že nemá českou právnickou osobu | f-00311 (CVCA: Varšava; ARES 0 výsledků), s-033 |
| 3 | Innova Capital (inv-0018) | `vyloucen`, `zahranicni_subjekt` | že nemá českou právnickou osobu | f-00319 (kontakt: Varšava, Lucemburk; ARES 0), s-034 |
| 4 | Versute Investments (inv-0023) | `overeny` | IČO 03965953; růstový kapitál a LBO; podfond VERSUTE Private Equity Fund Otevřený; Unipap | f-00326 (ARES), f-00329 (fáze), f-00332 (cílová hodnota aktiv 1,5–2 mld. Kč), f-00333 Unipap 24. 9. 2025 |
| 5 | Value4Capital (inv-0024) | `vyloucen`, `zahranicni_subjekt` | že nemá českou právnickou osobu; že V4C, s.r.o. v ARES nesouvisí | f-00336 (kontakt; ARES), s-035 |

Doplňková pole (sektor, ticket, kapitál) jsou fakty f-00299–f-00343. Mapování sektorů na slovník je u každého faktu v `evidence_note`. Po kontrole R1 bylo přemapováno na schválený PE slovník (1.11), což verdikty R1 o statusu nemění. Čas kontroly zapište do `review_minutes`.

### Výsledek kontroly PE (R1, 12. 10. 2026)

| Otázka | Výsledek |
|---|---|
| Verdikt TP | **5/5** |
| Ověření (`overeny`) potvrzeni | 2/2 (EVERITA, Versute) |
| Vyloučení jako zahraniční subjekt potvrzeni | 3/3 (Enterprise Investors, Innova, V4C) |
| (a) Pravost: skutečný PE investor | **5/5**. U všech tří vyloučených R1 uvádí „Skutečný PE investor: ano“. |
| (b) V rámci země pilotu: česká právnická osoba | **2/5** |

Výsledky jsou v počtech, protože při 5 záznamech jde o studii proveditelnosti. Pravost 5/5 je teď **měření** (kontrola R1), ne jen hodnocení sběrače. Čas kontroly R1: 45 min za 5 záznamů, tedy 9 min na záznam (5–15 min). U VC to bylo 15,5 min na investora.

**Poznámky R1 a zjištění sběrače:**

- U Enterprise Investors a Innova R1 vyhledávání v ARES nespouštěl a vycházel z faktů f-00311 a f-00319. U V4C nesouvislost s V4C, s.r.o. ověřil sám v ARES.
- U EVERITA R1 dohledal zprávu o Clintrial s datem 1. 9. 2026 (Investors in Healthcare). Fakt f-00308 uvádí 31. 8. 2026 podle data zveřejnění na webu EVERITA. Rozdíl jednoho dne není chyba faktu.
- **Versute – robots.txt.** R1 uvádí, že „versute.cz zakazuje robotům přístup“, a stránku podfondu ani článek Forbes neotevřel. Sběrač 12. 10. 2026 ověřil, že `https://versute.cz/robots.txt` obsahuje `User-agent: *` a prázdné `Disallow:`, tedy přístup povoluje. Odpověď nese hlavičku `X-Robots-Tag: noindex, follow`, která zakazuje jen indexování samotného souboru vyhledávači. Verdikt R1 zůstává. Jde o zjištění sběrače pro čtenáře, stejně jako v 4.6 („Možná přísnost hodnotitele“).
- **Osobní údaj v poznámce.** Poznámka R1 u V4C uvádí jméno fyzické osoby (společnice nesouvisející V4C, s.r.o.). Podle zásady minimalizace (1.10) navrhuji jméno z poznámky odstranit. Poznámky R1 sběrač sám nemění. **Úprava poznámek (12. 10. 2026).** Poznámky u V4C a Versute upravil agent na výslovný pokyn hodnotitele R1, který text sám nadiktoval. Změnilo se jen pole `note`, verdikty a ostatní pole zůstaly. U V4C je jméno fyzické osoby nahrazeno slovy „společnice nesouvisející firmy“. U Versute je věta o zákazu robotů nahrazena větou „robots.txt přístup povoluje; X-Robots-Tag noindex se týká jen indexace“. Historie Gitu se nepřepisuje: jméno pochází z veřejného rejstříku ARES a přepis by porušil historii commitů.

## 4.9 Kontrola vyloučených VC (odhad false negatives)

Precision měří jen ověřené záznamy. Jestli pilot nevyloučil někoho, kdo do VC patří, ukáže až kontrola vyloučených. Dřívější kontrola R1 našla dva false negatives (Lighthouse, Tachles, 4.6), ale nebyla náhodná. Proto vzniká samostatný náhodný vzorek.

**Výběr.** 10 z 32 vyloučených subjektů, `random.Random(2026).sample(sorted(ids), 10)`. Řádky jsou v `reviews.csv` s `category` = `vc_vyloucene` a založil je příkaz:

```
python -m investor_db review-template --reviewer R1 --category vc_vyloucene
```

Opakované spuštění vzorek nemění. Ve vzorku jsou čtyři PE subjekty, jedno dluhové financování, dva subjekty bez fondu, jeden zaniklý subjekt, jeden fond digitálních aktiv a jedna duplicita.

**Otázky pro hodnotitele** (návod a doklady u každého subjektu jsou v [review/kontrolni-list-faktu.md](../review/kontrolni-list-faktu.md), oddíl „Kontrola vyloučených VC“):

1. Dokládá uvedený zdroj důvod vyloučení?
2. Je subjekt opravdu mimo definici VC pilotu (Z1–Z4, 1.3 v [01](01-plan-a-kriteria.md))?

| Verdikt | Význam |
|---|---|
| `TP` | Vyloučení je správné. Zdroj důvod dokládá a subjekt do VC pilotu nepatří. |
| `FP` | Subjekt do VC pilotu patří, měl být ověřen nebo veden jako kandidát. Jde o false negative. |
| `nejiste` | Zdroje nestačí k rozhodnutí. |

Pokud zdroj důvod nedokládá, ale subjekt přesto do VC nepatří (jiný důvod), je verdikt `TP` a do poznámky se napíše správný důvod. Do poznámky se nepíší jména fyzických osob.

**Metrika.** `python -m investor_db metrics`, oddíl „Kontrola vyloučených VC“:

- podíl správných vyloučení TP / (TP + FP) s Wilsonovým intervalem;
- pesimistická varianta (nejisté jako chybné);
- počet možných false negatives ve vzorku.

Odhad false negatives ve všech 32 vyloučených = podíl chybných vyloučení × 32. Při vzorku 10 je interval široký.

### Výsledek kontroly vyloučených (R1, 12. 10. 2026)

| Ukazatel | Výsledek |
|---|---|
| Zkontrolováno | 10 z 32 vyloučených (seed 2026) |
| Vyloučení správně (`TP`) | 9 |
| Subjekt patří do VC pilotu (`FP`) | 0 |
| Nejisté | 1 |
| Podíl správných vyloučení TP / (TP + FP) | **9/9** (95% Wilsonův interval 70,1–100 %) |
| Pesimisticky, nejisté jako chybné | 9/10 (59,6–98,2 %) |
| Možné false negatives ve vzorku | 1 z 10 |
| Čas R1 | 36 min, 3,6 min na subjekt |

**Nejistý případ: Fond rizikového kapitálu, s.r.o. (`zanikly_subjekt`).** Důvod vyloučení dokládá jen vyhledávací API ARES (POST `/vyhledat`). R1 ho nemohl otevřít v prohlížeči ani výsledek zopakovat. Neaktivitu R1 považuje za pravděpodobnou, ale z uvedeného zdroje ji ověřit nešlo. Doklad „nic nenalezeno“ přes POST API je tedy pro hodnotitele nereprodukovatelný. Kontrolní list sice obsahuje nápovědu „vyhledej název na ares.gov.cz“, ale to stejný dotaz nezaručuje.

**Odhad false negatives mezi 32 vyloučenými.** Ve vzorku nebyl žádný `FP`. Bodový odhad je tedy 0. Horní mez 95% intervalu pro podíl chybných vyloučení je 29,9 %, tj. nejvýš zhruba 10 z 32 subjektů. Pesimisticky (nejisté jako chybné) je bodový odhad 1/10, tj. asi 3 subjekty. Hodnotitel u vzorku našel jen jeden nejistý doklad, ne subjekt, který by do VC patřil.

**Shrnutí kontrol false negatives.** Nenáhodná kontrola R1 v 4.6 našla dva false negatives (Lighthouse, Tachles). Oba byli kandidáti, ne vyloučení, a byly opraveny. Náhodný vzorek vyloučených žádný false negative nenašel.

## 4.10 Recall proti nezávislým seznamům (13. 10. 2026)

Kolik VC subjektů z veřejných seznamů, které pilot při hledání nepoužil, máme v databázi. Použité zdroje hledání jsou v `search_log.csv` (s-001 až s-017) a `candidate_sources.csv`. Žádný z obou seznamů mezi nimi není.

**Seznamy:**

| Seznam | Typ | Datum | Subjektů |
|---|---|---|---|
| L1 – Vestbee: [Top VC Funds In Czech Republic To Finance Your Startup](https://www.vestbee.com/insights/articles/top-vc-funds-in-czech-republic-to-finance-your-startup) | redakční přehled | 14. 10. 2021, aktualizováno 2023 | 19 |
| L2 – AIN.UA: [Top 17 most active Czech VC funds in H1 2022](https://en.ain.ua/2022/09/27/top-17-most-active-czech-vc-funds-in-h1-2022) | redakční žebříček | 27. 9. 2022 | 17 |

- Všech 17 subjektů z L2 je i v L1, sjednocení má 19 subjektů.
- L2 podle vlastního popisu vychází z dotazníku, otevřených zdrojů a dat Dealroom a Crunchbase. Slouží proto jen jako vodítko, stejně jako agregátory v metodice.
- Portfolio fondů Národní rozvojové banky ani seznam fondů EIF v ČR jako seznam veřejně nebyl k dispozici. Web NRB přehled portfolia nemá (s-015) a stránka EIF k fondu fondů CZFoF vrátila 404. Přehled CzechCrunch „Startupové Česko 2025“ má nejaktivnější fondy jen v grafu a v placené databázi.

**Které subjekty se počítají.** Počítají se subjekty, které seznamy uvádějí jako VC v ČR a které podle otevřených zdrojů nejsou zjevně mimo kritéria. Ze sjednocení 19 subjektů se proto nepočítá Pale Fire Capital. Podle otevřených článků investuje peníze partnerů ([Seznam Zprávy, 7. 4. 2026](https://www.seznamzpravy.cz/clanek/ekonomika-firmy-elitni-cesky-fond-prijima-krskova-odchovance-na-nove-nakupy-da-10-miliard-303124)) a jeho PE rameno cílí na zavedené firmy, ne na startupy. Neplní tedy Z3 a definici VC. Zbývá **18 subjektů**.

**Výsledek: nalezeno 14 z 18 (77,8 %, 95% Wilsonův interval 54,8–91,0 %).**

| Status v databázi | Počet | Subjekty |
|---|---|---|
| ověřený | 8 | Credo Ventures, DEPO Ventures, KAYA, Lighthouse Ventures, Presto Ventures, Reflex Capital, Rockaway Capital (u nás Rockaway Ventures), Tensor Ventures |
| kandidát | 3 | Inven Capital, J&T Ventures, Nation 1 VC |
| vyloučený s důvodem (nalezen, podle Z1–Z4 do VC nepatří) | 3 | ZAKA (`family_office`), Impulse Ventures (`bez_fondu`), Springtide Ventures (`cvc`) |
| **chybí** | **4** | viz níže |

**Chybějící subjekty** (zjištěno jen z otevřených stránek, do dat se nezapisovaly):

| Subjekt | Co víme | Jak by dopadl podle Z1–Z4 |
|---|---|---|
| Longevitytech.fund | Podle [CzechCrunch z 19. 2. 2022](https://cc.cz/jak-zvratit-starnuti-testuje-i-klinika-v-praze-zalozil-ji-cesky-fond-pro-dlouhovekost-ktery-dava-na-boj-s-vekem-miliony/) „český fond pro dlouhověkost“, uzavřený fond v ČR se zhruba stovkou akcionářů, 16 mil. USD, asi 40 investic. | pravděpodobně VC v ČR; Z1 (IČO) a Z4 (investice od 2023) nejsou doloženy → nejméně kandidát |
| Y Soft Ventures | Investiční divize brněnské firmy Y Soft. Fond Y Soft Ventures II spolufinancují externí investoři ([CzechCrunch, 16. 7. 2019](https://cc.cz/brnensti-y-soft-ventures-spousti-novy-investicni-fond-do-startupu-nenovision-posilaji-20-milionu-korun/)). | kandidát: podíl Y Soft na kapitálu (pravidlo CVC) a aktivita za 36 měsíců nejsou doloženy |
| Koopeo Ventures | Web uvádí KOOPEO Ventures SE, IČ 05269113, Brno, a 8 firem v portfoliu bez dat ([koopeoventures.com](http://www.koopeoventures.com/)). Zdroj kapitálu neuveden. | Z1 splněno; Z3 a Z4 nedoloženy → kandidát, nebo vyloučení `bez_fondu` |
| Air Ventures | Profil Vestbee uvádí web airventures.eu, doména 13. 10. 2026 neexistuje (DNS). Další údaje jen z agregátorů. | nelze rozhodnout; možná `neaktivni` |

**Co z toho plyne:**

- Recall pilotu vůči redakčním seznamům je kolem 78 %. Ze 4 chybějících je jeden pravděpodobný VC v ČR (Longevitytech.fund), dva by byli kandidáti a jeden je nejasný. Žádný chybějící subjekt není zjevně ověřitelný bez dalšího hledání.
- Hledání pilotu stálo hlavně na CVCA a médiích z let 2024–2026. Seznamy z let 2021–2022 obsahují fondy, které v CVCA nejsou a v nových článcích se neobjevují.
- Seznamy jsou staré a mají jen 19 subjektů, interval je proto široký. Nejde o náhodný vzorek všech VC v ČR, ale o viditelné fondy.

## 4.11 Kolo R1-v2 – nová kontrola ověřených investorů (13. 10. 2026)

**Proč nové kolo.** Původní kontrola R1 (4.6) nebyla provedena podle metodiky:

- poznámky 8 z 22 kontrol VC se odvolávají na Crunchbase nebo LinkedIn (Crunchbase 6×, LinkedIn 3×), další na nejmenované „databáze“. Agregátory jsou podle docs/02 jen vodítko a LinkedIn není povolený zdroj;
- časy jsou zaokrouhlené na 5 minut (5–25 min), nejde tedy o měření;
- Springtide, Patero a Gain dostaly nejdřív verdikt TP a teprve podle pravidel byly opraveny na FP, FP a nejisté.

Původní výsledek 15/15 (v době kontroly) proto zůstává jen jako historie. Hlavní metrikou je kolo R1-v2.

**Postup.** Hodnotitel R1 prošel všech 16 tehdy ověřených investorů podle kontrolního listu [`review/kontrolni-list-r1-v2.md`](../review/kontrolni-list-r1-v2.md): Z1 v ARES, doklad Z3 a nejnovější doložená investice (Z4), jen povolené zdroje. Výsledky jsou v [`review/r1-v2-vysledky.csv`](../review/r1-v2-vysledky.csv) a v `data/reviews.csv` s `review_round` = `r1_v2`. Původní řádky mají `review_round` = `r1` a jinak se nezměnily. Jména fyzických osob v poznámkách hodnotitele nahradil agent popisem role, protože databáze osobní údaje neukládá (docs/01, 1.10).

**Výsledek** (`python -m investor_db metrics`, oddíl „Precision – kolo R1-v2“; stav v době kontroly, tedy všech 16 tehdy ověřených):

| Ukazatel | Výsledek | 95% Wilsonův interval |
|---|---|---|
| TP / FP / nejisté | 11 / 0 / 5 | |
| **Přísně, nejisté = nepotvrzeno** | **11/16 = 68,8 %** | 44,4 % – 85,8 % |
| **Jen rozhodnuté případy, TP / (TP + FP)** | **11/11 = 100,0 %** | 74,1 % – 100,0 % |
| Čas R1 | 59 min, 3,7 min na investora (1,2–7,8 min, nezaokrouhleno) | |

**Nejisté případy:**

| Investor | Důvod podle R1 |
|---|---|
| i&i Biotech Investments | Z1: IČO vede na Biotech Investments s.r.o., vazba na značku i&i není v rejstříku ověřena. |
| IP Lab Ventures | Z4: uložený fakt je závazek EIF do fondu, ne investice do firmy. |
| Startguide VC | Z3: web uvádí jen cílovou velikost SG One a naplnění 30 %. |
| StartupYard | Z4: uložený fakt je tentýž vehikl jako u Z3, datovaná investice chybí. |
| Tilia Impact Ventures | Z4: zdrojem investice do Flox Intelligence je agregátor. |

FP hodnotitel nenašel. Nejisté případy nejsou vyvrácené záznamy, ale vady dokladů. Jejich opravy jsou popsané v 4.12.

**Kapitál třetích osob (Z3).** U 5 z 11 TP (KAYA, Presto, Purple, Soulmates, Tachles) hodnotitel investory fondu ve zdroji nenašel („peníze třetích stran: nevím“). Pravidla Z3 to připouštějí, protože vyžadují fakt o fondu, ne doklad, kdo do něj vložil peníze (viz docs/01, 1.3).

## 4.12 Opravy po kontrole R1-v2 (13. 10. 2026)

U každé vady agent zkusil najít primární zdroj nejvýše jednou. Když se to nepovedlo, dostal investor status `kandidat` s důvodem v poznámce faktu.

| Investor | Vada podle R1-v2 | Co se stalo | Status |
|---|---|---|---|
| Reflex Capital | Z4 (grid.online, 2/2025) měl jako zdroj blog J&T Ventures. | Fakt `f-00147` přepojen na [CzechCrunch z 12. 2. 2025](https://cc.cz/hodne-jsem-se-ucil-a-podnikatelsky-jeste-nevyhral-rika-kratky-pro-startup-po-liftagu-ziskal-miliony/), který jmenuje Reflex Capital mezi investory; ověřeno proti surovému textu. | `overeny` |
| Tilia Impact Ventures | Z4 (Flox Intelligence, 2/2026) stojí na databázi investic (agregátor). | Primární zdroj (web Tilie, tisková zpráva) jedním hledáním nenalezen, výsledky vedly jen na databáze. Důvod je v poznámce `f-00084`. | **`kandidat`** |
| i&i Biotech Investments | IČO vede na Biotech Investments s.r.o., vazba na značku i&i neověřena. | Veřejný rejstřík (ARES VR) uvádí jako společníky jen holdingové společnosti s.r.o. bez názvu i&i. Vazbu dokládá jen web fondu, rejstřík ji nepotvrzuje. Důvod je v poznámce `f-00211`. | **`kandidat`** |
| IP Lab Ventures | Z4 je stejný fakt jako Z3 (závazek EIF). | Podle docs/01 (1.3) Z4 formálně splňuje nový fond za 36 měsíců: závazek EIF do IP Lab Ventures Fund z 23. 9. 2026. Zapsáno výslovně do `f-00153`. Datovaná investice fondu jedním hledáním nenalezena. | `overeny` |
| StartupYard | Z4 je stejný fakt jako Z3 (vehikl Batch 15). | Z4 formálně splňuje nový vehikl StartupYard Batch 15 s.r.o. zapsaný 14. 11. 2024. Zapsáno výslovně do `f-00228`. Datovaná investice z let 2024+ jedním hledáním nenalezena. | `overeny` |
| Startguide VC | Z3 je jen cílová velikost SG One s naplněním 30 %. | Pravidla Z3 to připouštějí (fakt o fondu s `fund_name`). Uvedeno v poznámce `f-00284`. | `overeny` |

**Nový trychtýř** (`python -m investor_db metrics`): 52 nalezených, **14 ověřených, 6 kandidátů, 32 vyloučených**. Precision kola R1-v2 (11/16 a 11/11) se nemění, protože se počítá ze stavu v době kontroly.

**Přepočtené hodnoty** podle 14 ověřených:

- pole zadání: sektor 13/14, fáze 14/14, ticket 12/14 (obě meze 9/14), kapitál 11/14, zdroj 14/14;
- doložená investice za 36 měsíců 11/14 (u IP Lab, StartupYard a Tachles Z4 plní nový fond, vehikl nebo souhrnný údaj o investicích);
- čas modelu na ověřený záznam 7,9 min místo 6,9 min (docs/03, 3.5 a 3.8);
- získatelné z veřejných zdrojů 14 z 20 VC subjektů = 70 % (dříve 80 %);
- capture–recapture: Chapman pro samotné ověřené 13,7 (interval 12,0–17,3), s kandidáty 9,5–29,3 (intervaly 9,0–49,0).

Tabulky v 4.6 a 4.7 zachycují stav ke dni své kontroly a nepřepisují se.

