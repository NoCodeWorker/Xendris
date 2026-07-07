def get_statistics(data):
    mean = sum(data) / len(data)
    minimum = min(data)
    maximum = max(data)
    return {"mean": mean, "min": minimum, "max": maximum}
