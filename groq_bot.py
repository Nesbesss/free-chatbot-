from flask import Flask, render_template_string, request
from groq import Groq

app = Flask(__name__)

class GroqChatBot:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.messages = []

    def chat(self, user_message, friendliness, language_style):
        self.messages.append({"role": "user", "content": user_message})
        self.messages.append({"role": "system", "content": f"Respond in a {friendliness} tone and use {language_style} language."})
        
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model="llama3-70b-8192"
        )
        bot_response = chat_completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response

bot = GroqChatBot("Your_api_key_here") #get one at https://console.groq.com/keys, they are fully free (for now)!

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
            background-color: #e0f7fa;
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
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        #menu {
            background-color: #00796b;
            color: white;
            padding: 10px;
            display: flex;
            justify-content: space-around;
        }

        #menu button {
            background: none;
            border: none;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: color 0.3s;
        }

        #menu button:hover {
            color: #b2dfdb;
        }

        #chat-box {
            padding: 20px;
            height: 300px;
            overflow-y: auto;
            flex: 1;
        }

        #controls {
            padding: 20px;
            display: flex;
            align-items: center;
            border-top: 1px solid #ddd;
        }

        #user-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 20px;
            margin-right: 10px;
        }

        #send-button {
            padding: 10px 20px;
            background-color: #00796b;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        #send-button:hover {
            background-color: #004d40;
        }

        #settings {
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid #ddd;
        }

        #calculator {
            padding: 20px;
            display: none;
        }

        #calculator input, #calculator button {
            padding: 10px;
            margin: 5px;
        }

        #speech-toggle {
            background-color: #00796b;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            padding: 10px;
            margin-top: 10px;
        }

        #speech-toggle:hover {
            background-color: #004d40;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="menu">
            <button onclick="showChat()">Chat</button>
            <button onclick="showCalculator()">Calculator</button>
        </div>
        <div id="chat-box">
            <div id="chat"></div>
        </div>
        <div id="controls">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-button" onclick="sendMessage()">Send</button>
        </div>
        <div id="settings">
            <div>
                <label for="friendliness">Friendliness:</label>
                <select id="friendliness">
                    <option value="friendly">Friendly</option>
                    <option value="neutral">Neutral</option>
                    <option value="formal">Formal</option>
                </select>
            </div>
            <div>
                <label for="language-style">Language Style:</label>
                <select id="language-style">
                    <option value="kids">Kids</option>
                    <option value="work">Work</option>
                    <option value="general">General</option>
                </select>
            </div>
        </div>
        <button id="speech-toggle" onclick="toggleSpeech()">Toggle Speech</button>
        <div id="calculator">
            <input type="text" id="calc-input" placeholder="Enter expression...">
            <button onclick="calculate()">Calculate</button>
            <div id="calc-result"></div>
        </div>
    </div>
    <script>
        var conversationMode = false;
        var speechEnabled = true;

        function showChat() {
            document.getElementById('chat-box').style.display = 'block';
            document.getElementById('controls').style.display = 'flex';
            document.getElementById('calculator').style.display = 'none';
        }

        function showCalculator() {
            document.getElementById('chat-box').style.display = 'none';
            document.getElementById('controls').style.display = 'none';
            document.getElementById('calculator').style.display = 'block';
        }

        function sendMessage() {
            var userMessage = document.getElementById('user-input').value;
            var friendliness = document.getElementById('friendliness').value;
            var languageStyle = document.getElementById('language-style').value;
            document.getElementById('user-input').value = '';
            document.getElementById('chat').innerHTML += `<p>You: ${userMessage}</p>`;
            fetch('/submit_message', {
                method: 'POST',
                body: JSON.stringify({ user_message: userMessage, friendliness: friendliness, language_style: languageStyle }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('chat').innerHTML += `<p>Bot: ${data.bot_response}</p>`;
                if (speechEnabled) {
                    speak(data.bot_response);
                }
            });
        }

        document.getElementById('user-input').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });

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

        function toggleSpeech() {
            speechEnabled = !speechEnabled;
            alert(`Speech ${speechEnabled ? "enabled" : "disabled"}.`);
        }

        function calculate() {
            var expression = document.getElementById('calc-input').value;
            try {
                var result = eval(expression);
                document.getElementById('calc-result').innerText = "Result: " + result;
            } catch (e) {
                document.getElementById('calc-result').innerText = "Error: Invalid Expression";
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
    data = request.json
    user_message = data['user_message']
    friendliness = data['friendliness']
    language_style = data['language_style']
    bot_response = bot.chat(user_message, friendliness, language_style)
    return {'user_message': user_message, 'bot_response': bot_response}

if __name__ == '__main__':
    app.run(debug=True)
