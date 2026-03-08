BAD_WORDS = ["insulte1", "insulte2"]

def filter_content(text):
    for word in BAD_WORDS:
        if word in text.lower():
            return False
    return True
