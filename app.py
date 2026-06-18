import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Config & Styling ---
st.set_page_config(page_title="Roach Dynamos Diary", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #FFFFFF; }
    h1, h2, h3 { color: #FF8C00 !important; }
    .card { background-color:#262626; padding:15px; border-radius:10px; border-left: 5px solid #FF8C00; margin-bottom: 10px; }
    div.stButton > button { background-color: #FF8C00; color: #000000; font-weight: bold; border-radius: 8px; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- App State ---
if 'logs' not in st.session_state: st.session_state.logs = pd.DataFrame(columns=["Player", "Date", "Reflection", "Coach_Feedback"])
if 'milestones' not in st.session_state: st.session_state.milestones = pd.DataFrame(columns=["Player", "Moment", "Date"])

# --- Authentication ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    name = st.text_input("Enter your name:")
    if st.button("Log In"):
        st.session_state.authenticated = True
        st.session_state.user_name = name
        st.rerun()
    st.stop()

# --- Main Interface ---
st.sidebar.title(f"Hi, {st.session_state.user_name}!")
page = st.sidebar.radio("Navigation:", ["📖 My Training Diary", "⭐ My Best Moments", "📚 Technique Library", "📋 Coach's Dashboard"])

# --- Diary Page ---
if page == "📖 My Training Diary":
    st.title(f"📖 {st.session_state.user_name}'s Diary")
    reflection = st.text_area("How are you feeling about your training today?")
    if st.button("Save Diary Entry"):
        st.session_state.logs = pd.concat([st.session_state.logs, pd.DataFrame([{
            "Player": st.session_state.user_name, "Date": datetime.now().strftime("%B %d, %Y"), 
            "Reflection": reflection, "Coach_Feedback": "No feedback yet."}])], ignore_index=True)
        st.success("Entry saved!")
    
    st.subheader("Your Entries")
    for _, row in st.session_state.logs[st.session_state.logs['Player'] == st.session_state.user_name].tail(5).iterrows():
        st.markdown(f'<div class="card"><strong>{row["Date"]}</strong><br>{row["Reflection"]}<br><br><em>Coach: {row["Coach_Feedback"]}</em></div>', unsafe_allow_html=True)

# --- Milestones Page ---
elif page == "⭐ My Best Moments":
    st.title("⭐ My Best Moments")
    moment = st.text_input("What is a moment you're proud of?")
    if st.button("Save Memory"):
        st.session_state.milestones = pd.concat([st.session_state.milestones, pd.DataFrame([{"Player": st.session_state.user_name, "Moment": moment, "Date": datetime.now().strftime("%d/%m/%Y")}])], ignore_index=True)
    for _, row in st.session_state.milestones[st.session_state.milestones['Player'] == st.session_state.user_name].iterrows():
        st.info(f"{row['Date']}: {row['Moment']}")

# --- Technique Library ---
elif page == "📚 Technique Library":
    st.title("📚 Technique Library")
    with st.expander("Plank Tips"): st.write("Keep your core braced tight!")
    with st.expander("Sprint Tips"): st.write("Fast arms = fast feet!")

# --- Coach's Dashboard ---
elif page == "📋 Coach's Dashboard":
    if st.text_input("Password:", type="password") == "Dynamos2026":
        st.dataframe(st.session_state.logs)
        idx = st.number_input("Entry Index:", min_value=0, max_value=len(st.session_state.logs)-1)
        fb = st.text_area("Coach's Feedback:")
        if st.button("Update Diary"):
            st.session_state.logs.at[idx, 'Coach_Feedback'] = fb
            st.success("Feedback updated!")
