# Kontrolní list faktů

Vygenerováno příkazem `python -m investor_db review-guide` z `data/fact_reviews.csv`. Soubor neupravuj ručně, při změně dat ho vygeneruj znovu.

Kontrola obsahuje 85 z 273 faktů ve dvou kolech. U každého faktu otevři zdroj a posuď jen to, zda zdroj podporuje uvedené tvrzení. Verdikt (`spravne`, `chybne`, `nelze_overit`), datum, čas v minutách a poznámku zapiš do řádku se stejným `fact_id` v `data/fact_reviews.csv`. Podrobný návod je v `docs/04-rucni-kontrola.md`, sekce „Návod pro hodnotitele“.

# Původní kontrola – náhodný vzorek (36 faktů)

Náhodný vzorek faktů z původního sběru. Přesnost se z něj počítá zvlášť.

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

**Tvrzení:** i&i Biotech Investments investuje do těchto sektorů: biotechnologie, zdravotnické technologie (healthtech).

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

## 19. `f-00121` – J&T Ventures (status: kandidat)

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

# Kontrola po doplnění – všechny nové fakty (49 faktů)

Všechny fakty přidané doplňováním sektorů, ticketu a kapitálu, ne vzorek. Přesnost se počítá zvlášť.

## 37. `f-00249` – Tensor Ventures (status: overeny)

**Tvrzení:** Fond „Tensor Ventures Fund I SCSp“ investora Tensor Ventures byl uzavřen s velikostí 20 000 000 EUR; zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 20 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 38. `f-00250` – Tensor Ventures (status: overeny)

**Tvrzení:** Cílová velikost fondu „Tensor Ventures Co-investment Fund“ investora Tensor Ventures je 50 000 000 EUR (stav k 15. 5. 2024).

**Co hledat ve zdroji:** Najdi ve zdroji částku 50 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 39. `f-00251` – Tensor Ventures (status: overeny)

**Tvrzení:** Jeden investor (LP) se zavázal vložit do fondu „Tensor Ventures Co-investment Fund“ investora Tensor Ventures 20 000 000 EUR (stav k 15. 5. 2024); jde jen o část fondu.

**Co hledat ve zdroji:** Najdi ve zdroji částku 20 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), ne celkovou velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 40. `f-00252` – Tensor Ventures (status: overeny)

**Tvrzení:** Fond „Tensor Ventures Co-investment Fund“ investora Tensor Ventures byl uzavřen s velikostí 1 000 000 000 CZK (stav k 18. 9. 2025); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 1 000 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://forbes.cz/tensor-vybral-miliardu-a-miri-dal-cesti-investori-sazi-na-ai-i-kvantove-technologie/>  
Typ zdroje: média (sekundární), vydavatel: Forbes Česko

## 41. `f-00253` – KAYA VC (status: overeny)

**Tvrzení:** KAYA VC investuje do těchto sektorů: bez sektorového omezení (sector agnostic).

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://www.vestbee.com/blog/articles/kaya-secures-70-m>  
Typ zdroje: média (sekundární), vydavatel: Vestbee

## 42. `f-00254` – KAYA VC (status: overeny)

**Tvrzení:** Fond „KAYA Fund IV“ investora KAYA VC byl konečně uzavřen (final close) s velikostí 72 000 000 EUR (stav k 31. 3. 2021).

**Co hledat ve zdroji:** Najdi ve zdroji částku 72 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí výslovně uvádět konečné uzavření (final close, „definitivně uzavřel“). Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://www.globalprivatecapital.org/?p=27830>  
Typ zdroje: asociace (sekundární), vydavatel: Global Private Capital Association (GPCA)

## 43. `f-00255` – KAYA VC (status: overeny)

**Tvrzení:** Cílová velikost fondu „KAYA Fund V“ investora KAYA VC je 80 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 80 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://www.vestbee.com/blog/articles/kaya-secures-70-m>  
Typ zdroje: média (sekundární), vydavatel: Vestbee

## 44. `f-00256` – KAYA VC (status: overeny)

