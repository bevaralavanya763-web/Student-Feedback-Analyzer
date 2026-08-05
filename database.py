import sqlite3
import pandas as pd

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_NAME = "feedback.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():
    """
    Create and return SQLite database connection.
    """

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# CREATE FEEDBACK TABLE
# ==========================================================

def create_feedback_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS feedback(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        roll_number TEXT NOT NULL,

        student_name TEXT NOT NULL,

        department TEXT,

        program TEXT,

        year TEXT,

        section TEXT,

        event_name TEXT,

        event_type TEXT,

        faculty_name TEXT,

        rating INTEGER,

        feedback TEXT NOT NULL,

        sentiment TEXT,

        keywords TEXT,

        recommendation TEXT,

        date TEXT,

        time TEXT

    )

    """)

    conn.commit()
    conn.close()


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():
    """
    Creates required tables.
    """

    create_feedback_table()


# ==========================================================
# INSERT FEEDBACK
# ==========================================================

def insert_feedback(

    roll_number,
    student_name,
    department,
    program,
    year,
    section,
    event_name,
    event_type,
    faculty_name,
    rating,
    feedback,
    sentiment,
    keywords,
    recommendation,
    date,
    time

):

    conn = get_connection()
    cursor = conn.cursor()

    if isinstance(keywords, list):
        keywords = ", ".join(keywords)

    elif keywords is None:
        keywords = ""

    cursor.execute("""

    INSERT INTO feedback(

        roll_number,
        student_name,
        department,
        program,
        year,
        section,
        event_name,
        event_type,
        faculty_name,
        rating,
        feedback,
        sentiment,
        keywords,
        recommendation,
        date,
        time

    )

    VALUES(

        ?,?,?,?,?,?,
        ?,?,?,?,
        ?,?,?,?,
        ?,?

    )

    """,

    (

        roll_number,
        student_name,
        department,
        program,
        year,
        section,
        event_name,
        event_type,
        faculty_name,
        rating,
        feedback,
        sentiment,
        keywords,
        recommendation,
        date,
        time

    )

    )

    conn.commit()
    conn.close()


# ==========================================================
# GET COMPLETE FEEDBACK DATAFRAME
# ==========================================================

def get_feedback_dataframe():

    conn = get_connection()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM feedback

        ORDER BY id DESC

        """,

        conn

    )

    conn.close()

    return df


# ==========================================================
# GET ALL FEEDBACK
# ==========================================================

def get_all_feedback():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM feedback

    ORDER BY id DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# GET FEEDBACK BY ROLL NUMBER
# ==========================================================

def get_feedback_by_roll_number(

    roll_number

):

    conn = get_connection()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM feedback

        WHERE roll_number=?

        ORDER BY id DESC

        """,

        conn,

        params=(roll_number,)

    )

    conn.close()

    return df

    # ==========================================================
# SEARCH FEEDBACK
# ==========================================================

def search_feedback(keyword):

    conn = get_connection()

    value = f"%{keyword}%"

    df = pd.read_sql_query(

        """

        SELECT *

        FROM feedback

        WHERE

            roll_number LIKE ?

            OR student_name LIKE ?

            OR department LIKE ?

            OR event_name LIKE ?

            OR faculty_name LIKE ?

            OR feedback LIKE ?

            OR sentiment LIKE ?

        ORDER BY id DESC

        """,

        conn,

        params=(

            value,
            value,
            value,
            value,
            value,
            value,
            value

        )

    )

    conn.close()

    return df


# ==========================================================
# FILTER BY DEPARTMENT
# ==========================================================

def get_department_feedback(department):

    conn = get_connection()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM feedback

        WHERE department=?

        ORDER BY id DESC

        """,

        conn,

        params=(department,)

    )

    conn.close()

    return df


# ==========================================================
# FILTER BY SENTIMENT
# ==========================================================

