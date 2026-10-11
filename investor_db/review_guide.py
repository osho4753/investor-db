from dataclasses import dataclass
from datetime import date
from typing import Final

from investor_db.io import Dataset, Row
from investor_db.schema import (
    EXCLUSION_REASONS,
    FACT_EXCLUSION_REASON,
    FACT_FIELDS,
    INVESTMENT_SECTORS,
    INVESTMENT_STAGES,
    MONEY_FACT_FIELDS,
    PRIMARY_SOURCE_TYPES,
    REVIEW_ROUND_COMPLETION,
    REVIEW_ROUND_CORRECTION,
    CATEGORY_VC_EXCLUDED,
    REVIEW_ROUND_SAMPLE,
    REVIEW_ROUNDS,
    SOURCE_TYPES,
)
from investor_db.values import parse_date, parse_money, split_list


class GuideTemplateError(ValueError):
    pass


@dataclass(frozen=True)
class FieldGuide:
    claim: str
    look_for: str


@dataclass(frozen=True)
class FactGuide:
    fact_id: str
    investor_name: str
    investor_status: str
    claim: str
    look_for: str
    source_url: str
    source_label: str


AMOUNT_CHECK: Final = (
    "Najdi ve zdroji částku {money}: musí sedět číslo i měna (bez přepočtu na jinou měnu)."
)
APPROX_AMOUNT_CHECK: Final = (
    "Pokud zdroj uvádí přibližnou formulaci („téměř“, „přes“, „zhruba“), je fakt správný, "
    "když částka odpovídá číslu v této formulaci."
)

