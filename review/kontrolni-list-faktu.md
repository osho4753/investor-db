# Kontrolní list faktů

Vygenerováno příkazem `python -m investor_db review-guide` ze vzorku v `data/fact_reviews.csv`. Soubor neupravuj ručně, při změně dat ho vygeneruj znovu.

Vzorek obsahuje 36 z 223 faktů. U každého faktu otevři zdroj a posuď jen to, zda zdroj podporuje uvedené tvrzení. Verdikt (`spravne`, `chybne`, `nelze_overit`), datum, čas v minutách a poznámku zapiš do řádku se stejným `fact_id` v `data/fact_reviews.csv`. Podrobný návod je v `docs/04-rucni-kontrola.md`, sekce „Návod pro hodnotitele“.

## 1. `f-00001` – Stratum Partners (status: vyloucen)

**Tvrzení:** Stratum Partners investuje hlavně formou buyoutů a většinových podílů (PE), proto není VC a je odložen pro budoucí rozšíření.

**Co hledat ve zdroji:** Zdroj popisuje subjekt jako private equity (buyout, většinové podíly, zralé firmy), nebo ho do private equity zařazuje.

**Zdroj:** <https://cvca.cz/en/category/full-members/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 2. `f-00003` – CVI (status: vyloucen)

**Tvrzení:** CVI poskytuje hlavně dluhové financování (úvěry, mezanin, venture debt), ne kapitál za podíl, proto je vyloučen.

**Co hledat ve zdroji:** Zdroj popisuje hlavní strategii jako úvěry, dluh, mezanin nebo venture debt. Pokud zdroj uvádí kapitálové investice jako hlavní strategii, je verdikt chybne.

**Zdroj:** <https://cvca.cz/en/category/full-members/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 3. `f-00021` – Evropský investiční fond (EIF) (status: vyloucen)

**Tvrzení:** Evropský investiční fond (EIF) je fond fondů: investuje do jiných fondů, ne přímo do firem, proto je vyloučen.

**Co hledat ve zdroji:** Zdroj uvádí, že subjekt vkládá kapitál do jiných fondů, nikoli přímo do podílů ve firmách.

**Zdroj:** <https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic>  
Typ zdroje: jiný zdroj (sekundární), vydavatel: Wikipedie

## 4. `f-00027` – Credo Ventures (status: overeny)

**Tvrzení:** Credo Ventures investuje do těchto sektorů: bez sektorového omezení (sector agnostic).

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://www.credoventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Credo Ventures

## 5. `f-00028` – Credo Ventures (status: overeny)

**Tvrzení:** Typická investice investora Credo Ventures do jednoho startupu začíná na 1 000 000 USD.

**Co hledat ve zdroji:** Najdi ve zdroji částku 1 000 000 USD: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o dolní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://www.credoventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Credo Ventures

## 6. `f-00030` – Credo Ventures (status: overeny)

**Tvrzení:** O fondu „Credo Stage 5“ investora Credo Ventures platí: first close 88 mil. USD v březnu 2026.

**Co hledat ve zdroji:** Zdroj potvrzuje každou část tvrzení: název fondu, uvedené částky a měny, data a role subjektů (správce, GP, AIFM). Pokud zdroj potvrzuje jen část, je verdikt chybne a do note napiš, co chybí.

**Zdroj:** <https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic>  
Typ zdroje: jiný zdroj (sekundární), vydavatel: Wikipedie

## 7. `f-00032` – KAYA VC (status: overeny)

**Tvrzení:** Investor (VC značka) vystupuje pod názvem „KAYA VC“.

**Co hledat ve zdroji:** Zdroj uvádí tento název (rozdíl jen ve velkých písmenech nebo v právní formě nevadí) a popisuje stejný subjekt, ne jinou firmu s podobným názvem.

**Zdroj:** <https://cvca.cz/en/kaya-vc-2/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 8. `f-00058` – Tensor Ventures (status: overeny)

**Tvrzení:** Investor (VC značka) vystupuje pod názvem „Tensor Ventures“.

**Co hledat ve zdroji:** Zdroj uvádí tento název (rozdíl jen ve velkých písmenech nebo v právní formě nevadí) a popisuje stejný subjekt, ne jinou firmu s podobným názvem.

**Zdroj:** <https://tensor.ventures/>  
Typ zdroje: web investora (primární), vydavatel: Tensor Ventures

## 9. `f-00063` – Tensor Ventures (status: overeny)

**Tvrzení:** Typická investice investora Tensor Ventures do jednoho startupu začíná na 250 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 250 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o dolní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://cvca.cz/en/tensor-ventures/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 10. `f-00067` – i&i Biotech Investments (status: overeny)

