import streamlit as st
import os


from database import (
    get_total_feedback,
    get_sentiment_stats
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Student Feedback Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD CSS
# ============================================================

css_path = "assets/style.css"

if os.path.exists(css_path):

    with open(css_path) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.markdown("""
<style>

.main-header h1 {
    font-size: 38px;
}

.main-header h2 {
    font-size: 24px;
}

.main-header p {
    font-size: 18px;
}


@media (max-width: 768px){

    .main-header h1 {
        font-size: 25px;
    }

    .main-header h2 {
        font-size: 18px;
    }

    .main-header p {
        font-size: 14px;
    }

}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}


@media(max-width:768px){

.block-container {
    padding-left: 1rem;
    padding-right: 1rem;
}

}

</style>
""", unsafe_allow_html=True)
# ============================================================
# PATHS
# ============================================================

logo = "assets/college_logo.png"


# ============================================================
# SESSION STATUS
# ============================================================

faculty_logged_in = st.session_state.get(
    "faculty_logged_in",
    False
)


# ============================================================
# SIDEBAR
# ============================================================

if os.path.exists(logo):

    st.sidebar.image(
        logo,
        use_container_width=True
    )


st.sidebar.markdown(
    """
    <h3 style="text-align:center;">
    Dhanekula Institute of Engineering & Technology
    </h3>
    """,
    unsafe_allow_html=True
)


st.sidebar.divider()


# Home

st.sidebar.markdown("### 🏠 Home")

# ============================================================
# STUDENT SECTION
# ============================================================

st.sidebar.markdown("### 🎓 Student Portal")

if st.sidebar.button("📝 Submit Feedback", use_container_width=True):
    st.switch_page("pages/1_Submit_Feedback.py")

if st.sidebar.button("📄 My Report", use_container_width=True):
    st.switch_page("pages/2_My_Report.py")

# ============================================================
# FACULTY SECTION
# ============================================================

st.sidebar.markdown("### 👨‍🏫 Faculty Portal")

if faculty_logged_in:

    st.sidebar.success("Welcome Admin")

    st.sidebar.markdown("### 📊 Faculty Management")

    if st.sidebar.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/4_Dashboard.py")

    if st.sidebar.button("📋 Feedback Records", use_container_width=True):
        st.switch_page("pages/5_Feedback_Records.py")

    if st.sidebar.button("📈 Feedback Analysis", use_container_width=True):
        st.switch_page("pages/6_Feedback_Analysis.py")

    if st.sidebar.button("📄 Feedback Reports", use_container_width=True):
        st.switch_page("pages/7_Feedback_Reports.py")

else:

    if st.sidebar.button("🔐 Faculty Login", use_container_width=True):
        st.switch_page("pages/3_Faculty_Portal.py")
    

# ============================================================
# SETTINGS
# ============================================================

st.sidebar.markdown(
    "### ⚙️ Settings"
)


if faculty_logged_in:

    if st.sidebar.button("🚪 Logout"):

        st.session_state["faculty_logged_in"] = False

        st.success("Logged out successfully")

        st.rerun() 

    
# ============================================================
# RESPONSIVE HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [1, 4],
    gap="large"
)


with header_col1:

    if os.path.exists(logo):

        st.image(
            logo,
            width=120
        )


with header_col2:

    st.markdown(
        """
        <div class="main-header">

        <h2>
        Dhanekula Institute of Engineering & Technology
        </h2>

        <h1>
        🎓 AI-Powered Student Feedback Analyzer
        </h1>

        <p>
        Machine Learning based feedback analysis system
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()




# ============================================================
# LIVE STATISTICS
# ============================================================

try:

    total = get_total_feedback()

    sentiment_data = get_sentiment_stats()


    positive = 0
    neutral = 0
    negative = 0


    for item in sentiment_data:

        if item[0] == "Positive":
            positive = item[1]

        elif item[0] == "Neutral":
            neutral = item[1]

        elif item[0] == "Negative":
            negative = item[1]


except Exception:

    total = 0
    positive = 0
    neutral = 0
    negative = 0


if st.session_state.get("faculty_logged_in", False):

    col1, col2 = st.columns(2)

    col3, col4 = st.columns(2)

    with col1:
        st.metric("📝 Total Feedback", total)

    with col2:
        st.metric("😊 Positive", positive)

    with col3:
        st.metric("😐 Neutral", neutral)

    with col4:
        st.metric("☹️ Negative", negative)


st.divider()

# ============================================================
# CLICKABLE MODULE CARDS
# ============================================================

st.header("🚀 Application Modules")


st.markdown("""
<style>

div.stButton > button {

    width: 100%;
    height: 130px;
    border-radius: 18px;
    background-color: #B3E5FC;
    color: #0D3B66;
    font-size: 20px;
    font-weight: 600;
    border: 1px solid #81D4FA;
    white-space: pre-line;

}


div.stButton > button:hover {

    background-color: #81D4FA;
    color: #0D3B66;

}


</style>
""", unsafe_allow_html=True)



if st.session_state.get(
    "faculty_logged_in",
    False
):

    st.subheader("👨‍🏫 Faculty Services")


    col1, col2 = st.columns(
        2,
        gap="large"
    )


    with col1:

        if st.button(
            "📊 Dashboard\n\nFeedback statistics & trends",
            use_container_width=True
        ):

            st.switch_page(
                "pages/4_Dashboard.py"
            )


        if st.button(
            "📋 Feedback Records\n\nManage student feedback",
            use_container_width=True
        ):

            st.switch_page(
                "pages/5_Feedback_Records.py"
            )


    with col2:

        if st.button(
            "📈 Feedback Analysis\n\nAI sentiment analysis",
            use_container_width=True
        ):

            st.switch_page(
                "pages/6_Feedback_Analysis.py"
            )


        if st.button(
            "📄 Feedback Reports\n\nGenerate reports",
            use_container_width=True
        ):

            st.switch_page(
                "pages/7_Feedback_Reports.py"
            )


else:

    st.subheader("🎓 Student Services")


    col1, col2 = st.columns(
        2,
        gap="large"
    )


    with col1:

        if st.button(
            "📝 Submit Feedback\n\nShare your feedback",
            use_container_width=True
        ):

            st.switch_page(
                "pages/1_Submit_Feedback.py"
            )


    with col2:

        if st.button(
            "📄 My Report\n\nView your feedback report",
            use_container_width=True
        ):

            st.switch_page(
                "pages/2_My_Report.py"
            )


    st.subheader("👨‍🏫 Faculty Services")


    if st.button(
        "🔐 Faculty Login\n\nAuthorized access",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Faculty_Portal.py"
        )
