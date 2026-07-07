def safe_divide(items, divisor):
    if items is None or divisor == 0:
        return []
    result = []
    for item in items:
        try:
            result.append(item / divisor)
        except (TypeError, ValueError):
            continue
    return result
