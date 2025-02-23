from flask import Flask, render_template, request, send_file, jsonify
import os
from dotenv import load_dotenv
from modules.speech_to_text import SpeechToText
from modules.gpt_responder import GPTResponder
from modules.text_to_speech import TextToSpeech
import uuid
import time

load_dotenv()


app = Flask(__name__)


# Initialize modules
stt = SpeechToText()
gpt = GPTResponder()
tts = TextToSpeech()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_audio():
    # Save uploaded audio
    audio_file = request.files['audio']
    unique_id = str(uuid.uuid4())
    input_path = f"temp_{unique_id}.mp3"
    output_path = f"response_{unique_id}.mp3"
    
    audio_file.save(input_path)
    
    # Process audio
    text = stt.transcribe(input_path)
    response = gpt.get_response(text)
    tts.synthesize(response, output_path)
    
    # Cleanup input file
    os.remove(input_path)
    
    return send_file(output_path, as_attachment=True, mimetype='audio/mpeg')




if __name__ == '__main__':
    app.run(debug=True)