def get_sentiment_feedback(sentiment):

    conn = get_connection()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM feedback

        WHERE sentiment=?

        ORDER BY id DESC

        """,

        conn,

        params=(sentiment,)

    )

    conn.close()

    return df


# ==========================================================
# FILTER BY EVENT
# ==========================================================

def get_event_feedback(event_name):

    conn = get_connection()

    df = pd.read_sql_query(

        """

        SELECT *

        FROM feedback

        WHERE event_name=?

        ORDER BY id DESC

        """,

        conn,

        params=(event_name,)

    )

    conn.close()

    return df


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def get_dashboard_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM feedback WHERE sentiment='Positive'"
    )
    positive = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM feedback WHERE sentiment='Neutral'"
    )
    neutral = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM feedback WHERE sentiment='Negative'"
    )
    negative = cursor.fetchone()[0]

    cursor.execute(
        "SELECT ROUND(AVG(rating),2) FROM feedback"
    )

    average_rating = cursor.fetchone()[0]

    conn.close()

    if average_rating is None:
        average_rating = 0

    return {

        "total": total,

        "positive": positive,

        "neutral": neutral,

        "negative": negative,

        "average_rating": average_rating

    }


# ==========================================================
# TOTAL FEEDBACK
# ==========================================================

def get_total_feedback():

    return get_dashboard_summary()["total"]


# ==========================================================
# POSITIVE FEEDBACK
# ==========================================================

def get_positive_feedback():

    return get_dashboard_summary()["positive"]


# ==========================================================
# NEUTRAL FEEDBACK
# ==========================================================

def get_neutral_feedback():

    return get_dashboard_summary()["neutral"]


# ==========================================================
# NEGATIVE FEEDBACK
# ==========================================================

def get_negative_feedback():

    return get_dashboard_summary()["negative"]


# ==========================================================
# AVERAGE RATING
# ==========================================================

def get_average_rating():

    return get_dashboard_summary()["average_rating"]


# ==========================================================
# SENTIMENT STATISTICS
# ==========================================================

def get_sentiment_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            sentiment,

            COUNT(*) AS total

        FROM feedback

        GROUP BY sentiment

        ORDER BY total DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# DEPARTMENT STATISTICS
# ==========================================================

def get_department_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            department,

            COUNT(*) AS total

        FROM feedback

        GROUP BY department

        ORDER BY total DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# RATING DISTRIBUTION
# ==========================================================

def get_rating_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            rating,

            COUNT(*) AS total

        FROM feedback

        GROUP BY rating

        ORDER BY rating

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# FEEDBACK TREND
# ==========================================================

def get_feedback_trend():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            date,

            COUNT(*) AS total

        FROM feedback

        GROUP BY date

        ORDER BY date

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================================
# ALL KEYWORDS
# ==========================================================

def get_all_keywords():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT keywords

        FROM feedback

        WHERE keywords IS NOT NULL
        AND keywords!=''

    """)

    rows = cursor.fetchall()


    return [row["keywords"] for row in rows]

    # ==========================================================
# UPDATE FEEDBACK
# ==========================================================

def update_feedback(
    feedback_id,
    rating,
    feedback,
    sentiment,
    keywords,
    recommendation
):

    conn = get_connection()
    cursor = conn.cursor()

    if isinstance(keywords, list):
        keywords = ", ".join(keywords)
    elif keywords is None:
        keywords = ""
    else:
        keywords = str(keywords)

    cursor.execute("""

        UPDATE feedback

        SET

            rating=?,
            feedback=?,
            sentiment=?,
            keywords=?,
            recommendation=?

        WHERE id=?

    """,

    (

        rating,
        feedback,
        sentiment,
        keywords,
        recommendation,
        feedback_id

    )

    )

    conn.commit()
    conn.close()


# ==========================================================
# DELETE FEEDBACK
# ==========================================================

def delete_feedback(feedback_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM feedback WHERE id=?",

        (feedback_id,)

    )

    conn.commit()
    conn.close()


# ==========================================================
# EXPORT CSV
# ==========================================================

def export_feedback_csv(file_path):

    df = get_feedback_dataframe()

    df.to_csv(

        file_path,

        index=False,

        encoding="utf-8"

    )


# ==========================================================
# EXPORT EXCEL
# ==========================================================

def export_feedback_excel(file_path):

    df = get_feedback_dataframe()

    df.to_excel(

        file_path,

        index=False

    )


# ==========================================================
# DATABASE BACKUP
# ==========================================================

def backup_database(destination):

    import shutil

    shutil.copy(

        DATABASE_NAME,

        destination

    )


# ==========================================================
# CLEAR ALL FEEDBACK
# ==========================================================

def clear_feedback():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM feedback"

    )

    conn.commit()
    conn.close()


# ==========================================================
# CHECK IF DATABASE HAS RECORDS
# ==========================================================

def feedback_exists():

    return get_total_feedback() > 0


# ==========================================================
# DATABASE STATUS
# ==========================================================

def database_status():

    try:

        conn = get_connection()

        conn.execute("SELECT 1")

        conn.close()

        return True

    except Exception:

        return False


# ==========================================================
# INITIALIZE DATABASE AUTOMATICALLY
# ==========================================================

initialize_database()


# ==========================================================
# TEST DATABASE
# ==========================================================

if __name__ == "__main__":

    print("Initializing database...")

    initialize_database()

    print("Database created successfully.")

    print("Database Status :", database_status())

    print("Total Feedback :", get_total_feedback())

# ==========================================================
# GET FEEDBACK DATAFRAME
# ==========================================================

def get_feedback_dataframe():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM feedback
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df