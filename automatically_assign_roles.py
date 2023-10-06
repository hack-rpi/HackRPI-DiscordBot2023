import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from decouple import config
    


# Load environment variables from a .env file
load_dotenv()

# Get the bot token from the environment variables
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
token = config("DISCORD_BOT_TOKEN")


    # Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

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
            
            response = await bot.wait_for('message', check=check, timeout=60.0)
            name = response.content
        except:
            await user.send("You're too slowwwwww.")

        #make the role
        role = await ctx.guild.create_role(name=name)
        role = discord.utils.get(ctx.guild.roles, name=name)
        await ctx.send('Team Created with name ' + name)

        #add the author
        await user.add_roles(role)
        
        #request to add the member
        for member in members:
            try:
                #send the message to users
                request = await member.send("Would you like to join team")
                await request.add_reaction("✅")
                await request.add_reaction("❌")


                reaction, _ = await bot.wait_for("reaction_add", check=check, timeout=100.0)
                if str(reaction.emoji) == "✅":
                    await member.add_roles(role)
                    await member.send("Joined Team!")
                else:
                    await member.send("Team Request Denied")
            except:
                await member.send("You're too slowwwwww.")
    else:
        await ctx.send(f"Sorry friend, you can only have 4 members or fewer on a team :(")


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Run the bot with your token
bot.run(token)
