from string_processing import *
from text_errata import *


KNOWN_TITLES = {
    "attorney",
    "solicitor",
    "assistant",
    "general",
    "public",
    "guardian",
    "attorneys.",
    "attorneys for appellant.",
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

GOVT_TITLES = {
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
            return clean_party(part)
    return None


def party_type(party, title):
    return "government" if (party in GOVT_TITLES or title in GOVT_TITLES) else "private"


def parse_attorneys_from_item(case_attorney_item):
    clean_parts = split_clean(case_attorney_item)

    clean_parts = list(fix_jr_suffixes(clean_parts))

    attorney = {}
    party = party_from_parts(clean_parts)
    if party is not None:
        attorney["party"] = party

    name_index = None
    for i, part in enumerate(clean_parts):
        if is_person_title(part):
            title = clean_person_title(part)
            attorney["title"] = title
            attorney["party_type"] = party_type(part, title)

        if is_person_name(part):
            if name_index is not None:
                attorney["names"] = clean_person_name(clean_parts[name_index])
                yield attorney

                attorney = {}
                attorney["names"] = clean_person_name(part)
                if party:
                    attorney["party"] = party

            name_index = i

        if i == (len(clean_parts) - 1) and "names" in attorney:
            yield attorney


def parse_attorneys(case_attorney_items):
    """Parse attorney information from an array of case attorney items"""
    for item in case_attorney_items:
        for attorney in parse_attorneys_from_item(item):
            yield attorney
