# Měření tokenů: samostatná session, 13. 10. 2026

Měření spotřeby tokenů pro [docs/03](../docs/03-globalni-odhad.md), oddíl 3.5. Samostatná session Claude Code znovu ověřila 3 ověřené VC investory podle metodiky a skript `python -m investor_db tokens` sečetl spotřebu z jejího transkriptu.

## Postup

- **Výběr podle `effort_log.csv`** (čas modelu na ověření a doplnění, 16 ověřených):
  - snadný: Soulmates Ventures (`inv-0044`), 1,75 min, nejméně ze všech;
  - střední: Purple Ventures (`inv-0035`), 3,42 min, dolní medián (8. z 16);
  - složitý: Lighthouse Ventures (`inv-0037`), 13,77 min, nejvíce ze všech.
- **Oddělená pracovní kopie:** `git worktree add --detach` z commitu `244345a`. Z kopie byly smazány `data/`, `review/`, `ai-log/`, `site/`, `site_texts/`, `README.md`, `docs/03` a `docs/04`. Zůstal kód, testy, zadání, `docs/01` a `docs/02`. Po měření byla kopie odstraněna.
- **Známý únik:** `docs/02` v tabulce chyb zmiňuje web lhv.vc a fondy Lighthouse. Session tak u Lighthouse mohla mít nápovědu k doméně.
- **Spuštění:** `claude -p` s modelem `claude-opus-5-5` (stejný jako pilot), povolené nástroje jen `Read`, `Glob`, `Grep`, `WebSearch` a `WebFetch`. Zápis, Bash a subagenti byli zakázaní, takže session nemohla nic zapsat.
- **Session:** `aba0e2c0-8f8b-49c7-aaa0-aaf7bff8516d`, 28 kroků, 2 min 43 s (měřeno časem spuštění a konce příkazu, 00:45:01–00:47:47).
- **Předchozí pokus** (`c2cb4e98-…`) skončil hned chybou 401 kvůli neplatnému `ANTHROPIC_API_KEY` v prostředí, nespotřeboval žádné tokeny a do měření se nepočítá. Stejně tak krátký test přihlášení (`67f04ac6-…`).
- **Transkript** (JSONL, 0,5 MB) se do repozitáře neukládá, protože obsahuje texty stažených stránek. Tento soubor obsahuje prompt, výstup skriptu a odpověď session.

## Spotřeba (výstup `python -m investor_db tokens … --investors 3`)

Ceník: https://platform.claude.com/docs/en/about-claude/pricing (otevřeno 2026-10-13), webové vyhledávání 0.01 USD za dotaz.

| Model | Odpovědí | Vstup | Výstup (z toho thinking) | Cache čtení | Cache zápis 5m | Cache zápis 1h | Vyhledávání | Tokenů celkem | Cena |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | – | 260131 | 26305 (14030) | 0 | 0 | 0 | 7 | 286436 | 0.1092 USD |
| claude-opus-5-5 | 11 | 22 | 10242 (3345) | 714750 | 0 | 79620 | 0 | 804634 | 0.9848 USD |

Volání nástrojů: Read 2, ToolSearch 1, WebFetch 17, WebSearch 7.
Celkem 1091070 tokenů a 1.0940 USD.
Na investora (n = 3): 363690 tokenů a 0.3647 USD.

- Opus 5.5 je hlavní model session. Odpovědi se v JSONL opakují pro každý blok obsahu, skript je počítá jednou podle `message.id`.
- Haiku 5.5 používají nástroje WebFetch a WebSearch interně (shrnutí stránky, vyhledávání). Jeho spotřeba v odpovědích není, skript ji bere ze záznamu `cost-state` v transkriptu. Cena Haiku je počítaná v pásmu do 100 000 tokenů na požadavek. Záznam nerozlišuje jednotlivé požadavky, takže jde o předpoklad.
- Cena ze skriptu (1,0940 USD) se shoduje s cenou, kterou vypočítalo CLI Claude Code (`total_cost_usd` 1,0940036).

## Porovnání s daty pilotu (test reprodukovatelnosti)

