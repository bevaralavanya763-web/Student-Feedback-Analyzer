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



# ==========================================================
# PDF GENERATION
# ==========================================================

def create_student_pdf(data):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    content = []


    content.append(
        Paragraph(
            "Student Feedback Report",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    for _, row in data.iterrows():


        report = f"""

        Roll Number: {row['roll_number']}<br/>

        Student Name: {row['student_name']}<br/>

        Department: {row['department']}<br/>

        Program: {row['program']}<br/>

        Year: {row['year']}<br/>

        Section: {row['section']}<br/>

        Event Name: {row['event_name']}<br/>

        Event Type: {row['event_type']}<br/>

        Rating: {row['rating']} / 5<br/>

        Feedback: {row['feedback']}<br/>

        Sentiment: {row['sentiment']}<br/>

        Keywords: {row['keywords']}<br/>

        Recommendation: {row['recommendation']}<br/>

        Date: {row['date']}<br/>

        Time: {row['time']}

        """


        content.append(
            Paragraph(
                report,
                styles["Normal"]
            )
        )


        content.append(
            Spacer(1,20)
        )



    pdf.build(content)

    buffer.seek(0)

    return buffer





# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(
    page_title="My Feedback Report",
    page_icon="📄",
    layout="wide"
)



# ==========================================================
# PAGE HEADER
# ==========================================================


st.title(
    "📄 My Feedback Report"
)


st.caption(
    "View and download your submitted feedback analysis."
)


st.divider()



# ==========================================================
# SEARCH REPORT
# ==========================================================


roll_number = st.text_input(
    "Enter Roll Number"
).strip().upper()



if st.button(
    "🔍 View Report",
    use_container_width=True
):


    if roll_number.strip()=="":


        st.warning(
            "Please enter your Roll Number."
        )

        st.stop()



    df = get_feedback_dataframe()



    if df is None or df.empty:


        st.error(
            "No feedback data available."
        )

        st.stop()



    student_data = df[
        df["roll_number"].astype(str)
        ==
        roll_number.strip()
    ]



    if student_data.empty:


        st.error(
            "No feedback found."
        )

        st.stop()



    st.success(
        "Feedback found successfully."
    )


    st.subheader(
        "Your Feedback Details"
    )


    st.dataframe(
        student_data,
        use_container_width=True
    )



    st.divider()



    # ======================================================
    # CSV DOWNLOAD
    # ======================================================


    csv = student_data.to_csv(
        index=False
    )


    st.download_button(

        "⬇️ Download CSV",

        csv,

        "my_feedback_report.csv",

        "text/csv"

    )



    # ======================================================
    # EXCEL DOWNLOAD
    # ======================================================


    excel_buffer = BytesIO()


    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:


        student_data.to_excel(
            writer,
            index=False
        )



    excel_buffer.seek(0)



    st.download_button(

        "⬇️ Download Excel",

        excel_buffer,

        "my_feedback_report.xlsx",

        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )



    # ======================================================
    # PDF DOWNLOAD
    # ======================================================


    pdf_file = create_student_pdf(
        student_data
    )


    st.download_button(

        "⬇️ Download PDF",

        pdf_file,

        "my_feedback_report.pdf",

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