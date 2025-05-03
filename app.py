import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# --- Spotify-like Theme and CSS ---
st.set_page_config(page_title="Spotify for Learning", page_icon="🎧", layout="wide")

st.markdown("""
    <style>
        body, .stApp {
            background-color: #191414;
            color: #fff;
            font-family: 'Montserrat', 'Arial', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .snippet-card {
            background: #222;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 24px 0 rgba(0,0,0,0.15);
        }
        .snippet-title {
            color: #1DB954;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .snippet-meta {
            color: #b3b3b3;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background: linear-gradient(90deg, #1DB954 0%, #1ed760 100%);
            color: #191414;
            border-radius: 30px;
            border: none;
            font-weight: bold;
            padding: 0.5rem 2rem;
            margin-top: 1rem;
        }
        .stButton>button:hover {
            background: #1ed760;
            color: #191414;
        }
        .stAudio {
            background: #191414;
            border-radius: 12px;
            padding: 0.5rem;
        }
        .logo-spotify {
            width: 48px;
            vertical-align: middle;
            margin-right: 12px;
        }
        .playlist-header {
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
        }
        .playlist-title {
            font-size: 2.2rem;
            font-weight: 900;
            color: #fff;
            letter-spacing: -2px;
        }
        .playlist-desc {
            color: #b3b3b3;
            font-size: 1.1rem;
            margin-top: 0.5rem;
        }
        .snippet-cover {
            border-radius: 12px;
            width: 60px;
            height: 60px;
            object-fit: cover;
            margin-right: 1.5rem;
        }
        .snippet-content {
            display: flex;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Load API keys and setup ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel(
    'gemini-1.5-flash-001',
    generation_config={"temperature": 0.7, "max_output_tokens": 2048},
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
)
eleven_client = ElevenLabs(api_key=elevenlabs_api_key)

VOICE_OPTIONS = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "VR6AewLTigWG4xSOukaG",
    "Charlotte": "EXAVITQu4vr4xnSDxMaL",
    "Clyde": "2EiwWnXFnvU5JabPnv8n",
    "Dave": "pNInz6obpgDQGcFmaJgB"
}

# --- Spotify Logo URL ---
SPOTIFY_LOGO = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png"

# --- Playlist Header ---
st.markdown(f"""
<div class="playlist-header">
    <img src="{SPOTIFY_LOGO}" class="logo-spotify"/>
    <div>
        <div class="playlist-title">Spotify for Learning</div>
        <div class="playlist-desc">Your personalized, snackable learning playlist. Powered by Gemini & ElevenLabs.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- User Inputs (styled sidebar for Spotify feel) ---
with st.sidebar:
    st.image(SPOTIFY_LOGO, width=100)
    st.markdown("## Create Your Learning Playlist")
    topics = st.text_area("Enter your topics (one per line):", height=180)
    time_available = st.slider("How many minutes do you have?", 5, 60, 15, step=5)
    voice_name = st.selectbox("Choose a voice", list(VOICE_OPTIONS.keys()))
    voice_id = VOICE_OPTIONS[voice_name]
    generate = st.button("Generate Playlist")

def generate_snippet(topic):
    prompt = (
        f"Create a 5-minute audio script (about 750 words) about: {topic}\n"
        "Structure:\n"
        "1. Start with a hook/question\n"
        "2. Explain 3 key points\n"
        "3. Share a surprising fact\n"
        "4. End with practical takeaway\n"
        "Use conversational tone for audio listening."
    )
    response = gemini_model.generate_content(prompt)
    return response.text

def text_to_speech(text, voice_id):
    audio = eleven_client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    filename = "snippet.mp3"
    save(audio, filename)
    return filename

# --- Main Playlist Display ---
if generate:
    if not topics.strip():
        st.warning("Please enter at least one topic in the sidebar.")
    else:
        topic_list = [t.strip() for t in topics.split("\n") if t.strip()]
        num_snippets = min(time_available // 5, len(topic_list))
        if num_snippets == 0:
            st.warning("Not enough time for any snippets.")
        else:
            st.success(f"Creating {num_snippets} learning snippets...")
            for i, topic in enumerate(topic_list[:num_snippets], 1):
                with st.spinner(f"Generating snippet {i}: {topic}"):
                    try:
                        script = generate_snippet(topic)
                        audio_file = text_to_speech(script, voice_id)
                        # Card layout
                        st.markdown(
                            f"""
                            <div class="snippet-card">
                                <div class="snippet-content">
                                    <img src="https://cdn-icons-png.flaticon.com/512/727/727245.png" class="snippet-cover"/>
                                    <div>
                                        <div class="snippet-title">{i}. {topic}</div>
                                        <div class="snippet-meta">5 min • {voice_name} voice</div>
                                        <audio controls style="width:100%;">
                                            <source src="snippet.mp3" type="audio/mp3">
                                            Your browser does not support the audio element.
                                        </audio>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True
                        )
                        with open(audio_file, "rb") as f:
                            st.download_button(
                                label="Download MP3",
                                data=f,
                                file_name=f"{topic.replace(' ', '_')}.mp3",
                                mime="audio/mp3"
                            )
                    except Exception as e:
                        st.error(f"Error generating {topic}: {str(e)}")
            st.success("All snippets generated! Enjoy your learning playlist.")

st.markdown("---")
st.caption("Not affiliated with Spotify. UI inspired by Spotify. © 2025")

st.caption("Powered by Gemini & ElevenLabs. Your learning, your way.")
st.markdown("Made with ❤️ by Shivangi Sinha")