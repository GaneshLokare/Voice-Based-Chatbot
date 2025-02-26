import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO
from dotenv import load_dotenv
from modules.speech_to_text import SpeechToText
from modules.gpt_responder import GPTResponder
from modules.text_to_speech import TextToSpeech
import time
import uuid
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize modules
stt = SpeechToText()
gpt = GPTResponder()
tts = TextToSpeech()

# Create directories if they don't exist
os.makedirs('static/audio/input', exist_ok=True)
os.makedirs('static/audio/output', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    # Generate unique file names
    session_id = str(uuid.uuid4())
    input_path = f"static/audio/input/{session_id}.webm"
    output_path = f"static/audio/output/{session_id}.mp3"
    
    try:
        # Save the received audio file
        audio_file.save(input_path)
        
        # Process audio through the pipeline
        text = stt.transcribe(input_path)
        response = gpt.get_response(text)
        tts.synthesize(response, output_path)
        
        # Send response to client
        return jsonify({
            'userText': text,
            'aiResponse': response,
            'audioUrl': output_path,
            'sessionId': session_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(filename)

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    try:
        session_id = request.json.get('sessionId')
        
        if not session_id:
            return jsonify({'error': 'No session ID provided'}), 400
        
        input_path = f"static/audio/input/{session_id}.webm"
        output_path = f"static/audio/output/{session_id}.mp3"
        
        # Delete input file if it exists
        if os.path.exists(input_path):
            os.remove(input_path)
        
        # Delete output file if it exists
        if os.path.exists(output_path):
            os.remove(output_path)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)