import streamlit as st
import pandas as pd

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


from database import get_feedback_dataframe

import streamlit as st


def is_logged_in():

    return st.session_state.get(
        "faculty_logged_in",
        False
    )


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Feedback Records",
    page_icon="📋",
    layout="wide"
)



# ==========================================================
# FACULTY SECURITY
# ==========================================================

if not is_logged_in():

    st.warning(
        "🔒 Faculty login required."
    )

    st.stop()



# ==========================================================
# PDF CREATION
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
            "Student Feedback Records Report",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    for _, row in data.iterrows():


        text = f"""

        Roll Number: {row['roll_number']}<br/>

        Student Name: {row['student_name']}<br/>

        Department: {row['department']}<br/>

        Program: {row['program']}<br/>

        Year: {row['year']}<br/>

        Section: {row['section']}<br/>

        Event: {row['event_name']}<br/>

        Rating: {row['rating']}<br/>

        Feedback: {row['feedback']}<br/>

        Sentiment: {row['sentiment']}<br/>

        Keywords: {row['keywords']}<br/>

        Recommendation: {row['recommendation']}<br/>

        Date: {row['date']}<br/>

        Time: {row['time']}

        """


        content.append(
            Paragraph(
                text,
                styles["Normal"]
            )
        )


        content.append(
            Spacer(1,15)
        )


    pdf.build(content)

    buffer.seek(0)

    return buffer



# ==========================================================
# TITLE
# ==========================================================


st.title(
    "📋 Feedback Records"
)


st.caption(
    "View, filter and download complete student feedback data."
)


st.divider()



# ==========================================================
# LOAD DATA
# ==========================================================


df = get_feedback_dataframe()



if df.empty:

    st.info(
        "No feedback records available."
    )

    st.stop()
filtered_df = df.copy()



# ==========================================================
# FILTER SECTION
# ==========================================================


st.subheader(
    "🔍 Search & Filter"
)



col1, col2, col3 = st.columns(3)



with col1:

    search = st.text_input(
        "Search Student"
    ).strip().upper()



with col2:

    departments = [
        "All"
    ] + sorted(
        df["department"].unique().tolist()
    )


    department_filter = st.selectbox(
        "Department",
        departments
    )



with col3:

    sentiments = [
        "All"
    ] + sorted(
        df["sentiment"].unique().tolist()
    )


    sentiment_filter = st.selectbox(
        "Sentiment",
        sentiments
    )

if search:

    filtered_df = filtered_df[

        filtered_df["student_name"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )

        |

        filtered_df["roll_number"]
        .astype(str)
        .str.upper()
        .str.contains(
            search,
            na=False
        )

    ]





if department_filter != "All":

    filtered_df = filtered_df[
        filtered_df["department"]
        ==
        department_filter
    ]



if sentiment_filter != "All":

    filtered_df = filtered_df[
        filtered_df["sentiment"]
        ==
        sentiment_filter
    ]



st.divider()



# ==========================================================
# SUMMARY
# ==========================================================


c1,c2,c3 = st.columns(3)


c1.metric(
    "Total Records",
    len(filtered_df)
)


c2.metric(
    "Positive",
    len(
        filtered_df[
            filtered_df["sentiment"]
            ==
            "Positive"
        ]
    )
)


c3.metric(
    "Negative",
    len(
        filtered_df[
            filtered_df["sentiment"]
            ==
            "Negative"
        ]
    )
)



st.divider()



# ==========================================================
# TABLE
# ==========================================================


st.subheader(
    "📄 Feedback Records"
)


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)



st.divider()



# ==========================================================
# DOWNLOAD
# ==========================================================


st.subheader(
    "⬇️ Download Reports"
)



# CSV

csv = filtered_df.to_csv(
    index=False
)


st.download_button(

    "Download CSV",

    csv,

    "feedback_records.csv",

    "text/csv"

)



# Excel

excel_buffer = BytesIO()


with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    filtered_df.to_excel(
        writer,
        index=False
    )



excel_buffer.seek(0)



st.download_button(

    "Download Excel",

    excel_buffer,

    "feedback_records.xlsx",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)



# PDF

pdf = create_pdf(
    filtered_df
)



st.download_button(

    "Download PDF",

    pdf,

    "feedback_records.pdf",

    "application/pdf"

)



# ==========================================================
# FOOTER
# ==========================================================


st.divider()


st.markdown(
"""
<div style="text-align:center;color:gray;">

<b>AI-Powered Student Feedback Analyzer</b><br>

Dhanekula Institute of Engineering & Technology

</div>
""",
unsafe_allow_html=True
)