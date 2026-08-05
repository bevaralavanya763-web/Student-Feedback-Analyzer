from datetime import datetime


# ==========================================================
# CURRENT DATE
# ==========================================================

def get_current_date():
    """
    Returns today's date in DD-MM-YYYY format.
    """
    return datetime.now().strftime("%d-%m-%Y")


# ==========================================================
# CURRENT TIME
# ==========================================================

def get_current_time():
    """
    Returns current time in HH:MM:SS format.
    """
    return datetime.now().strftime("%H:%M:%S")


# ==========================================================
# CURRENT DATE & TIME
# ==========================================================

def get_current_datetime():
    """
    Returns current datetime object.
    """
    return datetime.now()


# ==========================================================
# VALIDATE ROLL NUMBER
# ==========================================================

def validate_roll_number(roll_number):

    if not roll_number:
        return False

    roll_number = str(roll_number).strip()

    return len(roll_number) >= 5


# ==========================================================
# VALIDATE STUDENT NAME
# ==========================================================

def validate_name(name):

    if not name:
        return False

    name = str(name).strip()

    return len(name) >= 3


# ==========================================================
# VALIDATE FEEDBACK
# ==========================================================

def validate_feedback(feedback):

    if not feedback:
        return False

    feedback = str(feedback).strip()

    return len(feedback) >= 10


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:
        return ""

    return " ".join(str(text).split())


# ==========================================================
# RATING EMOJI
# ==========================================================

def rating_emoji(rating):

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return "Not Rated"

    if rating == 5:
        return "⭐⭐⭐⭐⭐ Excellent"

    elif rating == 4:
        return "⭐⭐⭐⭐ Very Good"

    elif rating == 3:
        return "⭐⭐⭐ Good"

    elif rating == 2:
        return "⭐⭐ Fair"

    elif rating == 1:
        return "⭐ Poor"

    return "Not Rated"