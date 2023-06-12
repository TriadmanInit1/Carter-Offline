# Sanware Framework MK III - Branch 'Carter-Discord Boilerplate'

# Boilerplate for linking Discord bot with a Carter API. Written by TheMechanic57.

# Load packages.

from modules.sanware_carter import *

DisplayName(UIName)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Program

@client.event
async def on_message(message):
    # Script is below.

    Respond = False

    if message.author == client.user:
        return

    User = message.author
    sentence = message.content
    sentence = sentence.lower()
    WakeWord = UIName[1:]

    if WakeWord in sentence:
        Respond = True
    elif isinstance(message.channel, discord.channel.DMChannel):
        Respond = True
    else:
        pass

    if Respond:
        await message.channel.trigger_typing()
        SendToCarter(sentence, User, APIkey)
        with open('CarterResponse.txt') as f:
            ResponseOutput = f.read()

        print(message.content)
        await message.channel.send(f"{ResponseOutput}")
        print(ResponseOutput)
        os.remove("CarterResponse.txt")

client.run(DiscordAPI)
