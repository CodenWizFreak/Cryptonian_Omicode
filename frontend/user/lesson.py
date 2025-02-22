import streamlit as st
from datetime import datetime
from database.db import * # Import the MongoDB connection function
from backend.lessons.web3 import web3_lesson
from backend.lessons.history import history_lesson
from backend.lessons.geography import geography_lesson
from frontend.user.lesson_styles import local_css

def save_lesson_progress(wallet_address, lesson_name, progress):
    db = connect_db()
    data = {
        "wallet_address": wallet_address,
        "lesson_name": lesson_name,
        "progress": progress,
        "timestamp": datetime.now()
    }
    db.lessons.insert_one(data)
    st.success("Lesson progress saved successfully!")

def app(wallet_address):
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
    
    st.title("Lessons")

    lesson_options = {
        "Web3": web3_lesson,
        "History": history_lesson,
        "Geography": geography_lesson
    }

    lesson_choice = st.selectbox("Select a Lesson", list(lesson_options.keys()))

    if lesson_choice in lesson_options:
        lesson_options[lesson_choice]()  # Call the appropriate lesson function
        
        progress = st.slider("Progress (%)", 0, 100, 100)  # Default to 100% after completion
        
        if st.button("Mark as Completed"):
            save_lesson_progress(wallet_address, lesson_choice.lower(), progress)