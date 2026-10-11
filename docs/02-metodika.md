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

**Agregátory** (CB Insights, PitchBook, Caplight, Altss, Seedtable, Superscout, Crunchbase, Dealroom) slouží **jen jako vodítko** při hledání kandidátů a investic. Fakt se na ně nesmí odkazovat: každý fakt musí stát na primárním zdroji nebo na spolehlivém médiu, kde byl údaj skutečně nalezen. Validátor zdroj z domény agregátoru odmítne (`AGGREGATOR_NAMES` v `investor_db/schema.py`). Dva dřívější fakty z Caplightu byly nahrazeny články CzechCrunch (Startguide – Carebot, Depo – Flowpay).

**Nejednoznačné názvy** se identifikují podle domény webu a jmen týmu (např. jednatel v ARES = partner na webu). Pokud zdroj subjekt blíže neurčí, záznam zůstává `kandidat` s poznámkou o nejednoznačnosti.

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

Každý síťový požadavek z kódu projektu (`investor_db/rawtext.py`: `download`, `post_json`, `fetch_raw_text`) před stažením načte `robots.txt` daného webu přes `urllib.robotparser` a zakázanou cestu nestáhne (výjimka `RobotsDisallowedError`); mezi požadavky je prodleva. Pořadí „nejdřív robots.txt, pak stránka“ a odmítnutí zakázané cesty pokrývají testy v `tests/test_rawtext.py`. Ruční čtení stránek nástrojem asistenta tuto kontrolu automaticky neprovádí, proto se před prvním použitím nového webu `robots.txt` ověří ručně.

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

Subjekt je corporate VC, pokud **více než 50 % kapitálu fondu** pochází od jedné korporátní skupiny. Pravidlo se uplatňuje jednotně: je-li podíl doložen a převyšuje 50 %, subjekt se vylučuje s důvodem `cvc`; je-li doložen a nepřevyšuje 50 %, jde o VC; není-li rozložení kapitálu doloženo, ale zdroj uvádí vazbu na korporátní skupinu, status zůstává `kandidat`.

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
- Do `investors.csv` se přebírá hodnota z novějšího primárního zdroje; konflikt se popíše v `evidence_note` (včetně stáří zdrojů a konfliktu s agregátorem, který slouží jen jako vodítko).
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
| `investment_stages` | ne | `pre_seed`, `seed`, `serie_a`, `serie_b`, `growth`. Nepovinné doplňkové pole, není kritériem zařazení. |
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
| `oznamena_velikost_fondu` | Velikost fondu, u které zdroj nerozlišuje cíl a získanou částku (např. „launched a €40 million fund“, velikost uvedená při oznámení závazku LP). Nezapočítává se do kapitálu ani do cíle. | částka, `currency` a `fund_name` povinné |
| `fond_final_close` | Konečné uzavření fondu (final close) | částka, `currency` a `fund_name` povinné |
| `fond_uzavren` | Zdroj píše, že fond byl uzavřen, ale neupřesňuje, zda šlo o final close | částka, `currency` a `fund_name` povinné |
| `fond_first_close` | První uzavření fondu (first close) | částka, `currency` a `fund_name` povinné |
| `fond_zavazek_lp` | Vklad nebo závazek jednoho investora (LP) do fondu, např. EIF nebo NRI; jen část fondu | částka, `currency` a `fund_name` povinné |
| `fond_investovano` | Kolik fond už investoval | částka, `currency` a `fund_name` povinné |
| `fond_investovano_za_obdobi` | Kolik fond investoval jen za vymezené období (např. „během minulého roku“); dolní mez celkové investované částky | částka, `currency` a `fund_name` povinné |
| `pocet_fondu` | Kolik fondů investor má (výslovně, nebo pořadím posledního fondu, např. „pátý fond“) | kladné celé číslo; `value_as_of` = datum zdroje |
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
| `investor_id` | Jen u cíleného hledání údaje o jednom investorovi: odkaz do `investors.csv` |
| `target_field` | Jen u cíleného hledání: `investment_sectors`, `investment_stages`, `typical_ticket` nebo `kapital` |

Cílené hledání chybějícího údaje se zapisuje i tehdy, když nic nenajde (`results_count` = 0, poznámka „hledáno, nenalezeno“ a kde se hledalo). „Hledáno, nenalezeno“ je výsledek, ne mezera; metrika úplnosti ho vykazuje zvlášť. `investor_id` a `target_field` se vyplňují jen společně.

### `funds.csv` – jeden řádek = jedna částka fondu

