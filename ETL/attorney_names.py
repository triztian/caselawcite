
from string_processing import *

known_titles = {
    'attorney',
    'solicitor',
    'assistant',
    'general',
    'public',
    'guardian'
}

known_case_parts = {
    'appellant',
    'appellee', 
    'plaintiff',
    'defendant',
	'claimant',
}

non_name_words = {
    'llc',
    'ltd.',
    'inc.',
    'argued',
    'all of',
    'p.c.',
    '&',
	'coun',
	'corporation',
	'counsel'
}

def is_title(string):
    """Determines if the string is a position title."""
    return bool(set(string.split(' ')) & known_titles)


def is_place_of_origin(string):
    """Determines if the string is a location or non-person."""
    return string.startswith('of ') or string.startswith('both ')


def is_party_indicator(string):
    """Determines if the string indicates the party to which the attorney 
    belongs to.
    """
    return string.startswith('for ')


def is_other_string(string):
    """Indicates that the string represents some other entity or meaning."""
    return bool(set(string.split(' ')) & non_name_words)


def is_person_name(string):
    """Determines if the string is a person name or not."""
    return all([
        not is_title(string), 
        not is_other_string(string), 
        not is_place_of_origin(string),
        not is_party_indicator(string)
    ])


def fix_jr_suffixes(name_strings):
    """Fixes 'jr.' suffixes by combining them with the previous name"""
    prev = None
    for name_string in name_strings:
        current = name_string
        if current == "jr.":
            current = prev + ' jr.'

        yield current 
        prev = name_string


def parse_attorney_names(case_attorneys_items):
    clean_parts = [split_clean(item) for item in case_attorneys_items]

    name_strings = flatten(clean_parts)

    name_strings = fix_jr_suffixes(name_strings)

    return [string for string in name_strings if is_person_name(string)]