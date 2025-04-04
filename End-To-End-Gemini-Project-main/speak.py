import streamlit as st
from io import BytesIO
from gtts import gTTS

def speak(text):
  """Converts text to speech and plays it in the Streamlit app."""
  try:
    # Create a BytesIO object to hold the audio data
    audio_data = BytesIO()

    # Convert text to speech using gTTS
    tts = gTTS(text=text, lang='en')  # Change 'en' for desired language code

    # Write the audio data to the BytesIO object
    tts.write_to_fp(audio_data)

    # Reset the stream to the beginning
    audio_data.seek(0)

    # Play the audio in Streamlit
    st.audio(audio_data, format='audio/mpeg')

  except Exception as e:
    st.error(f"Error: {e}")

# Streamlit app layout and functionality
st.title("Text to Speech")
text = st.text_input("Enter text to be spoken:")

if st.button("Speak"):
  speak(text)