FIELD_GUIDES: Final[dict[str, FieldGuide]] = {
    "name": FieldGuide(
        claim="Investor (VC značka) vystupuje pod názvem „{value}“.",
        look_for=(
            "Zdroj uvádí tento název (rozdíl jen ve velkých písmenech nebo v právní formě nevadí) "
            "a popisuje stejný subjekt, ne jinou firmu s podobným názvem."
        ),
    ),
    "registry_id": FieldGuide(
        claim="{investor} má českou právnickou osobu s IČO {value}.",
        look_for=(
            "Najdi ve zdroji subjekt s IČO {value}. Zkontroluj, že IČO sedí číslice po číslici "
            "a že název nebo sídlo subjektu odpovídá investorovi {investor}, ne jiné firmě."
        ),
    ),
    "website": FieldGuide(
        claim="Oficiální web investora {investor} je {value}.",
        look_for=(
            "Zdroj je tento web, nebo na něj odkazuje jako na web investora. "
            "Doména musí být stejná a web musí patřit investorovi {investor}, ne firmě s podobným názvem."
        ),
    ),
    "investment_sectors": FieldGuide(
        claim="{investor} investuje do těchto sektorů: {labels}.",
        look_for=(
            "Zdroj jmenuje každý z uvedených sektorů (stačí obdobné označení, např. „climate“ pro cleantech). "
            "Pokud některý uvedený sektor ve zdroji chybí, je verdikt chybne."
        ),
    ),
    "investment_stages": FieldGuide(
        claim="{investor} investuje v těchto fázích: {labels}.",
        look_for=(
            "Zdroj jmenuje každou z uvedených fází (např. „early stage“ samo o sobě nestačí na série A). "
            "Pokud některá uvedená fáze ve zdroji chybí, je verdikt chybne."
        ),
    ),
    "typical_ticket_min": FieldGuide(
        claim="Typická investice investora {investor} do jednoho startupu začíná na {money}.",
        look_for=(
            AMOUNT_CHECK
            + " Musí jít o dolní mez investice fondu do jedné firmy (ticket, check size), "
            "ne o velikost celého kola ani velikost fondu."
        ),
    ),
    "typical_ticket_max": FieldGuide(
        claim="Typická investice investora {investor} do jednoho startupu dosahuje nejvýše {money}.",
        look_for=(
            AMOUNT_CHECK
            + " Musí jít o horní mez investice fondu do jedné firmy (ticket, check size), "
            "ne o velikost celého kola ani velikost fondu."
        ),
    ),
    "total_fund_size": FieldGuide(
        claim="Fond {fund} investora {investor} byl uzavřen s konečnou velikostí {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí v minulém čase říkat, že fond byl uzavřen (final close) s touto velikostí. "
            "Chybné je, pokud jde o cílovou velikost, first close, formulaci „až X“, velikost kola "
            "nebo závazek jednoho investora do fondu."
        ),
    ),
    "assets_under_management": FieldGuide(
        claim="{investor} spravuje aktiva (AUM) v celkovém objemu {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Musí jít o celková spravovaná aktiva investora, ne o velikost jednoho fondu "
            "ani o dosud investovaný kapitál."
        ),
    ),
    "invested_capital": FieldGuide(
        claim="{investor} dosud investoval celkem {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Musí jít o skutečně investovaný kapitál, ne o velikost fondu ani o spravovaná aktiva."
        ),
    ),
    "fond_final_close": FieldGuide(
        claim="Fond {fund} investora {investor} byl konečně uzavřen (final close) s velikostí {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí výslovně uvádět konečné uzavření (final close, „definitivně uzavřel“). "
            + APPROX_AMOUNT_CHECK
        ),
    ),
    "fond_uzavren": FieldGuide(
        claim="Fond {fund} investora {investor} byl uzavřen s velikostí {money}{as_of_clause}; zdroj neupřesňuje, zda šlo o final close.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí v minulém čase říkat, že fond byl uzavřen nebo upsán s touto velikostí. "
            "Chybné je, pokud jde o cíl, plán nebo first close. "
            + APPROX_AMOUNT_CHECK
        ),
    ),
    "fond_first_close": FieldGuide(
        claim="Fond {fund} investora {investor} dosáhl prvního uzavření (first close) ve výši {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí uvádět first close (první uzavření), ne konečnou nebo cílovou velikost. "
            + APPROX_AMOUNT_CHECK
        ),
    ),
    "fond_zavazek_lp": FieldGuide(
        claim="Jeden investor (LP) se zavázal vložit do fondu {fund} investora {investor} {money}{as_of_clause}; jde jen o část fondu.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí uvádět vklad nebo závazek jednoho investora do fondu (např. EIF, NRI), "
            "ne celkovou velikost fondu. "
            + APPROX_AMOUNT_CHECK
        ),
    ),
    "fond_investovano": FieldGuide(
        claim="Z fondu {fund} investora {investor} bylo investováno {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí uvádět, kolik fond už investoval (proinvestovaný kapitál), ne velikost fondu. "
            + APPROX_AMOUNT_CHECK
        ),
    ),
    "fond_investovano_za_obdobi": FieldGuide(
        claim="Z fondu {fund} investora {investor} bylo za období uvedené ve zdroji investováno {money}{as_of_clause}; jde o dolní mez celkové investované částky.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj musí uvádět částku investovanou za vymezené období (např. „během minulého roku“). "
            "Chybné je, pokud zdroj uvádí celkovou investovanou částku nebo velikost fondu. "
            + APPROX_AMOUNT_CHECK
        ),
    ),
    "pocet_fondu": FieldGuide(
        claim="Investor {investor} má celkem {value} fondů{as_of_clause}.",
        look_for=(
            "Zdroj musí uvádět počet fondů investora, výslovně (např. „spravuje tři fondy“) nebo pořadím "
            "posledního fondu (např. „pátý fond“). Počet musí sedět; jiný počet je chybne."
        ),
    ),
    "informace_o_fondu": FieldGuide(
        claim="O fondu {fund} investora {investor} platí: {value}{as_of_clause}.",
        look_for=(
            "Zdroj potvrzuje každou část tvrzení: název fondu, uvedené částky a měny, data a role subjektů "
            "(správce, GP, AIFM). Pokud zdroj potvrzuje jen část, je verdikt chybne a do note napiš, co chybí."
        ),
    ),
    "pravni_spravce": FieldGuide(
        claim="Právním správcem fondu {fund} investora {investor} je {value}.",
        look_for=(
            "Zdroj jmenuje právě tuto entitu jako správce, GP nebo AIFM uvedeného fondu. "
            "Zkontroluj přesný název entity, protože správci mívají podobné názvy."
        ),
    ),
    "cilova_velikost_fondu": FieldGuide(
        claim="Cílová velikost fondu {fund} investora {investor} je {money}{as_of_clause}.",
        look_for=(
            AMOUNT_CHECK
            + " Musí jít o cílovou nebo plánovanou velikost fondu (target, „až X“), "
            "ne o velikost kola ani o vklad do jedné firmy."
        ),
    ),
    "oznamena_velikost_fondu": FieldGuide(
        claim="Zdroj uvádí velikost fondu {fund} investora {investor} {money}{as_of_clause}, aniž rozlišuje cíl a získanou částku.",
        look_for=(
            AMOUNT_CHECK
            + " Zdroj uvádí velikost fondu bez slov jako cíl, target, „až“, uzavřen nebo získal. "
            "Chybné je, pokud zdroj typ výslovně uvádí; pak patří do cilova_velikost_fondu nebo fond_uzavren."
        ),
    ),
    "registrace_regulator": FieldGuide(
        claim="{investor} je u regulátora zapsán takto: {value}{as_of_clause}.",
        look_for=(
            "Zdroj (seznam regulátora) obsahuje tuto entitu s uvedeným typem registrace. "
            "Zkontroluj název a IČO entity, ne jen podobný název."
        ),
    ),
    "dolozena_investice": FieldGuide(
        claim="{investor} investoval do společnosti {value}{announced_clause}.",
        look_for=(
            "Zdroj uvádí, že do této společnosti investoval právě {investor} (nebo jeho fond), "
            "a datum oznámení odpovídá. Chybné je, pokud investoval jiný investor s podobným názvem "
            "nebo jde o jinou, starší investici."
        ),
    ),
}

