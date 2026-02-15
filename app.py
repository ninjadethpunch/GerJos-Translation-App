import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# App Configuration
st.set_page_config(page_title="Geralyn's Translation App", page_icon="🌐")

st.title("🌐 Geralyn's Translation App")
st.markdown("---")

# Language Selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From:", ["English", "Portuguese"], index=0)
with col2:
    target_lang = st.selectbox("To:", ["Portuguese", "English"], index=1)

# Map names to codes
lang_codes = {"English": "en", "Portuguese": "pt"}

# Input Method
input_method = st.radio("Choose Input Method:", ("Write Text", "Speak Out Loud"))

input_text = ""

if input_method == "Write Text":
    input_text = st.text_area("Enter text to translate:")

else:
    st.write("Click the microphone and speak:")
    audio_bytes = audio_recorder(text="Tap to Record", icon_size="2x")
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        # Convert audio to text
        recognizer = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                input_text = recognizer.recognize_google(audio_data, language=lang_codes[source_lang])
                st.success(f"I heard: {input_text}")
            except:
                st.error("Sorry, I couldn't understand the audio. Try again!")

# Translation Logic
if input_text:
    translated = GoogleTranslator(source=lang_codes[source_lang], target=lang_codes[target_lang]).translate(input_text)
    
    st.subheader("Translation:")
    st.success(translated)

    # Text to Speech for the translation
    tts = gTTS(text=translated, lang=lang_codes[target_lang])
    tts_file = "translation.mp3"
    tts.save(tts_file)
    st.audio(tts_file)