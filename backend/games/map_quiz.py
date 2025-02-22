import streamlit as st
import random
import os
from PIL import Image
from datetime import datetime

# Custom CSS with Streamlit
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main Container */
    .stApp {
        background: linear-gradient(to bottom right, #1a1a1a, #2d2d2d);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Title */
    .st-emotion-cache-1629p8f h1 {
        color: white;
        text-align: center;
        padding: 2rem 0;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    /* Radio Buttons Container */
    .st-emotion-cache-1dm5gw7 {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 20px 0;
    }
    
    /* Radio Button Labels */
    .st-emotion-cache-1dm5gw7 label {
        color: white !important;
        font-size: 1.1rem;
        margin: 10px 0;
        transition: all 0.3s ease;
        padding: 10px;
        border-radius: 8px;
    }
    
    .st-emotion-cache-1dm5gw7 label:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    /* Buttons */
    .stButton button {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        color: white !important;
        border: none !important;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
    }
    
    .stButton button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Score Display */
    h3 {
        color: white !important;
        font-size: 1.5rem !important;
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(4px);
    }
    
    /* Image Container */
    .st-emotion-cache-1v0mbdj {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease;
    }
    
    .st-emotion-cache-1v0mbdj:hover {
        transform: scale(1.02);
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    .stSuccess {
        background: rgba(40, 167, 69, 0.2);
        border: 1px solid rgba(40, 167, 69, 0.3);
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.2);
        border: 1px solid rgba(220, 53, 69, 0.3);
    }
    
    /* Custom Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Game Controls */
    .st-emotion-cache-14rvwmd {
        display: flex;
        gap: 10px;
    }
    
    /* Make text white */
    .st-emotion-cache-10trblm {
        color: white !important;
    }
    
    div[data-testid="stImage"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .stRadio > div[role="radiogroup"] > label > div:first-of-type {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Caption styling */
    .st-emotion-cache-1t4vedx {
        color: rgba(255, 255, 255, 0.7) !important;
        text-align: center;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

def get_states():
    state_images = os.listdir("assets/state")
    state_names = [img.replace(".png", "").replace("_", " ") for img in state_images]
    return list(zip(state_images, state_names))

def random_state(state_list, used_states):
    available_states = [state for state in state_list if state[1] not in used_states]
    if not available_states:
        return None, None
    return random.choice(available_states)

def update_activity_progress(wallet_address, activity_name, activity_type, progress, total, additional_data=None):
    # Placeholder function to simulate updating activity progress
    st.success(f"Activity progress updated for {wallet_address}: {activity_name}")

def resize_image(image, width):
    # Resize the image while maintaining aspect ratio
    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio)
    return image.resize((width, new_height))

def app(wallet_address):
    st.title("🎯 Guess the Indian State!")
    
    # Initialize session state
    if "used_states" not in st.session_state:
        st.session_state.used_states = set()
        st.session_state.score = 0
        st.session_state.difficulty = "Easy"
        st.session_state.game_started = False
        st.session_state.piece_collection = []

    # Difficulty level slider
    difficulty_level = st.select_slider("Select Difficulty Level", options=["Easy", "Medium", "Hard"], value=st.session_state.difficulty)
    st.session_state.difficulty = difficulty_level

    # Determine the number of states to guess based on difficulty
    if difficulty_level == "Easy":
        num_states = 5
    elif difficulty_level == "Medium":
        num_states = 10
    else:
        num_states = 15

    states = get_states()
    selected_image, selected_name = random_state(states, st.session_state.used_states)
    
    # Game Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 New Game", use_container_width=True):
            st.session_state.used_states.clear()
            st.session_state.score = 0
            st.session_state.game_started = True
            st.session_state.piece_collection = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.used_states.clear()
            st.session_state.score = 0
            st.session_state.game_started = False
            st.session_state.piece_collection = []
            st.rerun()

    with col3:
        if st.button("💾 Save Game", use_container_width=True):
            if st.session_state.game_started and len(st.session_state.piece_collection) > 0:
                saved_game = {
                    'board': st.session_state.used_states.copy(),
                    'collection': st.session_state.piece_collection.copy(),
                    'theme': difficulty_level,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address, 
                    'map quiz',  
                    3, 
                    len(st.session_state.piece_collection), 
                    num_states,
                    additional_data=saved_game
                )
                st.success("Game saved successfully!")
            else:
                st.warning("No active game to save!")

    if selected_image is None:
        st.session_state.used_states.clear()
        selected_image, selected_name = random_state(states, st.session_state.used_states)
    
    st.session_state.used_states.add(selected_name)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        image = Image.open(f"assets/state/{selected_image}")
        resized_image = resize_image(image, 4375)  # Resize image to 4375 width
        st.image(resized_image, caption="Can you identify this state?", use_container_width=True)
    
    with col2:
        st.markdown("### Choose your answer:")
        options = random.sample([state[1] for state in states if state[1] != selected_name], 4)
        options.append(selected_name)
        random.shuffle(options)
        
        choice = st.radio("", options, index=None)
        
        if st.button("🎯 Submit Answer"):
            if choice == selected_name:
                st.success(f"🎉 Correct! It's {selected_name}!")
                st.session_state.score += 10
                st.session_state.piece_collection.append(selected_name)
            else:
                st.error(f"❌ Incorrect! The correct answer was {selected_name}.")
    
    st.markdown(f"### 🏆 Score: {st.session_state.score}")

    # Check if the game is over
    if len(st.session_state.used_states) >= num_states:
        st.success(f"🎉 Congratulations! You've completed the {difficulty_level} level with a score of {st.session_state.score}!")
        st.session_state.game_started = False
