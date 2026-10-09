# 2. Metodika vyhledávání a ověřování

## 2.1 Přehled procesu

```
hledání kandidátů ─► deduplikace ─► triáž (kandidat / vyloucen) ─► ověření faktů ─► status overeny
        │                                                                 │
        └── data/search_log.csv                         data/facts.csv + data/sources.csv
                                                                          │
                                         ruční kontrola (R1, volitelně R2) ─► metriky
```

Každý krok zanechává stopu v CSV souborech, takže proces lze zopakovat a zkontrolovat.

## 2.2 Zdroje

Používají se pouze bezplatné veřejné zdroje. Placené databáze (Dealroom, Crunchbase Pro, PitchBook) se nepoužívají.

| Typ zdroje (`source_type`) | Primární | Příklady pro ČR | Co dokládá |
|---|---|---|---|
| `regulator` | ano | Seznamy regulovaných subjektů ČNB, registr ESMA | Registrace správce či fondu, právní správce |
| `rejstrik` | ano | ARES – REST API (základní údaje, veřejný rejstřík včetně statutárních orgánů, vyhledávání podle jména) | IČO, existence, forma a statutární orgán právnické osoby |
| `vyrocni_zprava` | ano | Výroční zprávy a účetní závěrky ve Sbírce listin | Velikost fondu, investovaný kapitál, AUM, portfolio |
| `web_investora` | ano | Web VC značky, její tiskové zprávy | Sektory, fáze, ticket, portfolio, fondy |
| `asociace` | ne | Seznam členů národní VC asociace, Invest Europe | Hledání kandidátů, potvrzení typu investora |
| `media` | ne | Odborná a zpravodajská média | Potvrzení investic a uzavření fondů |
| `jine` | ne | Ostatní | Jen jako doplněk |

**Primární zdroj** pochází přímo od investora nebo od úřadu, který údaj eviduje. Sekundární zdroje slouží k hledání kandidátů a potvrzení, ale nesmí být jediným důkazem kritéria Z1.

Konkrétní URL se zapisují až při sběru dat a jejich dostupnost se zaznamenává v `data/search_log.csv`.

**Obchodní rejstřík na or.justice.cz se nepoužívá:** jeho `robots.txt` zakazuje cestu `/ias/` (vyhledávání i výpisy). Při prvním sběru byla tato cesta omylem použita; všechny takto získané fakty byly nahrazeny ověřením v ARES, jehož API `robots.txt` povoluje. Sbírka listin (výroční zprávy) leží pod stejnou zakázanou cestou, a proto se v pilotu nevyužívá.

### Pravidla pro sběr faktů

- Každý fakt pochází ze stránky nebo dokumentu, který byl při sběru **skutečně otevřen**. Nic se nedoplňuje z paměti, obecné znalosti ani odhadem.
- Pokud se stránka nenačte nebo údaj neobsahuje, hodnota zůstává neznámá a neúspěch se zapíše do poznámky v protokolu hledání.
- `accessed_at` je skutečné datum přístupu.
- `evidence_note` stručně parafrázuje, co a kde na stránce je; delší pasáže se necitují.
- Stránky se čtou ručně po jedné, bez hromadného stahování.

### Pravidla pro sběr (scraping)

Scraping je povolen, ale v pilotu se neimplementuje. Pro budoucí automatizaci platí: respektovat `robots.txt` a podmínky užití webů, omezit rychlost dotazů, cachovat odpovědi a identifikovat se v hlavičce `User-Agent`.

## 2.3 Postup

1. **Hledání kandidátů.** Systematicky se projdou seznamy (regulátor, asociace, média). Každý průchod je jeden řádek v `search_log.csv`: zdroj, datum, dotaz či filtr, počet nalezených subjektů a čas. Kandidátem se stane každý subjekt, který otevřená stránka popisuje jako investiční fond či VC investora, nebo jako investora v pre-seed či seed kole. Investoři zmínění jen jako účastníci pozdějších kol (série B a výše) a subjekty, které stránka sama označuje za zahraniční investory v kolech, kandidáty nejsou; uvádějí se v poznámce průchodu. Typ a země kandidáta se vyplní jen tehdy, uvádí-li je zdroj, jinak zůstávají prázdné až do ověření.
2. **Deduplikace.** Kandidáti se porovnají podle IČO, domény webu a normalizovaného názvu (bez diakritiky, velikosti písmen a právní formy). Totéž kontroluje validační skript.
3. **Triáž.** Podle kritérií v [01-plan-a-kriteria.md](01-plan-a-kriteria.md) dostane subjekt status `kandidat`, nebo `vyloucen` s důvodem.
4. **Ověření faktů.** Pro každý údaj se zapíše fakt: hodnota, zdroj, datum přístupu, k jakému datu hodnota platí a stručný popis důkazu (kde přesně ve zdroji je a co říká). Primární zdroj má přednost.
5. **Přidělení statusu `overeny`.** Až když jsou doložena kritéria Z1–Z4 a validační skript projde.
6. **Ruční kontrola** – viz `docs/04-rucni-kontrola.md`.