**Tvrzení:** Investor (VC značka) vystupuje pod názvem „i&i Biotech Investments“.

**Co hledat ve zdroji:** Zdroj uvádí tento název (rozdíl jen ve velkých písmenech nebo v právní formě nevadí) a popisuje stejný subjekt, ne jinou firmu s podobným názvem.

**Zdroj:** <https://cvca.cz/en/biotech-investments/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 11. `f-00071` – i&i Biotech Investments (status: overeny)

**Tvrzení:** i&i Biotech Investments investuje do těchto sektorů: biotechnologie, zdravotnické technologie (healthtech), umělá inteligence (AI).

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://www.inibio.eu/>  
Typ zdroje: web investora (primární), vydavatel: i&i Biotech Fund

## 12. `f-00081` – Tilia Impact Ventures (status: overeny)

**Tvrzení:** Typická investice investora Tilia Impact Ventures do jednoho startupu začíná na 300 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 300 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o dolní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://tilia.vc/>  
Typ zdroje: web investora (primární), vydavatel: Tilia Impact Ventures

## 13. `f-00089` – Orbit Capital (status: vyloucen)

**Tvrzení:** Typická investice investora Orbit Capital do jednoho startupu dosahuje nejvýše 15 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 15 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o horní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://cvca.cz/en/orbit-capital-2/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 14. `f-00090` – Orbit Capital (status: vyloucen)

**Tvrzení:** Cílová velikost fondu „Orbit Capital Growth Equity“ investora Orbit Capital je 200 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 200 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://cvca.cz/en/orbit-capital-2/>  
Typ zdroje: asociace (sekundární), vydavatel: CVCA – Czech Private Equity and Venture Capital Association

## 15. `f-00099` – Inven Capital (status: kandidat)

**Tvrzení:** O fondu „Inven Capital, SICAV, a.s.“ investora Inven Capital platí: podfondy A–D; 500 mil. EUR od institucionálních investorů a globálních korporací a dalších 50 mil. EUR od EIB; patička webu uvádí © ČEZ, a. s..

**Co hledat ve zdroji:** Zdroj potvrzuje každou část tvrzení: název fondu, uvedené částky a měny, data a role subjektů (správce, GP, AIFM). Pokud zdroj potvrzuje jen část, je verdikt chybne a do note napiš, co chybí.

**Zdroj:** <https://www.invencapital.cz/>  
Typ zdroje: web investora (primární), vydavatel: Inven Capital

## 16. `f-00101` – Presto Ventures (status: overeny)

**Tvrzení:** Investor (VC značka) vystupuje pod názvem „Presto Ventures“.

**Co hledat ve zdroji:** Zdroj uvádí tento název (rozdíl jen ve velkých písmenech nebo v právní formě nevadí) a popisuje stejný subjekt, ne jinou firmu s podobným názvem.

**Zdroj:** <https://www.prestoventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Presto Ventures

## 17. `f-00108` – Presto Ventures (status: overeny)

**Tvrzení:** Cílová velikost fondu „Presto Tech Horizons“ investora Presto Ventures je 150 000 000 EUR (stav k 26. 6. 2024).

**Co hledat ve zdroji:** Najdi ve zdroji částku 150 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://www.e15.cz/byznys/burzy-a-trhy/czechoslovak-group-buduje-novy-fond-s-presto-ventures-miliardy-zamiri-do-obrany-a-bezpecnosti-1416821>  
Typ zdroje: média (sekundární), vydavatel: E15

## 18. `f-00114` – Rockaway Ventures (status: overeny)

**Tvrzení:** Rockaway Ventures investuje do těchto sektorů: e-commerce, média, kybernetická bezpečnost, čisté technologie (cleantech, climate), nemovitostní technologie (proptech).

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://rockawayventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Rockaway Ventures

## 19. `f-00121` – J&T Ventures (status: overeny)

**Tvrzení:** J&T Ventures investuje v těchto fázích: pre-seed, seed, série A.

**Co hledat ve zdroji:** Zdroj jmenuje každou z uvedených fází (např. „early stage“ samo o sobě nestačí na série A). Pokud některá uvedená fáze ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://www.jtventures.cz/>  
Typ zdroje: web investora (primární), vydavatel: J&T Ventures

## 20. `f-00127` – Purple Ventures (status: overeny)

**Tvrzení:** Investor (VC značka) vystupuje pod názvem „Purple Ventures“.

**Co hledat ve zdroji:** Zdroj uvádí tento název (rozdíl jen ve velkých písmenech nebo v právní formě nevadí) a popisuje stejný subjekt, ne jinou firmu s podobným názvem.