**Tvrzení:** Fond „KAYA Fund V“ investora KAYA VC dosáhl prvního uzavření (first close) ve výši 70 000 000 EUR (stav k 25. 6. 2025).

**Co hledat ve zdroji:** Najdi ve zdroji částku 70 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět first close (první uzavření), ne konečnou nebo cílovou velikost. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://www.vestbee.com/blog/articles/kaya-secures-70-m>  
Typ zdroje: média (sekundární), vydavatel: Vestbee

## 45. `f-00257` – Depo Ventures (status: overeny)

**Tvrzení:** Depo Ventures dosud investoval celkem 9 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 9 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o skutečně investovaný kapitál, ne o velikost fondu ani o spravovaná aktiva.

**Zdroj:** <https://depoventures.com/>  
Typ zdroje: web investora (primární), vydavatel: DEPO Ventures

## 46. `f-00258` – Depo Ventures (status: overeny)

**Tvrzení:** Fond „Grouport Ventures“ investora Depo Ventures byl uzavřen s velikostí 35 000 000 CZK; zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 35 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/cesti-depo-ventures-oteviraji-druhy-fond-v-desitkach-milionu-prvni-investice-podpori-startup-ktery-ukazuje-data-z-kryptouctu/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 47. `f-00259` – Depo Ventures (status: overeny)

**Tvrzení:** Cílová velikost fondu „Depo Angels Fund II“ investora Depo Ventures je 45 000 000 CZK (stav k 25. 1. 2022).

**Co hledat ve zdroji:** Najdi ve zdroji částku 45 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://cc.cz/cesti-depo-ventures-oteviraji-druhy-fond-v-desitkach-milionu-prvni-investice-podpori-startup-ktery-ukazuje-data-z-kryptouctu/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 48. `f-00260` – Depo Ventures (status: overeny)

**Tvrzení:** Cílová velikost fondu „Depo Ventures – třetí andělský fond“ investora Depo Ventures je 500 000 000 CZK (stav k 7. 10. 2022).

**Co hledat ve zdroji:** Najdi ve zdroji částku 500 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://cc.cz/vice-penez-pro-nejmladsi-startupy-depo-ventures-otevira-novy-andelsky-fond-cili-na-pul-miliardy/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 49. `f-00261` – Depo Ventures (status: overeny)

**Tvrzení:** Jeden investor (LP) se zavázal vložit do fondu „DEPO Ventures One SCSp“ investora Depo Ventures 94 000 000 CZK (stav k 26. 8. 2026); jde jen o část fondu.

**Co hledat ve zdroji:** Najdi ve zdroji částku 94 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), ne celkovou velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://www.nrb.cz/nri-dokoncila-vyber-venture-kapitaloveho-fondu-pro-program-fond-ukrajina/>  
Typ zdroje: média (sekundární), vydavatel: Národní rozvojová banka

## 50. `f-00262` – i&i Biotech Investments (status: overeny)

**Tvrzení:** Cílová velikost fondu „i&i Biotech Fund I SCSp“ investora i&i Biotech Investments je 50 000 000 EUR (stav k 24. 9. 2021).

**Co hledat ve zdroji:** Najdi ve zdroji částku 50 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://www.eif.org/press/all/eif-to-invest-25-million-to-support-biomedical-tech-transfer-in-central-europe>  
Typ zdroje: média (sekundární), vydavatel: European Investment Fund

## 51. `f-00263` – i&i Biotech Investments (status: overeny)

**Tvrzení:** Jeden investor (LP) se zavázal vložit do fondu „i&i Biotech Fund I SCSp“ investora i&i Biotech Investments 25 000 000 EUR (stav k 24. 9. 2021); jde jen o část fondu.

**Co hledat ve zdroji:** Najdi ve zdroji částku 25 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), ne celkovou velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://www.eif.org/press/all/eif-to-invest-25-million-to-support-biomedical-tech-transfer-in-central-europe>  
Typ zdroje: média (sekundární), vydavatel: European Investment Fund

## 52. `f-00264` – i&i Biotech Investments (status: overeny)

