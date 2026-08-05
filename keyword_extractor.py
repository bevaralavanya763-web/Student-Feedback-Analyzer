import re
from collections import Counter

# ======================================================
# STOP WORDS
# ======================================================

STOP_WORDS = {
    "the", "is", "was", "were", "are", "am", "a", "an",
    "and", "or", "of", "to", "for", "in", "on", "at",
    "with", "this", "that", "it", "its", "be", "been",
    "very", "really", "quite", "as", "by", "from",
    "our", "your", "their", "his", "her", "my", "we",
    "they", "he", "she", "i", "you", "them", "me",
    "have", "has", "had", "do", "does", "did",
    "will", "would", "should", "can", "could",
    "event", "workshop", "program", "session"
}


# ======================================================
# EXTRACT KEYWORDS
# ======================================================

def extract_keywords(text, top_n=5):
    """
    Extract important keywords from feedback.
    """

    if not text or text.strip() == "":
        return []

    # Lowercase
    text = text.lower()

    # Remove numbers and punctuation
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Split into words
    words = text.split()

    # Remove stop words
    words = [
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 2
    ]

    if not words:
        return []

    # Count frequencies
    counts = Counter(words)

    keywords = []

    for word, _ in counts.most_common():
        if word not in keywords:
            keywords.append(word)

        if len(keywords) >= top_n:
            break

    return keywords


# ======================================================
# LIST TO STRING
# ======================================================

def keywords_to_string(keywords):
    """
    Convert keyword list to comma-separated string.
    """

    if not keywords:
        return ""

    return ", ".join(keywords)


# ======================================================
# STRING TO LIST
# ======================================================

def string_to_keywords(keyword_string):
    """
    Convert comma-separated keywords into list.
    """

    if not keyword_string:
        return []

    return [
        word.strip()
        for word in keyword_string.split(",")
        if word.strip()
    ]