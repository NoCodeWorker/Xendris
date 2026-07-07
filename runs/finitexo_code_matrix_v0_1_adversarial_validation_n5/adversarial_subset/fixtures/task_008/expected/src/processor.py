from src.solver import get_statistics

def process(data):
    info = get_statistics(data)
    info["range"] = info["max"] - info["min"]
    return info
