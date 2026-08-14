# 🎙️ Python Voice Assistant

## OIBSIP - Python Programming Task 1

### 🔗 Live Demo

https://oibsip-2-f4xg.onrender.com

---

## 📌 Project Objective

The objective of this project is to build a Python-based voice assistant
that listens to user commands and responds with useful actions.

The project includes beginner-level voice assistant features as well as
advanced features such as natural language intent detection, email
sending, timed reminders, live weather information, general knowledge
questions, and custom commands.

A web-based version of the assistant is also deployed using Render.

---

## ✨ Features

### Beginner Features

- 🎤 Capture voice input using SpeechRecognition
- 🔊 Text-to-speech responses using pyttsx3
- 👋 Respond to greetings such as "Hello"
- 🕐 Tell the current time
- 📅 Tell the current date
- 🔎 Perform Google web searches
- ❌ Graceful handling when speech is not understood

### Advanced Features

- 🧠 Natural language intent detection
- 📧 Send emails using Gmail SMTP
- ⏰ Set timed reminders
- 🌦️ Fetch live weather information using OpenWeatherMap API
- ❓ Answer general knowledge questions using Wikipedia
- ⚙️ Support custom commands using a JSON configuration file
- 🔐 Secure handling of API keys and email credentials using environment variables
- 🌐 Deployable web version using Flask and Render

---

## 🛠️ Technologies Used

- Python
- SpeechRecognition
- pyttsx3
- Flask
- Requests
- python-dotenv
- SMTP
- OpenWeatherMap API
- Wikipedia API
- JSON
- HTML
- CSS
- JavaScript
- Gunicorn
- Render

---

## 📂 Project Structure

```text
Python-Task1-VoiceAssistant/
│
├── assistant.py
├── app.py
├── config.json
├── requirements.txt
├── README.md
├── .gitignore
└── .env
