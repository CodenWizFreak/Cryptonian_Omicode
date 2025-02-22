import streamlit as st

def geography_lesson():
    phases = ["Physical Geography", "Human Geography", "Environmental Issues"]
    current_phase = st.tabs(phases)

    with current_phase[0]:
        st.markdown("### Physical Geography")
        st.write("""
        Learn about Earth's physical features.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - Mountains & Rivers
            - Climate & Weather
            - Plate Tectonics
            - Natural Disasters
            """)
        if st.button("Take Quiz - Phase 1"):
            st.info("Quiz functionality to be implemented")

    with current_phase[1]:
        st.markdown("### Human Geography")
        st.write("""
        Study human settlements and their impact on the environment.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - Population Growth
            - Urbanization
            - Migration Patterns
            - Cultural Landscapes
            """)
        if st.button("Take Quiz - Phase 2"):
            st.info("Quiz functionality to be implemented")

    with current_phase[2]:
        st.markdown("### Environmental Issues")
        st.write("""
        Understand the challenges facing our planet.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - Climate Change
            - Deforestation
            - Pollution
            - Conservation Efforts
            """)
        if st.button("Take Quiz - Phase 3"):
            st.info("Quiz functionality to be implemented")
