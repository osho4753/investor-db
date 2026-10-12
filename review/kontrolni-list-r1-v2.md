# Kontrolní list R1-v2: ověření VC investoři (16)

Vygenerováno příkazem `python -m investor_db investor-review-guide` z `data/*.csv`. Odkazy a doklady neupravuj ručně, při změně dat list vygeneruj znovu. Vyplňuj jen kolonky v tabulkách.

Nové kolo kontroly R1-v2 u všech ověřených VC investorů. U každého investora ověř kritéria Z1–Z4 (docs/01, oddíl 1.3) a rozhodni, zda jde o skutečného VC investora se sídlem v ČR.

- **Povolené zdroje** podle docs/02: veřejné rejstříky (ARES), regulátor, web investora, výroční zprávy, asociace a média.
- **Nepoužívej** Crunchbase, LinkedIn ani agregátory (Dealroom, PitchBook, CB Insights, Caplight, Altss, Seedtable, Superscout). Nejsou to povolené zdroje ani pro kontrolu.
- **Odkaz ARES u Z1:** Odkaz vede na rozhraní ARES a prohlížeč zobrazí data ve formátu JSON: IČO je v poli „ico“, název v „obchodniJmeno“, sídlo v „sidlo“, vznik a zánik v „datumVzniku“ a „datumZaniku“, statutární orgány (u adres s „ekonomicke-subjekty-vr“) v „statutarniOrgany“.
- Odkazy níže jsou z našich zdrojů. Můžeš hledat i vlastní povolené zdroje, pak je uveď v kolonce „Co přesně jsem viděl“.
- **Verdikt:** `TP` = skutečný VC investor v ČR (Z1–Z4 platí), `FP` = nepatří mezi ověřené VC, `nejiste` = zdroje nestačí.
- **Čas** zapiš skutečný v minutách od otevření prvního odkazu po verdikt, bez zaokrouhlování.
- Nepiš jména fyzických osob.

## 1. Credo Ventures (`inv-0013`)

- **Z1 – registr:** IČO 28538137, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/28538137>
- **Z3 – kapitál třetích osob:** Fond „Credo Stage 5“ investora Credo Ventures byl konečně uzavřen (final close) s velikostí 88 000 000 USD (stav k 23. 3. 2026). Fakt `f-00296`, zdroj: <https://thenextweb.com/news/credo-ventures-88m-fund> (média (sekundární), vydavatel: TNW).
- **Nejnovější doložená investice (Z4):** Credo Ventures investoval do společnosti Wabi (oznámeno 5. 11. 2025). Fakt `f-00031`, zdroj: <https://www.credoventures.com/newsroom> (web investora (primární), vydavatel: Credo Ventures).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 2. Depo Ventures (`inv-0008`)

- **Z1 – registr:** IČO 04753101, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/04753101>
- **Z3 – kapitál třetích osob:** Fond „Grouport Ventures“ investora Depo Ventures byl uzavřen s velikostí 35 000 000 CZK; zdroj neupřesňuje, zda šlo o final close. Fakt `f-00258`, zdroj: <https://cc.cz/cesti-depo-ventures-oteviraji-druhy-fond-v-desitkach-milionu-prvni-investice-podpori-startup-ktery-ukazuje-data-z-kryptouctu/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložená investice (Z4):** Depo Ventures investoval do společnosti Flowpay (oznámeno 2. 4. 2024). Fakt `f-00246`, zdroj: <https://cc.cz/purple-presto-kaya-a-dalsi-investori-maji-apetit-startupove-fondy-nabiraji-dalsi-miliardy-korun/> (média (sekundární), vydavatel: CzechCrunch).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 3. i&i Biotech Investments (`inv-0009`)