| Sloupec | Povinný | Popis |
|---|---|---|
| `fund_id` | ano | `fd-0001` |
| `investor_id` | ano | Odkaz do `investors.csv` (správce, VC značka) |
| `fund_name` | ano | Název fondu; v rámci investora nejvýše jeden řádek s velikostí a jeden s investovanou částkou |
| `vintage` | ne | Rok založení nebo prvního uzavření (RRRR) |
| `amount` | ne | Částka fondu; prázdná, pokud zdroj doloží jen existenci fondu |
| `currency` | u částky | ISO 4217 |
| `amount_type` | u částky | `final_close`, `uzavren_bez_upresneni`, `first_close`, `cil`, `zavazek_jednoho_lp`, `investovano`, `investovano_za_obdobi` |
| `approx` | u částky | `ano` u přibližných formulací („téměř“, „přes“, „zhruba“), jinak `ne` |
| `amount_wording` | u `approx` = `ano` | Doslovná formulace ze zdroje, např. „téměř 55 mil. EUR“ |
| `value_as_of` | ne | Datum, ke kterému částka platí (datum uzavření, oznámení) |
| `fact_id` | ano | Fakt, který řádek dokládá |
| `fundraising_open` | ne | `ano`, pokud zdroje uvádějí, že fundraising fondu pokračuje (plánované navýšení, další close); `ne` nebo prázdné jinak |
| `conflict_note` | ne | Nevyřešený rozpor zdrojů u částky, měny nebo typu uzavření: verze, zdroje (fakty) a která verze je zapsána. Primární zdroj, který by rozpor rozhodl, nebyl nalezen. |

Každá částka má fakt se zdrojem a validátor kontroluje, že fakt patří stejnému investorovi a fondu, má stejnou částku a měnu a odpovídající typ: `final_close` dokládá `fond_final_close` nebo `total_fund_size`, `uzavren_bez_upresneni` dokládá `fond_uzavren` nebo `total_fund_size`, `first_close` dokládá `fond_first_close`, `cil` dokládá `cilova_velikost_fondu`, `zavazek_jednoho_lp` dokládá `fond_zavazek_lp` `investovano` dokládá `fond_investovano` a `investovano_za_obdobi` dokládá `fond_investovano_za_obdobi`. Fond bez částky dokládá libovolný fondový fakt (např. `informace_o_fondu`). Fond má nejvýše jeden řádek s velikostí (`final_close`, `uzavren_bez_upresneni`, `first_close`, `cil` nebo `zavazek_jednoho_lp`) a nejvýše jeden řádek s investovanou částkou (`investovano` nebo `investovano_za_obdobi`). Má-li fond doloženo více velikostí (např. first close a později final close), řádek nese nejlepší dostupný typ podle pořadí v definici získaného kapitálu; ostatní částky zůstávají jako fakty. Přibližné hodnoty se nevynechávají: číslo z formulace se zapíše s `approx` = `ano` a doslovnou formulací. Pravidlo pro `total_fund_size` v `investors.csv` (2.3) se tím nemění.

**Proč samostatná tabulka.** Správci mají více fondů (Lighthouse tři, Presto dva) a o každém zdroje uvádějí jiný typ částky. Dosud se to ztrácelo ve volném textu `informace_o_fondu` a do `investors.csv` se vešel jen jeden uzavřený fond. Tabulka fondů drží každou částku strukturovaně s typem a přesností, takže lze spočítat celkový kapitál a úplnost podle typu.

### Celkový investiční kapitál investora (odvozený, neukládá se)

*Definice platí od 11. 10. 2026. Předchozí verze přičítala cílovou velikost ke kapitálu. Cíl ale není kapitál, takže šlo o chybu definice.*

- **Získaný kapitál** je součet jen skutečně získaných částek fondů z `funds.csv`. U každého fondu se bere nejlepší typ: `final_close` > `uzavren_bez_upresneni` > `first_close`. Pokud je u fondu doložen jen `zavazek_jednoho_lp`, započte se jako dolní mez, protože fond získal nejméně tuto částku.
- **Cíl** (`cil`) se nikdy nepřičítá k získanému kapitálu a uvádí se zvlášť u fondů, které nemají získanou částku. Má-li investor jen cíl, je získaný kapitál **neznámý** a vedle se ukáže cíl.
- **Dolní mez.** Získaný kapitál je **bez** dolní meze jen tehdy, když platí všechny podmínky:
  - počet fondů správce doložený faktem `pocet_fondu` se shoduje s počtem fondů ve `funds.csv`,
  - všechny fondy mají získanou částku typu `final_close` nebo `uzavren_bez_upresneni` a žádná není přibližná,
  - žádný fond podle zdrojů ještě nesbírá peníze (`fundraising_open` = `ano`),
  - u žádného fondu není nevyřešený konflikt zdrojů (`conflict_note`).

  `first_close` a `zavazek_jednoho_lp` jsou vždy dolní mez. Pokud součet obsahuje závazek jednoho LP, ukazuje se zvlášť, jakou částku závazek tvoří. Konflikty zdrojů jsou v tabulce kapitálu ve zvláštním sloupci.
