from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
        custom_commands = config.get("custom_commands", {})
except Exception:
    custom_commands = {}


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Voice Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }

        h1 {
            margin-bottom: 10px;
        }

        input {
            width: 70%;
            padding: 12px;
            font-size: 16px;
        }

        button {
            padding: 12px 18px;
            margin: 8px;
            cursor: pointer;
        }

        #result {
            margin-top: 25px;
            padding: 20px;
            border-radius: 10px;
            background: #f2f2f2;
            min-height: 30px;
        }
    </style>
</head>

<body>

    <h1>🎙️ Python Voice Assistant</h1>

    <p>Type a command or use your microphone.</p>

    <input
        id="command"
        placeholder="Ask something..."
    >

    <br>

    <button onclick="sendCommand()">
        Send
    </button>

    <button onclick="startListening()">
        🎤 Speak
    </button>

    <div id="result">
        Assistant response will appear here.
    </div>


<script>

function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}


async function sendCommand(commandText = null) {

    const input = document.getElementById("command");

    const command = commandText || input.value;

    if (!command) {
        return;
    }

    document.getElementById("result").innerText = "Processing...";

    const response = await fetch("/command", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            command: command
        })
    });

    const data = await response.json();

    document.getElementById("result").innerText =
        data.response;

    speak(data.response);
}


function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "Speech recognition is not supported in this browser. Try Google Chrome."
        );

        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult = function(event) {

        const command =
            event.results[0][0].transcript;

        document.getElementById("command").value =
            command;

        sendCommand(command);
    };

    recognition.onerror = function() {

        document.getElementById("result").innerText =
            "Could not understand your voice.";
    };
}

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/command", methods=["POST"])
def command():

    data = request.get_json()

    user_command = data.get("command", "").lower().strip()

    if not user_command:
        return jsonify({
            "response": "Please enter a command."
        })


    # Greeting
    if any(word in user_command for word in
           ["hello", "hi", "hey"]):

        response = "Hello! How can I help you?"


    # Time
    elif "time" in user_command:

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        response = f"The current time is {current_time}."


    # Date
    elif "date" in user_command:

        current_date = datetime.now().strftime(
            "%B %d, %Y"
        )

        response = f"Today's date is {current_date}."


    # Weather
    elif (
        "weather" in user_command
        or "temperature" in user_command
    ):

        city = user_command

        for phrase in [
            "what is the weather in",
            "what's the weather in",
            "weather in",
            "temperature in",
            "what is the temperature in",
            "what's the temperature in"
        ]:
            city = city.replace(phrase, "")

        city = city.strip()

        if not city:
            response = "Please provide a city."

        elif not WEATHER_API_KEY:
            response = "Weather API is not configured."

        else:

            try:

                url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                )

                params = {
                    "q": city,
                    "appid": WEATHER_API_KEY,
                    "units": "metric"
                }

                result = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                weather = result.json()

                if result.status_code == 200:

                    temperature = weather["main"]["temp"]

                    condition = weather[
                        "weather"
                    ][0]["description"]

                    humidity = weather["main"]["humidity"]

                    response = (
                        f"The weather in {city} is "
                        f"{temperature:.1f} degrees Celsius "
                        f"with {condition}. "
                        f"Humidity is {humidity} percent."
                    )

                else:

                    response = (
                        "I couldn't retrieve the weather."
                    )

            except Exception:

                response = (
                    "Weather service is currently unavailable."
                )


    # Google search
    elif (
        "search" in user_command
        or "look up" in user_command
    ):

        query = user_command

        for phrase in [
            "search",
            "look up"
        ]:
            query = query.replace(
                phrase,
                "",
                1
            )

        query = query.strip()

        if query:

            search_url = (
                "https://www.google.com/search?q="
                + query.replace(" ", "+")
            )

            response = (
                f"Opening Google search for {query}: "
                f"{search_url}"
            )

        else:

            response = "What would you like me to search for?"


    # Custom commands
    elif user_command in custom_commands:

        response = (
            f"Custom command found: "
            f"{custom_commands[user_command]}"
        )


    # General knowledge
    elif any(
        phrase in user_command
        for phrase in [
            "who is",
            "what is",
            "what are",
            "tell me about"
        ]
    ):

        question = user_command

        for phrase in [
            "who is",
            "what is",
            "what are",
            "tell me about"
        ]:
            question = question.replace(
                phrase,
                "",
                1
            )

        question = question.strip()

        try:

            search_url = (
                "https://en.wikipedia.org/w/api.php"
            )

            params = {
                "action": "query",
                "list": "search",
                "srsearch": question,
                "format": "json",
                "srlimit": 1
            }

            result = requests.get(
                search_url,
                params=params,
                timeout=10
            )

            data = result.json()

            results = data.get(
                "query",
                {}
            ).get(
                "search",
                []
            )

            if results:

                title = results[0]["title"]

                summary_url = (
                    "https://en.wikipedia.org/api/rest_v1/page/summary/"
                    + requests.utils.quote(title)
                )

                summary = requests.get(
                    summary_url,
                    timeout=10
                ).json()

                response = summary.get(
                    "extract",
                    "I couldn't find an answer."
                )

                if len(response) > 600:
                    response = response[:600] + "."

            else:

                response = "I couldn't find information about that."

        except Exception:

            response = "Knowledge service is unavailable."


    else:

        response = (
            "I don't understand that command yet."
        )


    return jsonify({
        "response": response
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )