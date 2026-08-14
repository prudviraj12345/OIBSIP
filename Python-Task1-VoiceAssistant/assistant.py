import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import time
import threading
import re
import requests
import json


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# Load custom commands
try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    custom_commands = config.get("custom_commands", {})

except (FileNotFoundError, json.JSONDecodeError):
    custom_commands = {}


# ============================================================
# TEXT TO SPEECH
# ============================================================

engine = pyttsx3.init()


def speak(text):
    """Convert text into speech."""

    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


# ============================================================
# SPEECH RECOGNITION
# ============================================================

def listen():
    """Listen to microphone input and convert speech to text."""

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(source)

    try:

        command = recognizer.recognize_google(audio)

        print("You said:", command)

        return command.lower()

    except sr.UnknownValueError:

        speak(
            "Sorry, I couldn't understand you. "
            "Please repeat."
        )

        return ""

    except sr.RequestError:

        speak(
            "Sorry, the speech recognition service "
            "is unavailable."
        )

        return ""


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(command):
    """Identify the user's intended action."""

    if any(word in command for word in ["time", "clock"]):
        return "time"

    elif any(
        word in command
        for word in ["date", "day", "today"]
    ):
        return "date"

    elif any(
        word in command
        for word in ["search", "look up", "find"]
    ):
        return "search"

    elif "youtube" in command:
        return "youtube"

    elif any(
        word in command
        for word in ["email", "mail", "send an email"]
    ):
        return "email"

    elif any(
        word in command
        for word in ["reminder", "remind me", "remind"]
    ):
        return "reminder"

    elif any(
        word in command
        for word in [
            "weather",
            "temperature",
            "forecast"
        ]
    ):
        return "weather"

    elif any(
        word in command
        for word in [
            "who is",
            "what is",
            "what are",
            "where is",
            "when was",
            "tell me about"
        ]
    ):
        return "knowledge"

    elif any(
        word in command
        for word in ["hello", "hi", "hey"]
    ):
        return "greeting"

    elif any(
        word in command
        for word in ["stop", "exit", "goodbye"]
    ):
        return "exit"

    return "unknown"


# ============================================================
# CUSTOM COMMANDS
# ============================================================

def execute_custom_command(command):
    """Execute commands stored in config.json."""

    for custom_command, url in custom_commands.items():

        if custom_command.lower() in command:

            speak(
                f"Opening {custom_command}"
            )

            webbrowser.open(url)

            return True

    return False


# ============================================================
# EMAIL ADDRESS CLEANING
# ============================================================

def clean_email_address(text):
    """Convert spoken email words into an email address."""

    text = text.lower().strip()

    replacements = {
        " at ": "@",
        " dot ": ".",
        " underscore ": "_",
        " dash ": "-",
        " hyphen ": "-"
    }

    for spoken, symbol in replacements.items():
        text = text.replace(
            spoken,
            symbol
        )

    text = text.replace(" ", "")

    return text


# ============================================================
# SEND EMAIL
# ============================================================

def send_email():
    """Send an email using Gmail SMTP."""

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:

        speak(
            "Email settings are not configured."
        )

        return

    speak(
        "Who should I send the email to?"
    )

    recipient = listen()

    if not recipient:

        speak(
            "I couldn't understand the recipient."
        )

        return

    recipient = clean_email_address(
        recipient
    )

    print(
        "Recipient:",
        recipient
    )

    speak(
        f"I understood the email address as "
        f"{recipient}. Is that correct?"
    )

    confirmation = listen()

    if "no" in confirmation:

        speak(
            "Okay. Please say the email address again."
        )

        recipient = listen()

        if not recipient:

            speak(
                "I couldn't understand the email address."
            )

            return

        recipient = clean_email_address(
            recipient
        )

    speak("What is the subject?")

    subject = listen()

    if not subject:

        speak(
            "I couldn't understand the subject."
        )

        return

    speak(
        "What should I say in the email?"
    )

    body = listen()

    if not body:

        speak(
            "I couldn't understand the message."
        )

        return

    try:

        message = EmailMessage()

        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(message)

        speak(
            "Your email has been sent successfully."
        )

    except Exception as error:

        print(
            "Email error:",
            error
        )

        speak(
            "Sorry, I couldn't send the email."
        )


