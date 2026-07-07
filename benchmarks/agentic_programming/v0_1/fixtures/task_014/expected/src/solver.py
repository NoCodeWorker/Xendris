def merge_configs(base, override, merge_strategy="deep"):
    """Merge override into base config.

    If merge_strategy is 'shallow', performs a shallow merge.
    If merge_strategy is 'deep', recursively merges nested dicts.
    """
    if merge_strategy == "shallow":
        return {**base, **override}
    result = {}
    for key in base:
        if key in override:
            if isinstance(base[key], dict) and isinstance(override[key], dict):
                result[key] = merge_configs(base[key], override[key], merge_strategy="deep")
            else:
                result[key] = override[key]
        else:
            result[key] = base[key]
    for key in override:
        if key not in base:
            result[key] = override[key]
    return result
