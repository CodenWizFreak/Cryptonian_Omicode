# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import random
from decimal import Decimal

class NFTMarketplace:
    def __init__(self):
        # Initialize session state if not exists
        if 'nfts' not in st.session_state:
            st.session_state.nfts = []
        if 'wallet' not in st.session_state:
            st.session_state.wallet = {'balance': 1000, 'owned_nfts': []}
        if 'rewards' not in st.session_state:
            st.session_state.rewards = []
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []

    def list_nft(self, name, description, price, image_url):
        nft = {
            'id': len(st.session_state.nfts) + 1,
            'name': name,
            'description': description,
            'price': float(price),
            'image_url': image_url,
            'seller': 'current_user',
            'listed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.nfts.append(nft)
        return nft

    def buy_nft(self, nft_id):
        nft = next((nft for nft in st.session_state.nfts if nft['id'] == nft_id), None)
        if nft and st.session_state.wallet['balance'] >= nft['price']:
            st.session_state.wallet['balance'] -= nft['price']
            st.session_state.wallet['owned_nfts'].append(nft)
            st.session_state.nfts = [n for n in st.session_state.nfts if n['id'] != nft_id]
            
            # Record transaction
            transaction = {
                'type': 'purchase',
                'nft_id': nft_id,
                'price': nft['price'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.transactions.append(transaction)
            
            # Add rewards
            reward_points = int(nft['price'] * 0.05)  # 5% rewards
            st.session_state.rewards.append({
                'points': reward_points,
                'description': f"Purchase reward for NFT #{nft_id}",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return True
        return False

def main(wallet_address):
    marketplace = NFTMarketplace()
    
    # Sidebar
    st.sidebar.title("Wallet")
    st.sidebar.metric("Balance", f"${st.session_state.wallet['balance']:.2f}")
    
    # Top navigation
    st.title("NFT Marketplace")
    tab1, tab2, tab3, tab4 = st.tabs(["Market", "List NFT", "My NFTs", "Rewards"])
    
    # Market tab
    with tab1:
        st.header("Available NFTs")
        if st.session_state.nfts:
            cols = st.columns(3)
            for idx, nft in enumerate(st.session_state.nfts):
                with cols[idx % 3]:
                    st.image("https://via.placeholder.com/150", caption=nft['name'])
                    st.write(f"Description: {nft['description']}")
                    st.write(f"Price: ${nft['price']:.2f}")
                    if st.button(f"Buy Now", key=f"buy_{nft['id']}"):
                        if marketplace.buy_nft(nft['id']):
                            st.success("Purchase successful!")
                            st.rerun()
                        else:
                            st.error("Insufficient funds!")
        else:
            st.info("No NFTs currently listed")
    
    # List NFT tab
    with tab2:
        st.header("List Your NFT")
        with st.form("list_nft_form"):
            name = st.text_input("NFT Name")
            description = st.text_area("Description")
            price = st.number_input("Price ($)", min_value=0.01, value=1.0)
            image_url = st.text_input("Image URL", "https://via.placeholder.com/150")
            
            if st.form_submit_button("List NFT"):
                nft = marketplace.list_nft(name, description, price, image_url)
                st.success(f"NFT {nft['name']} listed successfully!")
                st.rerun()
    
    # My NFTs tab
    with tab3:
        st.header("My NFT Collection")
        if st.session_state.wallet['owned_nfts']:
            cols = st.columns(3)
            for idx, nft in enumerate(st.session_state.wallet['owned_nfts']):
                with cols[idx % 3]:
                    st.image("https://via.placeholder.com/150", caption=nft['name'])
                    st.write(f"Description: {nft['description']}")
                    st.write(f"Purchased for: ${nft['price']:.2f}")
        else:
            st.info("You don't own any NFTs yet")
    
    # Rewards tab
    with tab4:
        st.header("Rewards")
        if st.session_state.rewards:
            df = pd.DataFrame(st.session_state.rewards)
            total_points = df['points'].sum()
            st.metric("Total Reward Points", total_points)
            st.dataframe(df)
        else:
            st.info("No rewards earned yet")
