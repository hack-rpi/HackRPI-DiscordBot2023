from decouple import config
from task import Task, TaskList, create_task
from ticket import create_ticket as create
from discord import client
from discord.ext import commands 
from discord.ext.commands import has_permissions, MissingPermissions
import discord

# Connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
token = config("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)

# List of all tasks
tasks = TaskList()

# Initialize server
@bot.event
async def on_ready():
    print("Bot is online and ready to manage tasks!")

# Helper function to print all tasks
@bot.command()
async def print_tasks(ctx):
    msg = "Current Tasks:\n"
    for task in tasks:
        task_description = task.task
        team_in_charge = task.team_in_charge
        team_to_display = "Unclaimed"
        if team_in_charge is not None:
            team_to_display = team_in_charge
        msg += f"Team: {team_to_display} ---- Task: {task_description}\n"
    await ctx.send(msg)

# Bot receives a message
@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel

    if content.startswith("$newtask"):
        description = str(content[9:])
        create_task(tasks, description)

    if content.startswith("$claimtask"):
        description = str(content[11:])
        task = tasks.find(description)
        msg = ""
        if task is None:
            msg = "Unknown task"
        else:
            task.assign_team(author)
            msg = f"Task '{description}' claimed by {author}"
        await channel.send(msg)

    if content.startswith("$alltasks"):
        await print_tasks(channel)

    if content.startswith("$resolvetask"):
        description = str(content[13:])
        task = tasks.find(description)
        if task is None:
            msg = "Unknown task"
        else:
            task.completed()
            msg = f"Completed task '{description}'"
        await channel.send(msg)

    await bot.process_commands(message)  # Ensure commands are processed

bot.run(token)
