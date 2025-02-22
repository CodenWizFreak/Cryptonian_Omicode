
# -----------------------------------------------------------------------------
# Dummy implementations for update_activity_progress and get_user_progress
# -----------------------------------------------------------------------------

import streamlit as st
import random 
from datetime import datetime
import time

# Achievements
ACHIEVEMENTS = {
    'puzzle': {
        'collector': {'name': '🎨 Master Collector', 'desc': 'Collect all rare pieces', 'threshold': 3},
        'speedster': {'name': '⚡ Speed Solver', 'desc': 'Complete puzzle under 2 minutes', 'threshold': 120},
        'perfectionist': {'name': '✨ Perfectionist', 'desc': 'Complete 3 puzzles', 'threshold': 3}
    },
    'minesweeper': {
        'expert': {'name': '💫 Mine Expert', 'desc': 'Win without any flags', 'threshold': 1},
        'speed_demon': {'name': '🏃 Speed Demon', 'desc': 'Win under 1 minute', 'threshold': 60},
        'survivor': {'name': '🛡️ Survivor', 'desc': 'Win 5 games', 'threshold': 5}
    }
}
def update_activity_progress(wallet_address, game, activity_type, current, total, additional_data=None):
    # Placeholder for updating activity progress.
    # For debugging, you might print or log the progress here.
    # print(f"Updating progress for {wallet_address}: {game} - {activity_type} ({current}/{total})")
    pass

def get_user_progress(wallet_address, game):
    # Placeholder for getting user progress.
    # In production, fetch the actual progress from your database.
    return {
        'completed': 0,
        'current_progress': 0,
        'achievements': []
    }

# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

def create_rarity_animation(rarity):
    """Create animated sparkle effect based on rarity"""
    colors = ["#FFD700" if rarity > 90 else "#C0C0C0" if rarity > 70 else "#CD7F32"]
    return f"""
    <style>
    @keyframes sparkle {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.2); opacity: 0.8; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    .rarity-{rarity} {{
        background: linear-gradient(45deg, {colors[0]}, #FFFFFF);
    }}
    </style>
    """

def create_achievement_badge(title, description):
    """Create an achievement badge with animation"""
    return f"""
    <div style="
        background: linear-gradient(45deg, #4ECDC4, #556270);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: badge-glow 2s infinite alternate;
    ">
        <h3 style="color: white; margin: 0;">🏆 {title}</h3>
        <p style="color: #DDD; margin: 5px 0 0 0;">{description}</p>
    </div>
    <style>
    @keyframes badge-glow {{
        from {{ box-shadow: 0 0 10px #4ECDC4; }}
        to {{ box-shadow: 0 0 20px #4ECDC4; }}
    }}
    </style>
    """

def create_piece_card(piece, theme_colors):
    """Create a themed piece card with SVG and animations"""
    rarity_color = "#FFD700" if piece['rarity'] > 90 else "#C0C0C0" if piece['rarity'] > 70 else "#CD7F32"
    return f"""
    <div class="piece-card rarity-{piece['rarity']}" style="
        padding: 15px;
        border: 2px solid {rarity_color};
        border-radius: 10px;
        margin: 5px;
        background: linear-gradient(45deg, {theme_colors['primary']}22, {theme_colors['secondary']}22);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h4 style="color: {theme_colors['accent']}; text-align: center; margin: 10px 0;">
            Piece #{piece['type']}
        </h4>
        <p style="color: {rarity_color}; margin: 5px 0;">✨ {piece['effect']}</p>
        <p style="color: {theme_colors['secondary']}">📈 Rarity: {piece['rarity']}%</p>
    </div>
    """

def get_user_stats(wallet_address):
    """Get user's gaming statistics from database"""
    puzzle_progress = get_user_progress(wallet_address, 'Puzzle NFT Game')
    minesweeper_progress = get_user_progress(wallet_address, 'Minesweeper')
    return {
        'puzzle_nfts': puzzle_progress.get('completed', 0),
        'minesweeper_wins': minesweeper_progress.get('completed', 0),
        'total_revealed': minesweeper_progress.get('current_progress', 0),
        'achievements': puzzle_progress.get('achievements', []) + minesweeper_progress.get('achievements', [])
    }

def get_player_rank(stats):
    """Calculate player rank based on total score"""
    total_score = (stats['puzzle_nfts'] * 100 + 
                  stats['minesweeper_wins'] * 200 + 
                  len(stats['achievements']) * 300)
    
    if total_score < 500:
        return "🥉 Bronze"
    elif total_score < 1500:
        return "🥈 Silver"
    elif total_score < 3000:
        return "🥇 Gold"
    else:
        return "👑 Diamond"

def display_stats(wallet_address):
    """Display user stats in sidebar"""
    stats = get_user_stats(wallet_address)
    
    st.sidebar.markdown("### 🏆 Gaming Profile")
    
    # Profile Card
    st.sidebar.markdown(f"""
    <div style='padding: 10px; 
                background: linear-gradient(45deg, #1e3799, #0c2461); 
                border-radius: 10px; 
                color: white;'>
        <h3>👤 Player Stats</h3>
        <p>Wallet: {wallet_address[:6]}...{wallet_address[-4:]}</p>
        <p>Rank: {get_player_rank(stats)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🧩 NFTs", stats['puzzle_nfts'], f"+{len(stats['achievements'])}")
        st.metric("💣 Wins", stats['minesweeper_wins'])
    with col2:
        st.metric("🎯 Revealed", stats['total_revealed'])
        completion_rate = (stats['total_revealed'] / 64 * 100) if stats['total_revealed'] > 0 else 0
        st.metric("📊 Success", f"{completion_rate:.1f}%")
    
    # Achievements
    if stats['achievements']:
        st.sidebar.markdown("### 🌟 Achievements")
        for achievement in stats['achievements']:
            # Determine the correct category for each achievement
            if achievement in ACHIEVEMENTS['puzzle']:
                category = 'puzzle'
            elif achievement in ACHIEVEMENTS['minesweeper']:
                category = 'minesweeper'
            else:
                continue
            st.sidebar.markdown(create_achievement_badge(
                ACHIEVEMENTS[category][achievement]['name'],
                ACHIEVEMENTS[category][achievement]['desc']
            ), unsafe_allow_html=True)

def update_achievement(wallet_address, achievement_type):
    """Update player achievements and display badge"""
    # Determine the category of the achievement
    if achievement_type in ACHIEVEMENTS['puzzle']:
        category = 'puzzle'
    elif achievement_type in ACHIEVEMENTS['minesweeper']:
        category = 'minesweeper'
    else:
        st.error("Invalid achievement type")
        return

    achievement = ACHIEVEMENTS[category][achievement_type]
    st.markdown(create_achievement_badge(achievement['name'], achievement['desc']), unsafe_allow_html=True)
    update_activity_progress(wallet_address, 'achievements', achievement_type, 1, 1)
