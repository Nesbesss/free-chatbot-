from flask import Flask, render_template_string, request
from groq import Groq

app = Flask(__name__)

class GroqChatBot:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.messages = []

    def chat(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model="llama3-70b-8192"
        )
        bot_response = chat_completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response

bot = GroqChatBot("Your_api_key")  # Replace with your actual Groq API key

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Groq Chat Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        #chat-container {
            max-width: 500px;
            width: 100%;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }

        #chat-box {
            padding: 20px;
            height: 300px;
            overflow-y: auto;
        }

        #controls {
            padding: 20px;
            display: flex;
            align-items: center;
        }

        #user-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-right: 10px;
        }

        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="chat-box">
            <div id="chat"></div>
        </div>
        <div id="controls">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
            <button onclick="toggleConversationMode()">Toggle Conversation Mode</button>
        </div>
    </div>
    <script>
        var conversationMode = false;

        function sendMessage() {
            var userMessage = document.getElementById('user-input').value;
            document.getElementById('user-input').value = '';
            document.getElementById('chat').innerHTML += `<p>You: ${userMessage}</p>`;
            fetch('/submit_message', {
                method: 'POST',
                body: JSON.stringify({ user_message: userMessage }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('chat').innerHTML += `<p>Bot: ${data.bot_response}</p>`;
                speak(data.bot_response);
            });
        }

        function startVoiceRecognition() {
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            recognition.start();
            recognition.onresult = function(event) {
                var result = event.results[0][0].transcript;
                document.getElementById('user-input').value = result;
                sendMessage();
            }
            recognition.onerror = function(event) {
                console.error(event.error);
            }
            recognition.onend = function() {
                if (conversationMode) {
                    startVoiceRecognition();
                }
            }
        }

        function speak(message) {
            var synth = window.speechSynthesis;
            var utterance = new SpeechSynthesisUtterance(message);
            utterance.onend = function() {
                if (conversationMode) {
                    startVoiceRecognition();
                }
            }
            synth.speak(utterance);
        }

        function toggleConversationMode() {
            conversationMode = !conversationMode;
            if (conversationMode) {
                startVoiceRecognition();
                alert("Conversation mode enabled.");
            } else {
                alert("Conversation mode disabled.");
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/submit_message', methods=['POST'])
def submit_message():
    user_message = request.json['user_message']
    bot_response = bot.chat(user_message)
    return {'user_message': user_message, 'bot_response': bot_response}

if __name__ == '__main__':
    app.run(debug=True)
