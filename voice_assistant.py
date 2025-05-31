import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from gtts import gTTS
import tempfile
from pydub import AudioSegment
from pydub.playback import play
import os
import re
import google.generativeai as genai
import pygame

genai.configure(api_key="Your_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
conversation_active = True

emotion_keywords = {
    "joy": ["happy", "joy", "excited", "cheerful", "delighted"],
    "sorrow": ["sad", "down", "depressed", "unhappy", "heartbroken"],
    "anger": ["angry", "furious", "rage", "annoyed", "irritated"],
    "surprise": ["surprised", "shocked", "amazed", "astonished", "unexpected"],
    "neutral": []
}

def detect_emotion(user_input):
    user_input = user_input.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return emotion
    return "neutral"

def generate_ai_response(query, emotion=None):
    if emotion:
        query = f"User is feeling {emotion}. {query}"
    response = model.generate_content(query)
    return response.text

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', '', text)

pygame.mixer.init()

def speak(text):
    cleaned_text = clean_text(text)
    tts = gTTS(cleaned_text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file_name = temp_file.name
        tts.save(temp_file_name)
        audio = AudioSegment.from_mp3(temp_file_name)
        play(audio)
        os.remove(temp_file_name)

def listen_for_input():
    if not conversation_active:
        return ""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your query...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def stop_conversation():
    global conversation_active
    conversation_active = False
    speak("Goodbye!")
    root.quit()

def update_ui_response(user_query, ai_response):
    chat_display.insert(tk.END, "AI is speaking...\n", "highlight")
    chat_display.update_idletasks()
    speak(ai_response)
    chat_display.tag_remove("highlight", "1.0", tk.END)
    chat_display.insert(tk.END, f"AI: {ai_response}\n")
    chat_display.yview(tk.END)

def on_speak_button_click():
    if not conversation_active:
        return
    chat_display.insert(tk.END, "Listening...\n", "highlight")
    chat_display.update_idletasks()
    user_query = listen_for_input()
    chat_display.tag_remove("highlight", "1.0", tk.END)
    if user_query.lower() == 'exit':
        root.quit()
    elif user_query:
        try:
            chat_display.insert(tk.END, f"You: {user_query}\n")
            emotion = detect_emotion(user_query)
            ai_response = generate_ai_response(user_query, emotion)
            update_ui_response(user_query, ai_response)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def adjust_for_screen_size():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if screen_width <= 320 and screen_height <= 480:
        font_size = 10
        button_width = 12
        button_height = 1
    else:
        font_size = 12
        button_width = 20
        button_height = 2
    chat_display.config(font=("Arial", font_size))
    speak_button.config(font=("Arial", font_size), width=button_width, height=button_height)
    stop_button.config(font=("Arial", font_size), width=button_width, height=button_height)

root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("320x480")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_display = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", fg="#333333", padx=10, pady=10)
chat_display.pack(fill=tk.BOTH, expand=True)
chat_display.tag_config("highlight", background="#ffffcc", foreground="#000000")

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=5, fill=tk.X)

speak_button = tk.Button(button_frame, text="Speak", command=on_speak_button_click, bg="#4CAF50", fg="white", relief="raised")
speak_button.pack(side=tk.LEFT, padx=5, expand=True)

stop_button = tk.Button(button_frame, text="Stop", command=stop_conversation, bg="#FF5722", fg="white", relief="raised")
stop_button.pack(side=tk.LEFT, padx=5, expand=True)

root.update_idletasks()
adjust_for_screen_size()
root.mainloop()
