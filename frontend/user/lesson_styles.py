import streamlit as st

def local_css():
    st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: white;
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
        min-height: 200px;
        cursor: pointer;
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
    
    .progress-bar {
        height: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .progress {
        height: 100%;
        background: linear-gradient(45deg, #26d0ce, #1a2980);
        border-radius: 5px;
    }
    
    .back-button {
        color: white;
        text-decoration: none;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .certificate {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    
    .phase-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .quiz-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)