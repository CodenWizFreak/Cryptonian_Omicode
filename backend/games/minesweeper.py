# -----------------------------------------------------------------------------
# Game 2: Minesweeper
# -----------------------------------------------------------------------------

import streamlit as st
import random 
from datetime import datetime
import time
from backend.games.console import *


def app(wallet_address):
    """Minesweeper Game Implementation"""
    st.title("💣 Minesweeper")
    
    # Difficulty selection with visual indicators
    st.markdown("""
    <style>
    .difficulty-selector {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .difficulty-option {
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .difficulty-option:hover {
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    difficulty = st.select_slider(
        "Select Difficulty",
        options=["Easy", "Medium", "Hard"],
        value="Medium",
        help="Adjusts board size and number of mines"
    )
    
    difficulty_settings = {
        "Easy": {"size": 5, "mines": 5, "color": "#4CAF50"},
        "Medium": {"size": 6, "mines": 10, "color": "#FFC107"},
        "Hard": {"size": 7, "mines": 15, "color": "#F44336"}
    }
    
    # Initialize session state
    if 'board' not in st.session_state:
        st.session_state.board = None
        st.session_state.mines = None
        st.session_state.game_over = False
        st.session_state.game_won = False
        st.session_state.revealed = None
        st.session_state.flags = None
        st.session_state.moves = 0
        st.session_state.start_time = None
        st.session_state.powerups = 3

    def create_board(settings):
        """Create minesweeper board with given settings"""
        size = settings["size"]
        num_mines = settings["mines"]
        board = [[0 for _ in range(size)] for _ in range(size)]
        mines = set()
        
        while len(mines) < num_mines:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if (x, y) not in mines:
                board[x][y] = -1
                mines.add((x, y))
        
        for x in range(size):
            for y in range(size):
                if board[x][y] != -1:
                    board[x][y] = count_adjacent_mines(board, x, y)
        
        return board, mines

    def count_adjacent_mines(board, x, y):
        """Count mines in adjacent cells"""
        mines_count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board):
                    if board[nx][ny] == -1:
                        mines_count += 1
        return mines_count

    def reveal_cell(x, y, board, revealed):
        """Recursively reveal cells"""
        if not (0 <= x < len(board) and 0 <= y < len(board)) or revealed[x][y]:
            return
        
        revealed[x][y] = True
        if board[x][y] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    reveal_cell(x + dx, y + dy, board, revealed)

    # Game controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("🎮 New Game", use_container_width=True):
            settings = difficulty_settings[difficulty]
            st.session_state.board, st.session_state.mines = create_board(settings)
            st.session_state.revealed = [[False for _ in range(settings["size"])] 
                                       for _ in range(settings["size"])]
            st.session_state.flags = [[False for _ in range(settings["size"])] 
                                    for _ in range(settings["size"])]
            st.session_state.game_over = False
            st.session_state.game_won = False
            st.session_state.moves = 0
            st.session_state.start_time = time.time()
            st.session_state.powerups = 3

    # Display game stats
    with col2:
        if st.session_state.board:
            elapsed_time = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
            st.markdown(f"""
            <div style="text-align: center;">
                <p>⏱️ Time: {elapsed_time//60}m {elapsed_time%60}s</p>
                <p>🎯 Moves: {st.session_state.moves}</p>
                <p>💪 Powerups: {st.session_state.powerups}</p>
            </div>
            """, unsafe_allow_html=True)

    # Game board
    if st.session_state.board:
        st.markdown("""
        <style>
        .minesweeper-cell {
            width: 40px;
            height: 40px;
            margin: 2px;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .mine { background-color: #ff4444 !important; }
        .revealed { background-color: #e6f3ff; }
        .hidden { background-color: #f0f0f0; }
        .minesweeper-cell:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        settings = difficulty_settings[difficulty]
        for x in range(settings["size"]):
            cols = st.columns(settings["size"])
            for y in range(settings["size"]):
                with cols[y]:
                    cell_value = st.session_state.board[x][y]
                    is_revealed = st.session_state.revealed[x][y]
                    is_flagged = st.session_state.flags[x][y]
                    
                    if st.session_state.game_over and cell_value == -1:
                        st.markdown(f"""
                        <div class="minesweeper-cell mine">
                            {MINE_SVG}
                        </div>
                        """, unsafe_allow_html=True)
                    elif is_revealed:
                        color = "#1e88e5" if cell_value > 0 else "#4caf50"
                        st.markdown(f"""
                        <div class="minesweeper-cell revealed" 
                             style="color: {color};">
                            {cell_value if cell_value > 0 else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    elif is_flagged:
                        if st.button('🚩', key=f'flag_{x}_{y}'):
                            st.session_state.flags[x][y] = False
                    else:
                        if st.button('?', key=f'{x}_{y}'):
                            if not st.session_state.game_over and not st.session_state.game_won:
                                st.session_state.moves += 1
                                if cell_value == -1:
                                    st.session_state.game_over = True
                                    st.error("💥 BOOM! Game Over!")
                                else:
                                    reveal_cell(x, y, st.session_state.board, st.session_state.revealed)
                                    revealed_cells = sum(row.count(True) for row in st.session_state.revealed)
                                    update_activity_progress(wallet_address, 'Minesweeper', 2, 
                                                          revealed_cells, settings["size"]**2)
                                    
                                    # Check win condition
                                    safe_cells = settings["size"]**2 - len(st.session_state.mines)
                                    if revealed_cells == safe_cells:
                                        st.session_state.game_won = True
                                        game_time = int(time.time() - st.session_state.start_time)
                                        st.markdown(f"""
                                        <div style="text-align: center; animation: victory 1s infinite;">
                                            🎊 Congratulations! You've won! 🎊<br>
                                            Time: {game_time//60}m {game_time%60}s
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.balloons()
                                        
                                        # Achievement checks
                                        if game_time < 60:
                                            update_achievement(wallet_address, 'speed_demon')
                                        # If no flags are placed (i.e. flags remain False)
                                        if not any(any(row) for row in st.session_state.flags):
                                            update_achievement(wallet_address, 'expert')
                                        update_activity_progress(wallet_address, 'Minesweeper', 1, 1, 1)