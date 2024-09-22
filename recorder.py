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
        self.recording = False
        self.prompt = "No Audio File Detected"

    def on_press(self, key):  # used to toggle recording status when shift is pressed
        if key == keyboard.Key.shift:
            if self.recording:
                self.recording = False
            else:
                self.recording = True

    def record(self):
        self.audio = []  # reset audio recording

        print("Press SHIFT to start and stop recording")

        with keyboard.Listener(on_press=self.on_press) as listener:  # creates a new  keyboard listener
            while True:  # loop will execute until some audio has been recorded
                if self.recording:
                    print("Recording...")
                    self.recorder.start()

                    while self.recording:  # will loop until shift is pressed and recording status changed
                        frame = self.recorder.read()  # reads audio frame from recorder
                        self.audio.extend(frame)  # adds audio frame to array

                    break

                if self.audio:  # terminates loop after any audio has been recorded
                    self.recorder.stop()
                    break

            listener.stop()  # terminates keyboard listener

        print("Recording Stopped\n")

        with wave.open(self.file, 'wb') as f:
            params = (1, 2, 16000, 512, 'NONE', 'not compressed')
            f.setparams(params)
            f.writeframes(struct.pack('h' * len(self.audio), *self.audio))

    def transcribe(self):  # utilises whisper to translate audio file to text
        result = self.model.transcribe(self.file, fp16=False)
        self.prompt = result['text']
        return self.prompt
