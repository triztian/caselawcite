from string_processing import *


KNOWN_TITLES = {"attorney", "solicitor", "assistant", "general", "public", "guardian"}

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
            not is_title(string),
            not is_other_string(string),
            not is_place_of_origin(string),
            not is_party_indicator(string),
        ]
    )


def fix_jr_suffixes(name_strings):
    """Fixes 'jr.' suffixes by combining them with the previous name"""
    prev = None
    for name_string in name_strings:
        current = name_string
        if current == "jr.":
            current = prev + " jr."

        yield current
        prev = name_string


def parse_attorney_names(case_attorneys_items):
    """Extracts attorney names from a list of case_attorney_items"""
    clean_parts = [split_clean(item) for item in case_attorneys_items]

    name_strings = flatten(clean_parts)

    name_strings = fix_jr_suffixes(name_strings)

    return [string for string in name_strings if is_person_name(string)]
