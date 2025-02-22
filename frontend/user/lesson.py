# main.py
import streamlit as st
from frontend.user.lesson_styles import local_css
import streamlit.components.v1 as components

def app():
    local_css()
    
    # Load Font Awesome
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)
    
    # Display header and cards
    st.markdown("""
        <div class="header-container">
            <h1>Certified Learning Track</h1>
            <p class="subtitle">Deep dive into leading ecosystems and become a certified learner</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display cards in columns
    cols = st.columns(3)
    
    courses = [
        {"key": "web3", "title": "Web3 Basics", "icon": "fas fa-cube"},
        {"key": "geography", "title": "Indian Geography", "icon": "fas fa-mountain"},
        {"key": "history", "title": "Indian History", "icon": "fas fa-landmark"}
    ]
    
    for i, course in enumerate(courses):
        with cols[i]:
            st.markdown(f"""
            <div class='card'>
                <i class='{course["icon"]} feature-icon'></i>
                <h3>{course["title"]}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Add dropdown for course selection
    st.markdown("<br>", unsafe_allow_html=True)
    course_options = {
        "Select a course": None,
        "Web3 Basics": "web3",
        "Indian Geography": "geography",
        "Indian History": "history"
    }
    
    selected_course = st.selectbox(
        "Choose your course",
        options=list(course_options.keys()),
        format_func=lambda x: x
    )
    
    # Display selected course content
    if selected_course != "Select a course":
        course_key = course_options[selected_course]
        
        # Navigation tabs for course phases
        if course_key == "web3":
            phases = ["Introduction", "Smart Contracts", "DeFi & NFTs"]
            current_phase = st.tabs(phases)
            
            # Phase 1
            with current_phase[0]:
                st.markdown("### Introduction to Blockchain")
                st.write("""
                Blockchain is a distributed ledger technology that enables secure, transparent, 
                and immutable record-keeping. Let's explore the key concepts.
                """)
                with st.expander("Key Concepts"):
                    st.write("""
                    1. Decentralization
                    2. Consensus Mechanisms
                    3. Cryptography
                    4. Smart Contracts
                    """)
                if st.button("Take Quiz - Phase 1"):
                    st.info("Quiz functionality to be implemented")
            
            # Phase 2
            with current_phase[1]:
                st.markdown("### Smart Contracts & DApps")
                st.write("""
                Learn about self-executing contracts and decentralized applications.
                """)
                with st.expander("Topics Covered"):
                    st.write("""
                    - Solidity Programming
                    - Web3.js Integration
                    - DApp Architecture
                    - Testing and Deployment
                    """)
                if st.button("Take Quiz - Phase 2"):
                    st.info("Quiz functionality to be implemented")
            
            # Phase 3
            with current_phase[2]:
                st.markdown("### DeFi & NFTs")
                st.write("""
                Explore decentralized finance and non-fungible tokens.
                """)
                with st.expander("Key Topics"):
                    st.write("""
                    - Lending/Borrowing Protocols
                    - Yield Farming
                    - NFT Standards
                    - Token Economics
                    """)
                if st.button("Take Quiz - Phase 3"):
                    st.info("Quiz functionality to be implemented")
        
        elif course_key == "geography":
            phases = ["Physical Geography", "Climate", "Resources"]
            current_phase = st.tabs(phases)
            
            with current_phase[0]:
                st.markdown("### Physical Geography of India")
                st.write("""
                Explore India's diverse landscape and physiographic divisions.
                """)
                # Add content similar to web3 structure
            
            # Add other phases similarly
        
        elif course_key == "history":
            phases = ["Ancient India", "Medieval India", "Modern India"]
            current_phase = st.tabs(phases)
            
            with current_phase[0]:
                st.markdown("### Ancient Indian Civilization")
                st.write("""
                Journey through the rich history of ancient India.
                """)
                # Add content similar to web3 structure
            
            # Add other phases similarly
