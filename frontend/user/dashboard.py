import streamlit as st
import time

def set_style():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #000000, #1a1a2e);
        }
        
        .neo-container {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(0, 128, 255, 0.2);
            box-shadow: 0 4px 15px rgba(0, 128, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .neo-container:hover {
            box-shadow: 0 0 25px rgba(0, 128, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #00f, #0ff);
            height: 8px;
            border-radius: 4px;
            transition: width 1s ease;
            box-shadow: 0 0 10px rgba(0, 128, 255, 0.5);
        }
        
        .achievement {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(0, 128, 255, 0.3);
            transition: all 0.3s;
        }
        
        .achievement:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(38, 208, 206, 0.2);
            border: 1px solid #26d0ce;
        }
        
        .badge {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(45deg, #000, #1a1a2e);
            border: 2px solid #0ff;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px auto;
            font-size: 20px;
            color: #0ff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }
        
        .certificate {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(0, 128, 255, 0.2);
            transition: all 0.3s;
        }
        
        .certificate:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(38, 208, 206, 0.2);
            border: 1px solid #26d0ce;
        }
        
        .stats-value {
            font-size: 24px;
            color: #0ff;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard(wallet_address):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Progress Section
        with st.container():
            st.markdown('<div>', unsafe_allow_html=True)
            st.subheader("Your Progress")
            st.markdown('<div class="stats-value">15</div>Lessons Complete', unsafe_allow_html=True)
            st.markdown('<div class="stats-value">8</div>Games Won', unsafe_allow_html=True)
            st.markdown('<div class="stats-value">3</div>NFTs Earned', unsafe_allow_html=True)
            
        
        # Achievements Section
        st.markdown('<div>', unsafe_allow_html=True)
        st.subheader("Achievements")
        cols = st.columns(2)
        achievements = [
            {"name": "Web3 Novice", "progress": "100%", "desc": "Completed first Web3 lesson"},
            {"name": "Geography Explorer", "progress": "60%", "desc": "Visit 5 monuments"},
            {"name": "History Master", "progress": "40%", "desc": "Complete all history lessons"},
            {"name": "NFT Collector", "progress": "40%", "desc": "Collect 5 NFTs"}
        ]
        for idx, ach in enumerate(achievements):
            with cols[idx % 2]:
                st.markdown(f'''
                    <div class="achievement">
                        <div class="badge">{ach["progress"]}</div>
                        <h4>{ach["name"]}</h4>
                        <p>{ach["desc"]}</p>
                    </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Certificates Section
        st.markdown('<div >', unsafe_allow_html=True)
        st.subheader("Certificates")
        certificates = [
            {"name": "Web3 Fundamentals", "status": "Completed", "action": "Mint Certificate"},
            {"name": "Geography Explorer", "status": "In Progress", "action": "Download"},
            {"name": "History Scholar", "status": "65% Complete", "action": None}
        ]
        for cert in certificates:
            st.markdown(f'''
                <div class="certificate">
                    <h4>{cert["name"]}</h4>
                    <p>{cert["status"]}</p>
                    {f'<button>{cert["action"]}</button>' if cert["action"] else ''}
                </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def app(wallet_address):
    set_style()
    render_dashboard(wallet_address)
