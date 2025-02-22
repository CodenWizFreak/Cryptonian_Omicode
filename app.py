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
    
    st.sidebar.success(f"\U0001F4B0 Connected: {wallet_address[:3]}...{wallet_address[-3:]}")
    if st.sidebar.button("\U0001F511 Logout", key="logout", help="Disconnect your wallet and return to basic features."):
        st.session_state["wallet_connected"] = False
        st.session_state["wallet_address"] = ""
        st.session_state["selected_page"] = "home"
        st.rerun()
    
    pages = {
        "\U0001F4C8 Dashboard": "dashboard",
        "\U0001F4DA Lessons": "lesson",
        "\U0001F3AE Games": "game",
        "\U0001F6D2 Marketplace": "marketplace",
        "\U0001F3C6 Leaderboard": "leaderboard",
    }
    if "selected_page" not in st.session_state or st.session_state["selected_page"] == "home":
        st.session_state["selected_page"] = "dashboard"
else:
    pages = {
        "\U0001F3E0 Home": "home",
        "\U0001F4D6 About Us": "about",
    }


def navigate_to(page_name):
    st.session_state["selected_page"] = page_name
    st.rerun()

st.sidebar.markdown("### Navigation")

for label, module_name in pages.items():
    if st.sidebar.button(label, key=module_name, help=f"Go to {label}", use_container_width=True):
        navigate_to(module_name)

# Render the selected page
selected_page = st.session_state.get("selected_page", "dashboard" if st.session_state["wallet_connected"] else "home")
if selected_page == "home":
    home.app()
elif selected_page == "about":
    about.app()
elif selected_page == "dashboard":
    dashboard.app(wallet_address=wallet_address)
elif selected_page == "lesson":
    lesson.app(wallet_address=wallet_address)
elif selected_page == "game":
    game.app(wallet_address=wallet_address)
elif selected_page == "marketplace":
    marketplace.main(wallet_address=wallet_address)
elif selected_page == "leaderboard":
    leaderboard.app(wallet_address=wallet_address)

chatbot_ui()
