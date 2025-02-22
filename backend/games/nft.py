# -----------------------------------------------------------------------------
# Game 1: Puzzle NFT Game
# -----------------------------------------------------------------------------
import streamlit as st
import random 
from datetime import datetime
import time
from backend.games.console import *

# Theme colors
THEME_COLORS = {
    "Classic": {"primary": "#4ECDC4", "secondary": "#FF6B6B", "accent": "#FFD93D"},
    "Space": {"primary": "#2C3E50", "secondary": "#8E44AD", "accent": "#F1C40F"},
    "Fantasy": {"primary": "#2ECC71", "secondary": "#E74C3C", "accent": "#F39C12"},
    "Cyberpunk": {"primary": "#FF006E", "secondary": "#3A86FF", "accent": "#FFBE0B"}
}

# Achievements
ACHIEVEMENTS = {
    'puzzle': {
        'collector': {'name': '🎨 Master Collector', 'desc': 'Collect all rare pieces', 'threshold': 3},
        'speedster': {'name': '⚡ Speed Solver', 'desc': 'Complete puzzle under 2 minutes', 'threshold': 120},
        'perfectionist': {'name': '✨ Perfectionist', 'desc': 'Complete 3 puzzles', 'threshold': 3}
    }
}

def app(wallet_address):
    """Puzzle NFT Game Implementation with save/reset functionality"""
    st.title("🧩 Puzzle NFT Game")
    
    # Theme selection
    theme = st.selectbox("🎨 Select Theme", 
                        ["Classic", "Space", "Fantasy", "Cyberpunk"],
                        help="Different themes affect piece rarity and special effects!")
    
    # Initialize session state
    if 'puzzle_board' not in st.session_state:
        st.session_state.puzzle_board = [0] * 9
        st.session_state.piece_collection = []
        st.session_state.game_started = False
        st.session_state.start_time = None
        st.session_state.saved_games = []
    
    # Game Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 New Game", use_container_width=True):
            # Save current game if it exists
            if st.session_state.game_started and len(st.session_state.piece_collection) > 0:
                saved_game = {
                    'board': st.session_state.puzzle_board.copy(),
                    'collection': st.session_state.piece_collection.copy(),
                    'theme': theme,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address, 
                    'Puzzle NFT Game', 
                    2,  # Save game activity type
                    len(st.session_state.piece_collection), 
                    9
                )
                st.success("Current game saved! Starting new game...")
            
            # Reset game state
            st.session_state.puzzle_board = [0] * 9
            st.session_state.piece_collection = []
            st.session_state.game_started = False
            st.session_state.start_time = None
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Board", use_container_width=True):
            st.session_state.puzzle_board = [0] * 9
            st.rerun()

    with col3:
        if st.button("💾 Save Game", use_container_width=True):
            if st.session_state.game_started and len(st.session_state.piece_collection) > 0:
                saved_game = {
                    'board': st.session_state.puzzle_board.copy(),
                    'collection': st.session_state.piece_collection.copy(),
                    'theme': theme,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address, 
                    'Puzzle NFT Game', 
                    2,  # Save game activity type
                    len(st.session_state.piece_collection), 
                    9,
                    additional_data=saved_game
                )
                st.success("Game saved successfully!")
            else:
                st.warning("No active game to save!")
    
    def get_special_effect(rarity, theme):
        effects = {
            'Classic': ['Sparkle', 'Glow', 'Rainbow'],
            'Space': ['Nebula', 'Stardust', 'Black Hole'],
            'Fantasy': ['Magic Aura', 'Dragon\'s Breath', 'Fairy Dust'],
            'Cyberpunk': ['Neon Pulse', 'Digital Glitch', 'Matrix Code']
        }
        return random.choice(effects[theme])
    
    def mint_puzzle_piece():
        if len(st.session_state.piece_collection) < 9:
            piece_type = random.randint(1, 9)
            rarity = random.randint(1, 100)
            special_effect = get_special_effect(rarity, theme)
            
            while piece_type in [p['type'] for p in st.session_state.piece_collection]:
                piece_type = random.randint(1, 9)
            
            piece = {
                'type': piece_type,
                'rarity': rarity,
                'effect': special_effect,
                'theme': theme,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.piece_collection.append(piece)
            
            if rarity > 90:
                st.balloons()
                st.markdown(f"""
                <div class='legendary-piece' style='text-align: center; animation: pulse 2s infinite;'>
                    🌟 LEGENDARY {theme.upper()} PIECE MINTED! 🌟<br>
                    Special Effect: {special_effect}
                </div>
                """, unsafe_allow_html=True)
            elif rarity > 70:
                st.snow()
                st.info(f"✨ Rare {theme} piece minted! Effect: {special_effect}")
            else:
                st.success(f"New {theme} piece minted! Effect: {special_effect}")
            
            update_activity_progress(wallet_address, 'Puzzle NFT Game', 1, 
                                  len(st.session_state.piece_collection), 9)
        else:
            st.warning("Maximum pieces collected! Place them to complete the puzzle.")
    
    # Game Interface
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### 🎲 Mint New Pieces")
        if st.button("Mint Piece", use_container_width=True):
            mint_puzzle_piece()
            if not st.session_state.game_started:
                st.session_state.game_started = True
                st.session_state.start_time = time.time()
    
    with col2:
        st.markdown("### 🎯 Progress")
        progress = len([x for x in st.session_state.puzzle_board if x != 0]) / 9
        st.progress(progress)
        if st.session_state.start_time:
            elapsed_time = int(time.time() - st.session_state.start_time)
            st.markdown(f"⏱️ Time: {elapsed_time//60}m {elapsed_time%60}s")
    
    # Collection Display
    st.markdown("### 🗃️ Collection")
    piece_cols = st.columns(3)
    for idx, piece in enumerate(st.session_state.piece_collection):
        with piece_cols[idx % 3]:
            st.markdown(
                create_piece_card(piece, THEME_COLORS[theme]) + 
                create_rarity_animation(piece['rarity']),
                unsafe_allow_html=True
            )
    
    # Game Board
    st.markdown("### 🎮 Puzzle Board")
    board_cols = st.columns(3)
    for i in range(9):
        with board_cols[i % 3]:
            piece_value = st.session_state.puzzle_board[i]
            if piece_value != 0:
                piece = next((p for p in st.session_state.piece_collection if p['type'] == piece_value), None)
                if piece:
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; border: 2px solid #ccc; text-align: center;">
                        <p style="margin: 5px 0;">{piece['effect']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; text-align: center; border: 2px dashed #ccc;">
                    -
                </div>
                """, unsafe_allow_html=True)

    # Place pieces
    st.markdown("### 🎯 Place Pieces")
    place_cols = st.columns(3)
    for idx, piece in enumerate(st.session_state.piece_collection):
        with place_cols[idx % 3]:
            if st.button(f"Place #{piece['type']}", 
                        key=f"place_{piece['type']}", 
                        use_container_width=True):
                if 0 in st.session_state.puzzle_board:
                    empty_index = st.session_state.puzzle_board.index(0)
                    st.session_state.puzzle_board[empty_index] = piece['type']
                    
                    # Check completion
                    if 0 not in st.session_state.puzzle_board:
                        completion_time = int(time.time() - st.session_state.start_time)
                        st.balloons()
                        st.markdown(f"""
                        <div style="text-align: center; animation: victory 1s infinite;">
                            🎊 PUZZLE COMPLETED! 🎊<br>
                            Time: {completion_time//60}m {completion_time%60}s
                        </div>
                        <style>
                        @keyframes victory {{
                            0% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.1); }}
                            100% {{ transform: scale(1); }}
                        }}
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # Achievement checks
                        if completion_time < 120:
                            update_achievement(wallet_address, 'speedster')
                        if all(p['rarity'] > 70 for p in st.session_state.piece_collection):
                            update_achievement(wallet_address, 'collector')
                        
                        update_activity_progress(wallet_address, 'Puzzle NFT Game', 1, 9, 9)
                else:
                    st.warning("No empty spaces left!")


