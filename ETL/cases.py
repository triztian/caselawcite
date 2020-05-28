from string_processing import *


def parse_docket_number(string):
    pass


def parse_page(string):
    """Parses the page number from the string"""
    string = string.lower()
    try:
        string = string[: string.index("-")]
    except:
        pass

    return (
        int(remove_strings(string, "r", "b", "p", "d", "a", "c", "t").strip())
        if string != "?"
        else -1
    )


def sanitize_case(case_obj):
    return {
        "id": case_obj["id"],
        "jurisdiction": case_obj["jurisdiction"],
        "court": case_obj["court"],
        "volume": case_obj["volume"],
        "first_page": parse_page(case_obj["first_page"]),
        "last_page": parse_page(case_obj["last_page"]),
        "decision_date": case_obj["decision_date"],
        "url": case_obj["url"],
    }
