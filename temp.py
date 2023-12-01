from decouple import config
import discord
from discord.ext import commands
from dotenv import load_dotenv
import re

load_dotenv()

# Get the bot token from the environment variables
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN")
# Create a bot instance
bot = commands.Bot(command_prefix='?', intents = intents)

#creating a list of group name
group_name_list = []


@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')


@bot.command()
async def create_channels(ctx):
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild

        # Loop through all roles in the server
        for role in guild.roles:
            # Create a new text channel for each role
            text_channel = await guild.create_text_channel(name=role.name)

            # Create a new voice channel for each role
            voice_channel = await guild.create_voice_channel(name=role.name)

            # Set channel overwrites to allow only the role to read messages
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            await text_channel.edit(overwrites=overwrites)
            await voice_channel.edit(overwrites=overwrites)

            await ctx.send(f'Created text and voice channels for role "{role.name}".')

        await ctx.send("Channels have been created for all roles.")
    else:
        await ctx.send('Sorry, you do not have the required permissions to create channels.')


@bot.command()
async def delete_channels(ctx):
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild

        # Loop through all channels in the server
        for channel in guild.channels:
            # Check if the channel is a text or voice channel created by the bot
            if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                # Check if the channel name matches a role's name
                if channel.name in [role.name for role in guild.roles]:
                    # Delete the channel
                    await channel.delete()

        await ctx.send("Channels created for roles have been deleted.")
    else:
        await ctx.send('Sorry, you do not have the required permissions to delete channels.')


async def read_message(message):
    if message.author == bot.user:
        return

    words = "Successfully joined team"
    words2 = "Team Created with "

    if message.content.startswith(words2):
        await message.channel.send("Team name received.")
        team_name = message.content[len("Team Created with name"):].strip()
        group_name_list.append(team_name)
        await assign_groups(message)

    elif message.content.include(words):
        await message.channel.send("Team name received.")
        bot_message = "@user Successfully joined team team_name"
        pattern = r"@(\w+) Successfully joined team (\w+)"
        match = re.search(pattern, bot_message)

        if match:
            user = match.group(1)
            team_name = match.group(2)
        group_name_list.append(team_name)
        await assign_groups(message)

async def assign_groups(ctx):
    guild = ctx.guild
    text_channels = [channel for channel in ctx.guild.text_channels]
    voice_channels = [channel for channel in ctx.guild.voice_channels]

    # Create the groups
    for index, group_name in enumerate(group_name_list):
        # Create a new role for the group
        role = await guild.create_role(name=group_name, reason="Creating group role")

        # Create text and voice channels for the group
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        text_channel = await guild.create_text_channel(name=group_name, overwrites=overwrites)
        voice_channel = await guild.create_voice_channel(name=group_name, overwrites=overwrites)

        await ctx.send(f'Created group "{group_name}" with text and voice channels.')

    await ctx.send("Groups have been created.")

# Run the bot
bot.run(token)