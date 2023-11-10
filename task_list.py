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


#Bot receivees message
@bot.event
async def on_message(message):

    author = message.author
    content = message.content

    #If create task
    if content.startswith("$newtask"):
        description = content[9:]

        #Creates new task and adds it to list
        create_task(tasks, description)

    #If "claiming a task"
    if content.startswith("$claimtask"):
        description = content[11:]

        #Assign task with author
        task = tasks.find(description)

        if task is None:
            message.channel.send("Unknown task")
        else:
            task.assign_team(author)
    
    #If view all tasks
    


bot.run(token)
