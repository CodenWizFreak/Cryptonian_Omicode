import streamlit as st

def generate_events():
    return [
        ("Battle of Plassey", 1757),
        ("Dandi March", 1930),
        ("Quit India Movement", 1942),
        ("India's Independence", 1947),
        ("Green Revolution", 1965)
    ]

def check_order(user_order, correct_order):
    return user_order == correct_order

def app(wallet_address):
    st.title("🕰️ Timeline Tactician: Indian History Challenge")
    st.write("Arrange the historical events in the correct chronological order!")
    
    events = generate_events()
    years = [year for _, year in events]
    user_order = []
    
    for i, (event, _) in enumerate(events):
        selected_year = st.selectbox(f"When did {event} happen?", years, key=f"event_{i}")
        user_order.append((event, selected_year))
    
    if st.button("Check Order"):
        correct_order = [(event, year) for event, year in events]
        if check_order(user_order, correct_order):
            st.success("🎉 Correct! You know your history!")
        else:
            st.error("❌ Incorrect! Try again.")
            st.write("Correct order:")
            for event, year in correct_order:
                st.write(f"- {event} ({year})")