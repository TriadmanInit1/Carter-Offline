# Carter Offline

Carter Offline is an intent classifier which is based on a modified version of Janex, and utilises LazyLyrics' Carter-Py library.

It compares the input you send to your carter agent with a list of patterns in your chosen intents file, and then remembers the class. Once your Carter agent creates a response, the program saves the response to your intents, recording the interaction and improving your intents dataset.

See also:

```
https://github.com/LazyLyrics/carter-py
https://github.com/Cipher58/Janex
```

<h3> How to use </h3>

<h5> Adding to your project </h5>

Firstly, you'll need to install the library using the Python pip package manager.

```
python3 -m pip install Carter-Offline
```
Secondly, you need to import the library into your Python script.

```
from CarterOffline import *
```

<h4>Using Carter-Offline in your code</h4>

<h5>Define Variables</h5>

To use this program, you will need to define your API key, name and intent file path.

```
CarterAPI = "YOUR CARTER AGENT'S API"

input_string = "Hello!" # for example

User = "YOUR NAME"

# Create an instance of the CarterOffline class

CarterOffline = CarterOffline(intents_file_path, CarterAPI)
```

<h5>Speak to your agent</h5>

Here is the simple bit of code that sends the message to your Carter agent using the Carter-Py library, and then uses the Janex code to classify it, and save it to your intents file.

```
ResponseOutput = SendToCarter(CarterAPI, input_string, User)

print(ResponseOutput)

```