# ============================================================
# REMINDER
# ============================================================

def reminder_alert(message):
    """Wait and trigger the reminder."""

    time.sleep(
        message["seconds"]
    )

    speak(
        f"Reminder! {message['text']}"
    )


def set_reminder(command):
    """Create a timed reminder."""

    match = re.search(
        r"\d+",
        command
    )

    if not match:

        speak(
            "Please tell me the number of "
            "seconds for the reminder."
        )

        return

    seconds = int(
        match.group()
    )

    if seconds <= 0:

        speak(
            "Please provide a time greater than zero."
        )

        return

    reminder_text = re.sub(
        r"set a reminder|set reminder|remind me|reminder",
        "",
        command
    )

    reminder_text = re.sub(
        r"\d+\s*(seconds?|minutes?|hours?)",
        "",
        reminder_text
    )

    reminder_text = reminder_text.strip()

    if not reminder_text:
        reminder_text = "Your reminder is due."

    if "minute" in command:
        seconds *= 60

    elif "hour" in command:
        seconds *= 3600

    reminder = {
        "seconds": seconds,
        "text": reminder_text
    }

    reminder_thread = threading.Thread(
        target=reminder_alert,
        args=(reminder,),
        daemon=True
    )

    reminder_thread.start()

    if seconds < 60:

        speak(
            f"Reminder set for {seconds} seconds."
        )

    elif seconds < 3600:

        minutes = seconds // 60

        speak(
            f"Reminder set for {minutes} minutes."
        )

    else:

        hours = seconds // 3600

        speak(
            f"Reminder set for {hours} hours."
        )


# ============================================================
# WEATHER
# ============================================================

def get_weather(command):
    """Fetch live weather information."""

    if not WEATHER_API_KEY:

        speak(
            "Weather API is not configured."
        )

        return

    city = command

    phrases = [
        "what is the weather in",
        "what's the weather in",
        "tell me the weather in",
        "weather in",
        "weather at",
        "temperature in",
        "temperature at",
        "what is the temperature in",
        "what's the temperature in"
    ]

    for phrase in phrases:
        city = city.replace(
            phrase,
            ""
        )

    city = city.strip()

    if not city:

        speak(
            "Which city would you like the weather for?"
        )

        city = listen()

        if not city:

            speak(
                "I couldn't understand the city."
            )

            return

    print(
        "Weather location:",
        city
    )

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:

            if response.status_code == 404:
                speak(
                    f"I couldn't find the city {city}."
                )

            elif response.status_code == 401:
                speak(
                    "The weather API key is invalid."
                )

            else:
                speak(
                    "I couldn't retrieve the weather."
                )

            print(
                "Weather API response:",
                data
            )

            return

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        condition = data["weather"][0]["description"]
        country = data["sys"]["country"]

        weather_message = (
            f"The current weather in {city}, "
            f"{country} is {temperature:.1f} "
            f"degrees Celsius. "
            f"It feels like {feels_like:.1f} "
            f"degrees. "
            f"The condition is {condition}. "
            f"Humidity is {humidity} percent, "
            f"and wind speed is "
            f"{wind_speed:.1f} meters per second."
        )

        speak(weather_message)

    except requests.exceptions.Timeout:

        speak(
            "The weather service took too long "
            "to respond."
        )

    except requests.exceptions.ConnectionError:

        speak(
            "I couldn't connect to the weather service."
        )

    except Exception as error:

        print(
            "Weather error:",
            error
        )

        speak(
            "Sorry, I couldn't retrieve the weather."
        )


