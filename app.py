import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Config & Custom Styling ---
st.set_page_config(page_title="Roach Dynamos S&C", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #FFFFFF; }
    h1, h2, h3 { color: #FF8C00; }
    div.stButton > button { background-color: #FF8C00; color: #000000; font-weight: bold; border-radius: 8px; border: none; }
    div.stButton > button:hover { background-color: #FF4500; color: white; }
    .stProgress > div > div > div { background-color: #FF69B4; }
    div.stExpander { border: 1px solid #FF8C00; background-color: #262626; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- Authorized User List ---
AUTHORIZED_USERS = ["Player1", "Player2", "Coach1"]

# --- State Initialization ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'logs' not in st.session_state: st.session_state.logs = pd.DataFrame(columns=["Player", "Date", "Exercise", "Effort", "Reflection", "Coach_Feedback", "Flagged"])
if 'milestones' not in st.session_state: st.session_state.milestones = pd.DataFrame(columns=["Player", "Test_Name", "Result", "Date"])

# --- Login Logic ---
if not st.session_state.authenticated:
    st.title("⚽ Roach Dynamos S&C Portal")
    name = st.text_input("Enter your registered name:")
    if st.button("Log In"):
        if name in AUTHORIZED_USERS:
            st.session_state.authenticated = True
            st.session_state.user_name = name
            st.rerun()
        else: st.error("Name not recognized. Please check with your Coach.")
    st.stop()

# --- Main App Interface ---
st.sidebar.title(f"Hi, {st.session_state.user_name}!")
if st.sidebar.button("Log Out"):
    st.session_state.authenticated = False
    st.rerun()

page = st.sidebar.radio("Navigate:", ["My Dashboard", "Milestone Tracking", "Technique Library", "Coach's View"])

# --- Page: My Dashboard ---
if page == "My Dashboard":
    st.title("⚽ Training Session Log")
    focus = st.selectbox("Today's Focus:", ["Mobility", "Core Stability", "Ladder Drills", "Speed/Agility"])
    effort = st.slider("Effort level (1-10):", 1, 10, 8)
    reflection = st.text_area("How did you feel? (Reflect on your technique):")
    
    if st.button("Submit Session"):
        new_entry = {"Player": st.session_state.user_name, "Date": datetime.now().date(), 
                     "Exercise": focus, "Effort": effort, "Reflection": reflection, 
                     "Coach_Feedback": "Pending...", "Flagged": False}
        st.session_state.logs = pd.concat([st.session_state.logs, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Awesome work! Session saved! 🚀")

# --- Page: Milestone Tracking ---
elif page == "Milestone Tracking":
    st.title("📈 Milestone Tracker")
    user_data = st.session_state.milestones[st.session_state.milestones['Player'] == st.session_state.user_name]
    
    if not user_data.empty:
        last = user_data.iloc[-1]
        target = round(last['Result'] * 0.95, 2) if "Sprint" in last['Test_Name'] else round(last['Result'] * 1.07, 1)
        st.info(f"💡 Recommended Goal: **{target}**")
        use_manual = st.checkbox("Set custom goal?")
        target = st.number_input("Enter your goal:", value=target) if use_manual else target
    
    test = st.selectbox("Test Type:", ["Plank (seconds)", "10m Sprint (seconds)", "Jump Height (cm)"])
    val = st.number_input("Enter result:")
    if st.button("Update PB"):
        st.session_state.milestones = pd.concat([st.session_state.milestones, pd.DataFrame([{"Player": st.session_state.user_name, "Test_Name": test, "Result": val, "Date": datetime.now().date()}])], ignore_index=True)
        st.success("New PB recorded!")

# --- Page: Technique Library ---
elif page == "Technique Library":
    st.title("📚 Technique Library")
    with st.expander("Plank Form"): st.write("Keep body in a straight line. Squeeze glutes!")
    with st.expander("Sprint Form"): st.write("Drive arms hard. Stay low!")

# --- Page: Coach's View ---
elif page == "Coach's View":
    pwd = st.text_input("Enter Coach Password:", type="password")
    if pwd == "Dynamos2026":
        st.subheader("Team Overview")
        st.dataframe(st.session_state.logs)
        idx = st.number_input("Select row index for feedback:", 0, len(st.session_state.logs)-1)
        fb = st.text_area("Provide feedback:")
        flag = st.checkbox("Flag for discussion?")
        if st.button("Update Entry"):
            st.session_state.logs.at[idx, 'Coach_Feedback'] = fb
            st.session_state.logs.at[idx, 'Flagged'] = flag
            st.success("Entry updated!")
    else: st.warning("Access restricted. 🛡️")
