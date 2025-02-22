import streamlit as st
from datetime import datetime
from database.db import * # Import the MongoDB connection function
from frontend import home, about
from frontend.user import dashboard, lesson, game, marketplace, leaderboard
from frontend.user.chatbot import chatbot_ui

# ✅ Move this to the top before any other Streamlit functions
st.set_page_config(
    page_title="Cryptonian - Learn, Play, Earn",
    page_icon="🎮",
    layout="wide"
)

# Connect to MongoDB
db = connect_db()

def save_wallet_connection(wallet_address):
    existing_user = db.users.find_one({"wallet_address": wallet_address})
    status = "Login" if existing_user else "Sign Up"
    db.users.insert_one({
        "wallet_address": wallet_address,
        "status": status,
        "timestamp": datetime.now()
    })

# Sidebar navigation
st.sidebar.title("Navigation")

# Check session state for wallet connection
if "wallet_connected" not in st.session_state:
    st.session_state["wallet_connected"] = False
if "wallet_address" not in st.session_state:
    st.session_state["wallet_address"] = ""

# Navigation options based on wallet connection status
if st.session_state["wallet_connected"]:
    wallet_address = st.session_state["wallet_address"]
    save_wallet_connection(wallet_address)
    
    st.sidebar.success(f"Connected: {wallet_address[:3]}...{wallet_address[-3:]}")
    if st.sidebar.button("Logout", key="logout", help="Disconnect your wallet and return to basic features."):
        st.session_state["wallet_connected"] = False
        st.session_state["wallet_address"] = ""
        st.rerun()
    
    options = ["Dashboard", "Lessons", "Games", "Marketplace", "Leaderboard"]
    default_page = "Dashboard"
else:
    options = ["Home", "About Us"]
    default_page = "Home"

# Selectbox for navigation
page = st.sidebar.selectbox("Go to", options, index=options.index(default_page))

chatbot_ui()

# Render the selected page
if page == "Home":
    home.app()
elif page == "About Us":
    about.app()
elif page == "Dashboard":
    dashboard.app(wallet_address=wallet_address)
elif page == "Lessons":
    lesson.app(wallet_address=wallet_address)
elif page == "Games":
    game.app(wallet_address=wallet_address)
elif page == "Marketplace":
    marketplace.main(wallet_address=wallet_address)
elif page == "Leaderboard":
    leaderboard.app(wallet_address=wallet_address)