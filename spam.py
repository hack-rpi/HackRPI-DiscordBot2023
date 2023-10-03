from decouple import config
import discord
import asyncio
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
    

    author_id = str(message.author.id)
    if author_id in spam_count:
        spam_count[author_id] += 1
    else:
        spam_count[author_id] = 1


    if spam_count[author_id] > 5:
        await message.author.send("You are spamming. Please stop.")
        await message.author.add_roles(discord.utils.get(message.author.guild.roles, name="Timeout"))
        await message.author.send("You have been timed out for 10 minutes.")
        await message.delete()
        await asyncio.sleep(600) 
        await message.author.remove_roles(discord.utils.get(message.author.guild.roles, name="Timeout"))
        del spam_count[author_id]

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(token)
