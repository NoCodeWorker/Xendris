from src import formatter

def process_scores(students):
    """students is a list of (name, score) tuples.
    Returns a newline-separated string of formatted scores.
    """
    lines = []
    for student in students:
        lines.append(formatter.format_score(student))
    return "\n".join(lines)
