Data sbíral, kód psal a dokumentaci připravoval agent **Claude Code**. Pokyny pro něj jsem připravoval s pomocí chatového asistenta, rozhodoval a kontroloval jsem sám. Ruční kontrolu dat dělal člověk, ne model.

- **Žádný fakt z paměti modelu:** jen ze stránky, kterou agent v té session skutečně otevřel.
- **Nic se neodhaduje:** neznámá hodnota zůstává neznámá, domény se nehádají, agregátory slouží jen jako vodítko.
- **Konflikty zdrojů jsou vidět:** žádná verze se nevybírá potichu.
- **Kontroluje člověk:** verdikty mění jen hodnotitel, opravy po kontrole nemění metriku zpětně.

Výstup hlídal validátor, kontrola surového textu stránek a ruční kontroly po kolech.
