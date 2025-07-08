import re
import streamlit as st

# Styling
st.set_page_config(page_title="Password Strength Meter", page_icon="🔒", layout="centered")

# Custom CSS
st.markdown("""
<style>

    .main {
             background-color: #E0F7FA; /* Light Blue Shade */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh; 
        text-align: center;
    }
    .stTextInput {
        width: 60% !important;
        margin: 10px auto;
        text-align: center;
    }
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
   .stButton button {
    width: 50%;
    background-color: #5DADE2;
    color: white;
    font-size: 18px;
}

    .stButton button:hover {
        background-color: #7EC8E3;
    }
    .center-text {
        text-align: center;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔑 Password Strength Checker")
st.markdown('<p class="center-text">🔍 Enter your password below to check its security level.</p>', unsafe_allow_html=True)

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1  
    else:
        feedback.append("❗ Password should be at least **8 characters** long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1  
    else:
        feedback.append("🔠 Password should include **both uppercase and lowercase letters**.")

    if re.search(r"\d", password):
        score += 1  
    else:
        feedback.append("🔢 Password should include **at least one number**.")

    # Special characters
    if re.search(r"[!@#$%^&*]", password):
        score += 1  
    else: 
        feedback.append("🔣 Include at least **one special character** (!@#$%^&*).")

    # Display password strength
    if score == 4:
        st.success("✅ **Strong Password!** Your password is secure. 🔐")
    elif score == 3:
        st.info("⚠️ **Moderate Password!** Consider improving security by adding more elements.")
    else:
        st.error("🚨 **Weak Password!** Follow the suggestions below to strengthen it.")

    # Feedback
    if feedback:
        with st.expander("🛠️ Improve Your Password"):
            for item in feedback:
                st.markdown(f'<p class="center-text">{item}</p>', unsafe_allow_html=True)

# Password input field
password = st.text_input("🔏 Enter Your Password:", type="password", help="Ensure your password is strong")

# Button
if st.button("🔎 Check Strength"):
    if password:
        check_password_strength(password)
    else:
        st.warning("⚠️ Please enter a password first!")
