from decouple import config
import discord
from discord.ext import commands

# Get the bot token from the environment variables
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN")

# Create a bot instance
bot = commands.Bot(command_prefix='!',intents = intents)

#creating a list of group name
group_name_list = []


@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')


@bot.command()
async def create_teams(ctx, num_players: int):
    if ctx.author.guild_permissions.administrator:
        # Get the server
        server = ctx.guild

        # Get the list of members
        members = server.members

        # Calculate the number of teams
        num_teams = len(members) // num_players
        await ctx.send(f'Successfully created {num_teams} teams!')

        # Create teams
        for i in range(num_teams):
            # Create a text channel
            text_channel = await server.create_text_channel(f'team-{i + 1}')

            # Create a voice channel
            voice_channel = await server.create_voice_channel(f'team-{i + 1}')

            # Move members to the team
            for j in range(num_players):
                member = members.pop()
                await member.move_to(text_channel)
                await member.move_to(voice_channel)

            await text_channel.send(f'Team-{i + 1} has been created, and members have been assigned.')
    else:
        print('Sorry you have not right to create channels.')

async def read_message(message):
    if message.author == bot.user:
        return

    words = "Successfully joined team"

    if message.content.startwith(words):
        await message.channel.send("Team name received.")
        team_name = message.content[len("Team created with team name"):].strip()
        group_name_list.append(team_name)
        await assign_groups(message)

async def assign_groups(ctx):
    text_channels = [channel for channel in ctx.guild.text_channels]
    voice_channels = [channel for channel in ctx.guild.voice_channels]

    """# Check if there are enough text and voice channels to form groups
    if len(text_channels) < 1 or len(voice_channels) < 1:
        await ctx.send("Not enough channels to create groups.")
        return"""

    # Create groups by pairing a text channel and a voice channel
    groups = list(zip(text_channels, voice_channels))
    guild = ctx.guild
    # Create the channel
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }

    # Assign names to the groups
    for index, (text_channel, voice_channel) in enumerate(groups):
        group_name = group_name_list[index]
        allowed_roles = [discord.utils.get(guild.roles, name=group_name), discord.utils.get(guild.roles, name='RoleName2')]

        for role in allowed_roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True)
            
        await text_channel.edit(name=group_name)
        await voice_channel.edit(name=group_name)

        await ctx.send(f'Assigned name "{group_name}" to group {index + 1}.')

# Run the bot
bot.run(token)