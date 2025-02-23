from openai import OpenAI

class SpeechToText:
    def __init__(self):
        self.client = OpenAI()
    
    def transcribe(self, file_path):
        audio_file = open(file_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        print(transcription.text)
        return transcription.text