# ============================================================
# GENERAL KNOWLEDGE
# ============================================================

def answer_knowledge_question(command):
    """Answer general knowledge questions using Wikipedia."""

    question = command.lower().strip()

    # Remove question phrases
    phrases = [
        "who is",
        "what is",
        "what are",
        "where is",
        "when was",
        "when is",
        "tell me about",
        "explain"
    ]

    for phrase in phrases:
        question = question.replace(phrase, "", 1)

    question = question.strip()

    if not question:
        speak("What would you like to know?")
        return

    print("Knowledge search:", question)

    try:
        # Step 1: Search Wikipedia
        search_url = "https://en.wikipedia.org/w/api.php"

        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": question,
            "format": "json",
            "utf8": 1,
            "srlimit": 1
        }

        search_response = requests.get(
            search_url,
            params=search_params,
            timeout=10
        )

        search_data = search_response.json()

        results = search_data.get("query", {}).get("search", [])

        if not results:
            speak("I couldn't find information about that.")
            return

        # Get the best matching Wikipedia page
        page_title = results[0]["title"]

        print("Wikipedia page:", page_title)

        # Step 2: Get page summary
        summary_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + requests.utils.quote(page_title)
        )

        summary_response = requests.get(
            summary_url,
            timeout=10
        )

        if summary_response.status_code != 200:
            speak("I found the topic, but couldn't retrieve its information.")
            return

        data = summary_response.json()

        answer = data.get("extract")

        if answer:
            # Limit response length for voice
            if len(answer) > 600:
                answer = answer[:600] + "."

            speak(answer)

        else:
            speak("I couldn't find a useful answer.")

    except requests.exceptions.Timeout:

        speak(
            "The knowledge service took too long to respond."
        )

    except requests.exceptions.ConnectionError:

        speak(
            "I couldn't connect to the knowledge service."
        )

    except Exception as error:

        print("Knowledge error:", error)

        speak(
            "Sorry, I couldn't get that information."
        )


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(command):

    # Custom commands first
    if execute_custom_command(command):
        return True

    intent = detect_intent(command)

    # Greeting
    if intent == "greeting":

        speak(
            "Hello! How can I help you?"
        )

    # Time
    elif intent == "time":

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        speak(
            f"The current time is {current_time}"
        )

    # Date
    elif intent == "date":

        current_date = datetime.now().strftime(
            "%B %d, %Y"
        )

        speak(
            f"Today's date is {current_date}"
        )

    # Search
    elif intent == "search":

        search_query = command

        for phrase in [
            "search",
            "look up",
            "find"
        ]:

            search_query = search_query.replace(
                phrase,
                "",
                1
            )

        search_query = search_query.strip()

        if search_query:

            speak(
                f"Searching for {search_query}"
            )

            search_url = (
                "https://www.google.com/search?q="
                + search_query.replace(
                    " ",
                    "+"
                )
            )

            webbrowser.open(search_url)

        else:

            speak(
                "What would you like me to search for?"
            )

    # YouTube
    elif intent == "youtube":

        speak(
            "Opening YouTube"
        )

        webbrowser.open(
            "https://www.youtube.com"
        )

    # Email
    elif intent == "email":

        speak(
            "Sure, I can help you send an email."
        )

        send_email()

    # Reminder
    elif intent == "reminder":

        set_reminder(command)

    # Weather
    elif intent == "weather":

        get_weather(command)

    # General knowledge
    elif intent == "knowledge":

        answer_knowledge_question(command)

    # Exit
    elif intent == "exit":

        speak(
            "Goodbye! Have a nice day."
        )

        return False

    # Unknown
    else:

        speak(
            "I'm not sure what you mean. "
            "Please try again."
        )

    return True


# ============================================================
# MAIN PROGRAM
# ============================================================

speak(
    "Hello! I am your voice assistant. "
    "How can I help you?"
)

running = True

while running:

    command = listen()

    if command:

        running = process_command(command)