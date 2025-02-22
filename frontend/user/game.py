import streamlit as st
import random 
from datetime import datetime
import time
from backend.games import minesweeper, monument_scanner, nft, map_quiz, artifact_assembler, timeline_tactician
from backend.games.console import *

# SVG Assets
MINE_SVG = """<svg viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="#FF4444"/>
    <path d="M30,50 L70,50 M50,30 L50,70" stroke="white" stroke-width="8"/>
</svg>"""

FLAG_SVG = """<svg viewBox="0 0 100 100">
    <rect x="45" y="20" width="5" height="60" fill="#333"/>
    <path d="M50,20 L80,35 L50,50" fill="#FF4444"/>
</svg>"""

def local_css():
    st.markdown("""
    <style>
    /* Dropdown styling */
    .stSelectbox > div > div {
        background-color: black !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4A90E2 !important;
    }
    
    .stSelectbox > div > div[aria-selected="true"] {
        background-color: #4A90E2 !important;
    }
    
    /* Game cards styling */
    .game-card {
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
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(38, 208, 206, 0.2);
        border: 1px solid #26d0ce;
    }
    
    .icon-wrapper {
        color: #4A90E2;
        margin-bottom: 10px;
        font-size: 24px;
        text-align: center;
    }
    
    .game-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
        color: white;
    }
    
    .game-description {
        color: white;
        font-size: 14px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def app(wallet_address):
    """Main game selection and display"""
    # Display stats in sidebar
    display_stats(wallet_address)
    
    local_css()
    
    # Load Font Awesome
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)
    
    # Main game header
    st.markdown("<h1 style='text-align: center;'>🎮 Blockchain Games</h1>", unsafe_allow_html=True)
    
    # Create 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        # Monument Scanner
        st.markdown("""
        <div class="game-card">
            <div class="icon-wrapper">
                <i class="fas fa-camera"></i>
            </div>
            <div class="game-title">Monument Scanner</div>
            <div class="game-description">Scan monuments and learn their history</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Map Quiz Challenge
        st.markdown("""
        <div class="game-card">
            <div class="icon-wrapper">
                <i class="fas fa-map"></i>
            </div>
            <div class="game-title">Map Quiz Challenge</div>
            <div class="game-description">Test your knowledge of Indian geography</div>
        </div>
        """, unsafe_allow_html=True)

        # Artifact Assembler
        st.markdown("""
        <div class="game-card">
            <div class="icon-wrapper">
                <i class="fas fa-landmark"></i>
            </div>
            <div class="game-title">Artifact Assembler</div>
            <div class="game-description">Reassemble the artifact correctly!</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # NFT Puzzle
        st.markdown("""
        <div class="game-card">
            <div class="icon-wrapper">
                <i class="fas fa-puzzle-piece"></i>
            </div>
            <div class="game-title">NFT Puzzle</div>
            <div class="game-description">Assemble puzzles to earn unique NFTs</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Minesweeper
        st.markdown("""
        <div class="game-card">
            <div class="icon-wrapper">
                <i class="fas fa-flag"></i>
            </div>
            <div class="game-title">Minesweeper: Indian Edition</div>
            <div class="game-description">Clear the board and answer geography questions</div>
        </div>
        """, unsafe_allow_html=True)

        # Timeline Tactician
        st.markdown("""
        <div class="game-card">
            <div class="icon-wrapper">
                <i class="fas fa-timeline"></i>
            </div>
            <div class="game-title">Timeline Tactician</div>
            <div class="game-description">Arrange the historical events in the correct chronological order!</div>
        </div>
        """, unsafe_allow_html=True)
    
        # Game selection dropdown
    game_choice = st.selectbox(
        "Select your game",
        ["Select your game", "Monument Scanner", "NFT Puzzle", "Map Quiz Challenge", "Minesweeper: Indian Edition", "Artifact Assembler", "Timeline Tactician"],
        index=0
    )
    
    # Game logic based on selection
    if game_choice == "NFT Puzzle":
        nft.app(wallet_address)
    elif game_choice == "Minesweeper: Indian Edition":
        minesweeper.app(wallet_address)
    elif game_choice == "Monument Scanner":
        monument_scanner.app(wallet_address)
    elif game_choice == "Map Quiz Challenge":
        map_quiz.app(wallet_address)
    elif game_choice == "Timeline Tactician":
        timeline_tactician.app(wallet_address)
    elif game_choice == "Artifact Assembler":
        artifact_assembler.app(wallet_address)
