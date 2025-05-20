from flask import Flask, render_template, request
from groq import Groq
import os

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

# Get your API key at https://console.groq.com/keys. Set it as an environment variable GROQ_API_KEY or replace 'Your_api_key_here'.
bot = GroqChatBot(os.environ.get("GROQ_API_KEY", "Your_api_key_here"))

@app.route('/')
def index():
    return render_template('index.html')

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
