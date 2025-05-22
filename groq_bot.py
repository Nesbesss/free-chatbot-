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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            background: linear-gradient(to right, #83a4d4, #b6fbff); /* Gradient background */
            margin: 0;
            padding: 20px; /* Added padding for overall spacing */
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh; /* Use min-height for better responsiveness */
            box-sizing: border-box; /* Include padding in height calculation */
        }

        #chat-container {
            max-width: 600px;
            width: 100%;
            /* Glassmorphism styles */
            background: rgba(255, 255, 255, 0.15); /* Semi-transparent white */
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px); /* Safari support */
            border-radius: 15px; /* Slightly more pronounced radius for glass effect */
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); /* Adjusted shadow for depth */
            display: flex;
            flex-direction: column;
            overflow: hidden; /* Important for backdrop-filter to work on children correctly */
        }

        /* Menu is removed, no styles needed for #menu or #menu button */

        #chat-box {
            padding: 30px; /* Increased padding */
            height: 350px; 
            overflow-y: auto;
            flex: 1;
            background-color: transparent; /* Chat box itself should be transparent */
            color: #333; /* Darker text for readability on light glass */
        }

        /* Custom scrollbar for WebKit browsers */
        #chat-box::-webkit-scrollbar {
            width: 8px;
        }

        #chat-box::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        #chat-box::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }

        #chat-box::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }

        #chat p { 
            margin-bottom: 10px;
            line-height: 1.5;
            color: #111; /* Ensure chat text is dark and readable */
        }
        #chat p:first-child {
             margin-top: 0;
        }


        #controls {
            padding: 15px 25px; 
            display: flex;
            align-items: center;
            /* Glassmorphism for controls bar */
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-top: 1px solid rgba(255, 255, 255, 0.18);
            /* border-bottom-left-radius: 15px; /* Match container if it's the last element visually */
            /* border-bottom-right-radius: 15px; */
        }

        #user-input {
            flex: 1;
            padding: 12px 15px; 
            border: 1px solid rgba(255, 255, 255, 0.3); 
            border-radius: 20px; 
            margin-right: 10px;
            font-size: 16px; 
            background-color: rgba(255, 255, 255, 0.2); /* Slightly transparent input background */
            color: #000; /* Black text for input */
        }

        #user-input::placeholder {
            color: #333; /* Darker placeholder text */
        }
        
        #user-input:focus {
            outline: none;
            border-color: rgba(255, 255, 255, 0.5); /* Brighter border on focus */
            background-color: rgba(255, 255, 255, 0.3);
        }

        #send-button, .action-button { 
            padding: 10px 20px;
            background-color: #007bff; /* Solid color for primary buttons to stand out */
            color: #fff;
            border: none;
            border-radius: 20px; 
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
        }

        #send-button:hover, .action-button:hover,
        #send-button:focus, .action-button:focus {
            background-color: #0056b3; 
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover/focus */
        }
        
        .secondary-button { 
            padding: 8px 15px;
            background-color: rgba(108, 117, 125, 0.7); /* Slightly transparent secondary button */
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
            margin-left: 10px; 
        }

        .secondary-button:hover, .secondary-button:focus {
            background-color: rgba(84, 91, 98, 0.8);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* Enhanced shadow on hover/focus */
        }

        #settings {
            padding: 15px 25px; 
            display: flex;
            justify-content: space-between;
            align-items: center;
            /* Glassmorphism for settings area */
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-top: 1px solid rgba(255, 255, 255, 0.18);
            color: #333; /* Darker text for settings */
        }

        #settings label {
            margin-right: 8px;
            font-size: 14px;
            color: #111; /* Ensure labels are dark and readable */
        }

        #settings select {
            padding: 8px 10px;
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            font-size: 14px;
            background-color: rgba(255, 255, 255, 0.2);
            color: #000; /* Black text for select */
        }
        
        #settings > div { 
            display: flex;
            align-items: center;
        }

        #calculator {
            padding: 20px;
            display: none; 
            /* Glassmorphism for calculator area */
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-top: 1px solid rgba(255, 255, 255, 0.18);
            color: #333; /* Darker text for calculator */
        }

        #calculator input, #calculator button {
            padding: 10px;
            margin: 5px 0; 
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            font-size: 14px;
        }
        #calculator input {
            width: calc(100% - 22px); 
            background-color: rgba(255, 255, 255, 0.2);
            color: #000; /* Black text for calculator input */
        }
        #calculator button {
            background-color: #28a745; /* Keep calculate button solid green */
            color: white;
            cursor: pointer;
            transition: background-color 0.2s ease, box-shadow 0.2s ease; /* Added transition */
        }
        #calculator button:hover, #calculator button:focus {
            background-color: #1e7e34; /* Darker green on hover/focus */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* Shadow on hover/focus */
        }

        #calc-result {
            margin-top: 10px;
            font-weight: bold;
            color: #111; /* Ensure calc result is dark and readable */
        }

        /* Removed speech-toggle styles as element is gone */
    </style>
</head>
<body>
    <div id="chat-container">
        <!-- Menu is removed -->
        <div id="chat-box">
            <div id="chat"></div>
        </div>
        <div id="controls">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-button" onclick="sendMessage()">Send</button>
            <button class="secondary-button" onclick="toggleCalculator()">Calculator</button> <!-- New Calculator Toggle Button -->
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
        <div id="calculator">
            <input type="text" id="calc-input" placeholder="Enter expression...">
            <button onclick="calculate()">Calculate</button>
            <div id="calc-result"></div>
        </div>
    </div>
    <script>
        function toggleCalculator() { // Renamed and updated function
            var calculator = document.getElementById('calculator');
            var chatBox = document.getElementById('chat-box');
            var controls = document.getElementById('controls'); // Get the controls element
            if (calculator.style.display === 'none' || calculator.style.display === '') {
                calculator.style.display = 'block';
                chatBox.style.display = 'none'; 
                controls.style.display = 'none'; // Hide controls when calculator is open
            } else {
                calculator.style.display = 'none';
                chatBox.style.display = 'block'; 
                controls.style.display = 'flex'; // Show controls (as flex) when calculator is closed
            }
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
            });
        }

        document.getElementById('user-input').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });

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