EXCLUSION_GUIDES: Final[dict[str, FieldGuide]] = {
    "pe_budouci_rozsireni": FieldGuide(
        claim=(
            "{investor} investuje hlavně formou buyoutů a většinových podílů (PE), "
            "proto není VC a je odložen pro budoucí rozšíření."
        ),
        look_for=(
            "Zdroj popisuje subjekt jako private equity (buyout, většinové podíly, zralé firmy), "
            "nebo ho do private equity zařazuje."
        ),
    ),
    "cvc": FieldGuide(
        claim=(
            "{investor} je korporátní VC (corporate VC): fond je napojen na jednu korporátní skupinu. "
            "Vyloučit ho lze jen tehdy, když tato skupina dává více než 50 % kapitálu fondu."
        ),
        look_for=(
            "Zdroj uvádí, že fond patří pod korporátní skupinu nebo investuje její kapitál. "
            "Do note zapiš, zda zdroj dokládá i podíl skupiny na kapitálu fondu nad 50 %."
        ),
    ),
    "fond_fondu": FieldGuide(
        claim="{investor} je fond fondů: investuje do jiných fondů, ne přímo do firem, proto je vyloučen.",
        look_for="Zdroj uvádí, že subjekt vkládá kapitál do jiných fondů, nikoli přímo do podílů ve firmách.",
    ),
    "statni_fond": FieldGuide(
        claim=(
            "{investor} je státní fond, státní program nebo rozvojová instituce financovaná z veřejných "
            "prostředků, proto je vyloučen."
        ),
        look_for=(
            "Zdroj uvádí, že subjekt zřizuje nebo financuje stát, ministerstvo, veřejná instituce "
            "nebo fondy EU."
        ),
    ),
    "dluhovy_fond": FieldGuide(
        claim=(
            "{investor} poskytuje hlavně dluhové financování (úvěry, mezanin, venture debt), "
            "ne kapitál za podíl, proto je vyloučen."
        ),
        look_for=(
            "Zdroj popisuje hlavní strategii jako úvěry, dluh, mezanin nebo venture debt. "
            "Pokud zdroj uvádí kapitálové investice jako hlavní strategii, je verdikt chybne."
        ),
    ),
    "digitalni_aktiva": FieldGuide(
        claim=(
            "{investor} je fond digitálních aktiv: investuje do tokenů, blockchainových protokolů "
            "nebo kryptoměn, ne do podílů ve firmách, proto je vyloučen."
        ),
        look_for="Zdroj uvádí, že fond drží digitální aktiva (tokeny, kryptoměny, protokoly), ne podíly ve firmách.",
    ),
    "otevreny_smiseny_fond": FieldGuide(
        claim=(
            "{investor} je otevřený fond s průběžnou likviditou, který kombinuje podíly ve firmách "
            "s kotovanými akciemi, proto není VC fond a je vyloučen."
        ),
        look_for=(
            "Zdroj uvádí, že fond je otevřený (průběžný vstup a výstup investorů, např. měsíční likvidita) "
            "a drží i kotované akcie."
        ),
    ),
    "zahranicni_subjekt": FieldGuide(
        claim="{investor} nemá českou právnickou osobu (správce i fond sídlí v zahraničí), proto je vyloučen.",
        look_for=(
            "Zdroj uvádí zahraniční sídlo nebo zahraničního správce a nezmiňuje českou entitu investora."
        ),
    ),
    "business_angel": FieldGuide(
        claim="{investor} je jednotlivec (business angel), který investuje vlastní peníze bez fondu, proto je vyloučen.",
        look_for="Zdroj popisuje osobu, která investuje vlastní prostředky, ne fond s kapitálem třetích osob.",
    ),
    "family_office": FieldGuide(
        claim=(
            "{investor} investuje kapitál jedné rodiny nebo jednoho majitele (family office) "
            "a kapitál třetích osob není doložen, proto není VC fond a je vyloučen."
        ),
        look_for=(
            "Zdroj uvádí, že subjekt investuje vlastní kapitál majitele nebo rodiny, "
            "a nezmiňuje externí investory fondu."
        ),
    ),
    "bez_fondu": FieldGuide(
        claim=(
            "{investor} neinvestuje z vlastního fondu (např. poradce, investiční platforma "
            "nebo akcelerátor bez investičního vehiklu), proto je vyloučen."
        ),
        look_for="Zdroj popisuje činnost subjektu tak, že z ní nevyplývá žádný vlastní investiční fond nebo vehikl.",
    ),
    "neaktivni": FieldGuide(
        claim="{investor} nemá za posledních 36 měsíců doloženou žádnou investici ani nový fond, proto je vyloučen.",
        look_for="Nejnovější investice nebo fond uvedené ve zdroji jsou starší než 36 měsíců.",
    ),
    "zanikly_subjekt": FieldGuide(
        claim="Právnická osoba investora {investor} zanikla nebo už neexistuje, proto je vyloučen.",
        look_for="Zdroj (rejstřík) uvádí datum zániku subjektu, nebo subjekt tohoto jména nevrací.",
    ),
    "duplicita": FieldGuide(
        claim="{investor} je jen jiným názvem nebo jinou entitou investora, který už je v databázi, proto je vyloučen.",
        look_for="Zdroj ukazuje, že jde o tutéž značku (stejný tým, web nebo IČO) jako jiný záznam v databázi.",
    ),
}

