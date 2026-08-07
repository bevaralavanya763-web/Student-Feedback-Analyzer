import streamlit as st
import pandas as pd
import plotly.express as px


import streamlit as st


def is_logged_in():

    return st.session_state.get(
        "faculty_logged_in",
        False
    )

from database import get_feedback_dataframe



# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Feedback Analytics",
    page_icon="📊",
    layout="wide"
)



# ==========================================================
# FACULTY ACCESS CONTROL
# ==========================================================

if not is_logged_in():

    st.warning(
        "🔒 Faculty login required."
    )

    st.stop()



# ==========================================================
# HEADER
# ==========================================================


st.title(
    "📊 Feedback Analytics"
)


st.caption(
    "Advanced analysis of student feedback using AI insights."
)


st.divider()



# ==========================================================
# LOAD DATA
# ==========================================================


df = get_feedback_dataframe()



if df is None or df.empty:


    st.warning(
        "No feedback data available."
    )


    st.stop()



# ==========================================================
# BASIC METRICS
# ==========================================================


total = len(df)



positive = len(
    df[
        df["sentiment"]
        ==
        "Positive"
    ]
)



negative = len(
    df[
        df["sentiment"]
        ==
        "Negative"
    ]
)



neutral = len(
    df[
        df["sentiment"]
        ==
        "Neutral"
    ]
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(
    "📝 Total Feedback",
    total
)


c2.metric(
    "😊 Positive",
    positive
)


c3.metric(
    "😐 Neutral",
    neutral
)


c4.metric(
    "☹️ Negative",
    negative
)



st.divider()



# ==========================================================
# SENTIMENT ANALYSIS
# ==========================================================


st.subheader(
    "📌 Sentiment Distribution"
)



sentiment_df = (

    df["sentiment"]

    .value_counts()

    .reset_index()

)



sentiment_df.columns = [

    "Sentiment",

    "Count"

]



fig = px.pie(

    sentiment_df,

    names="Sentiment",

    values="Count",

    hole=0.45,

    title="Student Feedback Sentiment"

)



fig.update_traces(

    textinfo="percent+label"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



st.divider()



# ==========================================================
# DEPARTMENT ANALYSIS
# ==========================================================


st.subheader(
    "🏢 Department-wise Feedback"
)



dept_df = (

    df["department"]

    .value_counts()

    .reset_index()

)



dept_df.columns = [

    "Department",

    "Count"

]



fig2 = px.bar(

    dept_df,

    x="Department",

    y="Count",

    text="Count",

    title="Department Feedback Analysis"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)



st.divider()



# ==========================================================
# PROGRAM ANALYSIS
# ==========================================================


if "program" in df.columns:


    st.subheader(
        "🎓 Program-wise Feedback"
    )


    program_df = (

        df["program"]

        .value_counts()

        .reset_index()

    )


    program_df.columns = [

        "Program",

        "Count"

    ]



    fig3 = px.bar(

        program_df,

        x="Program",

        y="Count",

        text="Count",

        title="Program Analysis"

    )


    st.plotly_chart(

        fig3,

        use_container_width=True

    )





# ==========================================================
# YEAR-WISE ANALYSIS
# ==========================================================


st.subheader(
    "📅 Year-wise Feedback"
)



year_df = (

    df["year"]

    .value_counts()

    .reset_index()

)



year_df.columns = [

    "Year",

    "Count"

]



fig4 = px.bar(

    year_df,

    x="Year",

    y="Count",

    text="Count",

    title="Year-wise Feedback Distribution"

)



st.plotly_chart(

    fig4,

    use_container_width=True

)



st.divider()



# ==========================================================
# KEYWORD ANALYSIS
# ==========================================================


st.subheader(
    "🔑 Most Used Keywords"
)



keywords = []



if "keywords" in df.columns:


    for item in df["keywords"]:


        if isinstance(item, str):


            words = item.split(",")


            for word in words:


                word = word.strip()


                if word:

                    keywords.append(word)



if keywords:


    keyword_df = (

        pd.Series(keywords)

        .value_counts()

        .head(10)

        .reset_index()

    )


    keyword_df.columns = [

        "Keyword",

        "Count"

    ]



    fig5 = px.bar(

        keyword_df,

        x="Keyword",

        y="Count",

        text="Count",

        title="Top Feedback Keywords"

    )



    st.plotly_chart(

        fig5,

        use_container_width=True

    )



else:


    st.info(
        "No keywords available."
    )



st.divider()



# ==========================================================
# WORD CLOUD
# ==========================================================


st.subheader(
    "☁️ Keyword Word Cloud"
)



try:


    from wordcloud import WordCloud

    import matplotlib.pyplot as plt



    if keywords:


        text = " ".join(keywords)



        wordcloud = WordCloud(

            width=800,

            height=400,

            background_color="white"

        ).generate(text)



        fig, ax = plt.subplots()


        ax.imshow(
            wordcloud
        )


        ax.axis(
            "off"
        )


        st.pyplot(fig)



    else:


        st.info(
            "Not enough keyword data."
        )


except Exception:


    st.info(
        "Word cloud module unavailable."
    )



st.divider()



# ==========================================================
# FEEDBACK TREND
# ==========================================================


st.subheader(
    "📈 Feedback Trend"
)



if "date" in df.columns:


    trend_df = (

        df["date"]

        .value_counts()

        .reset_index()

    )


    trend_df.columns = [

        "Date",

        "Count"

    ]


    trend_df = trend_df.sort_values(
        "Date"
    )



    fig6 = px.line(

        trend_df,

        x="Date",

        y="Count",

        markers=True,

        title="Feedback Submission Trend"

    )


    st.plotly_chart(

        fig6,

        use_container_width=True

    )


st.divider()



# ==========================================================
# DOWNLOAD ANALYTICS DATA
# ==========================================================


st.subheader(
    "⬇️ Download Analytics Report"
)



csv = df.to_csv(
    index=False
)



st.download_button(

    label="Download CSV",

    data=csv,

    file_name="feedback_analysis_report.csv",

    mime="text/csv"

)



st.divider()



# ==========================================================
# COMPLETE RECORD VIEW
# ==========================================================


st.subheader(
    "📋 All Feedback Records"
)



st.dataframe(

    df,

    use_container_width=True,

    hide_index=True

)



st.divider()



# ==========================================================
# FOOTER
# ==========================================================


st.markdown(

"""
<div style="text-align:center;color:gray;">

<b>AI-Powered Student Feedback Analyzer</b><br>

Dhanekula Institute of Engineering & Technology<br>

Machine Learning Based Feedback System

</div>
""",

unsafe_allow_html=True

)