import streamlit as st
import random
from PIL import Image
import os
from datetime import datetime
from backend.games.console import *  # Import the same backend functions as other games

# Achievement definitions matching other games
ACHIEVEMENTS = {
    'artifact_assembler': {
        'master_curator': {'name': '🏛️ Master Curator', 'desc': 'Complete all artifacts on hard mode', 'threshold': 3},
        'speed_assembler': {'name': '⚡ Speed Assembler', 'desc': 'Complete puzzle under 2 minutes', 'threshold': 120},
        'perfectionist': {'name': '✨ Perfect Assembly', 'desc': 'Complete 3 puzzles without mistakes', 'threshold': 3}
    }
}

def load_puzzle_images():
    return [
        ("Taj Mahal", "assets/artifact_images/taj_mahal.jpeg"),
        ("Konark Sun Temple", "assets/artifact_images/konark_temple.jpeg"),
        ("Qutub Minar", "assets/artifact_images/qutub_minar.jpeg")
    ]

def scramble_image(image_path, grid_size=3):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    new_height = int(360 * aspect_ratio)
    
    image = img.resize((360, new_height), Image.LANCZOS)
    min_dim = min(image.size)
    left = (image.size[0] - min_dim) // 2
    top = (image.size[1] - min_dim) // 2
    image = image.crop((left, top, left + min_dim, top + min_dim))
    
    image = image.resize((600, 600))
    width, height = image.size
    piece_width = width // grid_size
    piece_height = height // grid_size
    
    pieces = []
    for i in range(grid_size):
        for j in range(grid_size):
            piece = image.crop((j * piece_width, i * piece_height, 
                              (j + 1) * piece_width, (i + 1) * piece_height))
            pieces.append(piece)
    random.shuffle(pieces)
    return pieces, (piece_width, piece_height)

