import ijson


def load_attorney_names_text(file):
    """Loads the `.casebody.data.attorneys` section for each case
    and produces a smaller object with some metadata
    """
    objects = ijson.items(file, "item")
    for obj in objects:
        sobj = {"id": obj["id"]}

        try:
            sobj["attorneys"] = obj["casebody"]["data"]["attorneys"]
        except:
            pass

        yield sobj


def load_cases(file):
    """Loads the case data and produces a simplified object containing"""
    objects = ijson.items(file, "item")
    for obj in objects:
        yield {
            "id": obj["id"],
            "first_page": obj["first_page"],
            "last_page": obj["last_page"],
            "decision_date": obj["decision_date"],
            "docket_number": obj["docket_number"],
            "court": obj["court"]["slug"],
            "volume": int(obj["volume"]["volume_number"]),
            "jurisdiction": obj["jurisdiction"]["slug"],
            "url": obj["url"],
        }
