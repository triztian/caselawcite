def flatten(l):
    """Flattens an array of arrays

    - Note: This function holds the full list in-memory
    """
    result = []
    for sublist in l:
        for item in sublist:
            result.append(item)
    return result


def remove_strings(src, *strings):
    """Removes (replaces) each of the strings with an empty string"""
    for s in strings:
        src = src.replace(s, "")
    return src


def clean_chars(input):
    """Remove 'special' non name characters"""
    return (
        remove_strings(input, "(", ")", "_", "-", "and ", "^", ">", "<")
        .replace("..", ".")
        .strip()
    )


def split_clean(input_item):
    """Splits each raw attorney item and cleans odd characters like parens, 
    ampersands, commas, etc and returns a single array with string names.
    """
    parts = input_item.split(",")
    parts = flatten([p.split("(") for p in parts])
    parts = flatten([p.split(")") for p in parts])
    parts = flatten([p.split(";") for p in parts])

    parts = [p.lower() for p in parts]
    parts = [clean_chars(p) for p in parts]
    parts = [p for p in parts if bool(p)]
    return parts
