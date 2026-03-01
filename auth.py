import streamlit as st
import datetime
from google_connect import connect_to_sheets
from utils import hash_password, check_password


def login_signup():

    users_sheet, _ = connect_to_sheets()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return

    users = users_sheet.get_all_records()

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("new_breathsmart.png", width=300)

    st.markdown(
        "<h3 style='text-align: center;'>Respiratory Risk Intelligence Platform</h3>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------------------------
    # Toggle between Login / Sign Up
    # ---------------------------------
    auth_mode = st.radio(
        "Select Option",
        ["Login", "Sign Up"],
        horizontal=True
    )

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # =================================
    # LOGIN LOGIC
    # =================================
    if auth_mode == "Login":

        if st.button("Login"):

            for user in users:
                if user["email"] == email:

                    if check_password(password, user["password"]):

                        st.session_state.logged_in = True
                        st.session_state.user_id = user["user_id"]
                        # st.session_state.role = user["role"]
                        st.session_state.name = user["full_name"]
                        st.session_state.division = user["division"]

                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Incorrect password.")
                        return

            st.error("User not found.")

    # =================================
    # SIGNUP LOGIC
    # =================================
    elif auth_mode == "Sign Up":

        name = st.text_input("Full Name")
        division = st.selectbox(
            "Division",
            ["Central", "Kawempe", "Makindye", "Nakawa", "Rubaga"]
        )

        if st.button("Create Account"):

            if email in [u["email"] for u in users]:
                st.error("Email already exists.")
                return

            if not email or not password or not name:
                st.error("Please fill in all fields.")
                return

            user_id = str(len(users) + 1)

            users_sheet.append_row([
                user_id,
                email,
                hash_password(password),
                name,
                division,
                str(datetime.datetime.now())
            ])

            st.success("Account created successfully. Please login.")

    st.markdown('</div>', unsafe_allow_html=True)
