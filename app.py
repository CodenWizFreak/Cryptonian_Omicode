import streamlit as st
from frontend import home, about
from frontend.user import dashboard, lesson, game, marketplace, leaderboard

# Configure page settings
st.set_page_config(
    page_title="Cryptonian - Learn, Play, Earn",
    page_icon="🎮",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")

# Check session state for wallet connection
if "wallet_connected" not in st.session_state:
    st.session_state["wallet_connected"] = False

if st.session_state["wallet_connected"]:
    if st.sidebar.button("Logout", key="logout", help="Disconnect your wallet and return to basic features."):
        st.session_state["wallet_connected"] = False
        st.rerun()
    
    options = ["Dashboard", "Lessons", "Games", "Marketplace", "Leaderboard"]
    default_page = "Dashboard"
else:
    if st.sidebar.button("Connect Wallet", key="connect_wallet", help="Connect your wallet to access all features."):
        st.session_state["wallet_connected"] = True
        st.rerun()
    
    options = ["Home", "About Us"]
    default_page = "Home"

# Selectbox for navigation
page = st.sidebar.selectbox("Go to", options, index=options.index(default_page))

# Render the selected page
if page == "Home":
    home.app()
elif page == "About Us":
    about.app()
elif page == "Dashboard":
    dashboard.app()
elif page == "Lessons":
    lesson.app()
elif page == "Games":
    game.app()
elif page == "Marketplace":
    marketplace.app()
elif page == "Leaderboard":
    leaderboard.app()
