from decouple import config
import discord
from discord.ext import commands

token = config("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix="!")

spam_count = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    