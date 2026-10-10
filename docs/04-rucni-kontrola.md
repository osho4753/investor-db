# 4. Ruční kontrola a precision

Ruční kontrolu provádí výhradně člověk. Model, který data sbíral, kontrolní tabulky nevyplňuje – generuje jen prázdné šablony.

## 4.1 Hodnotitelé

| Kód | Kdo | Povinnost |
|---|---|---|
| `R1` | Zadavatel projektu | Povinná kontrola všech ověřených investorů a vzorku faktů |
| `R2` | Nezávislý hodnotitel | Volitelná; pokud data R2 chybí, metriky shody se nepočítají |

Aby byla kontrola R2 nezávislá, R2 vyplňuje svou šablonu bez znalosti verdiktů R1 (např. na samostatné větvi, která se sloučí až po dokončení obou kontrol).

## 4.2 Kontrola investorů → precision

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

Čas strávený kontrolou záznamu zapište v minutách do sloupce `review_minutes` (kladné celé číslo); slouží k odhadu nákladů škálování a vykazuje se odděleně od času modelu.

Chyby v doplňkových polích (např. špatný ticket) se nepromítají do precision záznamu – zachytí je kontrola faktů.

**Výpočet:**

- precision = TP / (TP + FP),
- pesimistická varianta = TP / (TP + FP + nejisté),
- 95% Wilsonův interval, protože u malého vzorku je normální aproximace nepřesná.

## 4.3 Kontrola faktů → přesnost faktů

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

## 4.4 Shoda hodnotitelů

Pokud existují verdikty R2, počítá se pro investory zkontrolované oběma hodnoteli:

- **prosté procento shody**, které se uvádí vždy,
- **Cohenovo κ**. Při malém vzorku a vysokém podílu TP je κ nestabilní (paradox kappa), proto se interpretuje jen spolu s procentem shody a rozborem jednotlivých neshod.

Neshody se rozeberou a rozhodnutí se zapíše do `note`; verdikty se zpětně nepřepisují.

## 4.5 Výsledky

Výsledky budou doplněny po provedení kontroly výstupem příkazu `python -m investor_db metrics`.