**Tvrzení:** Fond „i&i Biotech Fund I SCSp“ investora i&i Biotech Investments byl uzavřen s velikostí 47 000 000 EUR (stav k 30. 11. 2022); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 47 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://www.uochb.cz/en/news/451/experienced-businessmen-join-forces-with-excellent-science-invest-eur-2-million-in-the-fund-of-iocb-prague-family>  
Typ zdroje: média (sekundární), vydavatel: ÚOCHB AV ČR

## 53. `f-00265` – i&i Biotech Investments (status: overeny)

**Tvrzení:** Z fondu „i&i Biotech Fund I SCSp“ investora i&i Biotech Investments bylo investováno 7 400 000 EUR (stav k 30. 11. 2022).

**Co hledat ve zdroji:** Najdi ve zdroji částku 7 400 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět, kolik fond už investoval (proinvestovaný kapitál), ne velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://www.uochb.cz/en/news/451/experienced-businessmen-join-forces-with-excellent-science-invest-eur-2-million-in-the-fund-of-iocb-prague-family>  
Typ zdroje: média (sekundární), vydavatel: ÚOCHB AV ČR

## 54. `f-00266` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo Stage 5“ investora Credo Ventures byl uzavřen s velikostí 88 000 000 USD (stav k 23. 3. 2026); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 88 000 000 USD: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://tech.eu/2026/03/23/credo-ventures-raises-88m-fund-5-to-double-down-on-pre-seed-in-cee-and-its-global-diaspora/>  
Typ zdroje: média (sekundární), vydavatel: Tech.eu

## 55. `f-00267` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo Stage 4“ investora Credo Ventures byl uzavřen s velikostí 75 000 000 EUR (stav k 10. 10. 2022); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 75 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://sifted.eu/articles/czech-credo-ventures-fund-75m-poland>  
Typ zdroje: média (sekundární), vydavatel: Sifted

## 56. `f-00268` – Tilia Impact Ventures (status: overeny)

**Tvrzení:** Fond „Tilia Impact Seed Fund“ investora Tilia Impact Ventures byl uzavřen s velikostí 26 000 000 EUR (stav k 21. 9. 2023); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 26 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/cesky-fond-urceny-na-investice-se-spolecenskymi-dopady-ma-dalsich-600-milionu-podporili-ho-winkler-ci-barta/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 57. `f-00269` – Tilia Impact Ventures (status: overeny)

**Tvrzení:** Cílová velikost fondu „Tilia Impact Seed Fund“ investora Tilia Impact Ventures je 32 000 000 EUR (stav k 21. 9. 2023).

**Co hledat ve zdroji:** Najdi ve zdroji částku 32 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://cc.cz/cesky-fond-urceny-na-investice-se-spolecenskymi-dopady-ma-dalsich-600-milionu-podporili-ho-winkler-ci-barta/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 58. `f-00270` – Tilia Impact Ventures (status: overeny)

**Tvrzení:** Fond „Tilia Impact Ventures – první fond“ investora Tilia Impact Ventures byl uzavřen s velikostí 43 000 000 CZK (stav k 28. 11. 2018); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 43 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/silke-horakova-a-petr-vitek-z-noveho-tilia-impact-ventures-chybel-nam-rizikovy-kapital-pro-socialni-inovace/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 59. `f-00271` – Rockaway Ventures (status: overeny)

**Tvrzení:** Fond „Rockaway Ventures Fund II“ investora Rockaway Ventures byl uzavřen s velikostí 55 000 000 EUR (stav k 14. 5. 2025); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 55 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/rockaway-ventures-oznamilo-druhy-fond-na-startupy-ma-pripravene-14-miliardy-korun/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 60. `f-00272` – Purple Ventures (status: overeny)

**Tvrzení:** Purple Ventures investuje do těchto sektorů: software, zdravotnické technologie (healthtech), energetika, kybernetická bezpečnost, média.

**Co hledat ve zdroji:** Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://tech.eu/2024/06/27/purple-ventures-launches-eur40m-fund-for-early-stage-software-startups/>  
Typ zdroje: média (sekundární), vydavatel: Tech.eu

## 61. `f-00273` – Purple Ventures (status: overeny)

