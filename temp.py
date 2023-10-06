from decouple import config
token = config("DISCORD_BOT_TOKEN")
import discord
from discord.ext import commands

# Create a bot instance
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')


@bot.command()
async def create_teams(ctx, num_players: int):
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
            await member.move_to(voice_channel)

        await text_channel.send(f'Team-{i + 1} has been created, and members have been assigned.')

    await ctx.send(f'Successfully created {num_teams} teams!')


# Run the bot
bot.run(token)