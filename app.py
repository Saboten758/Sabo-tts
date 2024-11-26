import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_bytes

# App Configuration
st.set_page_config(page_title="Sabo-TTS😎", layout="wide", page_icon="🎧")

# Initialize Session State
if "japanese_mode" not in st.session_state:
    st.session_state.japanese_mode = False

# Labels for Translation
labels = {
    "en": {
        "welcome": "Welcome to Sabo-TTS😎",
        "tts_tab": "Text-to-Speech Converter",
        "music_tab": "Music Player",
        "pdf_tab": "PDF to Audio Converter",
        "anime_tab": "Anime Wallpapers",
        "tts_settings": "TTS Settings",
        "select_language": "Select Language",
        "slow_speech": "Enable Slow Speech",
        "enter_text": "Enter the text you want to convert to speech:",
        "word_count": "Word Count",
        "character_count": "Character Count",
        "convert_button": "Convert to Speech",
        "download_audio": "Download Audio",
        "no_text_warning": "Please enter some text to convert!",
        "streams_available": "Available Streams",
        "add_stream": "Add Your Own Music Stream",
        "stream_name": "Stream Name",
        "stream_url": "Stream URL (must be a direct audio link)",
        "add_stream_button": "Add Stream",
        "pdf_upload": "Upload a PDF",
        "extract_text": "Extracted Text",
        "ocr_warning": "No text found in PDF, attempting OCR...",
        "pdf_error": "Failed to extract text from the PDF.",
        "error_occurred": "An error occurred",
        "anime_wallpaper_title": "Anime Wallpaper Gallery",
        "wallpaper_category": "Select Wallpaper Category",
        "fetch_wallpapers": "Fetch Wallpapers",
        "download_wallpaper": "Download Wallpaper"
    },
    "ja": {
        "welcome": "Sabo-TTSへようこそ😎",
        "tts_tab": "音声変換",
        "music_tab": "音楽プレイヤー",
        "pdf_tab": "PDFから音声へ",
        "anime_tab": "アニメ壁紙",
        "tts_settings": "TTS設定",
        "select_language": "言語を選択",
        "slow_speech": "遅い音声を有効にする",
        "enter_text": "音声に変換したいテキストを入力してください:",
        "word_count": "単語数",
        "character_count": "文字数",
        "convert_button": "音声に変換する",
        "download_audio": "音声をダウンロード",
        "no_text_warning": "変換するテキストを入力してください！",
        "streams_available": "利用可能なストリーム",
        "add_stream": "自分の音楽ストリームを追加",
        "stream_name": "ストリーム名",
        "stream_url": "ストリームURL（直接のオーディオリンク）",
        "add_stream_button": "ストリームを追加",
        "pdf_upload": "PDFをアップロード",
        "extract_text": "抽出されたテキスト",
        "ocr_warning": "PDFにテキストが見つかりませんでした。OCRを試みます...",
        "pdf_error": "PDFからテキストを抽出できませんでした。",
        "error_occurred": "エラーが発生しました",
        "anime_wallpaper_title": "アニメ壁紙ギャラリー",
        "wallpaper_category": "壁紙のカテゴリを選択",
        "fetch_wallpapers": "壁紙を取得",
        "download_wallpaper": "壁紙をダウンロード"
    },
}

# Utility Functions
def translate(key):
    """Translate a key based on the current language mode."""
    lang = "ja" if st.session_state.japanese_mode else "en"
    return labels[lang][key]

def generate_tts(text, language="en", slow=False):
    """Generate TTS audio from text."""
    tts = gTTS(text, lang=language, slow=slow)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Language Toggle Function
def toggle_language():
    """Toggle between English and Japanese modes."""
    st.session_state.japanese_mode = not st.session_state.japanese_mode

# Unsplash API Key (Replace with your own)
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"

# Top-level language toggle button
col1, col2 = st.columns([3, 1])
with col2:
    st.button(
        "🌐 Switch to Japanese" if not st.session_state.japanese_mode else "🌐 日本語から英語に切り替え", 
        on_click=toggle_language
    )

# Page Title
st.title(translate("welcome"))

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    translate("tts_tab"), 
    translate("pdf_tab"),
    translate("music_tab"), 
    translate("anime_tab")
])

# Tab 1: Text-to-Speech Converter
with tab1:
    st.sidebar.header(translate("tts_settings"))
    language = st.sidebar.selectbox(
        translate("select_language"),
        [("English", "en"), ("Spanish", "es"), ("French", "fr"), ("German", "de"), ("Hindi", "hi"), ("Japanese", "ja")],
        format_func=lambda x: x[0],
    )[1]

    slow_voice = st.sidebar.checkbox(translate("slow_speech"), value=False)

    st.header(translate("enter_text"))
    user_input = st.text_area(translate("enter_text"), "")

    st.write(f"**{translate('word_count')}:** {len(user_input.split())} | **{translate('character_count')}:** {len(user_input)}")

    if st.button(translate("convert_button")):
        if user_input.strip():
            audio = generate_tts(user_input, language=language, slow=slow_voice)
            st.audio(audio, format="audio/mp3", start_time=0)
            st.download_button(translate("download_audio"), data=audio, file_name="Sabo-tts-out😎.mp3", mime="audio/mpeg")
        else:
            st.warning(translate("no_text_warning"))

