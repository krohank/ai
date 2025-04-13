from flask import Flask, render_template, request, jsonify
from Backend.Chatbot import ChatBot
from Backend.SpeechToText import SpeechRecognition
from Backend.TextToSpeech import TextToSpeech
import threading
import os

app = Flask(__name__)

# Keep your existing backend functions
@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    # Your existing logic
    response = ChatBot(user_input)
    TextToSpeech(response)  # Optional for web
    
    return jsonify({
        'response': response,
        'status': 'success'
    })

@app.route('/voice', methods=['POST'])
def voice_input():
    # Web-compatible voice processing
    audio_file = request.files['audio']
    audio_path = "static/temp_audio.webm"
    audio_file.save(audio_path)
    
    text = SpeechRecognition(audio_path)
    os.remove(audio_path)
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
