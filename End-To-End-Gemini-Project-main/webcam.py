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





def get_gemini_response_2(input,picture):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,img])
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


st.set_page_config(page_title="VQA using Webcam")

st.header("VQA")
input=st.text_input("Input Prompt: ",key="input")




picture = st.camera_input("Take a picture")


if picture is not None:
    img = Image.open(picture)
    st.image(picture)

submit=st.button("Generate Answer")


if submit:

    response=get_gemini_response_2(input,picture)
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
listen = st.button("Listen me")



if listen:
    text = speech_to_text()

    st.write("You said:", text)
    response = get_gemini_response_2(text, picture)
    st.subheader("The Description is")
    st.write(response)
    speak(response)