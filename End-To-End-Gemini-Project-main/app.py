import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import base64
from streamlit_extras.stylable_container import stylable_container

cred = credentials.Certificate("firebase-key.json")
#firebase_admin.initialize_app(cred)



if 'username' not in st.session_state:
    st.session_state.username = ''
if 'useremail' not in st.session_state:
    st.session_state.useremail = ''


def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        }
        if username:
            payload["displayName"] = username
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyB3YSmrQ0gOzOtrmS9K1ytm5KgfShKNM4A"}, data=payload)
        try:
            return r.json()['email']
        except:
            st.warning(r.json())
    except Exception as e:
        st.warning(f'Signup failed: {e}')


def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    try:
        payload = {
            "returnSecureToken": return_secure_token
        }
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        payload = json.dumps(payload)
        print('payload sigin', payload)
        r = requests.post(rest_api_url, params={"key": "AIzaSyB3YSmrQ0gOzOtrmS9K1ytm5KgfShKNM4A"}, data=payload)
        try:
            data = r.json()
            user_info = {
                'email': data['email'],
                'username': data.get('displayName')  # Retrieve username if available
            }
            return user_info
        except:
            st.warning(data)
    except Exception as e:
        st.warning(f'Signin failed: {e}')


def f():
    try:
        # user = auth.get_user_by_email(email)
        # print(user.uid)
        # st.session_state.username = user.uid
        # st.session_state.useremail = user.email

        userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
        st.session_state.username = userinfo['username']
        st.session_state.useremail = userinfo['email']

        global Usernm
        Usernm = (userinfo['username'])

        st.session_state.signedout = True
        st.session_state.signout = True


    except:
        st.warning('Login Failed')


def t():
    st.session_state.signout = False
    st.session_state.signedout = False
    st.session_state.username = ''


if "signedout" not in st.session_state:
    st.session_state["signedout"] = False
if 'signout' not in st.session_state:
    st.session_state['signout'] = False

if not st.session_state["signedout"]:  # only show if the state is False, hence the button has never been clicked
    st.header('Welcome to :violet[ViQues] :wave:', divider="rainbow")
    def add_border_to_input(selector=".stTextInput > div", border_style="solid 1px #ccc"):
        """
        Adds a border to the input text element using CSS.

        Args:
            selector (str, optional): CSS selector targeting the input element. Defaults to ".stTextInput > div".
            border_style (str, optional): CSS style for the border. Defaults to "solid 1px #ccc".
        """
        st.markdown(f"""<style>
      {selector} {{
        border: 1px solid black;
      }}
      </style>""", unsafe_allow_html=True)


    def add_border_to_selectbox(selector=".stSelectbox > div", border_style="solid 1px #ccc"):
        """
        Adds a border to the input text element using CSS.

        Args:
            selector (str, optional): CSS selector targeting the input element. Defaults to ".stTextInput > div".
            border_style (str, optional): CSS style for the border. Defaults to "solid 1px #ccc".
        """
        st.markdown(f"""<style>
      {selector} {{
        border: 1px solid black;
        border-radius: 8px;
      }}
      </style>""", unsafe_allow_html=True)

    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
    add_border_to_selectbox()
    email = st.text_input('Email Address')
    add_border_to_input()
    password = st.text_input('Password', type='password')
    add_border_to_input()
    st.session_state.email_input = email
    st.session_state.password_input = password

    if choice == 'Sign up':
        username = st.text_input("Enter  your unique username")

        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
            unsafe_allow_html=True,
        )

        with stylable_container(
                key="container_with_border",
                css_styles=r"""
                                button p:after {
                                    font-family: 'Font Awesome 5 Free';
                                    content: '\f234';
                                    display: inline-block;
                                    padding-right: 3px;
                                    padding-left: 5px;
                                    vertical-align: middle;
                                    font-weight: 900;
                                }

                                """,
        ):
            cr = st.button("Create my account")

        if cr:
            # user = auth.create_user(email = email, password = password,uid=username)
            user = sign_up_with_email_and_password(email=email, password=password, username=username)

            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()
    else:
        # st.button('Login', on_click=f)
        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
            unsafe_allow_html=True,
        )

        with stylable_container(
                key="container_with_border",
                css_styles=r"""
                        button p:after {
                            font-family: 'Font Awesome 5 Free';
                            content: '\f2f6';
                            display: inline-block;
                            padding-right: 3px;
                            padding-left: 5px;
                            vertical-align: middle;
                            font-weight: 900;
                        }
                        
                        """,
        ):

            st.button('Login', on_click=f)


    def set_bg_image(img_file):
        """
        Sets the background image for the Streamlit app.

        Args:
            img_file (str): Path to the image file.
        """
        with open(img_file, "rb") as f:
            data = f.read()
        encoded_data = base64.b64encode(data).decode()

        page_bg_img = f'''
      <style>
        .stApp {{
          background-image: url("data:image/png;base64,{encoded_data}");
          background-size: cover;
        }}
      </style>
      '''
        st.markdown(page_bg_img, unsafe_allow_html=True)


    # Example usage
    set_bg_image("bg.png")

