import streamlit as st
from PIL import Image
import requests
import os
import io
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

st.set_page_config(page_title="ViQues - Visual QA", layout="wide")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Load Lottie animation
@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Firebase Authentication Functions
def sign_in_with_email_and_password(email, password):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
        params={"key": st.secrets["firebase_api_key"]},
        json=payload
    )
    if r.status_code == 200:
        return r.json()['email']
    else:
        st.warning(r.json().get('error', {}).get('message', 'Unknown Error'))
        return None

def sign_up_with_email_and_password(email, password):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signUp",
        params={"key": st.secrets["firebase_api_key"]},
        json=payload
    )
    if r.status_code == 200:
        return r.json()['email']
    else:
        st.warning(r.json().get('error', {}).get('message', 'Unknown Error'))
        return None

# Custom background setup
def set_bg_image(img_path):
    with open(img_path, "rb") as image_file:
        encoded = image_file.read()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{encoded.decode("latin1")}');
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

img_path = "bg.png"
if os.path.exists(img_path):
    set_bg_image(img_path)
else:
    st.warning("Background image not found.")

# Gemini Vision Pro API Call (Dummy Function)
def gemini_vision_pro(image, question):
    # Replace this stub with actual Gemini Vision Pro API call
    return "This is a dummy answer from Gemini Vision Pro."

# App Sections
def Home():
    st.title("🔍 ViQues - Enhanced Visual Question Answering System")
    lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie:
        st_lottie(lottie, height=300)
    st.markdown("""
        ViQues allows you to ask questions about images through file upload or webcam,
        powered by Gemini Pro Vision. Use text or speech input, get audio/text answers instantly!
    """)

def VQA_Image():
    st.header("📷 Upload Image for Question Answering")
    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        question = st.text_input("Enter your question")
        if st.button("Get Answer"):
            response = gemini_vision_pro(image, question)
            st.subheader("Answer")
            st.markdown(response)

def VQA_Webcam():
    st.header("🎥 Webcam Capture for Question Answering")
    picture = st.camera_input("Take a picture")
    if picture:
        img = Image.open(picture)
        st.image(img, caption="Captured Image", use_column_width=True)
        question = st.text_input("Enter your question")
        if st.button("Get Answer"):
            response = gemini_vision_pro(img, question)
            st.subheader("Answer")
            st.markdown(response)

def Login():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = sign_in_with_email_and_password(email, password)
        if user:
            st.session_state.authenticated = True
            st.success("Login Successful")

def Signup():
    st.title("📝 Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        user = sign_up_with_email_and_password(email, password)
        if user:
            st.session_state.authenticated = True
            st.success("Account Created Successfully")

# Main App Navigation
if not st.session_state.authenticated:
    page = option_menu("Main Menu", ["Login", "Signup"], orientation="horizontal")
    if page == "Login":
        Login()
    elif page == "Signup":
        Signup()
else:
    app = option_menu(
        menu_title=None,
        options=["Home", "Image QA", "Webcam QA", "Logout"],
        icons=["house", "image", "camera", "box-arrow-right"],
        orientation="horizontal"
    )

    if app == "Home":
        Home()
    elif app == "Image QA":
        VQA_Image()
    elif app == "Webcam QA":
        VQA_Webcam()
    elif app == "Logout":
        st.session_state.authenticated = False
        st.success("You have been logged out.")
