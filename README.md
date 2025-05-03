# 🎧 Spotify for Learning

Transform idle moments into personalized, bite-sized learning experiences.  
**Spotify for Learning** lets you generate a playlist of 5-minute, podcast-style audio snippets on any topic-just like Spotify, but for your mind.

---

## 🚀 Project Summary

In a world where attention is scarce and curiosity is boundless, “Spotify for Learning” empowers anyone to learn on the go. Our app solves the problem of inaccessible, long-form educational content by generating custom 5-minute audio snippets-delivered as a playlist you can listen to anywhere.

Built in under 24 hours for the Global AI Hackathon, our tool lets users enter any topics, choose their available time, and instantly receive a playlist of engaging, AI-generated audio explanations. The app’s Spotify-inspired interface makes learning approachable and delightful, whether you’re commuting, exercising, or cooking.

This solution is designed for lifelong learners, busy professionals, and anyone looking to turn “dead time” into active knowledge-building. Users can generate, listen, and download their own learning playlists in seconds. The seamless integration of Gemini AI for content and ElevenLabs for speech makes the experience both novel and practical.

---

## 🛠️ Tech Stack

- **Gemini API** – Generative AI for educational content
- **ElevenLabs API** – High-quality text-to-speech
- **Streamlit** – Modern, Spotify-inspired web UI
- **Python** – Core logic and integration
- **dotenv** – Secure secret management

---

## 📦 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/spotify-for-learning.git
cd spotify-for-learning
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

- Get a [Gemini API key](https://aistudio.google.com/app/apikey)
- Get an [ElevenLabs API key](https://elevenlabs.io/)

Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
```

> **Note:** `.env` is in `.gitignore` to keep your keys safe.

### 4. Run the app
```bash
streamlit run app.py
```

---

## ✨ Usage

1. Enter your learning topics (one per line) in the sidebar.
2. Choose your available time and preferred voice.
3. Click **Generate Playlist**.
4. Listen to each snippet, or download as MP3 for later.

---

## 🎙️ Voices

Choose from several built-in ElevenLabs voices.  
To add more, [list your available voices](https://docs.elevenlabs.io/api-reference/voices) and update the `VOICE_OPTIONS` dictionary in `app.py`.

---

## 🛡️ Security

- Your API keys are **never shared** or committed to git.
- Only `.env.example` is tracked for developer reference.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## 📄 License

MIT License

---

## 🙏 Credits

- [Google Gemini](https://ai.google.dev/)
- [ElevenLabs](https://elevenlabs.io/)
- [Streamlit](https://streamlit.io/)
- Spotify UI inspiration

---

## ⚠️ Disclaimer

This project is not affiliated with or endorsed by Spotify.  
All trademarks are property of their respective owners.

---