**Tvrzení:** Cílová velikost fondu „Purple Ventures 2“ investora Purple Ventures je 40 000 000 EUR (stav k 27. 6. 2024).

**Co hledat ve zdroji:** Najdi ve zdroji částku 40 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://tech.eu/2024/06/27/purple-ventures-launches-eur40m-fund-for-early-stage-software-startups/>  
Typ zdroje: média (sekundární), vydavatel: Tech.eu

## 62. `f-00274` – Purple Ventures (status: overeny)

**Tvrzení:** Jeden investor (LP) se zavázal vložit do fondu „Purple Ventures 2“ investora Purple Ventures 14 000 000 EUR (stav k 27. 6. 2024); jde jen o část fondu.

**Co hledat ve zdroji:** Najdi ve zdroji částku 14 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), ne celkovou velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://tech.eu/2024/06/27/purple-ventures-launches-eur40m-fund-for-early-stage-software-startups/>  
Typ zdroje: média (sekundární), vydavatel: Tech.eu

## 63. `f-00275` – Purple Ventures (status: overeny)

**Tvrzení:** Fond „Purple Ventures 2“ investora Purple Ventures byl uzavřen s velikostí 700 000 000 CZK; zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 700 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://purple-ventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Purple Ventures

## 64. `f-00276` – Purple Ventures (status: overeny)

**Tvrzení:** Z fondu „Purple Ventures 2“ investora Purple Ventures bylo investováno 250 000 000 CZK.

**Co hledat ve zdroji:** Najdi ve zdroji částku 250 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět, kolik fond už investoval (proinvestovaný kapitál), ne velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://purple-ventures.com/>  
Typ zdroje: web investora (primární), vydavatel: Purple Ventures

## 65. `f-00277` – Lighthouse Ventures (status: overeny)

**Tvrzení:** Fond „Lighthouse Seed Fund“ investora Lighthouse Ventures byl uzavřen s velikostí 23 000 000 EUR (stav k 7. 6. 2019); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 23 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/cesky-fond-lighthouse-ventures-vlozil-vyssi-stovky-tisic-eur-do-brnenskeho-ai-startupu-pekat-vision/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 66. `f-00278` – Lighthouse Ventures (status: overeny)

**Tvrzení:** Jeden investor (LP) se zavázal vložit do fondu „Lighthouse Seed Fund“ investora Lighthouse Ventures 15 000 000 EUR (stav k 7. 6. 2019); jde jen o část fondu.

**Co hledat ve zdroji:** Najdi ve zdroji částku 15 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), ne celkovou velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/cesky-fond-lighthouse-ventures-vlozil-vyssi-stovky-tisic-eur-do-brnenskeho-ai-startupu-pekat-vision/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 67. `f-00279` – Tachles (status: overeny)

**Tvrzení:** Oficiální web investora Tachles je https://tachlesvc.com/.

**Co hledat ve zdroji:** Zdroj je tento web, nebo na něj odkazuje jako na web investora. Doména musí být stejná a web musí patřit investorovi Tachles, ne firmě s podobným názvem.

**Zdroj:** <https://tachlesvc.com/team>  
Typ zdroje: web investora (primární), vydavatel: Tachles VC

## 68. `f-00280` – Tachles (status: overeny)

**Tvrzení:** Tachles investuje v těchto fázích: seed.

**Co hledat ve zdroji:** Zdroj jmenuje každou z uvedených fází (např. „early stage“ samo o sobě nestačí na série A). Pokud některá uvedená fáze ve zdroji chybí, je verdikt chybne.

**Zdroj:** <https://tachles.decilehub.com/submit_your_company>  
Typ zdroje: web investora (primární), vydavatel: Tachles VC (formulář na Decile Hub)

## 69. `f-00281` – Tachles (status: overeny)

**Tvrzení:** Fond „Tachles VC“ investora Tachles dosáhl prvního uzavření (first close) ve výši 500 000 000 CZK (stav k 13. 6. 2024).

**Co hledat ve zdroji:** Najdi ve zdroji částku 500 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět first close (první uzavření), ne konečnou nebo cílovou velikost. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/roky-hledali-startupy-pro-fond-karla-komarka-ted-rozbihaji-vlastni-v-prvni-fazi-maji-pul-miliardy/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 70. `f-00282` – Tachles (status: overeny)

