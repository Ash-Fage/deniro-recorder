import whisper
import wave
import struct
import time
from pvrecorder import PvRecorder


class Transcriber:
    def __init__(self):
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.model = whisper.load_model('base.en')
        self.audio = []
        self.file = "record.wav"
        self.recording = False
        self.prompt = "No Audio File Detected"

    def record(self):
        self.audio = []  # reset audio recording

        print("Recording for 1 minute...")

        self.recorder.start()

        # Record for 60 seconds
        start_time = time.time()
        while True:
            frame = self.recorder.read()  # Read audio frame from recorder
            self.audio.extend(frame)  # Add audio frame to array

            # Stop recording after 60 seconds
            if time.time() - start_time >= 60:
                break  # Exit the loop after 60 seconds

        self.recorder.stop()  # Stop the recorder after time limit is reached

        print("Recording Stopped\n")

        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))

    def transcribe(self):  # utilises whisper to translate audio file to text
        result = self.model.transcribe(self.file, fp16=False)
        self.prompt = result['text']
        return self.prompt
