from decouple import config
from task import Task, TaskList, create_task
from ticket import create_ticket as create
from discord import client
from discord.ext import commands 
from discord.ext.commands import has_permissions, MissingPermissions
import discord

#Connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
token = config("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)

#List of all tasks
tasks = TaskList()

#Initialize server
@bot.event
async def on_ready():
    print("HELLO!")

#Helper function to print all tasks
@bot.command()
async def print_tasks(channel):

    msg = ""
    #Iterate through all tasks
    for task in tasks:
        task_description = task.task
        team_in_charge = task.team_in_charge
        team_to_display = "Unclaimed"

        if  team_in_charge is not None:
            team_to_display = team_in_charge

        msg += team_to_display + "  ----   " + task_description + "\n"

    await channel.send(msg)

#Bot receivees message
@bot.event
async def on_message(message):

    author = message.author
    content = message.content
    channel = message.channel

    #If create task
    if content.startswith("$newtask"):
        description = str(content[9:])

        #Creates new task and adds it to list
        create_task(tasks, description)

    #If "claiming a task"
    if content.startswith("$claimtask"):
        description = str(content[11:])

        #Assign task with author
        task = tasks.find(description)
        msg = ""

        if task is None:
            msg = "Unknown task"
        else:
            task.assign_team(author)
            msg = "Task claimed by " + str(author)

        await channel.send(msg)

    #If view all tasks
    if content.startswith("$alltasks"):
        print_tasks(channel)

    #If resolve a task
    if content.startswith("$resolvetask"):
        description = str(content[13:])

        #Find this task
        task = tasks.find(description)
        
        #If not found
        if task is None:
            msg = "Unknown task"
        else:
            task.completed()
            msg = "Completed task " + description

        await channel.send(msg)

bot.run(token)