### Spojení značky s českou právnickou osobou (Z1)

Česká právnická osoba se přiřadí ke značce jen na základě jednoho z těchto doložených spojení:

- **(a)** web značky (impresum, kontakty, zásady ochrany osobních údajů) nebo její profil v asociaci subjekt jmenuje či uvádí jeho IČO a obchodní rejstřík či ARES subjekt potvrzuje;
- **(b)** obchodní firma obsahuje název značky a její sídlo se shoduje s adresou, kterou zveřejňuje značka, její profil v asociaci nebo zdroj o investorovi; odpovídá-li více subjektů, vybere se ten, jehož název ukazuje na poradenskou či správcovskou roli, a ostatní se uvedou v `evidence_note`;
- **(d)** osoby ve statutárním orgánu subjektu (podle obchodního rejstříku nebo ARES) se shodují s partnery či týmem, které jmenuje web značky nebo zdroj o investorovi.

Samotná shoda obchodní firmy s názvem značky **nestačí** (dřívější pravidlo c bylo zrušeno: u Techstars by přiřadilo nesouvisející firmu stejného jména). Nelze-li použít žádné z pravidel, Z1 zůstává nedoloženo a subjekt zůstává `kandidat`.

### Corporate VC

Subjekt je corporate VC, pokud **více než 50 % kapitálu fondu** pochází od jedné korporátní skupiny. Pravidlo se uplatňuje jednotně: je-li podíl doložen a převyšuje 50 %, subjekt se vylučuje jako `mimo_definici_pilotu`; je-li doložen a nepřevyšuje 50 %, jde o VC; není-li rozložení kapitálu doloženo, ale zdroj uvádí vazbu na korporátní skupinu, status zůstává `kandidat`.

### Velikost fondu (`total_fund_size`)

Přijímá se výslovné tvrzení v minulém čase, že fond byl uzavřen s danou velikostí, z webu investora, tiskové zprávy nebo spolehlivého média (např. „uzavřel třetí fond ve výši 22 mil. EUR“). Nepřijímá se first close, druhé či průběžné uzavření, cílová velikost, přibližné formulace („téměř“, „až X“) ani souhrn závazků. Do `total_fund_size` patří poslední takto uzavřený fond; ostatní údaje o fondech zůstávají ve faktu `informace_o_fondu`.

### Aktivita (Z4)

Z4 doloží buď investice do firmy (`dolozena_investice`), nebo nový fond: fakt `informace_o_fondu`, `total_fund_size` či `cilova_velikost_fondu` s `value_as_of` v posledních 36 měsících.

### Ověření proti surovému textu

Stránky se při sběru čtou nástrojem, který vrací shrnutí obsahu vytvořené jazykovým modelem, nikoli doslovný text. Proto se u všech peněžních částek a dat investic hodnota ověřuje proti surovému textu stránky: `python -m investor_db raw-text URL --grep VÝRAZ` stáhne stránku přes `urllib` (s kontrolou `robots.txt`, identifikací v hlavičce `User-Agent` a prodlevou mezi požadavky), převede HTML na text a vyhledá v něm hodnotu v obvyklých zápisech (např. „1–5M“, „3,3 mil.“, „5. 11. 2025“, „November 5, 2025“). Stažený text se ukládá do dočasné složky mimo repozitář. Výsledek se zapíše na konec `evidence_note` ve tvaru „Ověřeno proti surovému textu: ano“ nebo „ne (důvod)“.

**Omezení:** stránky vykreslované JavaScriptem, stránky za ochranou proti robotům nebo s HTTP chybou surový text neposkytnou; hodnota pak zůstává ověřená jen přes shrnutí a je tak označena. Vyhledávání zápisů je heuristické – nález ve stejné stránce ještě nezaručuje, že se hodnota vztahuje k tomuto investorovi, a nenalezení může znamenat jiný zápis. Rozhodující zůstává ruční kontrola faktů.

### Data s měsíční přesností

