import whisper
import wave
import struct
from pvrecorder import PvRecorder
from pynput import keyboard


class Transcriber:
    def __init__(self):
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.model = whisper.load_model('base.en')
        self.audio = []
        self.file = "record.wav"
        self.prompt = "No Audio File Detected"
        self.stop_recording = False

    def on_press(self, key):
        try:
            if key == keyboard.Key.space:
                self.stop_recording = True
                print("Space key pressed. Sending recording...\n")
        except Exception as e:
            print(f"Error: {e}")

    def record(self):
        self.audio = []  # reset audio recording
        self.stop_recording = False
        print("Press SPACE to stop recording...")

        self.recorder.start()

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        while not self.stop_recording:
            frame = self.recorder.read()
            self.audio.extend(frame)

        self.recorder.stop()
        listener.stop()

        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))

    def transcribe(self):  # utilises whisper to translate audio file to text
        result = self.model.transcribe(self.file, fp16=False)
        self.prompt = result['text']
        return self.prompt
