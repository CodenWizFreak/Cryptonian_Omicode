import streamlit as st
from backend.lessons.quiz_handler import run_quiz

def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def web3_lesson():
    phases = ["Introduction", "Smart Contracts & DApps", "DeFi & NFTs"]
    current_phase = st.tabs(phases)

    with current_phase[0]:
        st.markdown("### Introduction to Blockchain")
        st.write("""
        Blockchain is a distributed ledger technology that enables secure, transparent, 
        and immutable record-keeping. Let's explore the key concepts.
        """)
        with st.expander("Key Concepts"):
            st.write("""
            1. Decentralization
            2. Consensus Mechanisms
            3. Cryptography
            4. Smart Contracts
            """)
        st.markdown(load_markdown("content/introduction_to_blockchain.md"))
        if st.button("Take Quiz - Phase 1"):
            run_quiz("Introduction to Blockchain")

    with current_phase[1]:
        st.markdown("### Smart Contracts & DApps")
        st.write("""
        Learn about self-executing contracts and decentralized applications.
        """)
        with st.expander("Topics Covered"):
            st.write("""
            - Solidity Programming
            - Web3.js Integration
            - DApp Architecture
            - Testing and Deployment
            """)
        if st.button("Take Quiz - Phase 2"):
            st.info("Quiz functionality to be implemented")

    with current_phase[2]:
        st.markdown("### DeFi & NFTs")
        st.write("""
        Explore decentralized finance and non-fungible tokens.
        """)
        with st.expander("Key Topics"):
            st.write("""
            - Lending/Borrowing Protocols
            - Yield Farming
            - NFT Standards
            - Token Economics
            """)
        if st.button("Take Quiz - Phase 3"):
            st.info("Quiz functionality to be implemented")
