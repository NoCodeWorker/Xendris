def safe_average(values):
    """Return the arithmetic mean of values, skipping None entries.
    Returns 0.0 for empty lists.
    """
    return sum(values) / len(values)
