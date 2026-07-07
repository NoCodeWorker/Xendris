def compute_statistics(numbers):
    mean = sum(numbers) / len(numbers)
    return {"mean": mean, "count": len(numbers)}
