from decouple import config
import discord
from discord.ext import commands


async def check_profanity(sentence):
    word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    for word in word_list:
        if(sentence == word):
        # If a word from the list is found, send a response
            return word


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
        word_list = ["apple", "banana", "cherry"]

        # Convert the message content to lowercase for case-insensitive matching
        content = message.content.lower().strip()

        # Check if any word in the list is in the message content
        profanity = ""
        if message.author == bot.user:
            return
        # for word in word_list:
        #     # await message.channel.send(word)
        #     if(str(content) == word):
        #     # If a word from the list is found, send a response
        #         profanity = word

        profanity = check_profanity(content)
        if(profanity != "") : 
            await message.channel.send("Word isnt allowed, "+ profanity)
        else:
            await message.channel.send("Clean message" + profanity)

 
    bot.run(token)
