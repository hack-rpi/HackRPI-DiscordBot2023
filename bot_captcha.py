
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

   
    