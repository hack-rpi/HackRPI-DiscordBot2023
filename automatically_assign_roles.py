import discord
from discord.ext import commands
import os
from profanity_filter import ProfanityFilter
from dotenv import load_dotenv
from decouple import config


def alreadyOnTeam(member):
    team_color = 0x1bdf65 
    has_target_color_role = False
    for role in member.roles:
        if role.color.value == team_color:
            has_target_color_role = True
            break
    return has_target_color_role
    


# Load environment variables from a .env file
load_dotenv()

# Get the bot token from the environment variables
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN")


    # Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Team Command
@bot.command()
async def team(ctx, *members: discord.Member):
    if len(members) < 3:

    #assign roles to the author and users
        user = ctx.author
    #get name from author
        try:
            contains_profanity = True
            await user.send("Hello! What would you like to name your team?")
            while(contains_profanity):
                def check(message):
                    return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
                
                response = await bot.wait_for('message', check=check, timeout=300.0)
                message = response.content
                contains_profanity = ProfanityFilter().is_profane(message)
                if(contains_profanity):
                    await user.send("Don't use profanity please... Try again")
                    await user.send("What would you like your new name to be?")

        except:
            await user.send("You're too slow! This request timed out... Try again and be faster this time :)")


        #add the author
        if(alreadyOnTeam(user) == True):
            await ctx.send('Sorry, you are already on a team.')
        else:
            #make the role
            role = await ctx.guild.create_role(name=message, color=0x1bdf65)
            role = discord.utils.get(ctx.guild.roles, name=message)
            await ctx.send('Team Created with name ' + message)

            await user.add_roles(role)
            
            
            for member in members:
                #request to add the member
                if(alreadyOnTeam(member) == True):
                    await ctx.send(f"{member.mention} is already on a team")
                else:
                    request_message = await member.send(f"{member.mention}, please confirm if you want to join team " + message + ". Respond with 'confirm' or 'deny'.")

                    def check(message):
                        return (
                        message.author == member
                        and message.content.lower().strip() in ["confirm", "deny", "'confirm'", "'deny'"]
                    )

                    try:
                        response = await bot.wait_for("message", check=check, timeout=300.0)
                        if response.content.lower().strip() == "confirm" or response.content.lower() == "'confirm'":
                            await ctx.send(f"{member.mention} has joined team " + message)
                            await member.add_roles(role)
                        else:
                            await ctx.send(f"{member.mention} has denied the request.")
                    except:
                        await ctx.send(f"{member.mention} didn't respond in time. Request expired.")
    else:
        await ctx.send(f"Sorry friend, you can only have 4 members or fewer on a team :(")

#join command
@bot.command()
async def join(ctx):
    user = ctx.author
    #blacklist to prevent joining non-team roles
    banned_roles = ["HackRPI Bot", "RCOS ppl", "Verified", "Director", "Mentors", "Muted", "Timeout", "ali"]

    #team Identification system
    await user.send("What team would you like to join?")

    def check(message):
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
    try:
        response = await bot.wait_for('message', check=check, timeout=300.0)
        team_name = response.content
        try:
            role = discord.utils.get(ctx.guild.roles, name=team_name)
            if(team_name not in banned_roles):
                members_with_role = [member for member in ctx.guild.members if role in member.roles]
                if(len(members_with_role) <= 4):
                    #join that team!
                    await user.add_roles(role)
                    await ctx.send(user.mention + " Sucessfully joined team " + team_name)
                else:
                    #full team
                    await ctx.send("Team is already full.")
            else:
                #maybe add a punitive here? could add the user to a list of troublemakers?
                await ctx.send("Nice try bud, but you can't join non-team roles.")
        except:
            #tried to join a team that doesn't exist
            await ctx.send("Team not found")
    except:
        await user.send("Timed out... try again and be quicker :)... or don't. I'm not your dad.")

#Leave command
@bot.command()
async def leave(ctx):
    #checks to see if the user has a role with the team color
    color = "0x1bdf65"
    role_to_remove = discord.utils.get(ctx.guild.roles, color=discord.Colour(int(color, 16)))
    
    if not role_to_remove:
        await ctx.send("It looks like no one's made teams yet. You could be the first!")
        return

    #removes the user from any role with the team color (there should only ever be 1).
    user = ctx.message.author
    if role_to_remove in user.roles:
        await user.remove_roles(role_to_remove)
        await ctx.send(f"{user.mention} has been removed from {role_to_remove.name}")
    else:
        await ctx.send("You don't have a team to leave.")



# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot with your token
bot.run(token)
