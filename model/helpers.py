def found(text, keys, mode='all', substring=False):
    """
    Searches key elements in given text string(s) with three different modes: all, any, none

    Args:
        text: (list or str)
        keys: (list) keys to search in texts
        mode: (str) ['all', 'any', 'none']
        substring: (bool) search in substrings in given text string(s) or fully match

    Returns:
        result: (bool)

    """
    assert mode in ['all', 'any', 'none']
    if isinstance(text, str):
        text = [text]

    count = 0
    for key in keys:
        for item in text:
            if not substring and key.lower() == item.lower() or substring and key.lower() in item.lower():
                count += 1
                break

    if mode == 'all':
        return len(keys) == count
    elif mode == 'any':
        return count > 0
    else:
        return count == 0
