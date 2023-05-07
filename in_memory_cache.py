_cache = {}


def remove_key(key) -> bool:
    try:
        _cache.pop(key)
        return True
    except KeyError:
        return False


def add_item(key, data):
    _cache[key] = data
