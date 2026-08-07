import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


from database import (
    get_feedback_dataframe,
    get_average_rating
)

import streamlit as st


def is_logged_in():

    return st.session_state.get(
        "faculty_logged_in",
        False
    )



# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Feedback Reports",
    page_icon="📄",
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
# PDF CREATION FUNCTION
# ==========================================================


def create_pdf(data):

    buffer = BytesIO()


    pdf = SimpleDocTemplate(
        buffer
    )


    styles = getSampleStyleSheet()


    content = []



    content.append(

        Paragraph(

            "Student Feedback Analysis Report",

            styles["Title"]

        )

    )


    content.append(

        Spacer(
            1,
            20
        )

    )



    for _, row in data.iterrows():


        text = f"""

        Roll Number: {row.get('roll_number','')}<br/>

        Student Name: {row.get('student_name','')}<br/>

        Department: {row.get('department','')}<br/>

        Program: {row.get('program','')}<br/>

        Year: {row.get('year','')}<br/>

        Section: {row.get('section','')}<br/>

        Event Name: {row.get('event_name','')}<br/>

        Event Type: {row.get('event_type','')}<br/>

        Rating: {row.get('rating','')}/5<br/>

        Feedback: {row.get('feedback','')}<br/>

        Sentiment: {row.get('sentiment','')}<br/>

        Keywords: {row.get('keywords','')}<br/>

        Recommendation: {row.get('recommendation','')}<br/>

        Date: {row.get('date','')}<br/>

        Time: {row.get('time','')}

        """



        content.append(

            Paragraph(

                text,

                styles["Normal"]

            )

        )


        content.append(

            Spacer(
                1,
                15
            )

        )



    pdf.build(
        content
    )


    buffer.seek(0)


    return buffer




# ==========================================================
# HEADER
# ==========================================================


st.title(
    "📄 Feedback Reports"
)


st.caption(
    "Generate detailed student feedback analysis reports."
)


st.divider()



# ==========================================================
# LOAD DATA
# ==========================================================


df = get_feedback_dataframe()



if df is None or df.empty:


    st.info(
        "No feedback records available."
    )

    st.stop()



# ==========================================================
# SUMMARY METRICS
# ==========================================================


total = len(df)



positive = len(

    df[
        df["sentiment"]
        ==
        "Positive"
    ]

)



neutral = len(

    df[
        df["sentiment"]
        ==
        "Neutral"
    ]

)



negative = len(

    df[
        df["sentiment"]
        ==
        "Negative"
    ]

)



rating = get_average_rating()



c1,c2,c3,c4,c5 = st.columns(5)



c1.metric(
    "📝 Total",
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


c5.metric(
    "⭐ Rating",
    rating
)



st.divider()



# ==========================================================
# SENTIMENT REPORT
# ==========================================================


st.subheader(
    "📊 Sentiment Summary"
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

    hole=0.4,

    title="Feedback Sentiment Report"

)



fig.update_traces(

    textinfo="percent+label"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ==========================================================
# DEPARTMENT REPORT
# ==========================================================


st.subheader(
    "🏢 Department-wise Report"
)



department_df = (

    df["department"]

    .value_counts()

    .reset_index()

)



department_df.columns = [

    "Department",

    "Feedback Count"

]



fig2 = px.bar(

    department_df,

    x="Department",

    y="Feedback Count",

    text="Feedback Count",

    title="Department Feedback Summary"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)



st.divider()



# ==========================================================
# COMPLETE FEEDBACK TABLE
# ==========================================================


st.subheader(
    "📋 Feedback Data Preview"
)



st.dataframe(

    df,

    use_container_width=True,

    hide_index=True

)



st.divider()



# ==========================================================
# DOWNLOAD REPORTS
# ==========================================================


st.subheader(
    "⬇️ Generate Reports"
)



# ---------------- CSV ----------------


csv_data = df.to_csv(

    index=False

)



st.download_button(

    label="⬇️ Download CSV Report",

    data=csv_data,

    file_name="student_feedback_report.csv",

    mime="text/csv"

)



# ---------------- EXCEL ----------------


excel_buffer = BytesIO()



with pd.ExcelWriter(

    excel_buffer,

    engine="openpyxl"

) as writer:


    df.to_excel(

        writer,

        index=False,

        sheet_name="Feedback"

    )


excel_buffer.seek(0)



st.download_button(

    label="⬇️ Download Excel Report",

    data=excel_buffer,

    file_name="student_feedback_report.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)



# ---------------- PDF ----------------


pdf_file = create_pdf(df)



st.download_button(

    label="⬇️ Download PDF Report",

    data=pdf_file,

    file_name="student_feedback_report.pdf",

    mime="application/pdf"

)



st.success(

    "✅ Reports generated successfully."

)



st.divider()



# ==========================================================
# REPORT INSIGHTS
# ==========================================================


st.subheader(
    "💡 Report Insights"
)



positive_percentage = round(

    (positive / total) * 100,

    2

)



negative_percentage = round(

    (negative / total) * 100,

    2

)



neutral_percentage = round(

    (neutral / total) * 100,

    2

)



col1,col2,col3 = st.columns(3)



col1.info(

    f"""
😊 Positive Feedback

{positive_percentage}%
"""

)



col2.warning(

    f"""
😐 Neutral Feedback

{neutral_percentage}%
"""

)



col3.error(

    f"""
☹️ Negative Feedback

{negative_percentage}%
"""

)



st.divider()



# ==========================================================
# FOOTER
# ==========================================================


st.markdown(

"""
<div style="
text-align:center;
color:gray;
font-size:15px;
">

<b>
AI-Powered Student Feedback Analyzer
</b>

<br>

Dhanekula Institute of Engineering & Technology

<br>

Machine Learning Based Feedback System

<br>

© 2026

</div>
""",

unsafe_allow_html=True

)
st.divider()