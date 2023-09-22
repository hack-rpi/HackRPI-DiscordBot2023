from decouple import config
from ticket import Ticket
from ticket import create_ticket as create
import discord

#Discord token
token = config("DISCORD_BOT_TOKEN")
print(token)
#Connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN")

# Initialize the bot with the specified intents
bot = discord.Client(intents=intents)

#Bot is ready
@bot.event
async def on_ready():
    print("Welcome!")

#Bot receives help message
@bot.event
async def on_message(message):

    author = message.author

    #Make sure the message isn't from us
    if author == bot.user:
        return

    #If message starts with 
    content = message.content
    if content.startswith('!'):
        await message.channel.send('A mentor will be with you shortly!')

        #Starts at index 1 because index 0 is '!' 
        # which we need for the bot to recognize it as a help message
        reason = content[1:]   

        #Create ticket
        ticket = create(author, reason)
        
#Find ticket by team name and reason
def find_ticket(list, team_name, reason):

    for ticket in list:
        if ticket.name == team_name and ticket.reason == reason:
            return ticket
    
    #if no ticket found, create and return
    return create(team_name, reason)

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