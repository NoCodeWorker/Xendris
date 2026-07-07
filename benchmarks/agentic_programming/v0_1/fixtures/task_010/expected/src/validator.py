from src.reporter import format_summary

def check_data(numbers):
    if not numbers:
        return "empty"
    result = format_summary(numbers)
    if any(n < 0 for n in numbers):
        return f"warning: {result}"
    return f"ok: {result}"