Uvádí-li zdroj jen měsíc a rok (např. „duben 2026“), zapíše se `value_as_of` jako první den měsíce a `evidence_note` výslovně uvede měsíční přesnost.

### Konflikty mezi zdroji

- Všechny protichůdné hodnoty se zapíšou jako samostatné fakty; žádný se nemaže.
- Do `investors.csv` se přebírá hodnota z novějšího primárního zdroje; konflikt se popíše v `evidence_note`.
- Hodnoty se nikdy neprůměrují, nedopočítávají ani nepřevádějí mezi měnami.

## 2.4 Datové schéma

Všechny soubory jsou v `data/`, kódování UTF-8, oddělovač čárka, konce řádků LF. Data jsou ve formátu ISO 8601 (`RRRR-MM-DD`). Částky jsou nezáporná čísla s desetinnou tečkou a bez oddělovačů tisíců. Hodnoty s více položkami se oddělují středníkem `;`. **Prázdná buňka znamená neznámou hodnotu** – nula ani odhad se místo neznámé hodnoty nepoužívá.

### `investors.csv` – jeden řádek = jedna VC značka

| Sloupec | Povinný | Popis |
|---|---|---|
| `investor_id` | vždy | `inv-0001` |
| `name` | vždy | Název VC značky |
| `investor_type` | `overeny`, `vyloucen` | `vc`, `pe`, `cvc`, `fond_fondu`, `statni_fond`, `business_angel`, `family_office`, `akcelerator`, `crowdfunding`, `jiny` |
| `country` | `overeny`, `vyloucen` | ISO 3166-1 alpha-2 země české právnické osoby, resp. sídla (`CZ`) |
| `registry_id` | `overeny` | IČO vlastní české právnické osoby značky – správcovské či poradenské společnosti nebo fondu (8 číslic, kontrolní součet). **Nikdy IČO licencovaného třetího správce**, ten se ukládá jako fakt `pravni_spravce`; jinak by se různé značky jednoho správce jevily jako duplicity. |
| `website` | ne | URL webu značky |
| `investment_sectors` | ne | Řízený slovník, viz níže |
| `investment_stages` | `overeny` | `pre_seed`, `seed`, `serie_a`, `serie_b`, `growth` |
| `typical_ticket_min`, `typical_ticket_max` | ne | Typická velikost **jedné investice** do jedné firmy |
| `currency` | při částce | ISO 4217; platí pro všechny částky v řádku |
| `total_fund_size` | ne | Velikost **posledního fondu při final close**. Cílová velikost sem nepatří. |
| `assets_under_management` | ne | Celkový majetek spravovaný značkou napříč fondy (AUM) |
| `invested_capital` | ne | Kumulativně skutečně investovaný kapitál |
| `verification_status` | vždy | `overeny`, `kandidat`, `vyloucen` |
| `exclusion_reason` | `vyloucen` | Důvod vyloučení; u ostatních statusů prázdné |
| `evidence_urls` | `overeny` | **Odvozené** – URL všech zdrojů faktů záznamu oddělené `;`. Validátor kontroluje shodu s `facts.csv`. |
| `last_verified_at` | `overeny` | Datum posledního ověření; nesmí být starší než nejnovější `accessed_at` faktů záznamu |

Velikost fondu, AUM, investovaný kapitál a velikost jednotlivé investice jsou **čtyři různé veličiny** a nesmí se zaměňovat ani dopočítávat jedna z druhé.

**Měny:** Jeden řádek má jednu měnu. Pokud je některá částka doložena jen v jiné měně, do `investors.csv` se nezapíše a zůstane pouze ve `facts.csv`. Počet takových hodnot se vykazuje jako metrika (omezení dat).

**Řízený slovník sektorů:** `ai`, `agritech`, `biotech`, `cleantech`, `deeptech`, `ecommerce`, `edtech`, `energetika`, `fintech`, `gaming`, `hardware`, `healthtech`, `kyberbezpecnost`, `media`, `mobilita`, `proptech`, `prumysl`, `software`, `spotrebitelske`, `obrana_bezpecnost`, `cestovani`, `logistika`, `jine`, `sektorove_agnosticky`.

### `facts.csv` – jeden řádek = jeden doložený fakt

