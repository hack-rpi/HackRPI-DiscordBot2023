
from decouple import config
import discord
from discord.ext import commands, tasks
from captcha.image import ImageCaptcha
import random
import io
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
    channel = member.guild.system_channel  
    return

    await send_captcha(member, channel)

async def send_captcha(member, channel):
    
    data = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    image = captcha_generator.generate(data)
    image_data = io.BytesIO()
    image.save(image_data, format="PNG")
    image_data.seek(0)

   
    captchas[member.id] = data

   
   
    file = discord.File(fp=image_data, filename="captcha.png")
    embed = discord.Embed(title="Verification", description="Solve the CAPTCHA to get verified!")
    message = await channel.send(embed=embed, file=file, components=[[
        discord.ui.Button(style=discord.ButtonStyle.green, label="I'm Human", custom_id="verify_me")
    ]])

   
    try:
        interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id == "verify_me" and i.user == member, timeout=120)
        await interaction.response.send_message("Please type the CAPTCHA content to verify!", ephemeral=True)
    except TimeoutError:
        await message.edit(content="CAPTCHA verification time expired. Please request a new CAPTCHA if you wish to verify.", components=[])

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author.id in captchas:
        if message.content == captchas[message.author.id]:
            await message.channel.send(f"Welcome {message.author.mention}, you are now verified!")
            role = discord.utils.get(message.guild.roles, name="Verified")
            await message.author.add_roles(role)
            del captchas[message.author.id]
        else:
            await message.channel.send(f"{message.author.mention}, that's incorrect. Please try again.")

bot.run(token)
