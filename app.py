import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Roach Dynamos S&C", page_icon="⚽", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #FFFFFF; }
    p, div, li, span, label { color: #FFFFFF !important; }
    h1, h2, h3 { color: #FF8C00 !important; }
    div.stButton > button { background-color: #FF8C00; color: #000000; font-weight: bold; border-radius: 8px; border: none; }
    div.stButton > button:hover { background-color: #FF4500; color: white; }
    .stProgress > div > div > div { background-color: #FF69B4; }
    div.stExpander { border: 1px solid #FF8C00; background-color: #262626; color: #ffffff !important; }
    .card { background-color:#262626; padding:15px; border-radius:10px; border-left: 5px solid #FF8C00; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Initial Setup ---
AUTHORIZED_USERS = ["Player1", "Player2", "Coach1"]
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'logs' not in st.session_state: st.session_state.logs = pd.DataFrame(columns=["Player", "Date", "Exercise", "Effort", "Reflection", "Coach_Feedback", "Flagged"])
if 'milestones' not in st.session_state: st.session_state.milestones = pd.DataFrame(columns=["Player", "Test_Name", "Result", "Date"])

# --- Login ---
if not st.session_state.authenticated:
    st.title("⚽ Roach Dynamos S&C Portal")
    name = st.text_input("Enter your registered name:")
    if st.button("Log In"):
        if name in AUTHORIZED_USERS:
            st.session_state.authenticated = True
            st.session_state.user_name = name
            st.rerun()
        else: st.error("Name not recognized.")
    st.stop()

# --- Sidebar ---
# st.sidebar.image("logo.png", use_container_width=True) # Uncomment if logo file is uploaded
st.sidebar.title(f"Hi, {st.session_state.user_name}!")
if st.sidebar.button("Log Out"):
    st.session_state.authenticated = False
    st.rerun()
page = st.sidebar.radio("Navigate:", ["My Dashboard", "Milestone Tracking", "Technique Library", "Coach's View"])

# --- My Dashboard ---
if page == "My Dashboard":
    st.title(f"Welcome, {st.session_state.user_name}!")
    week = st.select_slider("Select Phase:", options=["Week 1-2: Foundations", "Week 3-4: Integration", "Week 5-6: Expression"])
    c1, c2 = st.columns(2)
    with c1: st.info(f"**Current Focus:** {week}")
    with c2: st.info("**Goal:** Master technique & build consistency.")

    st.subheader("Your Progress Calendar")
    user_logs = st.session_state.logs[st.session_state.logs['Player'] == st.session_state.user_name]
    if not user_logs.empty:
        for _, row in user_logs.tail(3).iterrows():
            st.markdown(f'<div class="card"><strong>{row["Date"]}</strong><br>{row["Exercise"]} - Effort: {row["Effort"]}/10</div>', unsafe_allow_html=True)
    
    st.subheader("➕ Log Today's Effort")
    focus = st.selectbox("Focus:", ["Mobility", "Core Stability", "Ladder Drills", "Speed/Agility"])
    effort = st.slider("Effort level (1-10):", 1, 10, 8)
    reflection = st.text_area("Reflection:")
    if st.button("Submit Session"):
        st.session_state.logs = pd.concat([st.session_state.logs, pd.DataFrame([{"Player": st.session_state.user_name, "Date": datetime.now().date(), "Exercise": focus, "Effort": effort, "Reflection": reflection, "Coach_Feedback": "Pending...", "Flagged": False}])], ignore_index=True)
        st.success("Session saved! 🚀")

# --- Milestone Tracking ---
elif page == "Milestone Tracking":
    st.title("📈 Milestone Tracker")
    user_data = st.session_state.milestones[st.session_state.milestones['Player'] == st.session_state.user_name]
    if not user_data.empty:
        last = user_data.iloc[-1]
        target = round(last['Result'] * 0.95, 2) if "Sprint" in last['Test_Name'] else round(last['Result'] * 1.07, 1)
        st.write(f"💡 Recommended Goal: **{target}**")
        if st.checkbox("Set custom goal?"): target = st.number_input("Goal:")
    test = st.selectbox("Test:", ["Plank (seconds)", "10m Sprint (seconds)", "Jump Height (cm)"])
    val = st.number_input("Result:")
    if st.button("Update PB"):
        st.session_state.milestones = pd.concat([st.session_state.milestones, pd.DataFrame([{"Player": st.session_state.user_name, "Test_Name": test, "Result": val, "Date": datetime.now().date()}])], ignore_index=True)
        st.success("PB recorded!")

# --- Technique Library ---
elif page == "Technique Library":
    st.title("📚 Technique Library")
    with st.expander("Plank Form"): st.write("Keep body in a straight line. Squeeze glutes!")
    with st.expander("Sprint Form"): st.write("Drive arms hard. Stay low!")

# --- Coach's View ---
elif page == "Coach's View":
    if st.text_input("Coach Password:", type="password") == "Dynamos2026":
        st.dataframe(st.session_state.logs)
        idx = st.number_input("Row Index:", 0, len(st.session_state.logs)-1)
        fb = st.text_area("Feedback:")
        flag = st.checkbox("Flag for discussion?")
        if st.button("Update Entry"):
            st.session_state.logs.at[idx, 'Coach_Feedback'] = fb
            st.session_state.logs.at[idx, 'Flagged'] = flag
            st.success("Updated!")
    else: st.warning("Access restricted.")