def app(wallet_address):
    st.title("🧩 Artifact Assembler: Piece it Together!")
    st.write("Reassemble the artifact by arranging the pieces in the correct order!")
    
    # Initialize session state
    if "assembler_state" not in st.session_state:
        st.session_state.assembler_state = {
            'completed_puzzles': [],
            'current_puzzle': None,
            'attempts': 0,
            'game_started': False,
            'start_time': None,
            'mistakes': 0,
            'perfect_assemblies': 0
        }
    
    # Game Controls matching other games
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 New Puzzle", use_container_width=True):
            if st.session_state.assembler_state['game_started'] and st.session_state.assembler_state['current_puzzle']:
                saved_game = {
                    'artifact': st.session_state.assembler_state['current_puzzle'],
                    'attempts': st.session_state.assembler_state['attempts'],
                    'completed': len(st.session_state.assembler_state['completed_puzzles']),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address,
                    'Artifact Assembler',
                    5,  # Activity type 5 for artifact assembler
                    len(st.session_state.assembler_state['completed_puzzles']),
                    3,  # Target number of artifacts
                    additional_data=saved_game
                )
                st.success("Current progress saved! Starting new puzzle...")
            
            st.session_state.assembler_state['current_puzzle'] = None
            st.session_state.assembler_state['attempts'] = 0
            st.session_state.assembler_state['game_started'] = True
            st.session_state.assembler_state['start_time'] = datetime.now()
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Progress", use_container_width=True):
            st.session_state.assembler_state = {
                'completed_puzzles': [],
                'current_puzzle': None,
                'attempts': 0,
                'game_started': False,
                'start_time': None,
                'mistakes': 0,
                'perfect_assemblies': 0
            }
            st.rerun()

    with col3:
        if st.button("💾 Save Progress", use_container_width=True):
            if st.session_state.assembler_state['game_started'] and st.session_state.assembler_state['current_puzzle']:
                saved_game = {
                    'artifact': st.session_state.assembler_state['current_puzzle'],
                    'attempts': st.session_state.assembler_state['attempts'],
                    'completed': len(st.session_state.assembler_state['completed_puzzles']),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address,
                    'Artifact Assembler',
                    5,
                    len(st.session_state.assembler_state['completed_puzzles']),
                    3,
                    additional_data=saved_game
                )
                st.success("Progress saved successfully!")
            else:
                st.warning("No active puzzle to save!")

    # Progress tracking
    st.markdown("### 🎯 Assembly Progress")
    progress = len(st.session_state.assembler_state['completed_puzzles']) / 3  # Progress towards completing all artifacts
    st.progress(progress)
    
    if st.session_state.assembler_state['start_time']:
        elapsed_time = (datetime.now() - st.session_state.assembler_state['start_time']).seconds
        st.markdown(f"⏱️ Time: {elapsed_time//60}m {elapsed_time%60}s")
    
    # Main game interface
    artifacts = load_puzzle_images()
    col1, col2 = st.columns(2)
    
    with col1:
        selected_artifact = st.selectbox("Choose an artifact:", 
                                      [name for name, _ in artifacts])
        grid_size = st.selectbox("Select difficulty:", 
                               [2, 3, 4], 
                               index=1,
                               help="2: Easy, 3: Medium, 4: Hard")
    
    artifact_image = next(path for name, path in artifacts if name == selected_artifact)
    pieces, (pw, ph) = scramble_image(artifact_image, grid_size)
    
    st.session_state.assembler_state['current_puzzle'] = {
        'name': selected_artifact,
        'difficulty': grid_size,
        'started_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Game area
    game_area_col1, game_area_col2 = st.columns(2)
    
    # Scrambled pieces
    with game_area_col1:
        st.write("#### Scrambled Pieces")
        rows = (len(pieces) + 1) // 2
        
        for i in range(rows):
            cols = st.columns(2)
            for j in range(2):
                idx = i * 2 + j
                if idx < len(pieces):
                    cols[j].markdown(f"<p style='text-align: center;'>Piece {idx+1}</p>", 
                                  unsafe_allow_html=True)
                    cols[j].image(pieces[idx], use_container_width=True)
    
    # Placement grid
    with game_area_col2:
        st.write("#### Arrange Pieces Here")
        user_order = []
        for i in range(grid_size):
            cols = st.columns(grid_size)
            for j in range(grid_size):
                idx = i * grid_size + j
                with cols[j]:
                    piece_num = st.selectbox(f"Position {idx+1}", 
                                           list(range(1, len(pieces) + 1)),
                                           key=f"piece_{idx}")
                    user_order.append(piece_num - 1)
    
    # Check solution
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Check Assembly", use_container_width=True):
            st.session_state.assembler_state['attempts'] += 1
            correct_order = list(range(len(pieces)))
            
            if user_order == correct_order:
                st.success("🎉 Correct! You've assembled the artifact!")
                completion_time = int((datetime.now() - st.session_state.assembler_state['start_time']).total_seconds())
                
                # Record completion
                completion_data = {
                    'artifact': selected_artifact,
                    'difficulty': grid_size,
                    'attempts': st.session_state.assembler_state['attempts'],
                    'time': completion_time,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if completion_data not in st.session_state.assembler_state['completed_puzzles']:
                    st.session_state.assembler_state['completed_puzzles'].append(completion_data)
                
                # Check achievements
                if completion_time < 120:
                    update_achievement(wallet_address, 'speed_assembler')
                if st.session_state.assembler_state['attempts'] == 1:
                    st.session_state.assembler_state['perfect_assemblies'] += 1
                    if st.session_state.assembler_state['perfect_assemblies'] >= 3:
                        update_achievement(wallet_address, 'perfectionist')
                if grid_size == 4 and len(st.session_state.assembler_state['completed_puzzles']) >= 3:
                    update_achievement(wallet_address, 'master_curator')
                
                # Update database
                update_activity_progress(
                    wallet_address,
                    'Artifact Assembler',
                    5,
                    len(st.session_state.assembler_state['completed_puzzles']),
                    3,
                    additional_data=completion_data
                )
                
                st.write(f"About the {selected_artifact}: This is a historical marvel of India!")
            else:
                st.error("❌ Incorrect! Try again.")
                st.session_state.assembler_state['mistakes'] += 1