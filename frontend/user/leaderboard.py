import streamlit as st
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas
def connect_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["mydatabase"] 
    return db

def set_style():
    st.markdown("""
        <style>
        /* Base theme */
        .stApp {
            background: #000000;
        }
        
        /* Leaderboard table */
        .leaderboard-table {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 24px;
            margin: 10px 0;
            border: 1px solid rgba(78, 108, 180, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(96, 165, 250, 0.1);
        }
        
        .leaderboard-header {
            color: #f8fafc;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 24px 0 16px 0;
        }
        
        .leaderboard-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(78, 108, 180, 0.2);
        }
        
        .leaderboard-row.current-user {
            border: 2px solid #60a5fa;  /* Golden blue border */
            border-radius: 8px;
            padding: 10px;
            background: rgba(96, 165, 250, 0.1);  /* Light blue background */
        }
        
        .leaderboard-rank {
            font-size: 18px;
            font-weight: bold;
            color: #60a5fa;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .leaderboard-wallet {
            font-size: 16px;
            color: #94a3b8;
        }
        
        .leaderboard-score {
            font-size: 18px;
            font-weight: bold;
            color: #93c5fd;
        }
        </style>
    """, unsafe_allow_html=True)

def calculate_leaderboard_scores(db):
    # Get all unique wallet addresses
    wallet_addresses = db.users.distinct("wallet_address")
    
    leaderboard = []
    
    for wallet_address in wallet_addresses:
        # Count the number of activities for the wallet
        num_activities = db.activity.count_documents({"wallet_address": wallet_address})
        
        # Count the number of achievements for the wallet
        num_achievements = db.achievements.count_documents({"wallet_address": wallet_address})
        
        # Calculate the leaderboard score
        score = num_activities + (10 * num_achievements)
        
        # Add to leaderboard
        leaderboard.append({
            "wallet_address": wallet_address,
            "score": score,
            "num_activities": num_activities,
            "num_achievements": num_achievements
        })
    
    # Sort the leaderboard by score in descending order
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    
    return leaderboard

def render_leaderboard(leaderboard, current_wallet_address):
    st.markdown('<div class="leaderboard-header">Leaderboard</div>', unsafe_allow_html=True)
    
    for index, entry in enumerate(leaderboard):
        # Check if the current row belongs to the logged-in user
        is_current_user = entry['wallet_address'] == current_wallet_address
        
        # Apply a special class for the current user's row
        row_class = "leaderboard-row current-user" if is_current_user else "leaderboard-row"
        
        # Add medals for top 3 ranks
        if index == 0:
            rank_display = "🥇 #1"  # Gold medal
        elif index == 1:
            rank_display = "🥈 #2"  # Silver medal
        elif index == 2:
            rank_display = "🥉 #3"  # Bronze medal
        else:
            rank_display = f"#{index + 1}"  # Normal rank
        
        st.markdown(f"""
            <div class="{row_class}">
                <div class="leaderboard-rank">{rank_display}</div>
                <div class="leaderboard-wallet">{entry['wallet_address']}</div>
                <div class="leaderboard-score">{entry['score']}</div>
            </div>
        """, unsafe_allow_html=True)

def app(wallet_address):
    try:
        set_style()
        
        # Connect to MongoDB
        db = connect_db()
        
        st.title("Leaderboard")
        
        # Calculate leaderboard scores
        leaderboard = calculate_leaderboard_scores(db)
        
        # Render the leaderboard
        render_leaderboard(leaderboard, wallet_address)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your MongoDB connection and make sure the database is running.")
