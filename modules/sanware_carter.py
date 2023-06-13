# Sanware

from modules.libraries import *

def SendToCarter(sentence, User, APIkey):

    original = sentence

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
    ResponseOutput = str(FullResponse)
    User = str(User)

    ResponseOutput = ResponseOutput.replace("Unknown person", User)
    ResponseOutput = ResponseOutput.replace("Unknown Person", User)
    ResponseOutput = ResponseOutput.replace("unknown person", User)
    ResponseOutput = ResponseOutput.replace("Player", User)
    ResponseOutput = ResponseOutput.replace("player", User)

    f = open("PersonalResponseOutput.txt", "w")
    f.write(f"{ResponseOutput}")
    f.close()

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    system_times = os.times()
    current_time = system_times[4]
    current_time_str = time.ctime(current_time)
    print("Current time: ", current_time_str)

    sentence = str(sentence)
    original = str(sentence)

    device = torch.device('cpu')

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    type(sentence)

    if type(sentence) == str:
        sentence = tokenize(sentence)
    else:
        return

    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    ConfidenceRate = prob.item()

    ResponseOutput = ResponseOutput.replace("Unknown person", "Boss")
    ResponseOutput = ResponseOutput.replace("Unknown Person", "Boss")
    ResponseOutput = ResponseOutput.replace("unknown person", "Boss")
    ResponseOutput = ResponseOutput.replace("Player", "Boss")
    ResponseOutput = ResponseOutput.replace("player", "Boss")

    if prob.item() > 0.95:
            target_class = None
            for intent_class in intents['intents']:
                if intent_class.get("tag") == tag:
                    target_class = intent_class
                    with open("Function.txt", "w") as f:
                        f.write(str(intent_class.get("tag")))
                    print(intent_class.get("tag"))
                    break

            ResponseOutput = ResponseOutput.replace(User, "")
            print(ResponseOutput)

            if target_class:
                    target_class.setdefault("patterns", []).append(original)
                    target_class.setdefault("responses", []).append(ResponseOutput)
            else:
                    new_class = {
                            "tag": User,
                            "patterns": [sentence],
                            "responses": [ResponseOutput]
                            }
                    intents['intents'].append(new_class)

            with open("intents.json", 'w') as json_file:
                json.dump(intents, json_file, indent=4, separators=(',', ': '))

            with open("CarterResponse.txt", "w") as f:
                f.write(ResponseOutput)

def VoiceCommand(UIName, User):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    seconds = 3.8
    filename = "audio.wav"
    threshold = 5000

    p = pyaudio.PyAudio()

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
