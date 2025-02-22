import streamlit as st
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

# Load API key from config or environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(topic):
    prompt = f"""
    Generate a 3-question multiple-choice quiz about {topic}.
    Format: JSON list with each question having 'question', 'options' (4 choices), and 'answer' (correct answer index).
    Example:
    [
        {{
            "question": "What is blockchain?",
            "options": ["A ledger", "A database", "A token", "A miner"],
            "answer": 0
        }},
        ...
    ]
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    try:
        quiz_data = json.loads(response.text)
        return quiz_data
    except json.JSONDecodeError:
        st.error("Failed to generate quiz. Try again later.")
        return []

def run_quiz(topic):
    # Initialize quiz data and answers list
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = generate_quiz(topic)
    
    # Create answers list for storing selections
    answers = [None] * len(st.session_state.quiz_data)
    
    st.write(f"## Quiz on {topic}")
    
    # Display questions and collect answers
    for i, question in enumerate(st.session_state.quiz_data):
        st.write(f"\n**Question {i+1}:** {question['question']}")
        
        # Radio button for each question
        selected = st.radio(
            "Choose your answer:",
            options=question['options'],
            key=f"q_{i}",
            index=None
        )
        
        # Store the answer index if an option is selected
        if selected:
            answers[i] = question['options'].index(selected)

    # Submit button
    if st.button("Submit Quiz"):
        if None in answers:
            st.warning("Please answer all questions before submitting.")
            return
            
        score = 0
        for i, question in enumerate(st.session_state.quiz_data):
            if answers[i] == question['answer']:
                score += 1
                
        st.write("---")
        st.write("## Quiz Results")
        st.write(f"Your score: {score} out of {len(st.session_state.quiz_data)}")
        
        # Show correct/incorrect answers
        for i, question in enumerate(st.session_state.quiz_data):
            st.write(f"\n**Question {i+1}:** {question['question']}")
            user_answer = question['options'][answers[i]]
            correct_answer = question['options'][question['answer']]
            
            if answers[i] == question['answer']:
                st.success(f"✓ Your answer: {user_answer} (Correct!)")
            else:
                st.error(f"✗ Your answer: {user_answer}")
                st.info(f"Correct answer: {correct_answer}")

        # Reset button
        if st.button("Take New Quiz"):
            st.session_state.clear()
            st.experimental_rerun()