import pyaudio
import wave
import pyttsx3



def record():

    # Set the parameters for the audio recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "media/input/test.wav"

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a streaming stream to record audio
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    engine = pyttsx3.init()
    engine.say("Recording Started")
    engine.runAndWait()

    print("Recording started...")

    # Create an empty list to store the recorded audio frames
    frames = []

    # Record audio for the specified duration
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio frames to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio recorded and saved as {WAVE_OUTPUT_FILENAME}.")
