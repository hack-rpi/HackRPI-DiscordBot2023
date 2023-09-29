import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from decouple import config


# Load environment variables from a .env file
load_dotenv()

# Get the bot token from the environment variables
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN")


    # Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define a simple command
@bot.command()
async def test(ctx):
    await ctx.send('Congrat\'s bud, it worked :)')

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot with your token
bot.run(token)