- **Z1 – registr:** IČO 10885978, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/10885978>
- **Z3 – kapitál třetích osob:** Fond „i&i Biotech Fund I SCSp“ investora i&i Biotech Investments byl uzavřen s velikostí 47 000 000 EUR (stav k 30. 11. 2022); zdroj neupřesňuje, zda šlo o final close. Fakt `f-00264`, zdroj: <https://www.uochb.cz/en/news/451/experienced-businessmen-join-forces-with-excellent-science-invest-eur-2-million-in-the-fund-of-iocb-prague-family> (média (sekundární), vydavatel: ÚOCHB AV ČR).
- **Nejnovější doložená investice (Z4):** i&i Biotech Investments investoval do společnosti Captain T Cell (oznámeno 17. 11. 2025). Fakt `f-00075`, zdroj: <https://www.inibio.eu/> (web investora (primární), vydavatel: i&i Biotech Fund).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 4. IP Lab Ventures (`inv-0052`)

- **Z1 – registr:** IČO 19110715, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-vr/19110715>
- **Z3 – kapitál třetích osob:** Jeden investor (LP) se zavázal vložit do fondu „IP Lab Ventures Fund“ investora IP Lab Ventures 656 000 000 CZK (stav k 23. 9. 2026); jde jen o část fondu. Fakt `f-00287`, zdroj: <https://cc.cz/vlada-posila-700-milionu-do-noveho-druhu-fondu-zameri-se-i-na-ai-ridi-ho-byvaly-sef-dame-jidlo/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložený fond (Z4, investice chybí):** O fondu „IP Lab Ventures Fund“ investora IP Lab Ventures platí: investice EIF 656 mil. Kč z Národního plánu obnovy; druhý VC fond z NPO po Tensor Ventures (stav k 23. 9. 2026). Fakt `f-00153`, zdroj: <https://cc.cz/vlada-posila-700-milionu-do-noveho-druhu-fondu-zameri-se-i-na-ai-ridi-ho-byvaly-sef-dame-jidlo/> (média (sekundární), vydavatel: CzechCrunch).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 5. KAYA VC (`inv-0006`)

- **Z1 – registr:** IČO 22585737, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/22585737>
- **Z3 – kapitál třetích osob:** Fond „KAYA Fund IV“ investora KAYA VC byl konečně uzavřen (final close) s velikostí 72 000 000 EUR (stav k 31. 3. 2021). Fakt `f-00254`, zdroj: <https://www.globalprivatecapital.org/?p=27830> (asociace (sekundární), vydavatel: Global Private Capital Association (GPCA)).
- **Nejnovější doložená investice (Z4):** KAYA VC investoval do společnosti Riptides (oznámeno 23. 4. 2025). Fakt `f-00040`, zdroj: <https://www.vestbee.com/blog/articles/riptides-secures-3-3-m> (média (sekundární), vydavatel: Vestbee).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 6. Lighthouse Ventures (`inv-0037`)

- **Z1 – registr:** IČO 07500912, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-vr/07500912>
- **Z3 – kapitál třetích osob:** Fond „Lighthouse Seed Fund“ investora Lighthouse Ventures byl uzavřen s velikostí 23 000 000 EUR (stav k 7. 6. 2019); zdroj neupřesňuje, zda šlo o final close. Fakt `f-00277`, zdroj: <https://cc.cz/cesky-fond-lighthouse-ventures-vlozil-vyssi-stovky-tisic-eur-do-brnenskeho-ai-startupu-pekat-vision/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložená investice (Z4):** Lighthouse Ventures investoval do společnosti Ranketta (oznámeno 27. 11. 2025). Fakt `f-00240`, zdroj: <https://tech.eu/2025/11/27/ranketta-receives-eur1m-to-improve-ecommerce-brand-performance-in-ai-search/> (média (sekundární), vydavatel: Tech.eu).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 7. Presto Ventures (`inv-0028`)

- **Z1 – registr:** IČO 11678704, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/11678704>
- **Z3 – kapitál třetích osob:** Fond „Presto Ventures – druhý fond“ investora Presto Ventures byl uzavřen s konečnou velikostí 30 000 000 EUR (stav k 23. 6. 2022). Fakt `f-00203`, zdroj: <https://uadn.net/?p=38907> (média (sekundární), vydavatel: UADN).
- **Nejnovější doložená investice (Z4):** Presto Ventures investoval do společnosti Vidar Systems (oznámeno 27. 11. 2024). Fakt `f-00109`, zdroj: <https://prestoventures.com/news> (web investora (primární), vydavatel: Presto Ventures).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 8. Purple Ventures (`inv-0035`)

