import os

try:

    os.system("python3 -m pip install pyttsx3")
    os.system("python3 -m pip install git+https://github.com/openai/whisper.git")
    os.system("python3 -m pip install pyaudio")
    os.system("python3 -m pip install wave")
    os.system("python3 -m pip install scipy")
    os.system("python3 -m pip install noisereduce")
    os.system("python3 -m pip install nextcord")
    os.system("python3 -m pip install art")
    print("All packages installed!")

except Exception as e:
    error_message = str(e)
    print("An error occurred while installing packages:", error_message)