| | Soulmates | Purple | Lighthouse |
|---|---|---|---|
| Status | `overeny` – shoda | `overeny` – shoda | `overeny` – shoda |
| IČO | shoda | shoda | shoda |
| Fáze | shoda | shoda | shoda |
| Ticket | shoda (max 3 mil. EUR) | shoda (250–400 tis. EUR) | shoda (200 tis.–1 mil. EUR) |
| Sektory | shoda | naše 5 obsaženo, session navíc 2 | naše 3 obsaženo, session navíc 2 |
| Kapitál | shoda (50 mil. EUR, `uzavren_bez_upresneni`) | 250 mil. Kč `investovano` shoda; „raised over CZK 700 million“ session nezařadila, my jako `uzavren_bez_upresneni` | rozdíl: 23 mil. EUR my jako `uzavren_bez_upresneni`, session jako AUM; session navíc závazek EIF 15 mil. EUR |
| Z4 | jiný doklad: session jen nový fond 2025, my investice 2024 | jiný doklad: session investice 2024, my investice 2025 | session novější investice (2026) než naše (2025) |

Status, IČO, fáze a ticket se shodují 3/3. Rozdíly jsou ve sektorech a hlavně v typu částky kapitálu, což odpovídá nálezům ruční kontroly (docs/04). Session neověřovala proti surovému textu stránek. Vlastní odhad času (~9 min) se od změřené délky (2 min 43 s) liší, jako čas se proto bere jen měření.

## Odpověď session (beze změn)

Všechny tři subjekty mají podle Z1–Z4 status **`overeny`**. U každého jsem IČO převzal z právní stránky jeho webu a potvrdil v ARES (spojení podle pravidla a). Do repozitáře jsem nic nezapsal a četl jsem jen docs/01 a docs/02. `robots.txt` jsem ručně zkontroloval jen u lhv.vc (vše povoleno), u ostatních webů ne.

### 1. Tabulka