- **Z1 – registr:** IČO 05775574, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/05775574>
- **Z3 – kapitál třetích osob:** Fond „Purple Ventures 2“ investora Purple Ventures byl uzavřen s velikostí 700 000 000 CZK; zdroj neupřesňuje, zda šlo o final close. Fakt `f-00275`, zdroj: <https://purple-ventures.com/> (web investora (primární), vydavatel: Purple Ventures).
- **Nejnovější doložená investice (Z4):** Purple Ventures investoval do společnosti Kilde (oznámeno 20. 10. 2025). Fakt `f-00135`, zdroj: <https://www.fxstreet.cz/klicova-slova+kilde.html> (média (sekundární), vydavatel: FXstreet.cz).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 9. Reflex Capital (`inv-0038`)

- **Z1 – registr:** IČO 24269158, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/24269158>
- **Z3 – kapitál třetích osob:** Fond „Reflex Capital – třetí fond“ investora Reflex Capital byl uzavřen s konečnou velikostí 22 000 000 EUR (stav k 22. 12. 2023). Fakt `f-00204`, zdroj: <https://cc.cz/nova-sila-pro-reflex-capital-ondreje-fryce-ve-tretim-fondu-ma-na-startupy-pres-pul-miliardy/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložená investice (Z4):** Reflex Capital investoval do společnosti grid.online (oznámeno 3. 3. 2025). Fakt `f-00147`, zdroj: <https://www.jtventures.cz/blog> (web investora (primární), vydavatel: J&T Ventures).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 10. Rockaway Ventures (`inv-0029`)

- **Z1 – registr:** IČO 06387136, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-vr/06387136>
- **Z3 – kapitál třetích osob:** Fond „Rockaway Ventures Fund II“ investora Rockaway Ventures byl uzavřen s velikostí 55 000 000 EUR (stav k 14. 5. 2025); zdroj neupřesňuje, zda šlo o final close. Fakt `f-00271`, zdroj: <https://cc.cz/rockaway-ventures-oznamilo-druhy-fond-na-startupy-ma-pripravene-14-miliardy-korun/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložená investice (Z4):** Rockaway Ventures investoval do společnosti Filuta AI (oznámeno 24. 6. 2025). Fakt `f-00116`, zdroj: <https://rockawayventures.com/> (web investora (primární), vydavatel: Rockaway Ventures).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 11. Soulmates Ventures (`inv-0044`)

- **Z1 – registr:** IČO 09789561, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/09789561>
- **Z3 – kapitál třetích osob:** Fond „Soulmates Ventures – fond 50 mil. EUR“ investora Soulmates Ventures byl uzavřen s velikostí 50 000 000 EUR (stav k 18. 3. 2025); zdroj neupřesňuje, zda šlo o final close. Fakt `f-00283`, zdroj: <https://vestbee.com/blog/articles/soulmates-ventures-raises-50-m-fund> (média (sekundární), vydavatel: Vestbee).
- **Nejnovější doložená investice (Z4):** Soulmates Ventures investoval do společnosti Twin Science (oznámeno 26. 8. 2024). Fakt `f-00163`, zdroj: <https://soulmatesventures.com/> (web investora (primární), vydavatel: Soulmates Ventures).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 12. Startguide VC (`inv-0047`)

- **Z1 – registr:** IČO 28418425, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/28418425>
- **Z3 – kapitál třetích osob:** Cílová velikost fondu „SG One“ investora Startguide VC je 6 000 000 EUR. Fakt `f-00284`, zdroj: <https://www.startguide.cz/sgone/> (web investora (primární), vydavatel: Start Guide).
- **Nejnovější doložená investice (Z4):** Startguide VC investoval do společnosti Carebot (oznámeno 2. 4. 2024). Fakt `f-00173`, zdroj: <https://cc.cz/purple-presto-kaya-a-dalsi-investori-maji-apetit-startupove-fondy-nabiraji-dalsi-miliardy-korun/> (média (sekundární), vydavatel: CzechCrunch).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 13. StartupYard (`inv-0049`)

