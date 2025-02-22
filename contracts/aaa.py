import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjMzNmMzOWY0LWEwZWUtNDBlZS1hZDZiLTE4Y2Q2MDRlYjk4MyIsIm9yZ0lkIjoiNDMxNzc3IiwidXNlcklkIjoiNDQ0MTM4IiwidHlwZSI6IlBST0pFQ1QiLCJ0eXBlSWQiOiI0YzMxYjdmNy00MDNmLTQ3ZmItOTliNS1mYTAyY2Q2NDRmN2EiLCJpYXQiOjE3Mzk3MzQ0NzUsImV4cCI6NDg5NTQ5NDQ3NX0.6QyE8boCjJR5JR4O2H2prZatcPP-afFmZs99-F3IEmw"

# Streamlit App
st.title("Moralis Authentication with Aptos")

# Connect Wallet Button
st.header("Connect Wallet")
if st.button("Connect Wallet"):
    st.write("Wallet connected successfully!")

# Request Challenge Section
st.header("Request Challenge")
address = st.text_input("Wallet Address")
public_key = st.text_input("Public Key")

if st.button("Request Challenge"):
    url = "https://authapi.moralis.io/challenge/request/aptos"
    payload = {
        "domain": "amazingdomain.dapp",
        "statement": "Please confirm you want to log in",
        "uri": "https://amazingdomain.dapp/",
        "expirationTime": "2023-03-10T00:00:00.000Z",
        "notBefore": "2020-01-01T00:00:00.000Z",
        "timeout": 30,
        "chainId": 1,
        "address": address,
        "publicKey": public_key,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }
    response = requests.post(url, json=payload, headers=headers)
    st.json(response.json())

# Verify Challenge Section
st.header("Verify Challenge")
message = st.text_area("Message")
signature = st.text_input("Signature")

if st.button("Verify Challenge"):
    url = "https://authapi.moralis.io/challenge/verify/aptos"
    payload = {
        "message": message,
        "signature": signature,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }
    response = requests.post(url, json=payload, headers=headers)
    st.json(response.json())
