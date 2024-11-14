from recorder import Transcriber
import socket


host = ''
port = 1212
tscribe = Transcriber()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            tscribe.record()
            transcription = tscribe.transcribe().strip()
            s.sendall(transcription.encode())
            print(transcription)


if __name__ == "__main__":
    main()
