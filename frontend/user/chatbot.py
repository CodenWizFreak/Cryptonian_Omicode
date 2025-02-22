import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Load API Key (set this in your environment variables for security)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Google AI Studio API key is missing. Set it as an environment variable.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Function to get chatbot response
def get_chat_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")

        # Stronger context about the chatbot's role
        prompt = (
            "You are the official AI assistant of Cryptonian, a gamified Web3 learning platform. "
            "Your job is to help users understand Web3 concepts, blockchain, cryptocurrencies, smart contracts, "
            "Indian history, and geography as taught in the app. "
            "Give answers that are pretty short, short bullets if needed, prefer one sentence answers."
            "Only provide answers relevant to Cryptonian’s topics and avoid unrelated discussions.\n\n"
            f"User: {user_input}\n"
            "AI:"
        )

        response = model.generate_content(prompt)
        return response.text if response else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"

    try:
        model = genai.GenerativeModel("gemini-pro")
        
        # Customizing the prompt
        prompt = (
            "You are Cryptonian AI, a helpful Web3 learning assistant. "
            "Provide clear, informative, and engaging responses. "
            "Keep explanations concise and beginner-friendly.\n\n"
            f"User: {user_input}\n"
            "AI:"
        )
        
        response = model.generate_content(prompt)  # Using modified prompt
        return response.text if response else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"


# Chatbot UI function
def chatbot_ui():
    st.sidebar.subheader("💬 Cryptonian Chatbot")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display chat history
    for chat in st.session_state["chat_history"]:
        with st.sidebar:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Bot:** {chat['bot']}")

    # User input
    user_input = st.sidebar.text_input("Ask me anything:", key="chat_input")
    
    if st.sidebar.button("Send"):
        if user_input:
            bot_response = get_chat_response(user_input)
            st.session_state["chat_history"].append({"user": user_input, "bot": bot_response})
            
            st.rerun()
            st.session_state["chat_input"] = ""
