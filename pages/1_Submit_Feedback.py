import streamlit as st

from database import insert_feedback

from sentiment import sentiment_result

from keyword_extractor import extract_keywords

from recommendation import generate_recommendation

from utils import (
    validate_roll_number,
    validate_name,
    validate_feedback,
    get_current_date,
    get_current_time,
    clean_text
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Submit Feedback",
    page_icon="📝",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title("📝 Student Feedback Submission")

st.caption(
    "AI-powered feedback analysis system"
)


st.divider()



# ==========================================================
# STUDENT INFORMATION
# ==========================================================

st.subheader("🎓 Student Information")


col1, col2 = st.columns(2)



with col1:

    roll_number = st.text_input(
        "Roll Number",
        placeholder="Enter your roll number"
    ).strip().upper()


    department = st.selectbox(
        "Department",
        [
            "Select Department",
            "CSE",
            "CSE(AI & ML)",
            "AI & ML",
            "AI & DS",
            "ECE",
            "EEE",
            "Mechanical",
            "Civil"
        ]
    )


    year = st.selectbox(
        "Year",
        [
            "1",
            "2",
            "3",
            "4"
        ]
    )



with col2:

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )


    program = st.selectbox(
        "Program",
        [
            "B.Tech",
            "M.Tech",
            "Diploma",
            "Other"
        ]
    )


    section = st.text_input(
        "Section",
        placeholder="Enter your section"
    )



st.divider()



# ==========================================================
# EVENT INFORMATION
# ==========================================================

st.subheader("🎯 Event Information")


col3, col4 = st.columns(2)



with col3:

    event_name = st.text_input(
        "Event Name",
        placeholder="Enter event name"
    )


    event_type = st.selectbox(
        "Event Type",
        [
            "Workshop",
            "Seminar",
            "Hackathon",
            "Technical Fest",
            "Guest Lecture",
            "Training Program",
            "Other"
        ]
    )



with col4:

    faculty_name = st.text_input(
        "Faculty Name",
        placeholder="Optional"
    )


    rating = st.slider(
        "⭐ Event Rating",
        min_value=1,
        max_value=5,
        value=4
    )



st.divider()



# ==========================================================
# FEEDBACK SECTION
# ==========================================================

st.subheader("💬 Your Feedback")


feedback = st.text_area(
    "Write your feedback",
    placeholder="Share your experience...",
    height=180
)


st.divider()


# ==========================================================
# SUBMIT BUTTON
# ==========================================================

submit = st.button(
    "🤖 Analyze & Submit Feedback",
    use_container_width=True
)



# ==========================================================
# PROCESS FEEDBACK
# ==========================================================

if submit:


    # ---------------- Validation ----------------


    feedback = clean_text(feedback)


    if not validate_roll_number(roll_number):

        st.error(
            "Please enter a valid Roll Number."
        )

        st.stop()



    if not validate_name(student_name):

        st.error(
            "Please enter a valid Student Name."
        )

        st.stop()



    if not validate_feedback(feedback):

        st.error(
            "Feedback should contain minimum 10 characters."
        )

        st.stop()



    if department == "Select Department":

        st.warning(
            "Please select your department."
        )

        st.stop()



    if event_name.strip() == "":

        st.warning(
            "Please enter event name."
        )

        st.stop()



    # ==================================================
    # AI SENTIMENT ANALYSIS
    # ==================================================


    with st.spinner(
        "Analyzing feedback using AI..."
    ):


        result = sentiment_result(
            feedback
        )


        sentiment = result["sentiment"]

        confidence = result["confidence"]



        keywords = extract_keywords(
            feedback
        )



        recommendation = generate_recommendation(
            sentiment,
            rating
        )



        date = get_current_date()

        time = get_current_time()



    # ==================================================
    # DISPLAY RESULTS
    # ==================================================


    st.success(
        "✅ Feedback analyzed successfully!"
    )


    st.divider()



    result_col1, result_col2 = st.columns(2)



    with result_col1:


        st.metric(
            "Sentiment",
            sentiment
        )


        st.metric(
            "Confidence",
            f"{confidence}%"
        )



    with result_col2:


        st.metric(
            "Rating",
            f"{rating}/5"
        )


        st.metric(
            "Keywords",
            len(keywords)
        )



    st.subheader(
        "🔑 Extracted Keywords"
    )


    if keywords:

        st.write(
            ", ".join(keywords)
        )

    else:

        st.info(
            "No important keywords detected."
        )



    st.subheader(
        "💡 AI Recommendation"
    )


    st.info(
        recommendation
    )



    # ==================================================
    # SAVE TO DATABASE
    # ==================================================


    try:


        insert_feedback(

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


        st.success(
            "🎉 Feedback saved successfully!"
        )


    except Exception as e:


        st.error(
            f"Database Error: {e}"
        )



    # ==================================================
    # SUMMARY
    # ==================================================


    st.divider()


    with st.expander(
        "📋 View Feedback Summary"
    ):


        st.subheader(
            "Student Details"
        )


        st.write(
            f"""
            **Roll Number:** {roll_number}

            **Name:** {student_name}

            **Department:** {department}

            **Program:** {program}

            **Year:** {year}

            **Section:** {section}
            """
        )



        st.subheader(
            "Event Details"
        )


        st.write(
            f"""
            **Event:** {event_name}

            **Type:** {event_type}

            **Faculty:** {faculty_name if faculty_name else "Not Provided"}

            **Rating:** ⭐ {rating}/5
            """
        )



        st.subheader(
            "AI Analysis"
        )


        st.write(
            f"""
            **Sentiment:** {sentiment}

            **Confidence:** {confidence}%

            **Keywords:** {", ".join(keywords) if keywords else "None"}

            **Recommendation:** {recommendation}
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
