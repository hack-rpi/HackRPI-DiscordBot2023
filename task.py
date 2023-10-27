import discord
from discord.ext import commands
from collections import defaultdict

class TaskQueue:
    def __init__(self, bot):
        self.bot = bot
        self.queues = defaultdict(list)  # A dictionary to store task queues by channel ID
        self.task_statuses = {}  # A dictionary to store task statuses by task ID
        self.task_assignments = {}  # A dictionary to store task assignments by task ID

    async def add_task(self, ctx, task_description):
        channel_id = ctx.channel.id
        task_id = len(self.queues[channel_id]) + 1
        self.queues[channel_id].append(task_id)
        self.task_statuses[task_id] = "Pending"
        self.task_assignments[task_id] = None
        await ctx.send(f"Task {task_id}: {task_description} has been added to the queue.")

    async def assign_task(self, ctx, task_id, member: discord.Member):
        channel_id = ctx.channel.id
        if task_id not in self.queues[channel_id]:
            await ctx.send(f"Task {task_id} does not exist in this channel's queue.")
            return
        if self.task_statuses[task_id] != "Pending":
            await ctx.send(f"Task {task_id} is not pending and cannot be assigned.")
            return
        self.task_assignments[task_id] = member
        self.task_statuses[task_id] = "Assigned"
        await ctx.send(f"Task {task_id} has been assigned to {member.display_name}.")

    async def complete_task(self, ctx, task_id):
        channel_id = ctx.channel.id
        if task_id not in self.queues[channel_id]:
            await ctx.send(f"Task {task_id} does not exist in this channel's queue.")
            return
        if self.task_statuses[task_id] != "Assigned":
            await ctx.send(f"Task {task_id} is not assigned and cannot be marked as complete.")
            return
        assigned_member = self.task_assignments[task_id]
        self.task_statuses[task_id] = "Completed"
        self.task_assignments[task_id] = None
        await ctx.send(f"Task {task_id} has been marked as completed by {assigned_member.display_name}.")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='add_task')
async def add_task(ctx, *, task_description):
    queue.add_task(ctx, task_description)

@bot.command(name='assign_task')
async def assign_task(ctx, task_id, member: discord.Member):
    queue.assign_task(ctx, int(task_id), member)

@bot.command(name='complete_task')
async def complete_task(ctx, task_id):
    queue.complete_task(ctx, int(task_id))

if __name__ == '__main__':
    TOKEN = 'YOUR_BOT_TOKEN'
    queue = TaskQueue(bot)
    bot.run(TOKEN)
