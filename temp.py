from decouple import config
import discord
from discord.ext import commands

# Get the bot token from the environment variables
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN", default = 'MTE1NDQ2MTAyMzUyMTIxMDM4OA.GiCzKZ.gnM4Fq0P1CF4cLeF-EQ1AazikKi-w4QQ6URm8A')

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