# Sanware

import requests
import json
from ai_config import *
import pyttsx3

import whisper
import pyaudio
import wave

from scipy.io import wavfile
import noisereduce as nr

import os
import nextcord as discord

from art import text2art

def SendToCarter(sentence, User, APIkey):
    response = requests.post("https://api.carterlabs.ai/chat", headers={
        "Content-Type": "application/json"
    }, data=json.dumps({
        "text": f"{sentence}",
        "key": f"{APIkey}",
        "playerId": f"{User}"
    }))

    RawResponse = response.json()
    Response = RawResponse["output"]
    FullResponse = Response["text"]
    ResponseOutput = FullResponse

    f = open("CarterResponse.txt", "w+")
    f.write(f"{ResponseOutput}")
    f.close()

def VoiceCommand(UIName, User):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    seconds = 3.8
    filename = "audio.wav"
    threshold = 5000  # adjust as needed

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Listening')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Wait for the user to start speaking
    while True:
        data = stream.read(chunk)
        signal = np.frombuffer(data, dtype=np.int16)
        amplitude = np.max(signal)
        if amplitude > threshold:
            break

    print('Recording')

    f = open("VAD.txt", "w")
    f.write("Speech Detected.")
    f.close()

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print(f'{UIName}: I have finished recording.')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    rate, data = wavfile.read("audio.wav")
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("cleaned_audio.wav", rate, reduced_noise)

    model = whisper.load_model("base.en")
    result = model.transcribe("cleaned_audio.wav")
    sentence = result["text"]

    print(f"{User}: {sentence}")

    SendToCarter(sentence, User, APIkey)

def speak(ResponseOutput):
    engine = pyttsx3.init()
    engine.say(ResponseOutput)
    engine.runAndWait()

def DisplayName(UIName):
    ascii_art = text2art(f"{UIName}")
    print(ascii_art)
