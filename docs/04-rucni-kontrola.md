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

Příkaz z aktuálního vzorku v `data/fact_reviews.csv` vygeneruje `review/kontrolni-list-faktu.md`. U každého faktu uvádí:

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
```

Příkaz doplní do `data/fact_reviews.csv` náhodný vzorek faktů. Hodnotitel otevře zdroj faktu a vyplní verdikt:

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

Výsledky budou doplněny po provedení kontroly výstupem příkazu `python -m investor_db metrics`.
