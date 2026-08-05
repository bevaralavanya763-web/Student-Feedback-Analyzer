import streamlit as st


# ==========================================================
# FIXED FACULTY CREDENTIALS
# ==========================================================

USERNAME = "admin"
PASSWORD = "admin123"

FACULTY_NAME = "Administrator"
FACULTY_ID = "ADMIN001"
DEPARTMENT = "Administration"


# ==========================================================
# LOGIN
# ==========================================================

def login(username, password):

    if username == USERNAME and password == PASSWORD:

        st.session_state["faculty_logged_in"] = True
        st.session_state["faculty_name"] = FACULTY_NAME
        st.session_state["faculty_id"] = FACULTY_ID
        st.session_state["department"] = DEPARTMENT
        st.session_state["username"] = USERNAME

        return True, "Login Successful."

    return False, "Invalid Username or Password."



# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    keys = [
        "faculty_logged_in",
        "faculty_name",
        "faculty_id",
        "department",
        "username"
    ]

    for key in keys:

        if key in st.session_state:
            del st.session_state[key]



# ==========================================================
# LOGIN STATUS
# ==========================================================

def is_logged_in():

    return st.session_state.get(
        "faculty_logged_in",
        False
    )



# ==========================================================
# CURRENT FACULTY
# ==========================================================

def current_faculty():

    if not is_logged_in():

        return None


    return {

        "faculty_name": st.session_state.get(
            "faculty_name"
        ),

        "faculty_id": st.session_state.get(
            "faculty_id"
        ),

        "department": st.session_state.get(
            "department"
        ),

        "username": st.session_state.get(
            "username"
        )

    }