**Tvrzení:** Tachles dosud investoval celkem 30 000 000 CZK (stav k 12. 2. 2025).

**Co hledat ve zdroji:** Najdi ve zdroji částku 30 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o skutečně investovaný kapitál, ne o velikost fondu ani o spravovaná aktiva.

**Zdroj:** <https://cc.cz/cesi-v-izraeli-na-lovu-miliardovych-jednorozcu-navzdory-konfliktu-se-tu-startupum-dari-hlasi/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 71. `f-00283` – Soulmates Ventures (status: overeny)

**Tvrzení:** Fond „Soulmates Ventures – fond 50 mil. EUR“ investora Soulmates Ventures byl uzavřen s velikostí 50 000 000 EUR (stav k 18. 3. 2025); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 50 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://vestbee.com/blog/articles/soulmates-ventures-raises-50-m-fund>  
Typ zdroje: média (sekundární), vydavatel: Vestbee

## 72. `f-00284` – Startguide VC (status: overeny)

**Tvrzení:** Cílová velikost fondu „SG One“ investora Startguide VC je 6 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 6 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://www.startguide.cz/sgone/>  
Typ zdroje: web investora (primární), vydavatel: Start Guide

## 73. `f-00285` – Startguide VC (status: overeny)

**Tvrzení:** Cílová velikost fondu „SG Two“ investora Startguide VC je 20 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 20 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), ne o velikost kola ani o vklad do jedné firmy.

**Zdroj:** <https://www.startguide.cz/sgtwo/>  
Typ zdroje: web investora (primární), vydavatel: Start Guide

## 74. `f-00286` – Startguide VC (status: overeny)

**Tvrzení:** Typická investice investora Startguide VC do jednoho startupu dosahuje nejvýše 2 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 2 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o horní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://www.startguide.cz/sgtwo/>  
Typ zdroje: web investora (primární), vydavatel: Start Guide

## 75. `f-00287` – IP Lab Ventures (status: overeny)

**Tvrzení:** Jeden investor (LP) se zavázal vložit do fondu „IP Lab Ventures Fund“ investora IP Lab Ventures 656 000 000 CZK (stav k 23. 9. 2026); jde jen o část fondu.

**Co hledat ve zdroji:** Najdi ve zdroji částku 656 000 000 CZK: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), ne celkovou velikost fondu. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/vlada-posila-700-milionu-do-noveho-druhu-fondu-zameri-se-i-na-ai-ridi-ho-byvaly-sef-dame-jidlo/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 76. `f-00288` – IP Lab Ventures (status: overeny)

**Tvrzení:** Typická investice investora IP Lab Ventures do jednoho startupu dosahuje nejvýše 1 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 1 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o horní mez investice fondu do jedné firmy (ticket, check size), ne o velikost celého kola ani velikost fondu.

**Zdroj:** <https://www.lupa.cz/aktuality/ceske-univerzitni-napady-maji-dostat-az-miliardu-na-cestu-z-laboratore-do-byznysu-vetsina-penez-jde-z-evropy/>  
Typ zdroje: média (sekundární), vydavatel: Lupa.cz

## 77. `f-00289` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo 1“ investora Credo Ventures byl uzavřen s velikostí 18 000 000 EUR; zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 18 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/dalsi-tezka-vaha-na-investicnim-poli-ceske-credo-otevira-svuj-treti-fond-ve-kterem-ma-pro-startupy-25-miliardy-korun/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 78. `f-00290` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo 2“ investora Credo Ventures byl uzavřen s velikostí 53 000 000 EUR; zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 53 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/dalsi-tezka-vaha-na-investicnim-poli-ceske-credo-otevira-svuj-treti-fond-ve-kterem-ma-pro-startupy-25-miliardy-korun/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch

## 79. `f-00291` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo Stage 3“ investora Credo Ventures byl uzavřen s velikostí 100 000 000 USD (stav k 1. 11. 2019); zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 100 000 000 USD: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci. Datum připadá na 1. den měsíce: může jít o údaj s přesností na měsíc, pak stačí shoda měsíce a roku.

