from string_processing import *


KNOWN_TITLES = {"attorney", "solicitor", "assistant", "general", "public", "guardian"}
TITLE_ERRATA = {
    "assis tant state’s attorney": "assistant states attorney",
    "assistant state’s .attorneys": "assistant states attorney",
    "assistant state’s attorneys": "assistant states attorney",
    "assistant state attorneys": "assistant state attorney",
    "as sistant attorney general": "assistant attorney general",
    "as sistant attorneys general": "assistant attorney general",
    "asst attorney generals": "asstistant attorney general",
    "solid- tor general": "solicitor general",
    "solid tor general": "solicitor general",
    "solic itor general": "solicitor general",
    "so licitor general": "solicitor general",
    "special assist ant attorneys general": "special assistant attorney general",
    "spe cial assistant state’s attorney": "special assistant states attorney",
    "spe- j cial assistant state’s attorney": "special assistant states attorney",
    "spe j cial assistant state’s attorney": "special assistant states attorney",
    "special assistant state’s attorneys": "special assistant states attorneys",
    "assistant state’s at-. torney": "assistant states attorney",
    "assistant state’s at torney": "assistant states attorney",
    "' states attorney": "states attorney",
    "' city attorney": "city attorney",
    "-attorney general": "attorney general",
    "deputy state's attorney": "deputy states attorney",
    "solicitors general": "solicitor general",
    "public defendei": "public defender",
    "asst attorney general": "assistant attorney general",
    "public dedender": "public defender",
    "state’s attorney": "states attorney",
    "state’ attorney": "states attorney",
    "ass’t county attorney": "assistant county attorney",
    'attorney" general': "attorney general",
    "‘attorney general": "attorney general",
    "solicitor géneral": "solicitor general",
    "associate state’s attorney": "associate states attorney",
    "former state’s attorney": "former states attorney",
    "deputy  state’s attorney": "deputy states attorney",
}

KNOWN_CASE_PARTIES = {
    "appellant",
    "appellee",
    "plaintiff",
    "defendant",
    "claimant",
}

KNOWN_NON_NAME_WORDS = {
    "llc",
    "ltd.",
    "inc.",
    "argued",
    "all of",
    "p.c.",
    "&",
    "coun",
    "corporation",
    "counsel",
    "pro se",
    "pro se.",
    "ec.",
    "appointed",
    "attorneys",
}

GOVT_PARTIES = {
    "assistant attorney general",
    "attorney general",
    "solicitor general",
    "the people",
    "assistant states attorney",
    "special assistant attorney general",
    "county attorney",
    "deputy states attorney",
    "regional solicitor",
    "solicitor of labor",
    "special attorney",
    "chief assistant city prosecutor",
    "city attorney",
    "guardian ad litem",
    "public guardian",
    "states attorney",
    "regional litigation attorney",
    "panel attorney",
    "first assistant attorney general",
    "village attorney",
    "city prosecuting attorney",
    "assistant prosecuting attorney",
    "prosecuting attorney",
    "chief assistant prosecutor",
}


def is_title(string):
    """Determines if the string is a position title."""
    return bool(set(string.split(" ")) & (KNOWN_TITLES | KNOWN_CASE_PARTIES))


def is_place_of_origin(string):
    """Determines if the string is a location or non-person."""
    return string.startswith("of ") or string.startswith("both ")


def is_party_indicator(string):
    """Determines if the string indicates the party to which the attorney 
    belongs to.
    """
    return string.startswith("for ")


def is_other_string(string):
    """Indicates that the string represents some other entity or meaning."""
    return string in KNOWN_NON_NAME_WORDS or bool(set(string) & KNOWN_NON_NAME_WORDS)


def is_person_name(string):
    """Determines if the string is a person name or not."""
    return all(
        [
            not is_person_title(string),
            not is_other_string(string),
            not is_place_of_origin(string),
            not is_party_indicator(string),
        ]
    )


def is_person_title(string):
    """Determines if the given string is a title or position"""
    return bool(set(string.split(" ")) & KNOWN_TITLES) and not is_party_indicator(
        string
    )


def clean_person_title_errata(string):
    corrected = string
    while corrected in TITLE_ERRATA:
        corrected = TITLE_ERRATA[corrected]
    return corrected


def clean_person_title(string):
    clean_title = remove_strings(string, "-", "'", ".", ":", "his ", "^", "•")

    try:
        for_county_index = clean_title.index(" of ")
        clean_title = clean_title[:for_county_index]
    except:
        pass

    clean_title = clean_person_title_errata(clean_title)

    return clean_title.strip()


def fix_jr_suffixes(name_strings):
    """Fixes 'jr.' suffixes by combining them with the previous name"""
    prev = None
    for name_string in name_strings:
        current = name_string
        if current == "jr." and prev is not None:
            current = prev + " jr."

        yield current
        prev = name_string


def parse_attorney_names(case_attorneys_items):
    """Extracts attorney names from a list of case_attorney_items"""
    clean_parts = [split_clean(item) for item in case_attorneys_items]

    name_strings = flatten(clean_parts)

    name_strings = fix_jr_suffixes(name_strings)

    return [string for string in name_strings if is_person_name(string)]


def party_from_parts(parts):
    for part in parts:
        if is_party_indicator(part):
            return part
    return None


def parse_attorneys_from_item(case_attorney_item):
    clean_parts = split_clean(case_attorney_item)

    clean_parts = list(fix_jr_suffixes(clean_parts))

    attorney = {}
    party = party_from_parts(clean_parts)
    if party is not None:
        party = party.replace("for ", "").replace(".", "").strip()
        attorney["party"] = party

    name_index = None
    for i, part in enumerate(clean_parts):
        if is_person_title(part):
            attorney["title"] = clean_person_title(part)
            attorney["party_type"] = "government" if part in GOVT_PARTIES else "private"

        if is_person_name(part):
            if name_index is not None:
                attorney["names"] = clean_parts[name_index]
                yield attorney

                attorney = {}
                attorney["names"] = part
                if party:
                    attorney["party"] = party

            name_index = i

        if i == (len(clean_parts) - 1) and "names" in attorney:
            print(attorney)
            yield attorney


def parse_attorneys(case_attorney_items):
    """Parse attorney information from an array of case attorney items"""
    for item in case_attorney_items:
        for attorney in parse_attorneys_from_item(item):
            yield attorney
