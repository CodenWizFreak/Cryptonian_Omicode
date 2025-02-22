import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64

def load_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
        
        .stApp {
            background: linear-gradient(to bottom, #000000, #1a1a2e);
            font-family: 'Poppins', sans-serif;
            margin-top:10px;
        }

        .header-container {
            text-align: center;
            padding: 20px;
            margin: 10px 0;
        }

        .wallet-button {
            background: linear-gradient(45deg, #26d0ce 0%, #1a2980 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto;
        }
        
        .wallet-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(38, 208, 206, 0.5);
            border: 2px solid #26d0ce;
        }

        .card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            margin: 10px 0;
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
            flex: 1;
            min-width: 250px;
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

        .wallet-address {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 1.1rem;
            text-align: center;
            margin: 20px auto;
            width: fit-content;
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

    # Wallet connection logic
    if "wallet_connected" not in st.session_state:
        st.session_state["wallet_connected"] = False

    wallet_address = st.text_input("Enter Wallet Address", value="", key="wallet_address_input")
    
    if st.button("Connect Wallet", key="connect_wallet_button"):
        if wallet_address:
            st.session_state["wallet_connected"] = True
            st.session_state["wallet_address"] = wallet_address
            st.experimental_rerun()
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

    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 20px; margin-top: 50px; color: white;">
            <p>© 2023 Cryptonian. All rights reserved.</p>
            <p><i class="fas fa-envelope"></i> info@cryptonian.com | <i class="fas fa-phone"></i> +91 123 456 7890</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
