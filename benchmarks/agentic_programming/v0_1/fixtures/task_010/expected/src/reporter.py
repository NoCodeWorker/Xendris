from src.analyzer import compute_statistics

def format_summary(numbers):
    stats = compute_statistics(numbers)
    return f"avg={stats['mean']:.2f}, n={stats['count']}"
