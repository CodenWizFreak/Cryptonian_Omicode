import streamlit as st

def history_lesson():
    phases = ["Ancient Civilizations", "Industrial Revolution", "Modern Era"]
    current_phase = st.tabs(phases)

    with current_phase[0]:
        st.markdown("### Ancient Civilizations")
        st.write("""
        Learn about early human societies and their development.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - Mesopotamia
            - Ancient Egypt
            - Indus Valley Civilization
            - Chinese Dynasties
            """)
        if st.button("Take Quiz - Phase 1"):
            st.info("Quiz functionality to be implemented")

    with current_phase[1]:
        st.markdown("### Industrial Revolution")
        st.write("""
        Explore the advancements in manufacturing, transport, and economy.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - Steam Engines
            - Mass Production
            - Social Changes
            - Economic Impact
            """)
        if st.button("Take Quiz - Phase 2"):
            st.info("Quiz functionality to be implemented")

    with current_phase[2]:
        st.markdown("### Modern Era")
        st.write("""
        Study the key events of the 20th and 21st centuries.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - World Wars
            - Cold War
            - Technological Revolutions
            - Globalization
            """)
        if st.button("Take Quiz - Phase 3"):
            st.info("Quiz functionality to be implemented")
