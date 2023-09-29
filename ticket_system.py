from decouple import config
from ticket import Ticket
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

# Initialize the bot with the specified intents
#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

#Queue of all teams
queue = []

#Bot is ready
@bot.event
async def on_ready():
    print("Welcome!")

#Prints queue (only to authorized ppl)
@bot.command()
async def print_queue(queue, channel):

    if len(queue) == 0:
        await print_msg("Empty queue", channel)
    else:
        await print_msg('Current queue: ', channel)
        for team in queue:
            return_msg = str(team.name) + ": " + str(team.reason)
            await print_msg(return_msg, channel)

#Print msg
@bot.command()
async def print_msg(msg, channel):
    await channel.send(msg)
    
#Bot receives help message
@bot.event
async def on_message(message):

    author = message.author
    content = message.content
    channel = message.channel
   
    #Make sure the message isn't from us
    if author == bot.user:
        return

    #Instructions
    if content.startswith("!mentorhelp"):
        await print_msg('Hi! Please keep the assistance requests in the following format:\n' + 
        '!mentors [Table #] [Programming Languages used] [Short Description]\n'
        'WARNING: If you do not follow this format, we will not get to you immediately', channel)

    #If help message
    elif content.startswith('!mentors'):
        reason = content[9:]   

        #if already in queue, remove original request
        ticket = find_ticket(queue, author)
            
        if ticket != None:
            resolve(queue, author)

        #Put into queue
        put_into_queue(queue, author, reason)
        await print_queue(queue, channel)
         
    #If resolve message
    elif content[0] == '?':
        
        #Team to remove from queue
        name = content[1:]
        ticket = find_ticket(queue, name)

        if ticket is None:
            await print_msg("Unknown team", channel)
            return 

        resolve(queue, name)
        await print_msg('Removed ' + name, channel)
        await print_msg('Modified queue: ', channel)
        
        if len(queue) == 0:
            await print_msg("Empty queue", channel)
        else:
            await print_queue(queue, channel)

    #print queue
    elif content.startswith('!q'):
        await print_queue(queue, channel)

    #Unknown command
    elif content.startswith('!') or content.startswith('?'):
        await print_msg('Command not found. Type !mentorhelp for commands', channel)

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