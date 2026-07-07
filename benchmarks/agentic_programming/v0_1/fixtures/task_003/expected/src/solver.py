def parse_entry(line):
    if ": " not in line:
        return None
    key, value_str = line.split(": ", 1)
    if not key or not value_str:
        return None
    try:
        if "." in value_str:
            value = float(value_str)
        else:
            value = int(value_str)
    except ValueError:
        value = value_str
    return (key, value)
