def safe_average(values):
    """Return the arithmetic mean of values, skipping None entries.
    Returns 0.0 for empty lists.
    """
    filtered = [v for v in values if v is not None]
    if not filtered:
        return 0.0
    return sum(filtered) / len(filtered)
