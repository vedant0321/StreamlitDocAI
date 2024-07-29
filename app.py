import streamlit as st
from streamlit_navigation_bar import st_navbar
from home import show_home  # Import the homepage function
from AI_Bot import show_AI_Bot  # Import the AI Bot function
from summary import show_summary  # Import the summary function
from contact import show_contact  # Import the contact function
# Sidebar
nav = st_navbar(["Home", "AI-Bot", "Summary", "Contact"])
# App title
# Center-aligned title
st.markdown("<h1 style='text-align: center;'>DocAI-App</h1>", unsafe_allow_html=True)

# Navigation logic
if nav == "Home":
    show_home()
elif nav == "AI-Bot":
    show_AI_Bot()
elif nav == "Summary":
    show_summary()
elif nav == "Contact":
    show_contact()