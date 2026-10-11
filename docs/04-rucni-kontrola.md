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
```

První příkaz založí kolo `vzorek`, tedy náhodný vzorek faktů z původního sběru. Pokud už hodnotitel vzorek má, nepřidá nic. Druhý příkaz založí kolo `po_doplneni` se všemi fakty od zadaného `fact_id`. Kolo je uvedeno ve sloupci `review_round` a přesnost se počítá pro každé kolo zvlášť. Hodnotitel otevře zdroj faktu a vyplní verdikt:

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

„Před“ je stav dat v commitu `25fff4c` (nový kód, data beze změny). „Po“ je stav po opravě definice kapitálu a třetím kole oprav (`ab775d8`). Kapitál se počítá podle opravené definice v [02-metodika.md](02-metodika.md): získaná částka fondu nebo AUM, cíl se nezapočítává.

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

Částky podle typu: uzavřený fond bez upřesnění 11, cílová velikost 4, first close 2, final close 1, závazek jednoho LP 1, investováno ve `funds.csv` 2 (Purple, i&i), AUM 2, `invested_capital` v `investors.csv` 3 (Depo, Tachles, Reflex).

### Přehled po investorech

Po zpřísnění pravidla (11. 10. 2026) je získaný kapitál u všech investorů dolní mez. Tensor má doložené oba fondy, ale fundraising druhého fondu pokračuje (plán navýšení na 1,5 mld. Kč). Credo má doloženo všech pět fondů, ale Stage 5 je first close a u Stage 3 a Stage 5 jsou nevyřešené konflikty zdrojů.

| Investor | Sektor | Ticket před → po | Získaný kapitál | Cíl (nezapočten) | Investováno / AUM | Hledáno, nenalezeno |
|---|---|---|---|---|---|---|
| Tensor Ventures | ✓ | beze změny | 20 mil. EUR + 1 mld. Kč, dolní mez (2 ze 2 fondů, fundraising Co-investment Fund pokračuje) | – | – | – |
| KAYA VC | – → ✓ | beze změny | 142 mil. EUR, dolní mez (ET3 bez částky, počet fondů nedoložen) | – | AUM 500 mil. USD | – |
| Depo Ventures | ✓ | beze změny | 129 mil. Kč, dolní mez; **z toho 94 mil. Kč závazek jednoho LP (NRI)**, uzavřený Grouport 35 mil. Kč | 545 mil. Kč | investováno 9 mil. EUR | – |
| i&i Biotech | ✓ | beze změny | 47 mil. EUR, dolní mez (přibližně) | – | investováno asi 7,4 mil. EUR | – |
| Credo Ventures | ✓ | beze změny | 146 mil. EUR + 188 mil. USD, dolní mez (5 z 5 fondů; Stage 5 first close; **konflikt**: měna Stage 3, typ uzavření Stage 5) | – | – | primární zdroj ke Stage 3 |
| Tilia Impact | ✓ | beze změny | 26 mil. EUR + 43 mil. Kč, dolní mez | – | – | – |
| Presto Ventures | ✓ | beze změny | 30 mil. EUR, dolní mez | 150 mil. EUR (Tech Horizons) | – | uzavření Tech Horizons |
| Rockaway Ventures | ✓ | – → – | 55 mil. EUR, dolní mez („necelých“) | – | – | ticket |
| Purple Ventures | – → ✓ | beze změny | 700 mil. Kč, dolní mez („přes“) | – | investováno čtvrt mld. Kč | – |
| Lighthouse Ventures | ✓ | beze změny | 23 mil. EUR, dolní mez (Fund II bez částky) | – | – | velikost Fund II |
| Reflex Capital | – → – | beze změny | 22 mil. EUR, dolní mez (fondy 1–2 neznámé) | – | investováno 150 mil. EUR za celého správce, **rozsah neznámý** (web: „€150M již investováno“) | sektor, rozsah 150 mil. EUR |
| Tachles | ✓ | – → – | 500 mil. Kč, dolní mez (first close, přibližně) | – | investováno 30 mil. Kč | ticket |
| Soulmates Ventures | ✓ | ?–3 mil. EUR beze změny | 50 mil. EUR, dolní mez (počet fondů nedoložen) | – | AUM 62 mil. EUR | dolní mez ticketu |
| Startguide VC | ✓ | – → ?–2 mil. EUR | neznámý | 26 mil. EUR (SG One a SG Two) | – | dolní mez ticketu |
| StartupYard | ✓ | beze změny | neznámý | – | – | kapitál |
| IP Lab Ventures | ✓ | – → ?–1 mil. EUR | neznámý | 1,2 mld. Kč | – | dolní mez ticketu |

### Konflikty a rozhodnutí při doplňování

- **KAYA – AUM 500 mil. USD.** Web neuvádí, co AUM zahrnuje. Vestbee (2025) uvádí hodnotu portfolia 350 mil. EUR, což je jiná veličina. AUM zůstává jako údaj správce a k získanému kapitálu se nepřičítá. Web dál uvádí „$85M Current Fund“, kdežto Vestbee first close Fund V 70 mil. EUR. Ticket je na webu v USD, ve Vestbee v EUR.
- **Tensor – druhý fond.** Ověřeno znovu: „více než miliardou korun“ v CzechCrunch (15. 5. 2024) je plán před získáním peněz, tedy cíl, vedle cíle „až 50 mil. EUR“. Forbes (18. 9. 2025) uvádí closing 1 mld. Kč („dokázal naraisovat miliardu korun během pěti měsíců“) s plánem navýšení na 1,5 mld. Kč. 1 mld. Kč je tedy získaný kapitál typu „uzavřen bez upřesnění“, ne final close. Fond Forbes nejmenuje, ztotožnění proběhlo podle pořadí („druhý fond“).
- **Credo – fondy 1–3.** Credo 1 má 18 mil. EUR, ale CzechCrunch (2019) uvádí start v roce 2011 a TechCrunch (2015) v roce 2010. Credo 2 mělo podle TechCrunch při uzavření v roce 2015 34 mil. EUR s cílem 40 mil. EUR, CzechCrunch (2019) uvádí 53 mil. EUR. Zapsán je pozdější údaj. Credo Stage 3 má podle money.pl (2020) 100 mil. USD, CzechCrunch a Vestbee uvádějí 100 mil. EUR. Zapsáno je USD, protože money.pl píše o získaných penězích, kdežto CzechCrunch o otevření fondu. Počet fondů 5 dokládá Tech.eu („their 5th fund“).
- **Credo Stage 5 – typ uzavření (konflikt).** Wikipedie (f-00030, f-00295) uvádí „first closing“ 88 mil. USD, ale zdroj, který cituje (Tech.eu, f-00266), first close neuvádí. TNW (23. 3. 2026, f-00296) píše o fondu „raised in a single closing“, tedy o jediném uzavření. Podle tvého rozhodnutí je ve `funds.csv` zapsán first close (konzervativní varianta). Rozpor je v `conflict_note` a ve sloupci Konflikt zdrojů v tabulce kapitálu.
- **Credo Stage 3 – měna (konflikt).** USD uvádějí money.pl (10. 3. 2020, f-00291; partner Habermann v citované tiskové zprávě „blisko 100 mln USD“) a Silicon Canals. EUR uvádějí CzechCrunch (8. 11. 2019), partner Andrej Kiska v rozhovoru (11. 11. 2019, f-00297) a Vestbee (2. 4. 2020). Primární zdroj (web Credo, newsroom, EIF) se nenašel a vyhledávání vrátilo jen norský Credo III, což je jiný subjekt (s-030). Rozpor je ve `funds.csv` označený a zapsána je nižší varianta 100 mil. USD. Součet Creda proto obsahuje sporný fond.
- **Lighthouse – první fond.** Článek uvádí 23 mil. EUR, rozpis vkladů ve stejném článku ale dává 20 mil. EUR.
- **IP Lab – velikost fondu.** CzechCrunch a MPO uvádějí cíl 1,2 mld. Kč, Lupa „až 40 mil. EUR (necelá miliarda Kč)“.
- **i&i – 50 mil. EUR.** EIF fond popisuje jako „€50 million fund“, ÚOCHB uvádí start s více než 45 mil. EUR a později přibližně 47 mil. EUR. 50 mil. EUR je proto vedeno jako cílová velikost.
- **Investovaný kapitál Purple** (čtvrt miliardy Kč) je ve `funds.csv` jako `investovano` v CZK, protože tam má měnu každá částka. V `investors.csv` zůstává prázdný, protože řádek je v EUR. Stejně je zapsána investovaná částka i&i (přibližně 7,4 mil. EUR).
- **Sektory Purple** jsou mapované na slovník: creator economy → `media`, security → `kyberbezpecnost`. Mapování je v `evidence_note`.
- **Reflex – sektory.** Sektory byly hledány přímo na reflexcapital.com (úvodní stránka cs i en, portfolio, kontakt). Web je neuvádí a píše jen „Investujeme zejména do lidí“. Sektorovou neomezenost výslovně neuvádí, proto se `sektorove_agnosticky` nezapisuje a hledání je v `search_log` (s-029). Na úvodní stránce je doslovně „€150M již investováno“ (anglicky „€150M invested“), doplněno jako `invested_capital` (f-00294). Žádný zdroj neuvádí, co částka zahrnuje (s-031). Forbes uvádí, že Reflex začal jako family office, kde Ondřej Fryc investoval vlastní prostředky. Částka je řádově vyšší než získaný kapitál známých fondů (třetí fond 22 mil. EUR, druhý „podobný“), takže pravděpodobně nejde jen o fondy. Zdroj to ale neříká, proto je v tabulce kapitálu uvedena jako údaj za celého správce s nejasným rozsahem.

### Pracnost

Doplňování trvalo modelu 13,0 min běhu nástrojů v první fázi (16 investorů, medián 0,8 min) 7,6 min ve druhé fázi (Credo, Tensor, Reflex, Purple, i&i; společný čas rozdělen rovnoměrně po 1,51 min) a 3,3 min ve třetí fázi (Tensor, Credo, Reflex; po 1,10 min). Je evidováno v `effort_log` jako činnost `doplneni`, odděleně od původního ověření (80,1 min). Cílená hledání bez výsledku jsou v `search_log` jako s-018 až s-031.

### Nové fakty ke kontrole

Doplňování přidalo 49 faktů (f-00249 až f-00297). Všechny jsou v `fact_reviews.csv` jako samostatné kolo `po_doplneni`, kontroluje se každý fakt, ne vzorek. Původní vzorek 36 faktů (kolo `vzorek`) zůstal beze změny, přibyl mu jen sloupec `review_round`. Přesnost faktů se vykazuje zvlášť pro obě kola. Hodnoty v 4.6 platí pro kolo `vzorek`, kolo `po_doplneni` čeká na kontrolu R1. U f-00036, f-00037 a f-00038 (KAYA, původní sběr) přibyla jen poznámka v `evidence_note`. U f-00252 (Tensor) přibyla poznámka o ověření, že jde o získaný kapitál.
