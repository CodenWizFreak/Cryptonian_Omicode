import streamlit as st
from datetime import datetime
from backend.games.console import *
import random

# List of all historical events
HISTORICAL_EVENTS = [
    ("Battle of Plassey", 1757),
    ("First War of Independence", 1857),
    ("Indian National Congress Founded", 1885),
    ("Partition of Bengal", 1905),
    ("Jallianwala Bagh Massacre", 1919),
    ("Non-Cooperation Movement", 1920),
    ("Dandi March", 1930),
    ("Civil Disobedience Movement", 1930),
    ("Congress Socialist Party Formation", 1934),
    ("Quit India Movement", 1942),
    ("India's Independence", 1947),
    ("First Five Year Plan", 1951),
    ("States Reorganization Act", 1956),
    ("Green Revolution", 1965),
    ("Indo-Pakistani War", 1971),
    ("Emergency Period Begins", 1975),
    ("Operation Blue Star", 1984),
    ("Economic Liberalization", 1991),
    ("Pokhran-II Nuclear Tests", 1998),
    ("Right to Information Act", 2005)
]

def calculate_score(user_order, correct_order):
    """Calculate score based on correct positions."""
    score = 0
    correct_positions = 0
    for i in range(len(user_order)):
        if user_order[i] == correct_order[i]:
            correct_positions += 1
            score += 100
    return score, correct_positions

def app(wallet_address):
    st.title("🕰️ Timeline Tactician: Indian History Challenge")

    # Initialize session state
    if "timeline_state" not in st.session_state:
        st.session_state.timeline_state = {
            'total_attempts': 0,
            'correct_attempts': 0,
            'current_streak': 0,
            'best_streak': 0,
            'game_started': False,
            'start_time': None,
            'results_history': [],  # List to store all results
            'current_events': HISTORICAL_EVENTS  # Use the full list of events
        }

    # Game Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.timeline_state = {
                'total_attempts': 0,
                'correct_attempts': 0,
                'current_streak': 0,
                'best_streak': 0,
                'game_started': False,
                'start_time': None,
                'results_history': [],
                'current_events': HISTORICAL_EVENTS  # Reset to full list
            }
            st.rerun()

    with col2:
        if st.button("💾 Save Progress", use_container_width=True):
            if st.session_state.timeline_state['game_started']:
                saved_session = {
                    'total_attempts': st.session_state.timeline_state['total_attempts'],
                    'correct_attempts': st.session_state.timeline_state['correct_attempts'],
                    'results_history': st.session_state.timeline_state['results_history'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address,
                    'Timeline Tactician',
                    6,
                    st.session_state.timeline_state['correct_attempts'],
                    10,
                    additional_data=saved_session
                )
                st.success("Session progress saved successfully!")
            else:
                st.warning("No active session to save!")

    # Progress and Stats Display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attempts", st.session_state.timeline_state['total_attempts'])
    with col2:
        st.metric("Correct Attempts", st.session_state.timeline_state['correct_attempts'])
    with col3:
        st.metric("Current Streak", st.session_state.timeline_state['current_streak'])

    # Main game interface
    events = st.session_state.timeline_state['current_events']
    years = [year for _, year in events]
    user_order = []
    
    # Event selection interface
    for i, (event, _) in enumerate(events):
        selected_year = st.selectbox(
            f"When did {event} happen?",
            years,
            key=f"event_{i}"
        )
        user_order.append((event, selected_year))
    
    if st.button("✅ Check Order", use_container_width=True):
        correct_order = events
        score, correct_positions = calculate_score(user_order, correct_order)
        
        # Store result
        result = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'score': score,
            'correct_positions': correct_positions,
            'total_positions': len(events),
            'user_order': user_order,
            'correct_order': correct_order
        }
        st.session_state.timeline_state['results_history'].append(result)

        update_activity_progress(wallet_address, 'Timeline Tactician', 6, st.session_state.timeline_state['correct_attempts'], 10, additional_data={'results_history': st.session_state.timeline_state['results_history']})
        
        # Update stats
        st.session_state.timeline_state['total_attempts'] += 1
        if correct_positions == len(events):
            st.session_state.timeline_state['correct_attempts'] += 1
            st.session_state.timeline_state['current_streak'] += 1
            st.success(f"🎉 Perfect! Score: {score} points!")
        else:
            st.session_state.timeline_state['current_streak'] = 0
            st.warning(f"Almost there! You got {correct_positions} out of {len(events)} correct. Score: {score} points")
            st.write("Correct order:")
            for event, year in correct_order:
                st.write(f"- {event} ({year})")

    # Display Results History
    if st.session_state.timeline_state['results_history']:
        st.markdown("### 📜 Results History")
        results_df = []
        for result in st.session_state.timeline_state['results_history']:
            results_df.append({
                'Time': result['timestamp'],
                'Score': result['score'],
                'Correct Positions': f"{result['correct_positions']}/{result['total_positions']}"
            })
        st.dataframe(results_df, use_container_width=True)
