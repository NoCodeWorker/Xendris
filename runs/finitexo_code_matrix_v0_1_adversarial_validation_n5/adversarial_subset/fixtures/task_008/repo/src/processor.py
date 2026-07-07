from src.solver import get_info

def process(data):
    info = get_info(data)
    info["range"] = info["max"] - info["min"]
    return info
