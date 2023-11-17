from decouple import config
from task import Task, TaskList, create_task
from ticket import create_ticket as create
from discord.ext import commands 
import discord

# Connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
token = config("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)

tasks = TaskList()

@bot.event
async def on_ready():
    print("Bot is online and ready to manage tasks!")

@bot.command()
async def print_tasks(ctx):
    msg = "Current Tasks:\n"
    for task in tasks:
        task_description = task.task
        team_in_charge = task.team_in_charge
        team_to_display = "Unclaimed" if team_in_charge is None else team_in_charge
        msg += f"Team: {team_to_display} ---- Task: {task_description}\n"
    await ctx.send(msg)

@bot.command()
async def new_task(ctx, *, description):
    create_task(tasks, description)
    await ctx.send(f"New task '{description}' added!")

@bot.command()
async def claim_task(ctx, *, description):
    task = tasks.find(description)
    if task is None:
        await ctx.send("Unknown task")
    else:
        task.assign_team(ctx.author)
        await ctx.send(f"Task '{description}' claimed by {ctx.author}")

@bot.command()
async def all_tasks(ctx):
    await print_tasks(ctx)

@bot.command()
async def resolve_task(ctx, *, description):
    task = tasks.find(description)
    if task is None:
        await ctx.send("Unknown task")
    else:
        task.completed()
        await ctx.send(f"Completed task '{description}'")

@bot.command()
async def unclaimed_tasks(ctx):
    unclaimed = [task.task for task in tasks if task.team_in_charge is None]
    if not unclaimed:
        await ctx.send("No unclaimed tasks.")
    else:
        msg = "Unclaimed Tasks:\n" + "\n".join(unclaimed)
        await ctx.send(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide all necessary arguments for the command.")
    else:
        await ctx.send("An error occurred while executing the command.")

bot.run(token)
