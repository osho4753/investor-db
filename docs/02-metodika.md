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
| `rejstrik` | ano | Obchodní rejstřík, ARES | IČO, existence a forma právnické osoby |
| `vyrocni_zprava` | ano | Výroční zprávy a účetní závěrky ve Sbírce listin | Velikost fondu, investovaný kapitál, AUM, portfolio |
| `web_investora` | ano | Web VC značky, její tiskové zprávy | Sektory, fáze, ticket, portfolio, fondy |
| `asociace` | ne | Seznam členů národní VC asociace, Invest Europe | Hledání kandidátů, potvrzení typu investora |
| `media` | ne | Odborná a zpravodajská média | Potvrzení investic a uzavření fondů |
| `jine` | ne | Ostatní | Jen jako doplněk |

**Primární zdroj** pochází přímo od investora nebo od úřadu, který údaj eviduje. Sekundární zdroje slouží k hledání kandidátů a potvrzení, ale nesmí být jediným důkazem kritéria Z1.

Konkrétní URL se zapisují až při sběru dat a jejich dostupnost se zaznamenává v `data/search_log.csv`.

### Pravidla pro sběr (scraping)

Scraping je povolen, ale v pilotu se neimplementuje. Pro budoucí automatizaci platí: respektovat `robots.txt` a podmínky užití webů, omezit rychlost dotazů, cachovat odpovědi a identifikovat se v hlavičce `User-Agent`.

## 2.3 Postup

1. **Hledání kandidátů.** Systematicky se projdou seznamy (regulátor, asociace, média). Každý průchod je jeden řádek v `search_log.csv`: zdroj, datum, dotaz či filtr, počet nalezených subjektů.
2. **Deduplikace.** Kandidáti se porovnají podle IČO, domény webu a normalizovaného názvu (bez diakritiky, velikosti písmen a právní formy). Totéž kontroluje validační skript.
3. **Triáž.** Podle kritérií v [01-plan-a-kriteria.md](01-plan-a-kriteria.md) dostane subjekt status `kandidat`, nebo `vyloucen` s důvodem.
4. **Ověření faktů.** Pro každý údaj se zapíše fakt: hodnota, zdroj, datum přístupu, k jakému datu hodnota platí a stručný popis důkazu (kde přesně ve zdroji je a co říká). Primární zdroj má přednost.
5. **Přidělení statusu `overeny`.** Až když jsou doložena kritéria Z1–Z4 a validační skript projde.
6. **Ruční kontrola** – viz `docs/04-rucni-kontrola.md`.

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
| `investor_type` | vždy | `vc`, `pe`, `cvc`, `fond_fondu`, `statni_fond`, `business_angel`, `family_office`, `akcelerator`, `crowdfunding`, `jiny` |
| `country` | vždy | ISO 3166-1 alpha-2 země české právnické osoby, resp. sídla (`CZ`) |
| `registry_id` | `overeny` | IČO české právnické osoby (8 číslic, kontrolní součet) |
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

**Řízený slovník sektorů:** `ai`, `agritech`, `biotech`, `cleantech`, `deeptech`, `ecommerce`, `edtech`, `energetika`, `fintech`, `gaming`, `hardware`, `healthtech`, `kyberbezpecnost`, `media`, `mobilita`, `proptech`, `prumysl`, `software`, `spotrebitelske`, `sektorove_agnosticky`.

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
| `cilova_velikost_fondu` | Cílová velikost fondu (nikdy se nepřebírá do `total_fund_size`) | částka, `currency` a `fund_name` povinné |
| `registrace_regulator` | Registrace správce či fondu u regulátora | — |
| `dolozena_investice` | Doložená investice; hodnota je název portfoliové firmy | `value_as_of` = datum investice, povinné |

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
| `note` | Poznámka (např. omezení zdroje) |

### `reviews.csv` a `fact_reviews.csv` – ruční kontrola

Popsány v `docs/04-rucni-kontrola.md`. Vyplňuje je výhradně člověk.

## 2.5 Validace integrity

`python -m investor_db validate` kontroluje:

- formát a unikátnost identifikátorů ve všech tabulkách,
- povinná pole podle statusu a hodnoty řízených slovníků,
- formáty dat (ne v budoucnosti), URL, IČO (kontrolní součet), částek a měn, `typical_ticket_min ≤ typical_ticket_max`,
- vazby mezi tabulkami (fakt → investor, fakt → zdroj, kontrola → investor/fakt),
- že každá vyplněná hodnota v `investors.csv` má fakt se shodnou hodnotou (u částek i měnou),
- shodu `evidence_urls` se zdroji faktů a `last_verified_at` s daty přístupu,
- kritéria Z1–Z4 u záznamů `overeny`,
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
