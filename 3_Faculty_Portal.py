import streamlit as st


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Faculty Portal",
    page_icon="👨‍🏫",
    layout="wide"
)


# ==========================================================
# FIXED LOGIN CREDENTIALS
# ==========================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

if "faculty_logged_in" not in st.session_state:
    st.session_state["faculty_logged_in"] = False


# ==========================================================
# TITLE
# ==========================================================

st.title("👨‍🏫 Faculty Portal")
st.caption("Authorized Faculty Login")
st.divider()


# ==========================================================
# LOGGED IN VIEW
# ==========================================================

if st.session_state["faculty_logged_in"]:

    st.success("Welcome, Admin")


    st.write(
        """
        **Username:** admin

        **Access Level:** Faculty Administrator

        **Available Modules:**
        - Dashboard
        - Feedback Records
        - Feedback Analysis
        - Reports
        """
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "📊 Open Dashboard",
            use_container_width=True
        ):

            st.switch_page(
                "pages/4_Dashboard.py"
            )


    with col2:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state["faculty_logged_in"] = False

            st.success(
                "Logged out successfully"
            )

            st.switch_page(
                "Home.py"
            )


    st.stop()



# ==========================================================
# LOGIN FORM
# ==========================================================

st.subheader("🔐 Faculty Login")


username = st.text_input(
    "Username"
)


password = st.text_input(
    "Password",
    type="password"
)



if st.button(
    "Login",
    use_container_width=True
):

    if (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    ):

        st.session_state["faculty_logged_in"] = True

        st.success(
            "Login Successful"
        )

        st.switch_page(
            "pages/4_Dashboard.py"
        )


    else:

        st.error(
            "Invalid Username or Password"
        )