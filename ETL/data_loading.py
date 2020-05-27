import ijson

def load_attorney_names_text(file):
    """Loads the `.casebody.data.attorneys` section for each case
    and produces a smaller object with some metadata
    """
    objects = ijson.items(file, 'item')
    for obj in objects:
        sobj = {
            'id': obj['id'],
            'first_page': obj['first_page'],
        }

        try: 
            sobj['attorneys'] = obj['casebody']['data']['attorneys']
        except:
            pass

        yield sobj