| Sloupec | Povinný | Popis |
|---|---|---|
| `fact_id` | ano | `f-00001` |
| `investor_id` | ano | Odkaz do `investors.csv` |
| `field` | ano | Jméno pole z `investors.csv` nebo doplňkový typ faktu (viz níže) |
| `value` | ano | Hodnota ve stejném formátu jako v `investors.csv` |
| `currency` | u částek | ISO 4217; u nepeněžních faktů prázdné |
| `fund_name` | u fondových faktů | Název fondu, ke kterému se fakt vztahuje |
| `value_as_of` | ne | Datum, ke kterému hodnota platí (např. datum final close, datum investice) |
| `source_id` | ano | Odkaz do `sources.csv` |
| `accessed_at` | ano | Datum přístupu ke zdroji |
| `evidence_note` | ano | Stručný popis důkazu: kde ve zdroji je a co přesně říká |

Doplňkové typy faktů:

| `field` | Význam | Pravidla |
|---|---|---|
| `pravni_spravce` | Právní správce či administrátor fondu | `fund_name` povinné |
| `informace_o_fondu` | Doložená existence fondu a jeho stav, který nepatří do jiného pole (např. first close, ročník, spuštění) | `fund_name` povinné; hodnota je stručný popis |
| `cilova_velikost_fondu` | Cílová velikost fondu (nikdy se nepřebírá do `total_fund_size`) | částka, `currency` a `fund_name` povinné |
| `registrace_regulator` | Registrace správce či fondu u regulátora | — |
| `dolozena_investice` | Doložená investice; hodnota je název portfoliové firmy | `value_as_of` = datum investice, povinné |
| `duvod_vylouceni` | Doklad důvodu vyloučení; hodnota je kód z `exclusion_reason` | povinný u každého vyloučeného subjektu |

Fakt `total_fund_size` musí mít vyplněné `fund_name`.

### `sources.csv` – jeden řádek = jeden zdroj

| Sloupec | Popis |
|---|---|
| `source_id` | `src-0001` |
| `url` | Unikátní URL zdroje |
| `publisher` | Kdo zdroj vydal |
| `source_type` | Typ zdroje podle tabulky v 2.2; primárnost se z něj odvozuje |

### `search_log.csv` – protokol hledání

| Sloupec | Popis |
|---|---|
| `search_id` | `s-001` |
| `searched_at` | Datum hledání |
| `source_url` | Prohledaný seznam či stránka |
| `query` | Dotaz, filtr nebo popis průchodu |
| `results_count` | Počet nalezených relevantních subjektů |
| `minutes` | Čas strávený průchodem zdroje v minutách (kladné číslo, nejvýše dvě desetinná místa) |
| `note` | Poznámka (např. omezení zdroje, nenačtená stránka) |

### `candidate_sources.csv` – kde byl kandidát nalezen

| Sloupec | Popis |
|---|---|
| `investor_id` | Odkaz do `investors.csv` |
| `search_id` | Průchod v `search_log.csv`, ve kterém byl subjekt nalezen |

Jeden subjekt může být nalezen ve více průchodech. Každý subjekt v `investors.csv` musí mít alespoň jeden řádek. Tabulka slouží k deduplikaci a k odhadu celkového počtu metodou capture–recapture.

### `effort_log.csv` – měření pracnosti

Čas hledání se eviduje u průchodu zdrojem v `search_log.csv`, protože jeden průchod najde více kandidátů a jeho čas nelze poctivě rozpočítat. Čas práce na konkrétním investorovi se eviduje zde:

| Sloupec | Popis |
|---|---|
| `investor_id` | Odkaz do `investors.csv` |
| `activity` | `triaz` (rychlé vyloučení jedním faktem), `overeni` (plné ověření Z1–Z4) |
| `actor` | `model` (AI asistent), `R1`, `R2` |
| `minutes` | Čas v minutách, kladné číslo s nejvýše dvěma desetinnými místy |
| `logged_at` | Datum záznamu |
| `note` | Poznámka |

Čas modelu se měří časovými značkami začátku a konce práce na investorovi a zahrnuje čekání na načtení stránek. Není přímo srovnatelný s časem člověka, proto se čas modelu a čas člověka vykazují zvlášť. Čas ruční kontroly zapisují hodnotitelé do sloupce `review_minutes` v `reviews.csv` a `fact_reviews.csv`.

### `reviews.csv` a `fact_reviews.csv` – ruční kontrola

Popsány v `docs/04-rucni-kontrola.md`. Vyplňuje je výhradně člověk.

## 2.5 Validace integrity

`python -m investor_db validate` kontroluje:

