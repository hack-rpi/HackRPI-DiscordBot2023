from decouple import config
from collections import deque
from discord.ext import commands
import discord
import asyncio
import time


token = config("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!", intents = intents)


spam_count = {}
last_messages = {} 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    author_id = str(message.author.id)

    if author_id not in last_messages:
        last_messages[author_id] = deque(maxlen=3)

    last_messages[author_id].append(time.time())

    if len(last_messages[author_id]) == 3 and (time.time() - last_messages[author_id][0]) <= 5:
        if author_id in spam_count:
            spam_count[author_id] += 1
        else:
            spam_count[author_id] = 1

        if spam_count[author_id] > 3:
            await message.author.send("You are spamming. Please stop.")
            timeout_role = discord.utils.get(message.author.guild.roles, name="Timeout")
            await message.author.add_roles(timeout_role)

            original_roles = message.author.roles.copy()

            for role in original_roles:
                if role != timeout_role:
                    print(role)
                    await message.author.remove_roles(role)

            await message.author.send("You have been placed in timeout for 2 minutes.")
            await message.delete()
            await asyncio.sleep(120) 


            await message.author.remove_roles(timeout_role)
            for role in original_roles:
                await message.author.add_roles(role)

            spam_count.pop(author_id, None)

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(token)
