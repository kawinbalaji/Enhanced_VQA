import speech_recognition as sr

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
text = speech_to_text()

if text:
  st.write("You said:", text)