- **Investováno** (`investovano` ve `funds.csv` a `invested_capital` v `investors.csv`) a **AUM** se uvádějí zvlášť a do získaného kapitálu se nepřičítají. AUM může zahrnovat i jiné než vlastní fondy. U `invested_capital` za celého správce odkazuje tabulka kapitálu na fakt s doslovnou formulací. Pokud zdroj neuvádí, co částka zahrnuje (např. vlastní kapitál zakladatelů nebo spoluinvestice), je to uvedeno v poznámce faktu. Částka investovaná jen za určité období (`investovano_za_obdobi`) je v tabulce označena jako dolní mez investovaného kapitálu a do `invested_capital` se nezapisuje.
- **Měny se nesčítají.** Má-li investor fondy v různých měnách, uvádějí se součty zvlášť.
- **Typ částky podle formulace zdroje.** Typ se určuje jen z toho, co říká zdroj samotný, ne z kontextu ani z pozdějšího zdroje. „První kolo jsme uzavřeli na X“ je first close, „plánujeme investovat X“ je plán investic (`informace_o_fondu`), ne cíl fondu, a velikost bez rozlišení cíle a získané částky je `oznamena_velikost_fondu`. Pravidlo přibylo po kontrole kola `po_doplneni` (12. 10. 2026), kde šest ze sedmi nálezů bylo chybným typem částky.
- Pro požadavek zadání „celkový investiční kapitál“ se investor počítá jako vyplněný, pokud má získaný kapitál nebo AUM. Investoři jen s cílem se vykazují zvlášť.

Hodnoty počítá `python -m investor_db metrics`.

**`invested_capital` v `investors.csv`** se vyplní, jen pokud je doložený přesnou částkou ve stejné měně, jakou má řádek; ostatní (přibližné nebo v jiné měně) zůstávají ve `funds.csv` jako `investovano` a ve faktech.

**Sektory:** pokud zdroj uvádí, že fond není sektorově omezen, zapisuje se `sektorove_agnosticky`; jde o vyplněnou hodnotu, ne o mezeru.

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
| `activity` | `triaz` (rychlé vyloučení jedním faktem), `overeni` (plné ověření Z1–Z4), `doplneni` (dodatečné doplňování sektorů, ticketu a kapitálu u ověřených investorů, měřené odděleně od původního sběru) |
| `actor` | `model` (AI asistent), `R1`, `R2` |
| `minutes` | Čas v minutách, kladné číslo s nejvýše dvěma desetinnými místy |
| `logged_at` | Datum záznamu |
| `note` | Poznámka |

Čas modelu se měří časovými značkami začátku a konce práce na investorovi a zahrnuje čekání na načtení stránek. Není přímo srovnatelný s časem člověka, proto se čas modelu a čas člověka vykazují zvlášť. Čas ruční kontroly zapisují hodnotitelé do sloupce `review_minutes` v `reviews.csv` a `fact_reviews.csv`.

### `reviews.csv` a `fact_reviews.csv` – ruční kontrola

