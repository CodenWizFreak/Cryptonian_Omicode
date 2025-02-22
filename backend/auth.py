import streamlit as st

def authenticate_user():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state["authenticated"] = True
            return True
        else:
            st.error("Invalid credentials")
            return False
    return st.session_state.get("authenticated", False)