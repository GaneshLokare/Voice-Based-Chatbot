from openai import OpenAI
from pathlib import Path

class TextToSpeech:
    def __init__(self, voice="alloy"):
        self.client = OpenAI()
        self.voice = voice
    
    def synthesize(self, text, output_path):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text,
        )
        response.stream_to_file(output_path)
        return output_path