STAGE_LABELS: Final = {
    "pre_seed": "pre-seed",
    "seed": "seed",
    "serie_a": "série A",
    "serie_b": "série B",
    "growth": "růstová fáze (growth)",
    "buyout": "odkup většinového nebo kontrolního podílu (buyout, MBO, MBI, LBO)",
    "growth_equity": "růstový kapitál do zralé firmy (growth equity, expansion capital)",
}

SECTOR_LABELS: Final = {
    "ai": "umělá inteligence (AI)",
    "agritech": "zemědělské technologie (agritech)",
    "biotech": "biotechnologie",
    "cleantech": "čisté technologie (cleantech, climate)",
    "deeptech": "deep tech",
    "ecommerce": "e-commerce",
    "edtech": "vzdělávací technologie (edtech)",
    "energetika": "energetika",
    "fintech": "finanční technologie (fintech)",
    "gaming": "hry (gaming)",
    "hardware": "hardware",
    "healthtech": "zdravotnické technologie (healthtech)",
    "kyberbezpecnost": "kybernetická bezpečnost",
    "media": "média",
    "mobilita": "mobilita",
    "proptech": "nemovitostní technologie (proptech)",
    "prumysl": "průmysl",
    "software": "software",
    "spotrebitelske": "spotřebitelské produkty a služby",
    "obrana_bezpecnost": "obrana a bezpečnost",
    "cestovani": "cestování",
    "logistika": "logistika",
    "jine": "jiné sektory",
    "sektorove_agnosticky": "bez sektorového omezení (sector agnostic)",
    "sluzby_firmam": "služby pro firmy (business services)",
    "zdravotnictvi": "zdravotní péče a služby (healthcare)",
    "vzdelavani": "vzdělávací služby (education)",
    "financni_sluzby": "finanční služby (financial services)",
    "maloobchod": "maloobchod (retail)",
    "stavebnictvi": "stavebnictví (construction)",
    "tmt": "telekomunikace, média a technologie (TMT)",
    "potravinarstvi": "potravinářství (food production)",
}