**Zdroj:** <https://www.money.pl/gielda/fundusz-credo-ventures-planuje-zainwestowac-prawie-100-mln-usd-w-cee-6487384000940161a.html>  
Typ zdroje: média (sekundární), vydavatel: money.pl

## 80. `f-00292` – Credo Ventures (status: overeny)

**Tvrzení:** Investor Credo Ventures má celkem 5 fondů (stav k 23. 3. 2026).

**Co hledat ve zdroji:** Zdroj musí uvádět počet fondů investora, výslovně (např. „spravuje tři fondy“) nebo pořadím posledního fondu (např. „pátý fond“). Počet musí sedět; jiný počet je chybne.

**Zdroj:** <https://tech.eu/2026/03/23/credo-ventures-raises-88m-fund-5-to-double-down-on-pre-seed-in-cee-and-its-global-diaspora/>  
Typ zdroje: média (sekundární), vydavatel: Tech.eu

## 81. `f-00293` – Tensor Ventures (status: overeny)

**Tvrzení:** Investor Tensor Ventures má celkem 2 fondů (stav k 18. 9. 2025).

**Co hledat ve zdroji:** Zdroj musí uvádět počet fondů investora, výslovně (např. „spravuje tři fondy“) nebo pořadím posledního fondu (např. „pátý fond“). Počet musí sedět; jiný počet je chybne.

**Zdroj:** <https://forbes.cz/tensor-vybral-miliardu-a-miri-dal-cesti-investori-sazi-na-ai-i-kvantove-technologie/>  
Typ zdroje: média (sekundární), vydavatel: Forbes Česko

## 82. `f-00294` – Reflex Capital (status: overeny)

**Tvrzení:** Reflex Capital dosud investoval celkem 150 000 000 EUR.

**Co hledat ve zdroji:** Najdi ve zdroji částku 150 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Musí jít o skutečně investovaný kapitál, ne o velikost fondu ani o spravovaná aktiva.

**Zdroj:** <https://www.reflexcapital.com/cs/>  
Typ zdroje: web investora (primární), vydavatel: Reflex Capital

## 83. `f-00295` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo Stage 5“ investora Credo Ventures dosáhl prvního uzavření (first close) ve výši 88 000 000 USD (stav k 1. 3. 2026).

**Co hledat ve zdroji:** Najdi ve zdroji částku 88 000 000 USD: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí uvádět first close (první uzavření), ne konečnou nebo cílovou velikost. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci. Datum připadá na 1. den měsíce: může jít o údaj s přesností na měsíc, pak stačí shoda měsíce a roku.

**Zdroj:** <https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic>  
Typ zdroje: jiný zdroj (sekundární), vydavatel: Wikipedie

## 84. `f-00296` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo Stage 5“ investora Credo Ventures byl konečně uzavřen (final close) s velikostí 88 000 000 USD (stav k 23. 3. 2026).

**Co hledat ve zdroji:** Najdi ve zdroji částku 88 000 000 USD: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí výslovně uvádět konečné uzavření (final close, „definitivně uzavřel“). Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://thenextweb.com/news/credo-ventures-88m-fund>  
Typ zdroje: média (sekundární), vydavatel: TNW

## 85. `f-00297` – Credo Ventures (status: overeny)

**Tvrzení:** Fond „Credo Stage 3“ investora Credo Ventures byl uzavřen s velikostí 100 000 000 EUR; zdroj neupřesňuje, zda šlo o final close.

**Co hledat ve zdroji:** Najdi ve zdroji částku 100 000 000 EUR: musí sedět číslo i měna (bez přepočtu na jinou měnu). Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. Chybné je, pokud jde o cíl, plán nebo first close. Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, když částka odpovídá číslu v této formulaci.

**Zdroj:** <https://cc.cz/andrej-kiska-z-credo-ventures-nejdriv-byla-slabina-ze-jsme-z-vychodni-evropy-ted-na-to-investori-v-silicon-valley-slysi/>  
Typ zdroje: média (sekundární), vydavatel: CzechCrunch
