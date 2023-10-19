import discord
from decouple import config
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

spam_dict = {}
timeout_role_id = 123456789  # Replace with your timeout role ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    now = message.created_at.timestamp()

    if user_id in spam_dict:
        last_messages = spam_dict[user_id]
        last_messages = [msg_time for msg_time in last_messages if now - msg_time <= 5]
        
        if len(last_messages) >= 3:
            await message.author.send("You are sending too many messages. You are now in timeout for 2 minutes.")
            timeout_role = message.guild.get_role(timeout_role_id)

            if timeout_role:
                # Remove all the user's roles
                original_roles = message.author.roles
                await message.author.edit(roles=[timeout_role])
                await asyncio.sleep(120)  # Timeout for 2 minutes (120 seconds)

                # Re-add the user's original roles
                await message.author.edit(roles=original_roles)
            
            return  # Prevent further message processing during the timeout
        
        last_messages.append(now)
        spam_dict[user_id] = last_messages
    else:
        spam_dict[user_id] = [now]

    if message.author.roles and any(role.id == timeout_role_id for role in message.author.roles):
        return  # Prevent users in timeout from sending messages

    await bot.process_commands(message)

# Run your bot with your token
token = config("DISCORD_BOT_TOKEN")
bot.run(token)