| Subjekt | Status | IČO | Z1 | Z2 | Z3 | Z4 (datum) | Sektory | Fáze | Ticket | Kapitál (fond: částka, měna, typ) | Zdroje |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Soulmates Ventures** | overeny | 09789561 | ✓ Web (Legal) jmenuje Soulmates Ventures, osoba rizikového kapitálu, s.r.o. s IČO 09789561. ARES: stejný název, sídlo Rohanské nábřeží 693/10, Karlín, 186 00 Praha 8, vznik 2021-01-04. Adresa sedí s kanceláří na webu. | ✓ SFDR stránka: fond investuje do early-stage firem, hlavně Seed a Series A. Web: Seed/SA. | ✓ Soulmates Ventures Fund SICAV, a.s. (SFDR stránka). Vestbee: „has raised a €50 million fund“. | ✓ 2025-03-18, nový fond (Vestbee). Konkrétní investici za 36 měsíců jsem nedohledal. | cleantech; energetika; mobilita; agritech; edtech; healthtech (ze streamů air, water, energy, mobility, circular economy, food & agriculture, education, healthcare; mapování education a healthcare na tech kódy je můj výklad) | seed; serie_a | min neznámé, max 3 000 000 EUR („up to €3,000,000“) | Fond bez názvu v článku: 50 000 000 EUR, **uzavren_bez_upresneni** (zdroj píše „raised“, ne „closed“; hraniční, mohl by být i oznamena_velikost_fondu). AUM 62 mil. EUR je údaj z webu, ne typ fondu. | soulmatesventures.com, /legal/, /sfdr/, ARES 09789561, vestbee.com/…/soulmates-ventures-raises-50-m-fund |
| **Purple Ventures** | overeny | 05775574 | ✓ Patička webu: Purple Ventures s.r.o., ID no 05775574, Masarykova 26, Brno. ARES: Purple Ventures s.r.o., Masarykova 409/26, 602 00 Brno, vznik 2017-02-03. | ✓ Web: VC do pre-seed a seed, menšinové podíly („minority equity stakes“). | ✓ Druhý fond je otevřen externím investorům: 35 externích investorů (cc.cz 30. 1. 2025). Právní název fondu je neznámý. Fond spravuje PURPLE VENTURES II GP Sàrl v Lucembursku (SFDR stránka), takže česká osoba je jen poradce nebo provozovatel webu. | ✓ Fond II spuštěn 2024-03-26 (cc.cz). Investice 2024 (jen roční přesnost): Delta Green, Get Moments, Sloneek, Flowlance („loni“ v článku z 30. 1. 2025). | healthtech; energetika; media; kyberbezpecnost; edtech; ecommerce; software | pre_seed; seed | 250 000–400 000 EUR, počáteční ticket (web). Článek z 2024 uvádí přibližně 6–19 mil. Kč, to je jiná měna. | Fond II: 1 000 000 000 CZK, **cil** („Cílová částka je nastavena na miliardu korun“). Fond II: 40 mil. EUR podle formulace „klade za cíl proinvestovat“ = plán investic, tedy informace_o_fondu, ne cíl. Fond II: „raised over CZK 700 million“ (web) a 300 + 350 mil. Kč (cc.cz) jsou průběžné částky při otevřeném fundraisingu; žádný typ ze seznamu přesně nesedí, nejblíž je informace_o_fondu. Fond II: 250 mil. Kč, **investovano** (approx, „a quarter billion“). Fond I: 15 mil. EUR, **oznamena_velikost_fondu** („spuštěn v roce 2018 s 15 mil. EUR“). | purple-ventures.com, /sfdr-disclaimer, ARES 05775574, cc.cz/brnensti-purple-ventures-spousti-druhy-fond…, cc.cz/live/startupovi-purple-ventures-maji-jiz-35… |
| **Lighthouse Ventures** | overeny | 07500912 | ✓ Zásady ochrany údajů jmenují Lighthouse Ventures GP s.r.o., IČO 07500912. ARES: stejný název, sídlo Evropská 2758/11, Dejvice, 160 00 Praha 6, vznik 2018-09-27. Sídlo se shoduje s kanceláří na webu. Zásady uvádějí starší adresu Rybná 716/24. | ✓ Web: „early-stage venture capital“, Idea/Seed. | ✓ Lighthouse Seed Fund financovaný z Czech ESIF Fund of Funds (web). Podle cc.cz z 7. 6. 2019 má fond kapitál od EIF a soukromých investorů. | ✓ 2026-08-31, Hermetiq, pre-seed kolo 2,2 mil. USD (titulek v News na lhv.vc; celý článek jsem neotevřel). Lighthouse Fund II spuštěn 2024, jen roční přesnost (FAQ). | software; fintech; ai; prumysl; ecommerce (FAQ uvádí i robotics a industry tech) | pre_seed; seed | 200 000–1 000 000 EUR (web i FAQ) | „Lighthouse Ventures“ (2019): EIF 15 000 000 EUR, **zavazek_jednoho_lp**. Celkem „spravuje kapitál ve výši 23 milionů eur“ je spíš AUM, typ fondu ne. Lighthouse Fund II: částka neznámá. | lhv.vc, /privacy-policy/, /faq/, /news-and-events/, ARES 07500912, cc.cz/cesky-fond-lighthouse-ventures-vlozil…pekat-vision |

**Poznámky a nejistoty:**
- **Soulmates:** SFDR stránka jmenuje jako poradce „Soulmates Ventures a.s.“, ale ARES potvrzuje s.r.o. (09789561). IČO fondu SICAV jsem nedohledal.
- **Purple:** Fond II spravuje lucemburský GP. U Z1 se proto spoléhám na to, že česká Purple Ventures s.r.o. je poradenská společnost značky. Podíl skupiny Purple na kapitálu fondu je pod 50 %: 350 mil. Kč z více než 700 mil. Kč, takže nejde o CVC.
- **Lighthouse:** Kapitál z let 2019 jsem k Lighthouse Seed Fund přiřadil podle souvislosti. Článek fond jmenuje jen jako „Lighthouse Ventures“.
- **Čísla částek:** částky ani data jsem neověřil proti surovému textu stránek. Nespouštěl jsem žádné skripty, takže všechna čísla jsou jen ze shrnutí nástroje WebFetch.

### 2. Počty

- **Otevřené stránky (WebFetch):** 17 celkem, 17 unikátních. Patří sem 1× `robots.txt` (lhv.vc) a 3× ARES.
- **Webová vyhledávání:** 7. Stránky agregátorů z výsledků (Seedtable, Caplight a podobné) jsem použil jen jako vodítko k doménám a neotevíral je.
- **Volání ARES:** 3 (05775574, 09789561, 07500912), všechna REST `ekonomicke-subjekty/{ico}`.

