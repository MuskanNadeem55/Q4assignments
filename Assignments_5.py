# main.py

import streamlit as st
from crypto_utils import get_cipher
from file_handler import load_data, save_data

st.set_page_config(page_title="Secure Data Vault", layout="centered")

st.title("🔐 Secure Data Vault")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# Load encryption cipher
cipher = get_cipher()

# Load saved data
users_data = load_data()

def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(token):
    return cipher.decrypt(token.encode()).decode()

if choice == "Register":
    st.subheader("📝 Create New Account")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Register"):
        if new_user in users_data:
            st.error("🚫 User already exists. Try a different username.")
        else:
            encrypted_password = encrypt_text(new_password)
            users_data[new_user] = {
                "password": encrypted_password,
                "data": []
            }
            save_data(users_data)
            st.success("✅ Account created successfully!")

elif choice == "Login":
    st.subheader("🔓 Login to Your Vault")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users_data:
            stored_password = users_data[username]["password"]
            if password == decrypt_text(stored_password):
                st.success(f"✅ Welcome {username}!")

                st.markdown("---")
                st.subheader("🔏 Store a Secret")
                secret = st.text_input("Enter something secret")

                if st.button("Save Secret"):
                    encrypted_secret = encrypt_text(secret)
                    users_data[username]["data"].append(encrypted_secret)
                    save_data(users_data)
                    st.success("🔐 Secret saved securely!")

                st.subheader("📂 Your Secrets")

                if users_data[username]["data"]:
                    for idx, item in enumerate(users_data[username]["data"], 1):
                        decrypted_item = decrypt_text(item)
                        st.write(f"{idx}. {decrypted_item}")
                else:
                    st.info("No secrets stored yet.")
            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("❌ Username not found.")
