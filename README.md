# AI Voice Assistant

This project is a voice-controlled AI assistant with emotional awareness, built using Python. It captures your speech, detects emotional cues, and generates natural language responses using Google's Gemini 1.5 Flash model. The assistant responds via voice and displays interaction in a graphical interface using Tkinter.

## Features

- Voice input via microphone
- Emotion detection from user input (joy, sorrow, anger, surprise, neutral)
- AI response generation using Google Gemini API
- Text-to-speech voice playback using gTTS and pydub
- GUI interface built with Tkinter
- Adaptive layout for small screens
- Button to stop and exit the assistant

## Prerequisites

Before running the application, ensure the following tools and packages are installed:

- Python 3.8 or above
- A working microphone and audio output device
- Internet connection (for API calls and TTS)

Then run:

```bash
pip install -r requirements.txt
```
On Ubuntu/Debian:
sudo apt-get install ffmpeg

git clone https://github.com/pranav11024/RaspberryPi-Emotion-Chatbot.git
cd ai-voice-assistant

Replace "Your_API_KEY" with your actual API key from Google AI Studio.

To Run:
python voice_assistant.py
