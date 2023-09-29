from decouple import config
token = config("DISCORD_BOT_TOKEN")
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.channels = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def create_team_channel(ctx, team_name):
    # Check if the command is run by an administrator or someone with appropriate permissions.
    if ctx.author.guild_permissions.administrator:
        # Create a text channel in the server's default category.
        category = None
        for cat in ctx.guild.categories:
            if cat.name == 'Default Category Name':  # Replace 'Default Category Name' with the actual name of your default category.
                category = cat
                break

        if category is not None:
            await category.create_text_channel(team_name)
            await ctx.send('Channel {} created successfully in the default category!'.format(team_name))
        else:
            await ctx.send("Default category not found. You may need to specify the correct category name.")

    else:
        await ctx.send('You do not have permission to create channels.')

bot.run("YOUR_TOKEN_HERE")