- formát a unikátnost identifikátorů ve všech tabulkách,
- povinná pole podle statusu a hodnoty řízených slovníků,
- formáty dat (ne v budoucnosti), URL, IČO (kontrolní součet), částek a měn, `typical_ticket_min ≤ typical_ticket_max`,
- vazby mezi tabulkami (fakt → investor, fakt → zdroj, kontrola → investor/fakt),
- že každá vyplněná hodnota v `investors.csv` má fakt se shodnou hodnotou (u částek i měnou); výjimkou je `name` u statusů `kandidat` a `vyloucen`, kde název stačí k identifikaci a jeho původ je v protokolu hledání,
- shodu `evidence_urls` se zdroji faktů a `last_verified_at` s daty přístupu,
- kritéria Z1–Z4 u záznamů `overeny` a doložení důvodu vyloučení faktem u záznamů `vyloucen`,
- duplicity investorů (IČO, doména, normalizovaný název), faktů a zdrojů.

Pole `investor_type` a `country` jsou klasifikace odvozené z ostatních faktů (typ ze strategie, země z IČO), proto pro ně samostatný fakt není vyžadován.

## 2.6 Metriky

`python -m investor_db metrics` počítá:

| Metrika | Definice |
|---|---|
| **Precision** | TP / (TP + FP) přes záznamy `overeny` zkontrolované R1; verdikt `nejiste` se vykazuje zvlášť a v pesimistické variantě se počítá jako FP. Uvádí se 95% Wilsonův interval. |
| Shoda hodnotitelů | Jen pokud existují data R2: prosté procento shody a Cohenovo κ. Při malém vzorku a vysokém podílu TP je κ nestabilní, proto se vždy uvádí i procento shody. |
| Přesnost faktů | správně / (správně + chybně) přes zkontrolované fakty; `nelze_overit` zvlášť. |
| Úplnost polí | Podíl vyplněných hodnot každého pole u záznamů `overeny`. |
| Primární zdroje | Podíl záznamů `overeny`, jejichž IČO je doloženo primárním zdrojem; podíl všech faktů z primárních zdrojů. |
| Doložení investiční činnosti | Podíl záznamů `overeny` s doloženou investicí za posledních 36 měsíců. |
| Aktuálnost | Podíl záznamů `overeny` ověřených v posledních 12 měsících. |
| Duplicity | Počet skupin potenciálních duplicit a počet záznamů vyloučených jako `duplicita`. |
| Hodnoty jen ve `facts.csv` | Počet peněžních hodnot, které nebyly převzaty do `investors.csv`, protože jsou v jiné měně než řádek. |
| Trychtýř | Počet nalezených subjektů a výsledné statusy podle úrovně zpracování (nezpracováno, rychlá triáž, plné ověření). |
| Pracnost | Zvlášť model a člověk: minuty hledání, minuty na investora podle činnosti (součet, průměr, medián), minuty ruční kontroly. |
| Odhad celkového počtu | Capture–recapture pro každou dvojici průchodů hledání (viz 2.7). |

## 2.7 Odhad celkového počtu VC v ČR (capture–recapture)

Z toho, kolik subjektů se objevuje ve dvou různých průchodech hledání, lze odhadnout, kolik jich existuje celkem, včetně těch, které žádný průchod nenašel. Pro každou dvojici průchodů s počty nalezených subjektů n₁, n₂ a překryvem m:

- Lincoln–Petersen: N = n₁ · n₂ / m (pro m = 0 nedefinováno),
- Chapmanova korekce (méně zkreslená u malých vzorků): N = (n₁ + 1)(n₂ + 1) / (m + 1) − 1,
- rozptyl Chapmanova odhadu: (n₁ + 1)(n₂ + 1)(n₁ − m)(n₂ − m) / ((m + 1)² (m + 2)); 95% interval je N ± 1,96 · √rozptyl, dolní mez nejméně rovna počtu pozorovaných subjektů.

Odhad se počítá pro dvě populace: jen ověření investoři a ověření spolu s dosud otevřenými kandidáty. Do výpočtu vstupují jen průchody, které v dané populaci našly alespoň 5 subjektů (`MIN_SEARCH_SIZE` v `investor_db/metrics.py`); u menších zdrojů (jednotlivé tiskové zprávy) je odhad degenerovaný.

**Omezení:** Metoda předpokládá nezávislé zdroje a stejnou pravděpodobnost nalezení každého subjektu. Ani jedno neplatí – sekundární zdroje (média, Wikipedie) přebírají hlavně viditelné fondy a navzájem se citují, takže překryv je vyšší než u nezávislých zdrojů. Odhad je proto **spíše dolní mezí** skutečného počtu a slouží jen k řádovému posouzení pokrytí pilotu.
