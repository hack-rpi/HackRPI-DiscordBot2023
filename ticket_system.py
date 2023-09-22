from decouple import config
from ticket import Ticket
import discord

#Discord token
token = config("DISCORD_BOT_TOKEN")

#Connection
client = discord.Client()

#Find ticket by team name
def find_ticket(list, team_name):

    for ticket in list:
        if ticket.name == team_name:
            return ticket
    
    #if no ticket found, create and return
    ticket = Ticket()
#Put team that needs help in queue
def put_into_queue(list, team_name, reason):
    
    #Create new ticket
    ticket = Ticket(team_name, reason)
    list.append(ticket)

#Remove team from queue after done helping
def resolve(list, team_name):
    list.remove(team_name)