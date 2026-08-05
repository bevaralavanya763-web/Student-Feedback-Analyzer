# ============================================================
# AI Recommendation Generator
# ============================================================

def generate_recommendation(sentiment, rating):
    """
    Generate recommendations based on
    sentiment and rating.
    """

    sentiment = sentiment.lower()

    # -------------------------
    # Positive
    # -------------------------
    if sentiment == "positive":

        if rating >= 4:
            return (
                "Students were highly satisfied. "
                "Continue organizing similar events and maintain the same quality."
            )

        return (
            "Overall feedback is positive. "
            "Improve a few areas to achieve excellent satisfaction."
        )

    # -------------------------
    # Neutral
    # -------------------------
    elif sentiment == "neutral":

        return (
            "Feedback is neutral. "
            "Collect additional suggestions from students and improve event engagement."
        )

    # -------------------------
    # Negative
    # -------------------------
    elif sentiment == "negative":

        if rating <= 2:
            return (
                "Students were dissatisfied. "
                "Review event planning, improve content delivery, "
                "increase interaction, and address student concerns."
            )

        return (
            "Some improvements are required. "
            "Analyze student feedback carefully and enhance future events."
        )

    # -------------------------
    # Default
    # -------------------------
    return (
        "Collect more feedback to generate meaningful recommendations."
    )


# ============================================================
# Recommendation Level
# ============================================================

def recommendation_level(sentiment):

    sentiment = sentiment.lower()

    if sentiment == "positive":
        return "Excellent"

    elif sentiment == "neutral":
        return "Average"

    elif sentiment == "negative":
        return "Needs Improvement"

    return "Unknown"