### 3. Odhadovaný čas

Subjekty jsem zpracoval souběžně a časové značky jsem neměřil. Časy jsou proto jen hrubý odhad podílu na celé session, která trvala asi 9 minut:

| Subjekt | Odhad |
|---|---|
| Soulmates Ventures | ~3 min |
| Purple Ventures | ~3,5 min |
| Lighthouse Ventures | ~3 min |

Zdroje vyhledávání: [cc.cz – Soulmates](https://cc.cz/ostravsti-soulmates-ventures-chteji-nastartovat-zelene-startupy-investovat-planuji-pres-300-milionu-korun/), [Vestbee – Soulmates €50M](https://www.vestbee.com/blog/articles/soulmates-ventures-raises-50-m-fund), [cc.cz – Purple druhý fond](https://cc.cz/brnensti-purple-ventures-spousti-druhy-fond-do-startupu-chteji-proinvestovat-pres-miliardu-korun/), [cc.cz – Purple 35 investorů](https://cc.cz/live/startupovi-purple-ventures-maji-jiz-35-externich-investoru-a-650-milionu-na-investice/), [cc.cz – Lighthouse/Pekat Vision](https://cc.cz/cesky-fond-lighthouse-ventures-vlozil-vyssi-stovky-tisic-eur-do-brnenskeho-ai-startupu-pekat-vision/), [lhv.vc](https://lhv.vc/), [soulmatesventures.com](https://www.soulmatesventures.com/), [purple-ventures.com](https://purple-ventures.com/).

## Prompt

```
Jsi v pracovní kopii repozitáře investor-db. Úkol slouží k měření spotřeby tokenů a k testu reprodukovatelnosti.

ZÁKAZY
- Čti pouze docs/01-plan-a-kriteria.md a docs/02-metodika.md. Nečti data/, docs/03, docs/04, review/, README.md, ai-log/,
  historii gitu (git log, git show, git diff, git blame, jiné větve) ani soubory mimo tuto složku (včetně ~/.claude).
  Obsahují výsledky, které nesmíš opsat.
- Nic nezapisuj do repozitáře, necommituj a nespouštěj skripty, které zapisují do souborů. Výsledek vypiš jen do odpovědi.

ÚKOL
Nezávisle ověř tyto 3 subjekty podle kritérií Z1–Z4 (docs/01, oddíl 1.3) a pravidel sběru (docs/02):
1. Soulmates Ventures
2. Purple Ventures
3. Lighthouse Ventures

Pro každý zjisti:
- Z1: IČO české právnické osoby z ARES (REST API https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/...), název a sídlo.
- Z2: strategie rizikového kapitálu podle zdroje.
- Z3: fond s kapitálem třetích osob (název fondu).
- Z4: investice nebo nový fond za posledních 36 měsíců (datum a zdroj). Dnešní datum je 2026-10-13.
- Pole zadání: sektory a fáze (kódy ze slovníků v docs/02), typický ticket (min, max, měna),
  kapitál po fondech s typem částky podle formulace zdroje (final_close, uzavren_bez_upresneni, first_close, cil,
  zavazek_jednoho_lp, investovano, oznamena_velikost_fondu).

PRAVIDLA
- Jen bezplatné veřejné zdroje, respektuj robots.txt, neobcházej ochrany (403, CAPTCHA).
- Domény neodhaduj: web subjektu hledej přes vyhledávání nebo jiný zdroj.
- Každý údaj jen ze stránky, kterou jsi v této session skutečně otevřel. Jinak napiš „neznámé“.
- Typ částky urči jen z formulace zdroje, ne z kontextu.
- Komunikuj česky.

VÝSTUP
1. Tabulka: subjekt | status (overeny / kandidat / vyloucen) | IČO | Z1 | Z2 | Z3 | Z4 (datum) | sektory | fáze | ticket | kapitál (fond: částka, měna, typ) | zdroje (URL).
2. Počty: otevřené stránky (URL celkem a unikátních), webová vyhledávání, volání ARES.
3. Odhadovaný čas práce v minutách pro každý subjekt (od začátku do konce jeho ověřování).
```