Popsány v `docs/04-rucni-kontrola.md`. Verdikty vyplňuje výhradně člověk. Sloupec `review_round` v `fact_reviews.csv` odlišuje kola kontroly faktů. `vzorek` je původní náhodný vzorek 36 faktů a jeho řádky se nemění. `po_doplneni` zahrnuje všechny fakty přidané doplňováním (f-00249 a dál), ne vzorek. Řádky kola zakládá `python -m investor_db fact-review-template --reviewer R1 --round po_doplneni --from-fact f-00249`.

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
| Přesnost faktů | správně / (správně + chybně) přes zkontrolované fakty; `nelze_overit` zvlášť. Vykazuje se zvlášť pro každé kolo (`vzorek`, `po_doplneni`). Původní kolo je náhodný vzorek (Cochran, 95 %, ±15 p. b., seed 2026); důvod volby ±15 p. b. (časová kapacita hodnotitele) viz [04-rucni-kontrola.md](04-rucni-kontrola.md#velikost-vzorku-faktů). |
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

## 2.8 Incidenty a poučení

| Incident | Dopad | Náprava | Poučení |
|---|---|---|---|
| **Porušení `robots.txt` na or.justice.cz.** Při prvním sběru jsem obchodní rejstřík četl přes cestu `/ias/` (vyhledávání a výpisy), kterou `robots.txt` zakazuje všem robotům. Zjištěno až při ověřování proti surovému textu, kdy kontrola `robots.txt` stažení odmítla. | 23 faktů a vyhledání entit vzniklo v rozporu s pravidly sběru. | Všechny fakty z or.justice.cz nahrazeny ověřením v ARES (surový JSON, `robots.txt` povoleno), původní fakty odstraněny (zůstávají v historii Gitu, commit `2fc5ece`). Zánik subjektu doložen vyhledávacím API ARES. Statutární orgány pro pravidlo (d) ověřeny proti surovému JSON veřejného rejstříku ARES. | `robots.txt` se kontroluje před prvním použitím každého webu, v kódu před každým požadavkem; rejstříková data se čerpají jen z ARES. |
| **Zamčený CSV soubor.** Zápis selhal na `data/investors.csv` (otevřený v Excelu) a později na `data/facts.csv` (neznámý proces). Ve druhém případě se zapsala jen část tabulek. | Data byla krátce nekonzistentní (validátor to odhalil); čas měření u dvou investorů musel být odhadnut. | Zápis z pomocných skriptů probíhá atomicky: všechny tabulky se nejdřív zapíší do dočasných souborů `*.tmp` a teprve pak se nahradí (`os.replace`) s opakováním při zamčení; `*.tmp` je v `.gitignore`. | CSV během práce neotevírat v Excelu (navíc může změnit kódování a oddělovač); po každém zápisu spustit `validate`. |
| **Nesoulad popisu commitu `c2fae0a`.** Popis uvádí rozšíření definice `mimo_definici_pilotu` o fondy digitálních aktiv, ale úprava se neprovedla, protože příkaz byl v řetězci za zápisem, který selhal. | Historie commitu je zavádějící; dokumentace byla do další dávky neúplná. | Úprava provedena a výslovně uvedena v commitu `c94022f`; pushnutá historie se nepřepisuje. | Úpravy dokumentace a dat nespojovat do jednoho řetězce příkazů; před commitem zkontrolovat `git diff` proti popisu. |
| **Šablona kontroly v nesouvisejícím commitu.** Soubor `data/reviews.csv` z dřívějšího běhu `review-template` se dostal do commitu `b7737ff` s kódem přes `git add -A`. | Commit míchá kód a data. | Popsáno v commitu `e9c570d`. | Přidávat soubory do commitu výslovně, ne `git add -A`. |
| **Příliš obecný důvod vyloučení.** Kód `mimo_definici_pilotu` slučoval corporate VC, fondy fondů, státní a dluhové fondy, fondy digitálních aktiv a otevřené smíšené fondy. Konkrétní znak byl jen v `evidence_note`. | Hodnotitel nemohl fakt `duvod_vylouceni` ověřit nezávisle, protože kontrolní list `evidence_note` záměrně neukazuje. | Kód rozdělen na `cvc`, `fond_fondu`, `statni_fond`, `dluhovy_fond`, `digitalni_aktiva` a `otevreny_smiseny_fond`. Sedm faktů a šest investorů dostalo kód podle již zapsaného `evidence_note`, nic se nově nedohledávalo. ID faktů ani vzorek kontroly se nezměnily. Validátor starý kód odmítá s nápovědou. | Hodnota faktu musí sama říkat, co se ověřuje; slovníky kódů navrhovat tak, aby každý kód odpovídal jednomu ověřitelnému znaku. |
| **Uložení CSV v Excelu.** Hodnotitel omylem uložil `reviews.csv` a `investors.csv` v Excelu: kódování Windows-1250, převedený formát dat a ořezané úvodní nuly v IČO. | Data by se načetla poškozená (neplatná IČO bez podpůrného faktu, jiný formát dat). | Validátor chybu zachytil před výpočtem metrik (IČO bez podpůrného faktu, neplatná data); soubory byly obnoveny a metriky se počítaly až z validních dat. | CSV upravovat v textovém editoru nebo importovat v Excelu se sloupci jako text a UTF-8; `metrics` záměrně odmítá nevalidní data. |
| **Nepovinné pole jako podmínka ověření.** Validátor vyžadoval u statusu `overeny` vyplněné `investment_stages`, metodika uváděla stádia jako doklad Z2. | Tachles splňoval Z1–Z4, ale zůstal kandidátem jen kvůli chybějícím stádiím. | Požadavek z validátoru odstraněn a pokryt testem (žádné doplňkové pole není pro `overeny` povinné); Z2 se posuzuje podle popisu strategie ve zdroji. | Kritéria zařazení a doplňková pole oddělovat; validátor má vynucovat jen Z1–Z4. |
| **Chyba hledání u Lighthouse Ventures.** Poznámka „poslední investice 2019“ vycházela z jediného článku z roku 2019, novější investice se nehledaly. | Ověřitelný investor zůstal kandidátem. | Doplněny investice z let 2025 (Tech.eu) a fondy z webu lhv.vc; poznámka u faktu opravena. | Absenci aktivity tvrdit jen po cíleném hledání novějších zdrojů. |
