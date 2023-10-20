from decouple import config
from ticket import Ticket
from ticket import create_ticket as create
from discord import client
from discord.ext import commands 
from discord.ext.commands import has_permissions, MissingPermissions
from auth import authorized
import discord

#Connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
token = config("DISCORD_BOT_TOKEN")

# Initialize the bot with the specified intents
#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

#Queue of all teams
queue = []

#Bot is ready
@bot.event
async def on_ready():

    assert(len(queue) == 0)
    channel = discord.utils.get(bot.get_all_channels(), name="mentoring-queue")
    await update_queue_in_channel(queue, channel)


#Updates queue in the mentoring-queue channel
@bot.command()
async def update_queue_in_channel(queue, channel):

    #Queue
    msg = ""
    if len(queue) == 0:
        msg = "Empty queue"
    else:
        msg += "Current queue: \n\n"
        for team in queue:
            if team.in_progress == False:
                msg += str(team.name) + ": " + str(team.reason) + "\n"

    #In progress
    msg += "\n\n"
    if len(queue) == 0:
        msg += "No teams in progress"
    else:
        msg += "In progress: \n\n"
        for team in queue:
            if team.in_progress == True:
                msg += str(team.name) + ": " + str(team.reason) + "\n"


    #If we create a new channel during production, change this number to 
    #the ID of any message sent by the bot in that new channel. The bot 
    #would then keep editing that message to display queue. The msg has 
    #to be from the bot and not a person, otherwise it won't work. Type
    #"!print" for the bot to print something
    message_to_change = await channel.fetch_message(1163937993640386630)
    await message_to_change.edit(content=msg)

#Print msg
@bot.command()
async def print_msg(msg, channel):
    await channel.send(msg)
    
#dm msg
@bot.command()
async def dm(msg, author):
    dm_channel = await author.create_dm()
    await dm_channel.send(msg)


#Bot receives help message
@bot.event
async def on_message(message):

    author = message.author
    content = message.content
    channel = discord.utils.get(bot.get_all_channels(), name="mentoring-queue")

    #Make sure the message isn't from us
    if author == bot.user:
        return

    #if empty msg 
    if content == "":
        return

    #Print anything
    if content.startswith("!print"):
        await channel.send("Hello!")

    #Instructions
    if content.startswith("!mentorhelp"):
        msg = """
                Hi! Please keep the assistance requests in the following format: 
                !mentors [Table #] [Programming Languages used] [Short Description] 
                WARNING: If you do not follow this format, we will not get to you immediately"""

        await dm(msg, author)

    #If help message        e.g. "!mentors Help debugging"
    elif content.startswith('!mentors'):
        reason = content[9:]   

        #if already in queue, remove original request
        ticket = find_ticket(queue, author)
            
        if ticket != None:
            resolve(queue, author)

        #How many ppl ahead of me?
        ppl_ahead_of_me = len(queue)

        #Put into queue
        put_into_queue(queue, author, reason)
        msg = "Currently " + str(ppl_ahead_of_me) + " people ahead"

        await dm(msg, author)
        await update_queue_in_channel(queue, channel)
    
    #If moving a team into progress     e.g. "!p team351"
    elif content.startswith("!p"):
        name = content[3:]

        #Set team's in_progress to True
        team = find_ticket(queue, name)

        if team is None:
            await dm("Unknown team. Example command: '!p team9999' ", author)
            return
        team.in_progress = True

        await update_queue_in_channel(queue, channel)

    #If moving a team from progress back to queue    e.g. "!q team351"
    elif content.startswith("!q"):
        name = content[3:]

        #Set team's in_progress to True
        team = find_ticket(queue, name)

        if team is None:
            await dm("Unknown team. Example command: '!q team9999' ", author)
            return
        team.in_progress = False

        await update_queue_in_channel(queue, channel)

    #If resolve message        e.g. "!r team351"
    elif content.startswith("!r"):

        #ONLY AUTHORIZED CAN DO THIS
        if not authorized(author):
            await dm("Not authorized", author)
            return

        #Team to remove from queue
        name = content[3:]
        ticket = find_ticket(queue, name)

        if ticket is None:
            await dm("Unknown team. Example command: '!r team9999' ", author)
            return 

        resolve(queue, name)
        await dm('Removed ' + name, author)
        await update_queue_in_channel(queue, channel)

#Find ticket by team name  
def find_ticket(list, team_name):

    for ticket in list:
        if str(ticket.name) == str(team_name):
            return ticket
    
    #If no ticket found
    return None

#Put team that needs help in queue
def put_into_queue(list, team_name, reason):
    
    #Create new ticket
    ticket = create(team_name, reason)
    list.append(ticket)

#Remove team from queue after done helping
def resolve(list, team_name):

    #Find ticket
    ticket = find_ticket(list, team_name)
    list.remove(ticket)


bot.run(token)
