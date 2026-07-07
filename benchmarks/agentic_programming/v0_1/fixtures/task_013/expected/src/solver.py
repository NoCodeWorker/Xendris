def word_frequency(text):
    """Return a dict mapping words to their occurrence count.

    Words are case-sensitive and separated by whitespace.
    """
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
