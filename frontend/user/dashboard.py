import streamlit as st
import pymongo
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
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
        
        /* Stats cards */
        .stats-container {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 24px;
            margin: 10px 0;
            border: 1px solid rgba(78, 108, 180, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(96, 165, 250, 0.1);
        }
        
        .stats-value {
            font-size: 36px;
            font-weight: bold;
            background: linear-gradient(90deg, #60a5fa, #93c5fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stats-label {
            color: #94a3b8;
            font-size: 16px;
        }
        
        /* Graph container */
        .graph-container {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(78, 108, 180, 0.2);
        }
        
        /* Section headers */
        .section-header {
            color: #f8fafc;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 24px 0 16px 0;
        }
        </style>
    """, unsafe_allow_html=True)

def get_user_stats(db, wallet_address):
    # Get user activity stats
    lessons_completed = db.lessons.count_documents({
        "wallet_address": wallet_address,
        "progress": 100  # Lessons with 100% progress are considered completed
    })
    games_played = db.activity.count_documents({
        "wallet_address": wallet_address
    })
    achievements_earned = db.achievements.count_documents({
        "wallet_address": wallet_address
    })
    
    return {
        "lessons_completed": lessons_completed,
        "games_played": games_played,
        "achievements_earned": achievements_earned
    }

def get_activity_timeline(db, wallet_address):
    # Get login activity data for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    user_logins = db.users.find({
        "wallet_address": wallet_address,
        "timestamp": {"$gte": thirty_days_ago}
    })
    
    # Convert to DataFrame
    df = pd.DataFrame(list(user_logins))
    if not df.empty and 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
        daily_activity = df.groupby('date').size().reset_index(name='count')
    else:
        # Create empty DataFrame with date range if no data
        date_range = pd.date_range(thirty_days_ago.date(), datetime.now().date(), freq='D')
        daily_activity = pd.DataFrame({'date': date_range.strftime('%Y-%m-%d'), 'count': 0})
    
    return daily_activity

def get_game_activity_stats(db, wallet_address):
    # Get game activity stats
    game_activity = db.activity.find({"wallet_address": wallet_address})
    game_stats = {
        'Puzzle NFT Game': 0,
        'Minesweeper': 0,
        'Timeline Tactician': 0,
        'Monument Scanner': 0,
        'map quiz': 0,
        'Artifact Assembler': 0
    }
    
    for activity in game_activity:
        sl_no = activity.get("sl_no")
        if sl_no == 1:
            game_stats['Puzzle NFT Game'] += 1
        elif sl_no == 2:
            game_stats['Minesweeper'] += 1
        elif sl_no == 6:
            game_stats['Timeline Tactician'] += 1
        elif sl_no == 4:
            game_stats['Monument Scanner'] += 1
        elif sl_no == 3:
            game_stats['map quiz'] += 1
        elif sl_no == 5:
            game_stats['Artifact Assembler'] += 1
    
    return game_stats

def render_stats(stats):
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown(f"""
            <div class="stats-container">
                <div class="stats-value">{stats['lessons_completed']}</div>
                <div class="stats-label">Lessons Completed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
            <div class="stats-container">
                <div class="stats-value">{stats['games_played']}</div>
                <div class="stats-label">Games Played</div>
            </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
            <div class="stats-container">
                <div class="stats-value">{stats['achievements_earned']}</div>
                <div class="stats-label">Achievements Earned</div>
            </div>
        """, unsafe_allow_html=True)

def render_activity_graph(activity_data):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=activity_data['date'],  # Date on x-axis
        y=activity_data['count'],  # Count on y-axis
        marker_color='#60a5fa',  # Bar color
        opacity=0.8,  # Bar opacity
        text=activity_data['count'],  # Display count values on bars
        textposition='auto'  # Automatically position text
    ))
    
    fig.update_layout(
        title="Daily Login Activity",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            tickformat='%Y-%m-%d'  # Format x-axis as YYYY-MM-DD
        ),
        yaxis=dict(
            title="Login Count",
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)'
        )
    )
    
    # Render the plotly chart with a unique key
    st.plotly_chart(fig, use_container_width=True, key="daily_activity_graph")
    
def render_game_activity_stats(game_stats):
    fig = go.Figure(data=[go.Pie(
        labels=list(game_stats.keys()),
        values=list(game_stats.values()),
        hole=.3,
        marker_colors=['#60a5fa', '#93c5fd', '#dbeafe', '#bfdbfe', '#a5b4fc', '#818cf8']
    )])
    
    fig.update_layout(
        title="Game Activity Distribution",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def get_lesson_progress(db, wallet_address):
    lessons = db.lessons.find({"wallet_address": wallet_address})
    lesson_stats = {
        "completed": 0,
        "in_progress": 0
    }
    
    for lesson in lessons:
        progress = lesson.get("progress", 0)
        if progress == 100:
            lesson_stats["completed"] += 1
        else:
            lesson_stats["in_progress"] += 1
    
    return lesson_stats

def render_lesson_progress(lesson_stats):
    fig = go.Figure(data=[go.Pie(
        labels=list(lesson_stats.keys()),
        values=list(lesson_stats.values()),
        hole=.3,
        marker_colors=['#60a5fa', '#93c5fd']
    )])
    
    fig.update_layout(
        title="Lesson Progress",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def app(wallet_address):
    try:
        set_style()
        
        # Connect to MongoDB
        db = connect_db()
        
        st.title("Learning Dashboard")
        
        # Get user data
        user_stats = get_user_stats(db, wallet_address)
        activity_data = get_activity_timeline(db, wallet_address)
        game_stats = get_game_activity_stats(db, wallet_address)
        lesson_stats = get_lesson_progress(db, wallet_address)
        
        # Render stats
        st.markdown('<div class="section-header">Overview</div>', unsafe_allow_html=True)
        render_stats(user_stats)
        
        # Render graphs
        st.markdown('<div class="section-header">Analytics</div>', unsafe_allow_html=True)
        
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            render_activity_graph(activity_data)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            render_lesson_progress(lesson_stats)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Render game activity stats
        st.markdown('<div class="section-header">Game Activity</div>', unsafe_allow_html=True)
        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        render_game_activity_stats(game_stats)
        st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your MongoDB connection and make sure the database is running.")

# Example usage
# app("your_wallet_address_here")