LIST_LABELS: Final = {"investment_sectors": SECTOR_LABELS, "investment_stages": STAGE_LABELS}

SOURCE_TYPE_LABELS: Final = {
    "regulator": "regulátor",
    "rejstrik": "veřejný rejstřík",
    "vyrocni_zprava": "výroční zpráva",
    "web_investora": "web investora",
    "asociace": "asociace",
    "media": "média",
    "jine": "jiný zdroj",
}

ARES_HOST: Final = "ares.gov.cz"
ARES_SEARCH_SUFFIX: Final = "/vyhledat"
ARES_JSON_HINT: Final = (
    "Odkaz vede na rozhraní ARES a prohlížeč zobrazí data ve formátu JSON: IČO je v poli „ico“, "
    "název v „obchodniJmeno“, sídlo v „sidlo“, vznik a zánik v „datumVzniku“ a „datumZaniku“, "
    "statutární orgány (u adres s „ekonomicke-subjekty-vr“) v „statutarniOrgany“."
)
ARES_SEARCH_HINT: Final = (
    "Odkaz vede na vyhledávací rozhraní ARES, které nejde otevřít přímo v prohlížeči. "
    "Vyhledej název ve webovém vyhledávání na https://ares.gov.cz."
)
MONTH_PRECISION_HINT: Final = (
    "Datum připadá na 1. den měsíce: může jít o údaj s přesností na měsíc, pak stačí shoda měsíce a roku."
)
MISSING_FUND_NAME: Final = "(název fondu neuveden)"


def format_czech_date(day: date) -> str:
    return f"{day.day}. {day.month}. {day.year}"


def format_money(value: str, currency: str) -> str:
    amount = parse_money(value)
    if amount is None:
        raise GuideTemplateError(f"hodnota „{value}“ není částka")
    digits = f"{amount:,f}".replace(",", " ").replace(".", ",")
    return f"{digits} {currency}".strip()


def list_labels(field: str, value: str) -> str:
    labels = LIST_LABELS[field]
    unknown = [code for code in split_list(value) if code not in labels]
    if unknown:
        raise GuideTemplateError(f"pole {field} nemá popis pro hodnoty: {', '.join(unknown)}")
    return ", ".join(labels[code] for code in split_list(value))


def field_guide(fact: Row) -> FieldGuide:
    field = fact["field"]
    if field == FACT_EXCLUSION_REASON:
        if fact["value"] not in EXCLUSION_GUIDES:
            raise GuideTemplateError(f"důvod vyloučení „{fact['value']}“ nemá šablonu")
        return EXCLUSION_GUIDES[fact["value"]]
    if field not in FIELD_GUIDES:
        raise GuideTemplateError(f"pole „{field}“ nemá šablonu")
    return FIELD_GUIDES[field]


def template_values(fact: Row, investor_name: str) -> dict[str, str]:
    as_of = parse_date(fact["value_as_of"])
    as_of_text = format_czech_date(as_of) if as_of else ""
    values = {
        "investor": investor_name,
        "value": fact["value"],
        "fund": f"„{fact['fund_name']}“" if fact["fund_name"] else MISSING_FUND_NAME,
        "as_of_clause": f" (stav k {as_of_text})" if as_of else "",
        "announced_clause": f" (oznámeno {as_of_text})" if as_of else " (datum oznámení neuvedeno)",
        "money": "",
        "labels": "",
    }
    if fact["field"] in MONEY_FACT_FIELDS:
        values["money"] = format_money(fact["value"], fact["currency"])
    if fact["field"] in LIST_LABELS:
        values["labels"] = list_labels(fact["field"], fact["value"])
    return values