if st.session_state.signout:
    def intro():
        import streamlit as st
        import base64


        st.header("Welcome to ViQues! 👋", divider="rainbow")


        st.markdown(
            """
            
            Enhanced Visual Question Answering System Using DenseNet

            _👈 Check out the application by navigating through the sections!_
            
            #### What our system can do?
            
            - Give responses for your visual based queries in any domain.
            
            - Upload images of your choice to provide answers for your queries.
            
            - Capture real time images to provide answers for your queries.
            
            - Uses both text and speech as input format for questions.
            
            - Give answers in both text and voice format. 
            
            
            


        """
        )
        def set_bg_image(img_file):
            """
            Sets the background image for the Streamlit app.

            Args:
                img_file (str): Path to the image file.
            """
            with open(img_file, "rb") as f:
                data = f.read()
            encoded_data = base64.b64encode(data).decode()

            page_bg_img = f'''
          <style>
            .stApp {{
              background-image: url("data:image/png;base64,{encoded_data}");
              background-size: cover;
            }}
          </style>
          '''
            st.markdown(page_bg_img, unsafe_allow_html=True)

        # Example usage
        set_bg_image("back.png")


    def VQA():
        import base64
        import speech_recognition as sr
        from io import BytesIO
        from gtts import gTTS
        import time
        from dotenv import load_dotenv

        load_dotenv()

        import streamlit as st
        import os
        import pathlib
        import textwrap
        from PIL import Image

        import google.generativeai as genai

        os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        def get_gemini_response(input, image):
            model = genai.GenerativeModel('gemini-pro-vision')
            if input != "":
                response = model.generate_content([input, image])
            else:
                response = model.generate_content(image)
            return response.text

        def get_gemini_response_3(text, image):
            model = genai.GenerativeModel('gemini-pro-vision')
            if text != "":
                response = model.generate_content([text, image])
            else:
                response = model.generate_content(image)
            return response.text
        def set_bg_image(img_file):
            """
            Sets the background image for the Streamlit app.

            Args:
                img_file (str): Path to the image file.
            """
            with open(img_file, "rb") as f:
                data = f.read()
            encoded_data = base64.b64encode(data).decode()

            page_bg_img = f'''
          <style>
            .stApp {{
              background-image: url("data:image/png;base64,{encoded_data}");
              background-size: cover;
            }}
          </style>
          '''
            st.markdown(page_bg_img, unsafe_allow_html=True)

        # Example usage
        set_bg_image("back.png")
        
        def speak(response):
            try:
                # Create a BytesIO object to hold the audio data
                audio_data = BytesIO()

                # Convert text to speech using gTTS
                tts = gTTS(text=response, lang='en')  # Change 'en' for desired language code

                # Write the audio data to the BytesIO object
                tts.write_to_fp(audio_data)

                # Reset the stream to the beginning
                audio_data.seek(0)

                # Play the audio in Streamlit
                st.audio(audio_data, format='audio/mpeg')

            except Exception as e:
                st.error(f"Error: {e}")

        st.header("Get Response :desktop_computer:", divider='rainbow')

        def add_border_to_input(selector=".stTextInput > div", border_style="solid 1px #ccc"):
            """
            Adds a border to the input text element using CSS.

            Args:
                selector (str, optional): CSS selector targeting the input element. Defaults to ".stTextInput > div".
                border_style (str, optional): CSS style for the border. Defaults to "solid 1px #ccc".
            """
            st.markdown(f"""<style>
          {selector} {{
            border: 1px solid black;
          }}
          </style>""", unsafe_allow_html=True)
        input = st.text_input("Text Input Prompt: ", key="input")
        add_border_to_input()
        uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        image = ""
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.sidebar.image(image, caption="Uploaded Image.", use_column_width=True)

        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
            unsafe_allow_html=True,
        )

        with stylable_container(
                key="container_with_border",
                css_styles=r"""
                button p:after {
                    font-family: 'Font Awesome 5 Free';
                    content: '\f1d8';
                    display: inline-block;
                    padding-right: 3px;
                    padding-left: 5px;
                    vertical-align: middle;
                    font-weight: 900;
                }
                button p:after {
                    font-family: 'Font Awesome 5 Free';
                    content: '\f130';
                    display: inline-block;
                    padding-right: 3px;
                    padding-left: 5px;
                    vertical-align: middle;
                    font-weight: 900;
                }
                """,
        ):

            submit = st.button("Generate Answer ")
        st.text("")

        ## If ask button is clicked

        if submit:
            response = get_gemini_response(input, image)
            st.subheader("The Answer is")
            st.write(response)
            speak(response)



        def speech_to_text():
            """
            Performs speech recognition using microphone input.
            """
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak Anything...")
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print("You said: {}".format(text))
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""

        # Your Streamlit app code here

        listen = st.button("Use mic")

        if listen:
            st.write("Speak something...")
            text = speech_to_text()
            st.subheader("You asked:")
            st.write(text)
            response = get_gemini_response_3(text, image)
            st.subheader("The Answer is")
            st.write(response)
            speak(response)


    def VQA_Webcam():
        import base64
        import speech_recognition as sr
        from io import BytesIO
        from gtts import gTTS

        from dotenv import load_dotenv

        load_dotenv()

        import streamlit as st
        import os
        import pathlib
        import textwrap
        from PIL import Image

        import google.generativeai as genai

        os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        def get_gemini_response_2(input, picture):
            model = genai.GenerativeModel('gemini-pro-vision')
            if input != "":
                response = model.generate_content([input, img])
            else:
                response = model.generate_content(img)
            return response.text

        def set_bg_image(img_file):
            """
            Sets the background image for the Streamlit app.

            Args:
                img_file (str): Path to the image file.
            """
            with open(img_file, "rb") as f:
                data = f.read()
            encoded_data = base64.b64encode(data).decode()

            page_bg_img = f'''
          <style>
            .stApp {{
              background-image: url("data:image/png;base64,{encoded_data}");
              background-size: cover;
            }}
          </style>
          '''
            st.markdown(page_bg_img, unsafe_allow_html=True)

        # Example usage
        set_bg_image("back.png")

        def speak(response):
            try:
                # Create a BytesIO object to hold the audio data
                audio_data = BytesIO()

                # Convert text to speech using gTTS
                tts = gTTS(text=response, lang='en')  # Change 'en' for desired language code

                # Write the audio data to the BytesIO object
                tts.write_to_fp(audio_data)

                # Reset the stream to the beginning
                audio_data.seek(0)

                # Play the audio in Streamlit
                st.audio(audio_data, format='audio/mpeg')

            except Exception as e:
                st.error(f"Error: {e}")

        st.header("Get Response :desktop_computer:", divider='rainbow')

        def add_border_to_input(selector=".stTextInput > div", border_style="solid 1px #ccc"):
            """
            Adds a border to the input text element using CSS.

            Args:
                selector (str, optional): CSS selector targeting the input element. Defaults to ".stTextInput > div".
                border_style (str, optional): CSS style for the border. Defaults to "solid 1px #ccc".
            """
            st.markdown(f"""<style>
          {selector} {{
            border: 1px solid black;
          }}
          </style>""", unsafe_allow_html=True)
        input = st.text_input("Text Input Prompt: ", key="input")
        add_border_to_input()


        picture = st.sidebar.camera_input("Take a picture", key="my_camera")




        if picture is not None:
            img = Image.open(picture)
            st.sidebar.image(picture)
        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
            unsafe_allow_html=True,
        )
        with stylable_container(
                key="container_with_border",
                css_styles=r"""
                        button p:after {
                            font-family: 'Font Awesome 5 Free';
                            content: '\f1d8';
                            display: inline-block;
                            padding-right: 3px;
                            padding-left: 5px;
                            vertical-align: middle;
                            font-weight: 900;
                        }
                        button p:after {
                            font-family: 'Font Awesome 5 Free';
                            content: '\f130';
                            display: inline-block;
                            padding-right: 3px;
                            padding-left: 5px;
                            vertical-align: middle;
                            font-weight: 900;
                        }
                        """,
        ):
            submit = st.button("Generate Answer")
        st.text("")



        if submit:
            response = get_gemini_response_2(input, picture)
            st.subheader("The Answer is")
            st.write(response)
            speak(response)

        def speech_to_text():
            """
            Performs speech recognition using microphone input.
            """
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak Anything...")
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print("You said: {}".format(text))
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""

        # Your Streamlit app code here

        listen = st.button("Use mic")

        if listen:
            st.write("Speak something...")
            text = speech_to_text()

            st.subheader("You asked")
            st.write(text)
            response = get_gemini_response_2(text, picture)
            st.subheader("The Answer is")
            st.write(response)
            speak(response)


    #with st.sidebar:
        #selected = option_menu("Main Menu", ["Home", 'Settings'],
                              # icons=['house', 'gear'], menu_icon="cast", default_index=1)
        #selected



    def sign_out():
        import base64

        st.write("Are you sure want to sign out?")
        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
            unsafe_allow_html=True,
        )
        with stylable_container(
                key="container_with_border",
                css_styles=r"""
                                button p:after {
                                    font-family: 'Font Awesome 5 Free';
                                    content: '\f011';
                                    display: inline-block;
                                    padding-right: 3px;
                                    padding-left: 5px;
                                    vertical-align: middle;
                                    font-weight: 900;
                                }
                                
                                """,
        ):
            st.button('Sign Out',on_click=t)

        def set_bg_image(img_file):
            """
            Sets the background image for the Streamlit app.

            Args:
                img_file (str): Path to the image file.
            """
            with open(img_file, "rb") as f:
                data = f.read()
            encoded_data = base64.b64encode(data).decode()

            page_bg_img = f'''
          <style>
            .stApp {{
              background-image: url("data:image/png;base64,{encoded_data}");
              background-size: cover;
            }}
          </style>
          '''
            st.markdown(page_bg_img, unsafe_allow_html=True)

        # Example usage
        set_bg_image("back.png")


    with st.sidebar:
        selected = option_menu("ViQues", ["Home", "Upload Image", "Capture Image","Sign Out"],icons = ["house", "cloud-upload","image","box-arrow-left"],menu_icon = "cast",default_index = 0)

    # Call respective function based on selected option
    if selected == "Home":
        intro()
    elif selected == "Upload Image":
        VQA()
    elif selected == "Capture Image":
        VQA_Webcam()
    elif selected == "Sign Out":
        sign_out()




            
                
    


