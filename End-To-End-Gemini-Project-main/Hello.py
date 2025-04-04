import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to ViQues! 👋")
    st.sidebar.success("Select a option above.")

    st.markdown(
        """
        Enhanced Visual Question Answering System Using DenseNet.

        **👈 Select an option the dropdown on the left** to see explore
        of what VQA System can do!

        
    """
    )





def VQA():
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



    st.header("VQA")
    input = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.sidebar.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Generate Answer")

    ## If ask button is clicked

    if submit:
        response = get_gemini_response(input, image)
        st.subheader("The Description is")
        st.write(response)
        speak(response)

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
    listen = st.button("Ask me")

    if listen:
        text = speech_to_text()
        st.subheader("You asked:")
        st.write(text)
        response = get_gemini_response_3(text, image)
        st.subheader("The Description is")
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



    st.header("VQA")
    input = st.text_input("Input Prompt: ", key="input")

    picture = st.sidebar.camera_input("Take a picture")

    if picture is not None:
        img = Image.open(picture)
        st.sidebar.image(picture)

    submit = st.button("Generate Answer")

    if submit:
        response = get_gemini_response_2(input, picture)
        st.subheader("The Description is")
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
    listen = st.button("Speak Out")

    if listen:
        text = speech_to_text()

        st.subheader("You asked")
        st.write(text)
        response = get_gemini_response_2(text, picture)
        st.subheader("The Description is")
        st.write(response)
        speak(response)

page_names_to_funcs = {
    "Home": intro,
    "VQA System": VQA,
    "VQA Webcam": VQA_Webcam,

}

demo_name = st.sidebar.selectbox("Choose a option", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()













