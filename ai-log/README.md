# ai-log

Exporty konverzací s agentem Claude Code, ve kterých vznikl plán, data, kód a dokumentace projektu. Popis práce s AI, pokynů pro agenta a jeho chyb je v [README](../README.md#práce-s-ai).

## Jak exporty vznikají

- Zdrojem jsou lokální transkripty Claude Code (JSONL ve složce `~/.claude/projects/`).
- Exporty se převádějí nástrojem **claude-conversation-extractor** do Markdownu, **bez přepínače `--detailed`**:
  - **Velikost.** Detailní export obsahuje plné výstupy nástrojů. Transkript má 18,9 MB, většinu tvoří stažené stránky a výpisy příkazů.
  - **Autorská práva.** Plné výstupy obsahují texty stažených stránek (média, weby investorů). Ty se do repozitáře neukládají, stejně jako cache surového textu. Fakta odkazují na zdroj URL a krátce parafrázují důkaz.
- Export bez `--detailed` obsahuje zprávy uživatele a odpovědi agenta. Volání nástrojů a jejich výstupy v něm nejsou, ty dokládají commity a data.

## Sessions a fáze

Celá práce proběhla v jedné session Claude Code, `d385e1f5-0229-46e8-8649-3f0ea24e7385`. Ta při zaplnění kontextu pokračovala po automatickém shrnutí. Fáze jsou proto vymezené daty a commity, ne samostatnými sessions.

| Fáze | Datum | Commity | Obsah |
|---|---|---|---|
| 1. Plán a kostra | 9. 10. 2026 | `d191549`–`a3265f6` | plán a kritéria, metodika, datové schéma, validátor, metriky, CLI |
| 2. Pilot VC ČR | 9. 10. 2026 | `fbd0803`–`de4b18e` | hledání kandidátů, triáž, ověření v 5 dávkách, ověření proti surovému textu, náhrada or.justice.cz za ARES |
| 3. Ruční kontrola R1 | 10.–11. 10. 2026 | `74ea856`–`d5232eb` | kontrolní list, kontrola investorů a vzorku faktů, opravy po kontrole (Lighthouse, Tachles, J&T, CVC) |
| 4. Globální odhad | 11. 10. 2026 | `3282965`, `64d0fe1` | odhad počtu, spolehlivosti a nákladů; první export konverzace |
| 5. Doplnění podle zadání | 11. 10. 2026 | `25fff4c`–`50b0205` | `funds.csv`, sektory, ticket a kapitál, oprava definice kapitálu, konflikty zdrojů |
| 6. Kontrola doplnění | 12. 10. 2026 | `5fdc535`–`3a77208` | kolo `po_doplneni` (42/44), opravy typů částek, kolo `po_oprave` |
| 7. Ostatní kategorie | 12. 10. 2026 | `daf41f9`–`afb338e` | plán pro PE, family office, angely a velké soukromé investory; mini-pilot PE; studie proveditelnosti; odhad po kategoriích |
| 8. Kontroly a uzávěrka | 12. 10. 2026 | `c6a471b`–konec | kontrola PE a vyloučených VC, PE slovník, sjednocení času modelu, závěrečné README |

## Soubory

| Soubor | Obsah |
|---|---|
| [claude-conversation-2026-10-09-d385e1f5.md](claude-conversation-2026-10-09-d385e1f5.md) | Úplný export celé session `d385e1f5` nástrojem claude-conversation-extractor bez `--detailed`: 43 zpráv uživatele od prvního zadání po prezentační web, fáze 1–8. |

Měření spotřeby tokenů ze samostatné session bylo připraveno, ale zrušeno (docs/03, 3.5). Samostatná session „měření tokenů“ proto neexistuje.
