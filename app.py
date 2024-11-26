# app.py

import streamlit as st
from gtts import gTTS
from io import BytesIO

# Function to generate TTS
def generate_tts(text, language="en", slow=False):
    """Generate TTS audio from text."""
    tts = gTTS(text, lang=language, slow=slow)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# App Layout
st.set_page_config(page_title="Sabo-TTS😎", layout="wide")

# Tabs
tab1, tab2 = st.tabs(["Text-to-Speech Converter", "Music Player"])

# Tab 1: Text-to-Speech Converter
with tab1:
    st.title("Text-to-Speech (TTS) Converter")

    # Sidebar: Options
    st.sidebar.header("TTS Settings")
    language = st.sidebar.selectbox(
        "Select Language",
        [
            ("English", "en"),
            ("Spanish", "es"),
            ("French", "fr"),
            ("German", "de"),
            ("Hindi", "hi"),
        ],
        format_func=lambda x: x[0]
    )[1]

    slow_voice = st.sidebar.checkbox("Enable Slow Speech", value=False)

    # Input Area
    st.header("Enter Text")
    user_input = st.text_area("Enter the text you want to convert to speech:", "")

    # Live Word & Character Count
    st.write(f"**Word Count:** {len(user_input.split())} | **Character Count:** {len(user_input)}")

    # History of Conversions
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("Convert to Speech"):
        if user_input.strip():
            # Generate and display TTS
            audio = generate_tts(user_input, language=language, slow=slow_voice)
            st.audio(audio, format="audio/mp3", start_time=0)

            # Add to history
            st.session_state.history.append(user_input)

            # Download Button
            st.download_button(
                label="Download Audio",
                data=audio,
                file_name="Sabo-tts-out😎.mp3",
                mime="audio/mpeg"
            )
        else:
            st.warning("Please enter some text to convert!")

    # Display Conversion History
    if st.session_state.history:
        st.subheader("Conversion History")
        for i, text in enumerate(st.session_state.history[::-1], start=1):
            st.write(f"{i}. {text}")

# Tab 2: Music Player
with tab2:
    st.title("Online Music Player")

    # Predefined music streams
    if "music_streams" not in st.session_state:
        st.session_state.music_streams = [
            {"name": "Lofi Beats", "url": "https://stream-relay-geo.ntslive.net/stream"},
            {"name": "Night Wave Plaza", "url": "https://radio.plaza.one/mp3"},
        ]

    # Display music player
    st.subheader("Available Streams")
    for i, stream in enumerate(st.session_state.music_streams):
        st.markdown(f"**{i+1}. {stream['name']}**")
        st.audio(stream["url"], format="audio/mp3")

    # Add new music stream
    st.subheader("Add Your Own Music Stream")
    new_stream_name = st.text_input("Stream Name")
    new_stream_url = st.text_input("Stream URL (must be a direct audio link)")
    if st.button("Add Stream"):
        if new_stream_name and new_stream_url:
            st.session_state.music_streams.append({"name": new_stream_name, "url": new_stream_url})
            st.success(f"Added new stream: {new_stream_name}")
        else:
            st.warning("Please provide both a name and a valid URL!")
