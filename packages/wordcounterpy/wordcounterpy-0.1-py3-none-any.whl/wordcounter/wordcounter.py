def count_words(text):
    return len(text.split())

def word_frequencies(text):
    words = text.lower().split()
    freq = {}
    for word in words:
        word = word.strip('.,!?;:"\'')
        freq[word] = freq.get(word, 0) + 1
    return freq

def most_common_word(text):
    freqs = word_frequencies(text)
    if not freqs:
        return None
    return max(freqs, key=freqs.get)
