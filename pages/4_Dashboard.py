import streamlit as st
import pandas as pd
import plotly.express as px


import streamlit as st


def is_logged_in():

    return st.session_state.get(
        "faculty_logged_in",
        False
    )

from database import (
    get_total_feedback,
    get_average_rating,
    get_department_stats,
    get_sentiment_stats,
    get_rating_stats,
    get_feedback_trend,
    get_feedback_dataframe
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Faculty Dashboard",
    page_icon="📊",
    layout="wide"
)



# ==========================================================
# FACULTY ACCESS CONTROL
# ==========================================================

if not is_logged_in():

    st.warning(
        "🔒 Faculty login required to access Dashboard."
    )

    st.info(
        "Please login from Faculty Portal."
    )

    st.stop()



# ==========================================================
# HEADER
# ==========================================================

st.title(
    "📊 Faculty Dashboard"
)


st.caption(
    "AI-powered student feedback analytics"
)


st.divider()



# ==========================================================
# FETCH DATA
# ==========================================================


total_feedback = get_total_feedback()


average_rating = get_average_rating()


sentiment_data = get_sentiment_stats()



positive = 0
neutral = 0
negative = 0



for sentiment, count in sentiment_data:


    if sentiment == "Positive":

        positive = count


    elif sentiment == "Neutral":

        neutral = count


    elif sentiment == "Negative":

        negative = count



# Percentage calculation

if total_feedback > 0:

    positive_percentage = round(
        (positive / total_feedback) * 100,
        2
    )


    neutral_percentage = round(
        (neutral / total_feedback) * 100,
        2
    )


    negative_percentage = round(
        (negative / total_feedback) * 100,
        2
    )

else:

    positive_percentage = 0

    neutral_percentage = 0

    negative_percentage = 0



# ==========================================================
# TOP CARDS
# ==========================================================


col1, col2, col3, col4, col5 = st.columns(5)



col1.metric(
    "📝 Total Feedback",
    total_feedback
)


col2.metric(
    "😊 Positive",
    f"{positive_percentage}%"
)


col3.metric(
    "😐 Neutral",
    f"{neutral_percentage}%"
)


col4.metric(
    "☹️ Negative",
    f"{negative_percentage}%"
)


col5.metric(
    "⭐ Average Rating",
    average_rating
)



st.divider()



# ==========================================================
# SENTIMENT PIE CHART
# ==========================================================


st.subheader(
    "📌 Sentiment Distribution"
)



if sentiment_data:


    sentiment_df = pd.DataFrame(
        sentiment_data,
        columns=[
            "Sentiment",
            "Count"
        ]
    )


    fig = px.pie(

        sentiment_df,

        names="Sentiment",

        values="Count",

        hole=0.45,

        title="Overall Feedback Sentiment"

    )


    fig.update_traces(

        textinfo="percent+label"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:


    st.info(
        "No feedback data available."
    )



st.divider()

# ==========================================================
# DEPARTMENT AND RATING ANALYSIS
# ==========================================================


col1, col2 = st.columns(2)



# ==========================================================
# DEPARTMENT WISE FEEDBACK
# ==========================================================


with col1:


    st.subheader(
        "🏢 Department-wise Feedback"
    )


    department_data = get_department_stats()



    if department_data:


        dept_df = pd.DataFrame(

            department_data,

            columns=[
                "Department",
                "Feedback Count"
            ]

        )


        fig = px.bar(

            dept_df,

            x="Department",

            y="Feedback Count",

            text="Feedback Count",

            title="Department Analysis"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:


        st.info(
            "No department data available."
        )





# ==========================================================
# RATING DISTRIBUTION
# ==========================================================


with col2:


    st.subheader(
        "⭐ Rating Distribution"
    )


    rating_data = get_rating_stats()



    if rating_data:


        rating_df = pd.DataFrame(

            rating_data,

            columns=[
                "Rating",
                "Count"
            ]

        )


        fig = px.bar(

            rating_df,

            x="Rating",

            y="Count",

            text="Count",

            title="Student Rating Analysis"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:


        st.info(
            "No rating data available."
        )



st.divider()



# ==========================================================
# FEEDBACK TREND
# ==========================================================


st.subheader(
    "📈 Feedback Submission Trend"
)



trend_data = get_feedback_trend()



if trend_data:


    trend_df = pd.DataFrame(

        trend_data,

        columns=[
            "Date",
            "Feedback Count"
        ]

    )


    fig = px.line(

        trend_df,

        x="Date",

        y="Feedback Count",

        markers=True,

        title="Daily Feedback Trend"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:


    st.info(
        "No trend data available."
    )



st.divider()



# ==========================================================
# RECENT FEEDBACK RECORDS
# ==========================================================


st.subheader(
    "📋 Recent Feedback"
)

feedback_df = get_feedback_dataframe()

if not feedback_df.empty:

    st.dataframe(
        feedback_df.tail(10),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No feedback records available.")



st.divider()



# ==========================================================
# SUMMARY
# ==========================================================


st.subheader(
    "📌 Dashboard Summary"
)



summary_col1, summary_col2 = st.columns(2)



with summary_col1:


    st.success(

        f"""
        Total Feedback: {total_feedback}

        Positive Feedback: {positive}

        Neutral Feedback: {neutral}

        Negative Feedback: {negative}
        """

    )



with summary_col2:


    department_count = len(
        get_department_stats()
    )


    st.info(

        f"""
        Average Rating: ⭐ {average_rating}

        Departments Covered: {department_count}

        AI Sentiment Analysis Enabled

        Database Connected
        """

    )



# ==========================================================
# FOOTER
# ==========================================================


st.divider()


st.markdown(

"""
<div style="text-align:center;color:gray;">

<b>AI-Powered Student Feedback Analyzer</b><br>

Dhanekula Institute of Engineering & Technology<br>

© 2026

</div>
""",

unsafe_allow_html=True

)