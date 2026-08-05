from textblob import TextBlob


# ======================================================
# SENTIMENT ANALYSIS
# ======================================================

def analyze_sentiment(feedback):
    """
    Analyze student feedback using TextBlob.

    Returns:
        sentiment, polarity
    """

    try:

        if not feedback or feedback.strip() == "":
            return "Neutral", 0.0

        polarity = TextBlob(feedback).sentiment.polarity

        if polarity > 0.15:
            sentiment = "Positive"

        elif polarity < -0.15:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        return sentiment, round(polarity, 3)

    except Exception:

        return "Neutral", 0.0


# ======================================================
# CONFIDENCE SCORE
# ======================================================

def get_confidence(polarity):
    """
    Converts polarity score into confidence percentage.
    """

    confidence = min(abs(polarity) * 100, 100)

    return round(confidence, 2)


# ======================================================
# COMPLETE SENTIMENT RESULT
# ======================================================

def sentiment_result(feedback):
    """
    Returns sentiment analysis result as dictionary.
    """

    sentiment, polarity = analyze_sentiment(feedback)

    return {

        "sentiment": sentiment,

        "polarity": polarity,

        "confidence": get_confidence(polarity)

    }