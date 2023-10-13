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
bot = commands.Bot(command_prefix='!')

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
    await ctx.send(f'Successfully created {num_teams} teams!')

async def read_message(message):
    if message.author == bot.user:
        return

    words = "Team created with team name"

    if message.content.startwith(words):
        await message.channel.send("Team name received.")
        team_name = message.content[len("Team created with team name"):].strip()
        group_name_list.append(team_name)

async def edit_channel_name():
    for channel in discord.channels:
        for i in range(0,len(group_name_list)):
            new_name = group_name_list[i]
            await channel.edit(name=new_name)


# Run the bot
bot.run(token)