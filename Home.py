import streamlit as st
import datetime
#import pandas as pd
from google_connect import connect_to_sheets
from utils import calculate_risk
from auth import login_signup
import time

st.set_page_config(page_title="BreatheSmart UG")

# --------------------------------------------------
# GLOBAL CSS (Hide Streamlit UI + Add Animations)
# --------------------------------------------------
st.markdown("""
<style>

/* Hide Streamlit UI */
[data-testid="stSidebar"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Fade animation */
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0px); }
}

.big-title {
    font-size: 40px;
    font-weight: 700;
    text-align: center;
}

.card {
    padding: 30px;
    border-radius: 12px;
    background-color: rgba(240,245,250,0.6);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------
def dashboard_page():

    if not st.session_state.get("logged_in"):
        return

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    col1, col2 = st.columns([7, 2])

    with col1:
        st.image("new_breathsmart.png", width=300)
        st.markdown(f"## 👋 Welcome, {st.session_state.name}")
        st.write("Log today’s respiratory symptoms below.")

    with col2:
        if st.button("Logout"):
            st.session_state.clear()
            time.sleep(0.3)
            st.rerun()

    st.markdown("---")

    users_sheet, logs_sheet = connect_to_sheets()

    with st.container():
        with st.form("log_form"):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### Symptoms")
                wheezing = st.checkbox("Wheezing")
                night_symptoms = st.checkbox("Night-time symptoms")
                runny_nose = st.checkbox("Runny nose")
                cough = st.checkbox("Coughing")
                itchy_eyes = st.checkbox("Itchy eyes")
                chest = st.checkbox("Chest Tightness")
                congestion = st.checkbox("Nasal Congestion")

            with col2:
                st.markdown("### Environment")
                dust_exposure = st.checkbox("Dust exposure")
                smoke_exposure = st.checkbox("Smoke exposure")
                cold_weather = st.checkbox("Cold weather")

            with col3:
                st.markdown("### Medication")
                inhaler_used = st.checkbox("Used rescue inhaler")
                others = st.checkbox("Other medications")

            submitted = st.form_submit_button("Submit Daily Log")

        # ✅ HANDLE SUBMISSION INSIDE SAFE BLOCK
        if submitted:

            data = {
                "wheezing": wheezing,
                "chest": chest,
                "night_symptoms": night_symptoms,
                "runny_nose": runny_nose,
                "itchy_eyes": itchy_eyes,
                "dust_exposure": dust_exposure,
                "smoke_exposure": smoke_exposure,
                "cold_weather": cold_weather,
                "cough": cough,
                "congestion": congestion,
                "inhaler_used": inhaler_used,
                "others": others,
            }

            risk = calculate_risk(data)

            logs_sheet.append_row([
                str(datetime.date.today()),
                st.session_state.user_id,
                st.session_state.division,
                wheezing,
                chest,
                night_symptoms,
                runny_nose,
                itchy_eyes,
                dust_exposure,
                smoke_exposure,
                cold_weather,
                cough,
                congestion,
                inhaler_used,
                others,
                risk
            ])

            st.success("✅ Log saved successfully")

            if risk >= 11:
                st.error("⚠ High risk detected. Consider preventive action for next 24 hours.")
            elif risk >= 6 and risk <= 10:
                st.warning("🟡 Moderate risk level. Monitor symptoms and environment closely for the next 24 hours.")
            else:
                st.info("🟢 Low risk today. Keep breathing smart!")

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# MAIN FLOW CONTROLLER
# --------------------------------------------------

if not st.session_state.logged_in:
    login_signup()
else:
    dashboard_page()