**Zdroj:** <https://purple-ventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Purple Ventures

## 21. `f-00131` – Purple Ventures (status: overeny)

**Tvrzení:** Purple Ventures investuje v těchto fázích: pre-seed, seed.

**Co hledat ve zdroji:** Zdroj jmenuje každou z uvedených fází (např. „early stage“ samo o sobě nestačí na série A). Pokud některá uvedená fáze ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://purple-ventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Purple Ventures

## 22. `f-00141` – Reflex Capital (status: overeny)

**Tvrzení:** Oficiální web investora Reflex Capital je https://www.reflexcapital.com/cs/.

**Co hledat ve zdroji:** Zdroj je tento web, nebo na něj odkazuje jako na web investora. Doména musí být stejná a web musí patřit investorovi Reflex Capital, ne firmě s podobným názvem.

**Zdroj:** <https://www.reflexcapital.com/cs/>  
Typ zdroje: web investora (primární), vydavatel: Reflex Capital

## 23. `f-00145` – Reflex Capital (status: overeny)

**Tvrzení:** Typická investice investora Reflex Capital do jednoho startupu dosahuje nejvýše 2 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 2 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o horní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://cc.cz/nova-sila-pro-reflex-capital-ondreje-fryce-ve-tretim-fondu-ma-na-startupy-pres-pul-miliardy/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 24. `f-00148` – Tachles (status: overeny)

**Tvrzení:** Tachles investuje do těchto sektorů: kybernetická bezpečnost, software, umělá inteligence (AI).

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://cc.cz/roky-hledali-startupy-pro-fond-karla-komarka-ted-rozbihaji-vlastni-v-prvni-fazi-maji-pul-miliardy/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 25. `f-00158` – Soulmates Ventures (status: overeny)

**Tvrzení:** Soulmates Ventures investuje v těchto fázích: seed, série A.

**Co hledat ve zdroji:** Zdroj jmenuje každou z uvedených fází (např. „early stage“ samo o sobě nestačí na série A). Pokud některá uvedená fáze ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://soulmatesventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Soulmates Ventures

## 26. `f-00160` – Soulmates Ventures (status: overeny)

**Tvrzení:** Typická investice investora Soulmates Ventures do jednoho startupu dosahuje nejvýše 3 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 3 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o horní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://soulmatesventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Soulmates Ventures

## 27. `f-00164` – 10X (status: vyloucen)

**Tvrzení:** 10X je otevřený fond s průběžnou likviditou, který kombinuje podíly ve firmách s kotovanými akciemi, proto není VC fond a je vyloučen.

**Co hledat ve zdroji:** Zdroj uvádí, že fond je otevřený (průběžný vstup a výstup investorů, např. měsíční likvidita) a drží i kotované akcie.

**Zdroj:** <https://cc.cz/koukal-pod-ruce-ppf-jt-i-pente-z-milionu-korun-po-dvaceti-letech-spravuje-miliardu-a-otevira-fond/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 28. `f-00168` – Startguide VC (status: overeny)

**Tvrzení:** Startguide VC má českou právnickou osobu s IČO 28418425.

**Co hledat ve zdroji:** Najdi ve zdroji subjekt s IČO 28418425. Zkontroluj, že IČO sedí číslice po číslici a že název nebo sídlo subjektu odpovídá investorovi Startguide VC, ne jiné firmě.

**Zdroj:** <https://www.startguide.cz/>  
Typ zdroje: web investora (primární), vydavatel: Start Guide

## 29. `f-00173` – Startguide VC (status: overeny)

**Tvrzení:** Startguide VC investoval do společnosti Carebot (oznámeno 2. 4. 2024).

**Co hledat ve zdroji:** Zdroj uvádí, že do této společnosti investoval právě Startguide VC (nebo jeho fond), a datum oznámení odpovídá. Chybné je, pokud investoval jiný investor s podobným názvem nebo jde o jinou, starší investici.

**Zdroj:** <https://cc.cz/purple-presto-kaya-a-dalsi-investori-maji-apetit-startupove-fondy-nabiraji-dalsi-miliardy-korun/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 30. `f-00178` – Zaka VC (status: vyloucen)

**Tvrzení:** Zaka VC investuje v těchto fázích: pre-seed, seed.

**Co hledat ve zdroji:** Zdroj jmenuje každou z uvedených fází (např. „early stage“ samo o sobě nestačí na série A). Pokud některá uvedená fáze ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://en.ain.ua/2024/03/11/zaka-vc-invests-in-eigen-therapeutics>  
Typ zdroje: média (sekundární), vydavatel: AIN.UA

