from string_processing import *

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

PARTY_ERRATA = {
    "bespondent": "despondent",
    "the peoplé": "the people",
    "the people i": "the people",
    "the peoole": "the people",
    "the opeople": "the people",
    "fhe people": "the people",
    "the eeople": "the people",
    "the peo pie": "the people",
    "the peoole": "the people",
    "the feople": "the people",
    "t ie people": "the people",
    "eespondent": "despondent",
    "ap pellees": "appellees",
    "ap pellee": "appellee",
    "ap pellants": "appellants",
    "appehees": "appellees",
    "intervenorappellee": "intervenor appellee",
    "plaintiffappellant": "plaintiff appellant",
    "plaintiffappellantcrossappellee": "plaintiff appellant cross appellee",
    "plaintiffappellee": "plaintiff appellee",
    "plaintiffinerror": "plaintiff in error",
    "people": "the people",
    "claimantappellant": "claimant appellant",
    "appellées": "appellees",
    "appellánt": "appellees",
    "appelles": "appellees",
}


def clean_special_chars(string):
    return remove_strings(
        string, "for ", "■", "•", '"', "^", ":", "*", "%", "„", "!", "|",
    )


def clean_person_name(name):
    return clean_special_chars(name).replace("’", "'")


def clean_person_title(string):
    clean_title = remove_strings(string, "-", "'", ".", ":", "his ", "^", "•")

    try:
        for_county_index = clean_title.index(" of ")
        clean_title = clean_title[:for_county_index]
    except:
        pass

    clean_title = clean_person_title_errata(clean_title)

    return clean_title.strip()


def correct_errata(string, erratas):
    corrected = string
    while corrected in erratas:
        corrected = erratas[corrected]
    return corrected


def clean_person_title_errata(string):
    return correct_errata(string, TITLE_ERRATA)


def clean_party_errata(string):
    return correct_errata(string, PARTY_ERRATA)


def clean_party(string):
    return clean_party_errata(
        clean_special_chars(string)
        .replace("  ", " ")
        .replace("’", "'")
        .replace('"', "'")
        .strip()
    )
