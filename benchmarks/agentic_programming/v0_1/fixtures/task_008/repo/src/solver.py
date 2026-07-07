def get_info(data):
    mean = sum(data) / len(data)
    minimum = min(data)
    maximum = max(data)
    return {"mean": mean, "min": minimum, "max": maximum}
