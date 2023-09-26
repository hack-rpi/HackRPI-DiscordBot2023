from decouple import config
from ticket import Ticket
from ticket import create_ticket as create
import discord

#Connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
token = config("DISCORD_BOT_TOKEN")

# Initialize the bot with the specified intents
bot = discord.Client(intents=intents)

#Queue of all teams
queue = []

#Bot is ready
@bot.event
async def on_ready():
    print("Welcome!")

#Bot receives help message
@bot.event
async def on_message(message):

    author = message.author
    content = message.content
   
    #Make sure the message isn't from us
    if author == bot.user:
        return

    #If help message
    if content[0] == '!':
        #Starts at index 1 because index 0 is '!' 
        # which we need for the bot to recognize it as a help message
        reason = content[1:]   

        #Put into queue
        put_into_queue(queue, author, reason)

        await message.channel.send('Current queue: ')
        for team in queue:
            return_msg = str(team.name) + ": " + str(team.reason)
            await message.channel.send(return_msg)
        
    #If resolve message
    elif content[0] == '?':
        
        #Team to remove from queue
        name = content[1:]
        ticket = find_ticket(queue, name)
        queue.remove(ticket)

        await message.channel.send('Removed ' + name)
        await message.channel.send('Modified queue: ')
        
        if len(queue) == 0:
            await message.channel.send("Empty queue")
        else:
            for team in queue:
                return_msg = str(team.name) + ": " + str(team.reason)
                await message.channel.send(return_msg)

    #print queue
    elif content == "print":
        if len(queue) == 0:
            await message.channel.send("Empty queue")
        for team in queue:
            return_msg = str(team.name) + ": " + str(team.reason)
            await message.channel.send(return_msg)

#Find ticket by team name  
def find_ticket(list, team_name):

    for ticket in list:
        if str(ticket.name) == team_name:
            return ticket
    
    #If no ticket found
    return "Something went wrong"

#Put team that needs help in queue
def put_into_queue(list, team_name, reason):
    
    #Create new ticket
    ticket = create(team_name, reason)
    list.append(ticket)

#Remove team from queue after done helping
def resolve(list, team_name, reason):

    #Find ticket
    ticket = find_ticket(list, team_name, reason)
    list.remove(ticket)

bot.run(token)