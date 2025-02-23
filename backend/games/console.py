
# -----------------------------------------------------------------------------
# Dummy implementations for update_activity_progress and get_user_progress
# -----------------------------------------------------------------------------

import streamlit as st
import random 
from datetime import datetime
import logging
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

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
    },
    'minesweeper': {
        'expert': {'name': '💫 Mine Expert', 'desc': 'Win without any flags', 'threshold': 1},
        'speed_demon': {'name': '🏃 Speed Demon', 'desc': 'Win under 1 minute', 'threshold': 60},
        'survivor': {'name': '🛡️ Survivor', 'desc': 'Win 5 games', 'threshold': 5}
    }
}

# SVG Assets
MINE_SVG = """<svg viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="#FF4444"/>
    <path d="M30,50 L70,50 M50,30 L50,70" stroke="white" stroke-width="8"/>
</svg>"""

MINE_SVG = """<svg viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="#FF4444"/>
    <path d="M30,50 L70,50 M50,30 L50,70" stroke="white" stroke-width="8"/>
</svg>"""

FLAG_SVG = """<svg viewBox="0 0 100 100">
    <rect x="45" y="20" width="5" height="60" fill="#333"/>
    <path d="M50,20 L80,35 L50,50" fill="#FF4444"/>
</svg>"""


#MongoDB
def connect_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["mydatabase"]

def update_activity_progress(wallet_address, activity_type, sl_no, completion, points, additional_data=None):
    
    try:
        db = connect_db()
        activities = db.activity
        
        update_data = {
            'completion': completion,
            'points': points,
            'updated_at': datetime.now()
        }
        
        if additional_data:
            update_data['additional_data'] = additional_data
            
        activities.update_one(
            {
                'wallet_address': wallet_address,
                'activity_type': activity_type,
                'sl_no': sl_no
            },
            {
                '$set': update_data
            },
            upsert=True
        )
        
        logger.info(f"Activity progress updated: {wallet_address} - {activity_type} - {sl_no}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating activity progress: {e}")
        raise Exception(f"Failed to update activity progress: {e}")

def get_user_progress(wallet_address, activity_type):
    
    try:
        db = connect_db()
        activities = db.activity
        
        pipeline = [
            {
                '$match': {
                    'wallet_address': wallet_address,
                    'activity_type': activity_type
                }
            },
            {
                '$group': {
                    '_id': None,
                    'completed': {
                        '$sum': {
                            '$cond': [{'$eq': ['$completion', 100]}, 1, 0]
                        }
                    },
                    'total_points': {'$sum': '$points'},
                    'current_progress': {'$avg': '$completion'}
                }
            }
        ]
        
        stats = list(activities.aggregate(pipeline))
        achievements = list(db.achievements.find(
            {'wallet_address': wallet_address, 'activity_type': activity_type},
            {'_id': 0, 'achievement_type': 1}
        ))
        
        result = {
            'completed': 0,
            'total_points': 0,
            'current_progress': 0,
            'achievements': [ach['achievement_type'] for ach in achievements]
        }
        
        if stats:
            result.update({
                'completed': stats[0]['completed'],
                'total_points': stats[0]['total_points'] or 0,
                'current_progress': round(stats[0]['current_progress'] or 0, 2)
            })
            
        return result
        
    except Exception as e:
        logger.error(f"Error fetching user progress: {e}")
        raise Exception(f"Failed to fetch user progress: {e}")

def update_achievement(wallet_address, achievement_type):
    try:
        db = connect_db()
        achievements = db.achievements
        
        activity_type = 'puzzle' if 'puzzle' in achievement_type else 'minesweeper'
        
        existing = achievements.find_one({
            'wallet_address': wallet_address,
            'achievement_type': achievement_type
        })
        
        if not existing:
            achievements.insert_one({
                'wallet_address': wallet_address,
                'achievement_type': achievement_type,
                'activity_type': activity_type,
                'earned_at': datetime.now()
            })
            
            achievement = ACHIEVEMENTS[activity_type][achievement_type]
            st.markdown(create_achievement_badge(
                achievement['name'], 
                achievement['desc']
            ), unsafe_allow_html=True)
            
    except Exception as e:
        raise Exception(f"Failed to update achievement: {e}")

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
            st.sidebar.markdown(create_achievement_badge(
                ACHIEVEMENTS['puzzle' if 'puzzle' in achievement else 'minesweeper'][achievement]['name'],
                ACHIEVEMENTS['puzzle' if 'puzzle' in achievement else 'minesweeper'][achievement]['desc']
            ), unsafe_allow_html=True)