def source_label(source: Row) -> str:
    kind = "primární" if source["source_type"] in PRIMARY_SOURCE_TYPES else "sekundární"
    return f"{SOURCE_TYPE_LABELS[source['source_type']]} ({kind}), vydavatel: {source['publisher']}"


def source_hints(url: str) -> list[str]:
    if ARES_HOST not in url:
        return []
    return [ARES_SEARCH_HINT if url.endswith(ARES_SEARCH_SUFFIX) else ARES_JSON_HINT]


def date_hints(fact: Row) -> list[str]:
    as_of = parse_date(fact["value_as_of"])
    return [MONTH_PRECISION_HINT] if as_of and as_of.day == 1 else []


def build_fact_guide(fact: Row, investor: Row, source: Row) -> FactGuide:
    guide = field_guide(fact)
    values = template_values(fact, investor["name"])
    look_for = " ".join([guide.look_for.format(**values), *date_hints(fact), *source_hints(source["url"])])
    return FactGuide(
        fact_id=fact["fact_id"],
        investor_name=investor["name"],
        investor_status=investor["verification_status"],
        claim=guide.claim.format(**values),
        look_for=look_for,
        source_url=source["url"],
        source_label=source_label(source),
    )


def sampled_fact_ids(dataset: Dataset) -> list[str]:
    return sorted({row["fact_id"] for row in dataset.fact_reviews})


def review_rounds_present(dataset: Dataset) -> list[str]:
    present = {row["review_round"] for row in dataset.fact_reviews}
    return [review_round for review_round in REVIEW_ROUNDS if review_round in present]


def round_fact_ids(dataset: Dataset, review_round: str) -> list[str]:
    return sorted({row["fact_id"] for row in dataset.fact_reviews if row["review_round"] == review_round})


def build_fact_guides(dataset: Dataset, fact_ids: list[str]) -> list[FactGuide]:
    facts = {row["fact_id"]: row for row in dataset.facts}
    investors = {row["investor_id"]: row for row in dataset.investors}
    sources = {row["source_id"]: row for row in dataset.sources}
    guides = []
    for fact_id in fact_ids:
        fact = facts[fact_id]
        guides.append(build_fact_guide(fact, investors[fact["investor_id"]], sources[fact["source_id"]]))
    return guides


def missing_templates() -> list[str]:
    missing = [field for field in FACT_FIELDS if field != FACT_EXCLUSION_REASON and field not in FIELD_GUIDES]
    missing += [f"{FACT_EXCLUSION_REASON}={reason}" for reason in EXCLUSION_REASONS if reason not in EXCLUSION_GUIDES]
    missing += [f"source_type={kind}" for kind in SOURCE_TYPES if kind not in SOURCE_TYPE_LABELS]
    missing += [f"investment_stages={stage}" for stage in INVESTMENT_STAGES if stage not in STAGE_LABELS]
    missing += [f"investment_sectors={sector}" for sector in INVESTMENT_SECTORS if sector not in SECTOR_LABELS]
    return missing


def render_fact_guide(index: int, guide: FactGuide) -> str:
    return "\n".join([
        f"## {index}. `{guide.fact_id}` – {guide.investor_name} (status: {guide.investor_status})",
        "",
        f"**Tvrzení:** {guide.claim}",
        "",
        f"**Co hledat ve zdroji:** {guide.look_for}",
        "",
        f"**Zdroj:** <{guide.source_url}>  ",
        f"Typ zdroje: {guide.source_label}",
        "",
    ])


ROUND_HEADINGS: Final = {
    REVIEW_ROUND_SAMPLE: (
        "Původní kontrola – náhodný vzorek",
        "Náhodný vzorek faktů z původního sběru. Přesnost se z něj počítá zvlášť.",
    ),
    REVIEW_ROUND_COMPLETION: (
        "Kontrola po doplnění – všechny nové fakty",
        "Všechny fakty přidané doplňováním sektorů, ticketu a kapitálu, ne vzorek. Přesnost se počítá zvlášť.",
    ),
    REVIEW_ROUND_CORRECTION: (
        "Kontrola po opravě – fakty změněné po kontrole",
        "Fakty, kterým se po kontrole změnil typ, zdroj nebo hodnota, a fakty přidané při opravě. "
        "Posuzuje se současný stav faktu; verdikt patří do řádku s kolem po_oprave. Přesnost se počítá zvlášť.",
    ),
}