#Tab 2: pdf
with tab2:
    st.subheader(translate("pdf_upload"))
    uploaded_pdf = st.file_uploader("", type=["pdf"])

    if uploaded_pdf:
        try:
            pdf_reader = PdfReader(uploaded_pdf)
            extracted_text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

            if not extracted_text.strip():
                st.warning(translate("ocr_warning"))
                images = convert_from_bytes(uploaded_pdf.read())
                extracted_text = "\n".join(pytesseract.image_to_string(img) for img in images)

            if extracted_text.strip():
                st.text_area(translate("extract_text"), extracted_text, height=300)
                audio = generate_tts(extracted_text, language=language, slow=slow_voice)
                st.audio(audio, format="audio/mp3", start_time=0)
                st.download_button(translate("download_audio"), data=audio, file_name="PDF-to-Audio😎.mp3", mime="audio/mpeg")
            else:
                st.error(translate("pdf_error"))
        except Exception as e:
            st.error(f"{translate('error_occurred')}: {e}")



# Tab 3: Music Player
with tab3:
    st.subheader(translate("streams_available"))
    if "music_streams" not in st.session_state:
        st.session_state.music_streams = [
            {"name": "Lofi Beats", "url": "https://stream-relay-geo.ntslive.net/stream"},
            {"name": "Night Wave Plaza", "url": "https://radio.plaza.one/mp3"},
        ]

    for i, stream in enumerate(st.session_state.music_streams):
        st.markdown(f"**{i+1}. {stream['name']}**")
        st.audio(stream["url"], format="audio/mp3")

    st.subheader(translate("add_stream"))
    new_stream_name = st.text_input(translate("stream_name"))
    new_stream_url = st.text_input(translate("stream_url"))
    if st.button(translate("add_stream_button")):
        if new_stream_name and new_stream_url:
            st.session_state.music_streams.append({"name": new_stream_name, "url": new_stream_url})
            st.success(f"{translate('add_stream')} {new_stream_name}")
        else:
            st.warning(translate("no_text_warning"))

# Tab 4: Anime Wallpapers
with tab4:
    st.header(translate("anime_wallpaper_title"))
    
    # Cached wallpaper categories
    wallpaper_categories = [
        "waifu", "neko", "shinobu", "megumin", 
        "punch", "wave", "highfive", "handhold", 
        "kiss", "cry", "blush", "smile", 
        "pat", "cuddle", "hug", "nom", 
        "bite", "slap", "bonk", "yeet"
    ]
    
    # Category and display settings
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_category = st.selectbox(
            translate("wallpaper_category"), 
            wallpaper_categories
        )
    
    with col2:
        num_images = st.slider("Number of Images", 3, 20, 6)
    
    # Fetch wallpapers button
    if st.button(translate("fetch_wallpapers"), type="primary"):
        # Progress indicator
        progress_text = f"Fetching {num_images} {selected_category} images..."
        progress_bar = st.progress(0, text=progress_text)
        
        try:
            # Efficient image fetching with error handling
            wallpapers = []
            failed_attempts = 0
            max_attempts = num_images * 2  # Allow double attempts to get desired number
            
            while len(wallpapers) < num_images and failed_attempts < max_attempts:
                try:
                    response = requests.get(
                        f"https://api.waifu.pics/sfw/{selected_category}", 
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        image_url = response.json().get('url')
                        
                        # Prevent duplicate images
                        if image_url and image_url not in wallpapers:
                            wallpapers.append(image_url)
                            
                            # Update progress bar
                            progress = int((len(wallpapers) / num_images) * 100)
                            progress_bar.progress(progress, text=progress_text)
                    else:
                        failed_attempts += 1
                
                except requests.RequestException:
                    failed_attempts += 1
            
            # Clear progress bar
            progress_bar.empty()
            
            # Handle insufficient images
            if len(wallpapers) < num_images:
                st.warning(f"Could only fetch {len(wallpapers)} images")
            
            # Display images in responsive grid
            cols = st.columns(3)
            
            for i, wallpaper_url in enumerate(wallpapers):
                col = cols[i % 3]
                with col:
                    # Enhanced image display with caching
                    st.image(
                        wallpaper_url, 
                        use_container_width=True,
                        caption=f"{selected_category.capitalize()} #{i+1}"
                    )
                    
                    # Download button with improved error handling
                    try:
                        image_response = requests.get(wallpaper_url, timeout=10)
                        image_response.raise_for_status()
                        
                        st.download_button(
                            label=translate("download_wallpaper"),
                            data=image_response.content,
                            file_name=f"{selected_category}_wallpaper_{i+1}.jpg",
                            mime="image/jpeg",
                            key=f"download_{i}"  # Unique key for each button
                        )
                    except requests.RequestException:
                        st.error(f"Download failed for image {i+1}")
        
        except Exception as e:
            st.error(f"Unexpected error: {e}")
    
    # Aesthetic styling
    st.markdown("""
    <style>
    .stImage {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    .stImage:hover {
        transform: scale(1.05);
    }
    .stMarkdown {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Informative footer
    st.markdown("""
    ### 🌟
    Images are fetched from Waifu.pics API. Select the different categories to explore >_<
    """)