- **Z1 – registr:** IČO 06002820, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/06002820>
- **Z3 – kapitál třetích osob:** O fondu „StartupYard Batch 15 s.r.o.“ investora StartupYard platí: nový vehikl ročníku akcelerátoru; program financují soukromí investoři (Credo Ventures, Rockaway Capital Partners, business angels) (stav k 14. 11. 2024). Fakt `f-00228`, zdroj: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/22266852> (veřejný rejstřík (primární), vydavatel: Ministerstvo financí ČR – ARES).
- **Nejnovější doložený fond (Z4, investice chybí):** O fondu „StartupYard Batch 15 s.r.o.“ investora StartupYard platí: nový vehikl ročníku akcelerátoru; program financují soukromí investoři (Credo Ventures, Rockaway Capital Partners, business angels) (stav k 14. 11. 2024). Fakt `f-00228`, zdroj: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/22266852> (veřejný rejstřík (primární), vydavatel: Ministerstvo financí ČR – ARES).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 14. Tachles (`inv-0039`)

- **Z1 – registr:** IČO 14376032, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-vr/14376032>
- **Z3 – kapitál třetích osob:** Fond „Tachles VC“ investora Tachles dosáhl prvního uzavření (first close) ve výši 500 000 000 CZK (stav k 13. 6. 2024). Fakt `f-00281`, zdroj: <https://cc.cz/roky-hledali-startupy-pro-fond-karla-komarka-ted-rozbihaji-vlastni-v-prvni-fazi-maji-pul-miliardy/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložený fond (Z4, investice chybí):** O fondu „Tachles VC“ investora Tachles platí: první investiční rok 2024: sedm startupů za přibližně 30 mil. Kč (stav k 12. 2. 2025). Fakt `f-00201`, zdroj: <https://cc.cz/cesi-v-izraeli-na-lovu-miliardovych-jednorozcu-navzdory-konfliktu-se-tu-startupum-dari-hlasi/> (média (sekundární), vydavatel: CzechCrunch).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 15. Tensor Ventures (`inv-0003`)

- **Z1 – registr:** IČO 06257241, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-vr/06257241>
- **Z3 – kapitál třetích osob:** Fond „Tensor Ventures Co-investment Fund“ investora Tensor Ventures byl uzavřen s velikostí 1 000 000 000 CZK (stav k 18. 9. 2025); zdroj neupřesňuje, zda šlo o final close. Fakt `f-00252`, zdroj: <https://forbes.cz/tensor-vybral-miliardu-a-miri-dal-cesti-investori-sazi-na-ai-i-kvantove-technologie/> (média (sekundární), vydavatel: Forbes Česko).
- **Nejnovější doložená investice (Z4):** Tensor Ventures investoval do společnosti DYNANIC (oznámeno 28. 11. 2024). Fakt `f-00066`, zdroj: <https://brnotechregion.eu/en/news/cipova-revoluce-z-univerzitniho-brna-tensor-ventur> (média (sekundární), vydavatel: Brno Tech Region).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |

## 16. Tilia Impact Ventures (`inv-0027`)

- **Z1 – registr:** IČO 17621615, ARES: <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/17621615>
- **Z3 – kapitál třetích osob:** Fond „Tilia Impact Seed Fund“ investora Tilia Impact Ventures byl uzavřen s velikostí 26 000 000 EUR (stav k 21. 9. 2023); zdroj neupřesňuje, zda šlo o final close. Fakt `f-00268`, zdroj: <https://cc.cz/cesky-fond-urceny-na-investice-se-spolecenskymi-dopady-ma-dalsich-600-milionu-podporili-ho-winkler-ci-barta/> (média (sekundární), vydavatel: CzechCrunch).
- **Nejnovější doložená investice (Z4):** Tilia Impact Ventures investoval do společnosti Flox Intelligence (oznámeno 1. 2. 2026). Fakt `f-00084`, zdroj: <https://funding.tech.eu/investors/Tilia%20Impact%20Ventures> (jiný zdroj (sekundární), vydavatel: Tech.eu).

| Kolonka (vyplní hodnotitel) | Hodnota |
|---|---|
| Verdikt (`TP` / `FP` / `nejiste`) | |
| Co přesně jsem viděl (zdroj, údaj, datum) | |
| Čas v minutách (skutečný, nezaokrouhlený) | |