## 31. `f-00181` – Zaka VC (status: vyloucen)

**Tvrzení:** Zaka VC investoval do společnosti Eigen Therapeutics (oznámeno 11. 3. 2024).

**Co hledat ve zdroji:** Zdroj uvádí, že do této společnosti investoval právě Zaka VC (nebo jeho fond), a datum oznámení odpovídá. Chybné je, pokud investoval jiný investor s podobným názvem nebo jde o jinou, starší investici.

**Zdroj:** <https://en.ain.ua/2024/03/11/zaka-vc-invests-in-eigen-therapeutics>  
Typ zdroje: média (sekundární), vydavatel: AIN.UA

## 32. `f-00187` – Orbit Capital (status: vyloucen)

**Tvrzení:** Orbit Capital poskytuje hlavně dluhové financování (úvěry, mezanin, venture debt), ne kapitál za podíl, proto je vyloučen.

**Co hledat ve zdroji:** Zdroj popisuje hlavní strategii jako úvěry, dluh, mezanin nebo venture debt. Pokud zdroj uvádí kapitálové investice jako hlavní strategii, je verdikt chybne.

**Zdroj:** <https://tech.eu/2026/07/02/orbit-capital-closes-eur107m-venture-debt-fund-for-cee-scaleups/>  
Typ zdroje: média (sekundární), vydavatel: Tech.eu

## 33. `f-00197` – IP Lab Ventures (status: overeny)

**Tvrzení:** IP Lab Ventures má českou právnickou osobu s IČO 19110715.

**Co hledat ve zdroji:** Najdi ve zdroji subjekt s IČO 19110715. Zkontroluj, že IČO sedí číslice po číslici a že název nebo sídlo subjektu odpovídá investorovi IP Lab Ventures, ne jiné firmě. Odkaz vede na rozhraní ARES a prohlížeč zobrazí data ve formátu JSON: IČO je v poli „ico“, název v „obchodniJmeno“, sídlo v „sidlo“, vznik a zánik v „datumVzniku“ a „datumZaniku“, statutární orgány (u adres s „ekonomicke-subjekty-vr“) v „statutarniOrgany“.

**Zdroj:** <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty-vr/19110715>  
Typ zdroje: veřejný rejstřík (primární), vydavatel: Ministerstvo financí ČR – ARES (veřejný rejstřík)

## 34. `f-00199` – IP Lab Ventures (status: overeny)

**Tvrzení:** IP Lab Ventures investuje do těchto sektorů: deep tech, biotechnologie, průmysl, umělá inteligence (AI).

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://www.e15.cz/byznys/e15-a-byznys/ip-lab-ventures-sazi-na-deep-tech-z-vedeckych-napadu-chce-budovat-firmy-svetove-urovne-1431586>  
Typ zdroje: média (sekundární), vydavatel: E15

## 35. `f-00211` – i&i Biotech Investments (status: overeny)

**Tvrzení:** i&i Biotech Investments má českou právnickou osobu s IČO 10885978.

**Co hledat ve zdroji:** Najdi ve zdroji subjekt s IČO 10885978. Zkontroluj, že IČO sedí číslice po číslici a že název nebo sídlo subjektu odpovídá investorovi i&i Biotech Investments, ne jiné firmě. Odkaz vede na rozhraní ARES a prohlížeč zobrazí data ve formátu JSON: IČO je v poli „ico“, název v „obchodniJmeno“, sídlo v „sidlo“, vznik a zánik v „datumVzniku“ a „datumZaniku“, statutární orgány (u adres s „ekonomicke-subjekty-vr“) v „statutarniOrgany“.

**Zdroj:** <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/10885978>  
Typ zdroje: veřejný rejstřík (primární), vydavatel: Ministerstvo financí ČR – ARES

## 36. `f-00214` – Inven Capital (status: kandidat)

**Tvrzení:** Inven Capital má českou právnickou osobu s IČO 02059533.

**Co hledat ve zdroji:** Najdi ve zdroji subjekt s IČO 02059533. Zkontroluj, že IČO sedí číslice po číslici a že název nebo sídlo subjektu odpovídá investorovi Inven Capital, ne jiné firmě. Odkaz vede na rozhraní ARES a prohlížeč zobrazí data ve formátu JSON: IČO je v poli „ico“, název v „obchodniJmeno“, sídlo v „sidlo“, vznik a zánik v „datumVzniku“ a „datumZaniku“, statutární orgány (u adres s „ekonomicke-subjekty-vr“) v „statutarniOrgany“.

**Zdroj:** <https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/02059533>  
Typ zdroje: veřejný rejstřík (primární), vydavatel: Ministerstvo financí ČR – ARES
