var conversationMode = false;
var speechEnabled = true;

function showChat() {
    document.getElementById('chat-box').style.display = 'block';
    document.getElementById('controls').style.display = 'flex';
    document.getElementById('calculator').style.display = 'none';
}

// function showCalculator() {
//     document.getElementById('chat-box').style.display = 'none';
//     document.getElementById('controls').style.display = 'none';
//     document.getElementById('calculator').style.display = 'block';
// }
// Calculator functionality disabled due to security concerns with eval().

function sendMessage() {
    var userMessage = document.getElementById('user-input').value;
    var friendliness = document.getElementById('friendliness').value;
    var languageStyle = document.getElementById('language-style').value;
    document.getElementById('user-input').value = '';
    document.getElementById('chat').innerHTML += `<div class="message user-message"><p>${userMessage}</p></div>`;
    fetch('/submit_message', {
        method: 'POST',
        body: JSON.stringify({ user_message: userMessage, friendliness: friendliness, language_style: languageStyle }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('chat').innerHTML += `<div class="message bot-message"><p>${data.bot_response}</p></div>`;
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

// function calculate() {
//     var expression = document.getElementById('calc-input').value;
//     try {
//         var result = eval(expression); // Security risk
//         document.getElementById('calc-result').innerText = "Result: " + result;
//     } catch (e) {
//         document.getElementById('calc-result').innerText = "Error: Invalid Expression";
//     }
// }
// Calculator functionality disabled due to security concerns with eval().
