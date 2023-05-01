my_id = 228642352


def remove_key_safe(dictionary: dict, key) -> bool:
    try:
        dictionary.pop(key)
        return True
    except KeyError:
        return False
