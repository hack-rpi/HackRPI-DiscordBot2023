from decouple import config
import discord
from discord.ext import commands
from captcha.image import ImageCaptcha
import random
import io
import os
from PIL import Image
import asyncio

token = config("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
captcha_generator = ImageCaptcha()

captchas = {}

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.event
async def on_member_join(member):
    await send_captcha(member)

async def send_captcha(member):
    data = ''.join(random.choices('ABCDEFGHJKMNPQRSTUVWXYZabcdefghkmnpqrstuvwxyz123456789', k=5))
    
    # Generate the captcha image and save its content to a BytesIO object
    captcha_image = captcha_generator.generate(data)
    
    # Convert the BytesIO object to bytes
    captcha_bytes = captcha_image.getvalue()

    # Save the bytes to a temporary file
    temp_file = f"captcha_{member.id}.png"
    with open(temp_file, "wb") as f:
        f.write(captcha_bytes)

    captchas[member.id] = data

    dm_channel = await member.create_dm()

    # Open the saved image using PIL, then close it immediately after
    image = Image.open(temp_file)
    image.close()

    # Create a discord.File object from the saved file
    file = discord.File(fp=temp_file, filename="captcha.png")

    embed = discord.Embed(title="Verification", description="Solve the CAPTCHA to get verified!")
    await dm_channel.send(embed=embed, file=file)

    timeout = 300  # 5 minutes
    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < timeout:
        try:
            # Wait for the user's response in DM
            response = await bot.wait_for('message', check=lambda m: m.author == member and isinstance(m.channel, discord.DMChannel), timeout=timeout)
            
            # Check the response against the stored CAPTCHA data
            if response.content == captchas[member.id]:
                # Assign the role and send the welcome message
                role = discord.utils.get(member.guild.roles, name="Verified")
                await member.add_roles(role)
                await dm_channel.send(f"Welcome {member.mention}, you are now verified and have been given the 'Verified' role!")
                del captchas[member.id]
                return
            else:
                await dm_channel.send(f"Sorry {member.mention}, that's incorrect. Please try the CAPTCHA again.")
                timeout -= (asyncio.get_event_loop().time() - start_time)  # Deduct the elapsed time from the total timeout
        except asyncio.TimeoutError:
            await dm_channel.send(f"Verification timed out. Please request a new CAPTCHA if you wish to verify.")
            return

    os.remove(temp_file)  # Remove the temporary file outside the loop

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the message is from a guild
    if message.guild is None:
        return

    if message.author.id in captchas:
        if message.content == captchas[message.author.id]:
            await message.author.send(f"Welcome {message.author.mention}, you are now verified!")
            role = discord.utils.get(message.guild.roles, name="Verified")
            await message.author.add_roles(role)
            del captchas[message.author.id]
        else:
            await message.author.send(f"{message.author.mention}, that's incorrect. Please try again.")

bot.run(token)