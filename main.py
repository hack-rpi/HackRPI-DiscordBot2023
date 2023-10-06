from decouple import config
import discord
from discord.ext import commands
from datetime import timedelta


def check_profanity(sentence):
    bad_words = set()

    # Specify the file path
    file_path = "profanity-list.txt"  # Replace with the path to your file
    # Open the file and append its contents to the set
    with open(file_path, "r") as file:
        for line in file:
            # Assuming each line in the file contains a single item to add to the set
            item = line.strip()  # Remove leading/trailing whitespace
            bad_words.add(item)
    words = sentence.split()
    sentence_set = set(words)
    # word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

    # for word in word_list:
    #     if(sentence == word):
    #     # If a word from the list is found, send a response
    #         return word    
    return sentence_set.intersection(bad_words)

if __name__ =='__main__':
    # Define your intents
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.messages = True
    intents.message_content = True
    token = config("DISCORD_BOT_TOKEN")


    # Initialize the bot with the specified intents
    bot = discord.Client(intents=intents)


    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.event
    async def on_message(message):


        # Define a list of channel IDs where you want the function to work
        allowed_channel_ids = [1157414659587063898, 1154875483553529981]  # Replace with your desired channel IDs

        # Check if the message is sent in one of the allowed channels
        if message.channel.id not in allowed_channel_ids:
            print(message.channel.id)
            return  # Exit the function if it's not in an allowed channel
        print("after")
        # Convert the message content to lowercase for case-insensitive matching
        content = message.content.lower().strip()

        # Check if any word in the list is in the message content
        if message.author == bot.user:
            return
        if content.startswith("!"):
            return
        profanity = check_profanity(content)
        print(profanity)    
        if(len(profanity) != 0 ) : 
        #     await message.channel.send("Clean message")
        # else:
            curses = ""
            for badWord in profanity:
                curses += badWord + ", "
            user = message.author
            dm_channel = await user.create_dm()
            await dm_channel.send(f"Words like " + curses.rstrip()+" aren't allowed.")
            # await message.channel.send(f"Profanity isn't allowed.")

    bot.run(token)


