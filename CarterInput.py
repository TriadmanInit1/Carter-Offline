from modules.sanware_carter import *
from ai_config import *


def CarterInput(sentence):

    sentence = input(f"{User}: ")
    SendToCarter(sentence, User, APIkey)

    with open("CarterResponse.txt") as f:
        ResponseOutput = f.read()

    print(ResponseOutput)

    speak(ResponseOutput)

sentence = input(f"{User}: ")
CarterInput(sentence)
