import discord
from discord.ext import commands
import os
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

# Define a simple command
@bot.command()
async def team(ctx, *members: discord.Member):
    if len(members) < 3:

    #assign roles to the author and users
        user = ctx.author
    #get name from author
        try:
            await user.send("Hey buddddd... could you send me ur team name pweaseeee.")

            def check(message):
                return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
            
            response = await bot.wait_for('message', check=check, timeout=300.0)
            name = response.content
        except:
            await user.send("You're too slowwwwww.")


        #add the author
        if(alreadyOnTeam(user) == True):
            await ctx.send('Sorry, you are already on a team.')
        else:
            #make the role
            role = await ctx.guild.create_role(name=name, color=0x1bdf65)
            role = discord.utils.get(ctx.guild.roles, name=name)
            await ctx.send('Team Created with name ' + name)

            await user.add_roles(role)
            
            #request to add the member
            for member in members:
                if(alreadyOnTeam(member) == True):
                    await ctx.send(f"{member.mention} is already on a team")
                else:
                    request_message = await member.send(f"{member.mention}, please confirm if you want to join team " + name + ". Respond with 'confirm' or 'deny'.")

                    def check(message):
                        return (
                        message.author == member
                        and message.content.lower().strip() in ["confirm", "deny", "'confirm'" "'deny'"]
                    )

                    try:
                        response = await bot.wait_for("message", check=check, timeout=300.0)
                        if response.content.lower().strip() == "confirm" or response.content.lower() == "'confirm'":
                            await ctx.send(f"{member.mention} has joined team " + name)
                            await member.add_roles(role)
                        else:
                            await ctx.send(f"{member.mention} has denied the request.")
                    except:
                        await ctx.send(f"{member.mention} didn't respond in time. Request expired.")
    else:
        await ctx.send(f"Sorry friend, you can only have 4 members or fewer on a team :(")

@bot.command()
async def join(ctx):
    user = ctx.author
    banned_roles = ["HackRPI Bot", "RCOS ppl", "Verified", "Director", "Mentors", "Muted", "Timeout", "ali"]

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
                    await user.add_roles(role)
                    await ctx.send("Sucessfully joined team " + team_name)
                else:
                    await ctx.send("Team is already full.")
            else:
                await ctx.send("Nice try bud, but you can't join non-team roles.")
        except:
            await ctx.send("Team not found")
    except:
        await user.send("Time out")


@bot.command()
async def leave(ctx):
    color = "0x1bdf65"
    role_to_remove = discord.utils.get(ctx.guild.roles, color=discord.Colour(int(color, 16)))
    
    if not role_to_remove:
        await ctx.send("Role not found.")
        return

    user = ctx.message.author
    if role_to_remove in user.roles:
        await user.remove_roles(role_to_remove)
        await ctx.send(f"You've been removed from the team")
    else:
        await ctx.send("You don't have a team to leave.")



# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot with your token
bot.run(token)
