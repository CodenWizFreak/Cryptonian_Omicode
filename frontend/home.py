import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
import json
from pathlib import Path

def load_css():
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
        
        /* Main Styles */
        .stApp {
            background: linear-gradient(to bottom, #000000, #1a1a2e);
            font-family: 'Poppins', sans-serif;
            margin-top:10px;
        }
        
        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            padding: 20px;
            margin: 10px 0; /* Added margin */
        }
        
        .title-container {
            text-align: center;
        }
        
        .wallet-button {
            position: absolute;
            right: 20px;
            top: 20px;
            background: linear-gradient(45deg, #26d0ce 0%, #1a2980 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .wallet-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(38, 208, 206, 0.5);
            border: 2px solid #26d0ce;
        }

        /* Section Margins */
        h1, h3, .stHeader {
            margin: 10px 0; /* Added margin */
        }
        
        /* Card Styling */
        .card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            margin: 10px 0; /* Added margin */
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin: 15px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 200px;
            height: 100%;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(38, 208, 206, 0.2);
            border: 1px solid #26d0ce;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #26d0ce, #1a2980);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-card {
            background: linear-gradient(45deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            animation: pulse 2s infinite;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            min-height: 150px;
        }
        
        .stat-card-container {
            margin: 10px 0; /* Added margin */
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        .cool-feature-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 5px;
            margin: 15px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 220px;
            height: 100%;
        }
        
        .cool-feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(38, 208, 206, 0.2);
            border: 1px solid #26d0ce;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            margin: 10px 0; /* Added margin */
        }
        </style>
        """

def app():
    st.markdown(load_css(), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="header-container">
            <h1>🎮 Cryptonian 🎮</h1>
            <h3>Learn, Play, Earn - A gamified Web3 learning app</h3>
        </div>
    """, unsafe_allow_html=True)

    def check_wallet_connection():
        """Check if wallet is connected by reading from the file"""
        wallet_file = Path("back_api/wallet_address.json")
        if wallet_file.exists():
            with open(wallet_file) as f:
                data = json.load(f)
                st.session_state["wallet_connected"] = data["connected"]
                st.session_state["wallet_address"] = data["wallet_address"]
        else:
            st.session_state["wallet_connected"] = False
            st.session_state["wallet_address"] = ""

    # Wallet connection logic
    if "wallet_connected" not in st.session_state:
        st.session_state["wallet_connected"] = False
    check_wallet_connection()

    wallet_address = st.text_input("Enter Wallet Address", value="", key="wallet_address_input")
    
    if st.button("Connect Wallet", key="connect_wallet_button"):
        if wallet_address:
            st.session_state["wallet_connected"] = True
            st.session_state["wallet_address"] = wallet_address
            st.rerun()
        else:
            st.error("Please enter a wallet address.")

    if st.session_state["wallet_connected"]:
        short_address = f"{st.session_state['wallet_address'][:3]}...{st.session_state['wallet_address'][-3:]}"
        st.markdown(f"""
            <div class="wallet-address">
                Connected: {short_address}
            </div>
        """, unsafe_allow_html=True)
    
    # Key Features Section
    st.header("✨ Key Features")
    col1, col2, col3 = st.columns(3)

    features = [
        {"icon": "fas fa-book-open", "title": "Learning Modules", "desc": "Gamified quizzes on Web3, Indian geography, and history."},
        {"icon": "fas fa-gamepad", "title": "CV-Powered Games", "desc": "Scan monuments/maps to play interactive games and mint NFTs."},
        {"icon": "fas fa-globe", "title": "Web3 Integration", "desc": "Earn tokens, mint NFTs, and trade in the marketplace."}
    ]

    for idx, feature in enumerate([col1, col2, col3]):
        with feature:
            st.markdown(f"""
                <div class="card">
                    <i class="{features[idx]['icon']} feature-icon"></i>
                    <h3>{features[idx]['title']}</h3>
                    <p>{features[idx]['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Statistics Section
    st.header("📊 Platform Statistics")
    col1, col2, col3 = st.columns(3)

    stats = [
        {"icon": "fas fa-users", "value": "100,000+", "label": "Total Users"},
        {"icon": "fas fa-images", "value": "50,000+", "label": "NFTs Minted"},
        {"icon": "fas fa-check-circle", "value": "1,000,000+", "label": "Quizzes Completed"}
    ]

    for idx, stat in enumerate([col1, col2, col3]):
        with stat:
            st.markdown(f"""
                <div class="stat-card">
                    <i class="{stats[idx]['icon']}" style="font-size: 2rem;"></i>
                    <h2>{stats[idx]['value']}</h2>
                    <p>{stats[idx]['label']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Cool Features Section
    st.header("🚀 Cool Features")
    col1, col2, col3, col4 = st.columns(4)

    features = [
        {
            "icon": "fas fa-camera",
            "title": "Monument Scanner",
            "desc": "Upload selfies with monuments and learn their history through AI."
        },
        {
            "icon": "fas fa-paint-brush",
            "title": "Dynamic NFTs",
            "desc": "Watch your NFTs evolve as you progress through different learning modules."
        },
        {
            "icon": "fas fa-map-marked-alt",
            "title": "Geo-Quiz Challenges",
            "desc": "Test your knowledge of Indian geography with our interactive map quizzes."
        },
        {
            "icon": "fas fa-store",
            "title": "Token-Powered Marketplace",
            "desc": "Use earned tokens to unlock premium content or trade with other learners."
        }
    ]

    for idx, feature in enumerate([col1, col2, col3, col4]):
        with feature:
            st.markdown(f"""
                <div class="cool-feature-card">
                    <i class="{features[idx]['icon']}" style="font-size: 2rem; color: #26d0ce; display:flex; min-height:30px;"></i>
                    <h3>{features[idx]['title']}</h3>
                    <p style="align-items: center; justify-content: space-between;">{features[idx]['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 20px; margin-top: 50px; color: white;">
            <p>© 2023 Cryptonian. All rights reserved.</p>
            <p><i class="fas fa-envelope"></i> info@cryptonian.com | <i class="fas fa-phone"></i> +91 123 456 7890</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
