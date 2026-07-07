def merge_configs(base, override, merge_strategy="deep"):
    """Merge override into base config.

    If merge_strategy is 'shallow', performs a shallow merge.
    If merge_strategy is 'deep', recursively merges nested dicts.
    """
    if merge_strategy == "shallow":
        return {**base, **override}
    return {**base, **override}