def render_round(dataset: Dataset, review_round: str, first_index: int) -> tuple[list[str], int]:
    guides = build_fact_guides(dataset, round_fact_ids(dataset, review_round))
    if not guides:
        return [], first_index
    heading, description = ROUND_HEADINGS[review_round]
    lines = [f"# {heading} ({len(guides)} faktů)", "", description, ""]
    lines += [render_fact_guide(index, guide) for index, guide in enumerate(guides, start=first_index)]
    return lines, first_index + len(guides)


EXCLUSION_REVIEW_INTRO: Final = (
    "Náhodný vzorek 10 z vyloučených VC subjektů (seed 2026). U každého subjektu odpověz na dvě otázky: "
    "1) Dokládá uvedený zdroj důvod vyloučení? 2) Je subjekt opravdu mimo definici VC pilotu (Z1–Z4 v docs/01, 1.3), "
    "nebo měl být ověřen či veden jako kandidát? Verdikt zapiš do `data/reviews.csv` do řádku s `category` = `vc_vyloucene`: "
    "`TP` = vyloučení je správné, `FP` = subjekt patří do VC pilotu (false negative), `nejiste` = zdroje nestačí. "
    "Do poznámky napiš, co rozhodlo; nepiš jména fyzických osob."
)


def exclusion_review_ids(dataset: Dataset) -> list[str]:
    return sorted({row["investor_id"] for row in dataset.reviews if row["category"] == CATEGORY_VC_EXCLUDED})


def render_exclusion_review(dataset: Dataset) -> list[str]:
    investor_ids = exclusion_review_ids(dataset)
    if not investor_ids:
        return []
    investors = {row["investor_id"]: row for row in dataset.investors}
    sources = {row["source_id"]: row for row in dataset.sources}
    lines = [f"# Kontrola vyloučených VC ({len(investor_ids)} subjektů)", "", EXCLUSION_REVIEW_INTRO, ""]
    for index, investor_id in enumerate(investor_ids, start=1):
        investor = investors[investor_id]
        reason = investor["exclusion_reason"]
        facts = [
            row for row in dataset.facts
            if row["investor_id"] == investor_id and row["field"] == FACT_EXCLUSION_REASON and row["value"] == reason
        ]
        lines += [f"## V{index}. `{investor_id}` – {investor['name']} (důvod vyloučení: `{reason}`)", ""]
        for fact in facts:
            guide = build_fact_guide(fact, investor, sources[fact["source_id"]])
            lines += [
                f"**Fakt `{guide.fact_id}`:** {guide.claim}",
                "",
                f"**Co hledat ve zdroji:** {guide.look_for}",
                "",
                f"**Poznámka sběrače:** {fact['evidence_note']}",
                "",
                f"**Zdroj:** <{guide.source_url}>  ",
                f"Typ zdroje: {guide.source_label}",
                "",
            ]
    return lines


def render_checklist(dataset: Dataset) -> str:
    header = [
        "# Kontrolní list faktů",
        "",
        "Vygenerováno příkazem `python -m investor_db review-guide` z `data/fact_reviews.csv`. "
        "Soubor neupravuj ručně, při změně dat ho vygeneruj znovu.",
        "",
        f"Kontrola obsahuje {len(sampled_fact_ids(dataset))} z {len(dataset.facts)} faktů v {len(review_rounds_present(dataset))} kolech. "
        "U každého faktu otevři zdroj a posuď jen to, zda zdroj podporuje uvedené tvrzení. "
        "Verdikt (`spravne`, `chybne`, `nelze_overit`), datum, čas v minutách a poznámku zapiš "
        "do řádku se stejným `fact_id` a kolem (`review_round`) v `data/fact_reviews.csv`. "
        "Podrobný návod je v `docs/04-rucni-kontrola.md`, sekce „Návod pro hodnotitele“.",
        "",
    ]
    body: list[str] = []
    next_index = 1
    for review_round in REVIEW_ROUNDS:
        lines, next_index = render_round(dataset, review_round, next_index)
        body += lines
    body += render_exclusion_review(dataset)
    return "\n".join(header + body)
