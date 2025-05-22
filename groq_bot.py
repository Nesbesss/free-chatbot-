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
            background: linear-gradient(to right, #400000, #111111); /* Red/Black gradient */
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
            color: #f0f0f0; /* General light text color for the body */
        }

        #chat-container {
            max-width: 600px;
            width: 100%;
            background: rgba(10, 10, 10, 0.25); /* Semi-transparent dark background */
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 50, 50, 0.2); /* Subtle red border */
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4); /* Darker shadow */
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        #chat-box {
            padding: 30px;
            height: 350px; 
            overflow-y: auto;
            flex: 1;
            background-color: transparent;
            color: #e0e0e0; /* Light text for chat box content */
        }

        /* Custom scrollbar for WebKit browsers - Red/Black theme */
        #chat-box::-webkit-scrollbar {
            width: 8px;
        }

        #chat-box::-webkit-scrollbar-track {
            background: rgba(30, 0, 0, 0.1); /* Dark red track */
            border-radius: 10px;
        }

        #chat-box::-webkit-scrollbar-thumb {
            background: rgba(120, 0, 0, 0.6); /* Red thumb */
            border-radius: 10px;
        }

        #chat-box::-webkit-scrollbar-thumb:hover {
            background: rgba(180, 0, 0, 0.8); /* Brighter red thumb on hover */
        }

        #chat p { 
            margin-bottom: 10px;
            line-height: 1.5;
            color: #f0f0f0; /* Light text for chat messages */
        }
        #chat p:first-child {
             margin-top: 0;
        }

        #toggle-settings-button { /* New Settings Button Styling */
            background-color: rgba(50, 0, 0, 0.6); /* Dark red, semi-transparent */
            color: #f0f0f0;
            border: 1px solid rgba(255, 80, 80, 0.4); /* Red-themed border */
            padding: 10px 15px;
            border-radius: 20px; /* Match other buttons */
            cursor: pointer;
            margin-right: 10px; /* Space between it and user-input */
            font-size: 14px; /* Slightly smaller than send button */
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
        }

        #toggle-settings-button:hover, #toggle-settings-button:focus {
            background-color: rgba(80, 0, 0, 0.8); /* Brighter on hover/focus */
            box-shadow: 0 2px 8px rgba(204, 0, 0, 0.25);
        }

        #controls {
            padding: 15px 25px; 
            display: flex;
            align-items: center;
            background: rgba(5, 5, 5, 0.2); /* Slightly darker semi-transparent background */
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-top: 1px solid rgba(255, 50, 50, 0.2); /* Subtle red border */
        }

        #user-input {
            flex: 1;
            padding: 12px 15px; 
            border: 1px solid rgba(255, 50, 50, 0.3); /* Red-themed border */
            border-radius: 20px; 
            margin-right: 10px;
            font-size: 16px; 
            background-color: rgba(0, 0, 0, 0.25); /* Semi-transparent black input background */
            color: #f0f0f0; /* Light text for input */
        }

        #user-input::placeholder {
            color: #bbbbbb; /* Dimmer light color for placeholder */
        }
        
        #user-input:focus {
            outline: none;
            border-color: rgba(255, 80, 80, 0.5); /* Brighter red border on focus */
            background-color: rgba(0, 0, 0, 0.3);
        }

        #send-button, .action-button { 
            padding: 10px 20px;
            background-color: #cc0000; /* Prominent red */
            color: #ffffff; /* White text on button */
            border: none;
            border-radius: 20px; 
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
        }

        #send-button:hover, .action-button:hover,
        #send-button:focus, .action-button:focus {
            background-color: #ff3333; /* Brighter red on hover/focus */
            box-shadow: 0 4px 12px rgba(204, 0, 0, 0.3); /* Red shadow on hover/focus */
        }
        
        /* .secondary-button styles were removed as the button was removed */

        #settings {
            padding: 15px 25px; 
            display: none; /* Hidden by default */
            justify-content: space-between;
            align-items: center;
            background: rgba(5, 5, 5, 0.2); /* Consistent with controls bar */
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-top: 1px solid rgba(255, 50, 50, 0.2); /* Subtle red border */
            color: #f0f0f0; /* Light text for settings */
        }

        #settings label {
            margin-right: 8px;
            font-size: 14px;
            color: #e0e0e0; /* Light text for labels */
        }

        #settings select {
            padding: 8px 10px;
            border-radius: 5px;
            border: 1px solid rgba(255, 50, 50, 0.3); /* Red-themed border */
            font-size: 14px;
            background-color: rgba(0, 0, 0, 0.25); /* Semi-transparent black background */
            color: #f0f0f0; /* Light text for select */
        }
         /* Basic styling for options for better visibility in dark themes, browser support varies */
        #settings select option {
            background-color: #333333; /* Dark background for options */
            color: #f0f0f0; /* Light text for options */
        }
        
        #settings > div { 
            display: flex;
            align-items: center;
        }

        /* Calculator styles removed */
    </style>
</head>
<body>
    <div id="chat-container">
        <!-- Menu is removed -->
        <div id="chat-box">
            <div id="chat"></div>
        </div>
        <div id="controls">
            <button id="toggle-settings-button" onclick="toggleSettings()">Settings</button> <!-- New Settings Button -->
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-button" onclick="sendMessage()">Send</button>
            <!-- Calculator toggle button removed -->
        </div>
        <div id="settings"> <!-- Ensure it's hidden by default via CSS -->
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
        <!-- Calculator HTML structure removed -->
    </div>
    <script>
        // toggleCalculator function removed

        function toggleSettings() {
            var settingsDiv = document.getElementById('settings');
            if (settingsDiv.style.display === 'none' || settingsDiv.style.display === '') {
                settingsDiv.style.display = 'flex'; // Restore to its original display type
            } else {
                settingsDiv.style.display = 'none';
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

        // calculate function removed
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
