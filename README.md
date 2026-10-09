# Investor Intelligence Database

Reprodukovatelný proces vyhledávání, klasifikace a ověřování reálných investorů z veřejně dostupných dat. Hlavní prioritou je spolehlivost dat, ne počet záznamů.

**Pilot:** venture kapitálové (VC) značky s českou právnickou osobou, 20–30 kandidátů.

## Principy

- Pouze bezplatné veřejné zdroje.
- CSV soubory v Gitu jsou jediným zdrojem pravdy; integritu hlídá validační skript a testy.
- Každá vyplněná hodnota je doložena faktem se zdrojem, datem přístupu a popisem důkazu.
- Neznámé hodnoty zůstávají prázdné; nic se neodhaduje ani nepřepočítává mezi měnami.
- Ruční kontrolu provádí člověk, ne model, který data sbíral.

## Povinné výstupy

| # | Výstup | Kde ho najít |
|---|---|---|
| 1 | Plán výzkumu a kritéria zařazení/vyloučení | [docs/01-plan-a-kriteria.md](docs/01-plan-a-kriteria.md) |
| 2 | Metodika vyhledávání a ověřování | [docs/02-metodika.md](docs/02-metodika.md) |
| 3 | Odhad globálního pokrytí, počtu investorů a spolehlivosti | `docs/03-globalni-odhad.md` *(připravuje se)* |
| 4 | Pilotní vzorek v ČR a zdůvodnění výběru země | `data/investors.csv` *(připravuje se)*, [docs/01-plan-a-kriteria.md](docs/01-plan-a-kriteria.md) |
| 5 | Zdroje a data ověření záznamů i faktů | `data/facts.csv`, `data/sources.csv`, `data/search_log.csv` *(připravuje se)* |
| 6 | Ruční kontrola vzorku a precision | [docs/04-rucni-kontrola.md](docs/04-rucni-kontrola.md), `data/reviews.csv`, `data/fact_reviews.csv` *(vyplní hodnotitelé)* |
| 7 | Odhad nákladů a složitosti globálního škálování | `docs/03-globalni-odhad.md` *(připravuje se)* |
| 8 | Kód, testy, dokumentace, historie commitů, ai-log | `investor_db/`, `tests/`, `docs/`, `git log`, [ai-log/](ai-log/) |

## Použití

Vyžaduje Python 3.11+. Kód používá pouze standardní knihovnu; pro testy je potřeba pytest ≥ 8 (deklarován v `pyproject.toml` jako volitelná závislost `dev`).

```
python -m investor_db validate                              # kontrola integrity dat
python -m investor_db metrics                               # precision a další metriky
python -m investor_db review-template --reviewer R1         # šablona kontroly investorů
python -m investor_db fact-review-template --reviewer R1    # šablona kontroly vzorku faktů
python -m pytest                                            # testy
```

## Struktura

```
data/          CSV tabulky (jediný zdroj pravdy)
docs/          plán, metodika, odhady, ruční kontrola
investor_db/   schéma, validace, metriky, CLI
tests/         testy nad fiktivními daty
ai-log/        exporty dialogů s AI
```

Pytest je zvolen místo `unittest`, protože parametrizované testy validačních pravidel a dočasné složky (`tmp_path`) jsou s ním výrazně kratší a čitelnější; samotný kód na něm nezávisí.
