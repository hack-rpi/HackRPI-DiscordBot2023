from decouple import config
import discord
from discord.ext import commands
from datetime import timedelta
from captcha.image import ImageCaptcha
import random
import io
import os
from PIL import Image
import asyncio
from collections import defaultdict

def check_profanity(sentence):
    bad_words = set()
    # Specify the file path
    file_path = "profanity-list.txt"  # Replace with the path to your file
    # Open the file and append its contents to the set
    with open(file_path, "r") as file:
        for line in file:
            # Assuming each line in the file contains a single item to add to the set
            item = line.strip()  # Remove leading/trailing whitespace
            bad_words.add(item)
    words = sentence.split()
    sentence_set = set(words)
    return sentence_set.intersection(bad_words)

# token = config("DISCORD_BOT_TOKEN")


class TaskQueue:
    def __init__(self, bot):
        self.bot = bot
        self.queues = defaultdict(list)  # A dictionary to store task queues by channel ID
        self.task_statuses = {}  # A dictionary to store task statuses by task ID
        self.task_assignments = {}  # A dictionary to store task assignments by task ID

    def add_task(self, channel_id, task_description):
            if task_description.strip() == "":
                return "Empty task, please enter a task description."
            task_id = len(self.queues[channel_id]) + 1
            self.queues[channel_id].append(task_id)
            self.task_statuses[task_id] = "Pending"
            self.task_assignments[task_id] = None
            return f"Task {task_id}: {task_description} has been added to the queue."

    def assign_task(self, channel_id, task_id, member: discord.Member):
        task_id = int(task_id)
        if task_id == "":
            return "Empty task ID, please enter a task ID."
        if task_id not in self.queues[channel_id]:
            return f"Task {task_id} does not exist in this channel's queue."
        if self.task_statuses[task_id] != "Pending":
            return f"Task {task_id} is not pending and cannot be assigned."
        self.task_assignments[task_id] = member
        self.task_statuses[task_id] = "Assigned"
        return f"Task {task_id} has been assigned to {member.display_name}."

    def complete_task(self, channel_id, task_id):
        task_id = int(task_id)
        if task_id == "":
            return "Empty task ID, please enter a task ID."
        if task_id not in self.queues[channel_id]:
            return f"Task {task_id} does not exist in this channel's queue."
        if self.task_statuses[task_id] != "Assigned":
            return f"Task {task_id} is not assigned and cannot be marked as complete."
        assigned_member = self.task_assignments[task_id]
        self.task_statuses[task_id] = "Completed"
        self.task_assignments[task_id] = None
        return f"Task {task_id} has been marked as completed by {assigned_member.display_name}."
    def list_tasks(self, channel_id):
        tasks = self.queues[channel_id]
        if not tasks:
            return "No tasks in the queue."
        task_list = "\n".join([f"Task {task_id}: {self.task_statuses[task_id]}" for task_id in tasks])
        return f"Tasks in the queue:\n{task_list}"

    def clear_tasks(self, channel_id):
        self.queues[channel_id] = []
        self.task_statuses = {}
        self.task_assignments = {}
        return "Task queue cleared."


if __name__ =='__main__':
    # Define your intents
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.messages = True
    intents.message_content = True
    token = config("DISCORD_BOT_TOKEN")
    

    # Initialize the bot with the specified intents
    bot = discord.Client(intents=intents)
    captcha_generator = ImageCaptcha()

    captchas ={}
    queue = TaskQueue(bot)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    async def send_captcha(member):
        while True:  # Continues until correct CAPTCHA or timeout
            data = ''.join(random.choices('ABCDEFGHJKMNPQRSTUVWXYZ123456789', k=5))
            captcha_image = captcha_generator.generate(data)
            captcha_bytes = captcha_image.getvalue()

            temp_file = f"captcha_{member.id}.png"
            with open(temp_file, "wb") as f:
                f.write(captcha_bytes)

            captchas[member.id] = data

            dm_channel = await member.create_dm()

            image = Image.open(temp_file)
            image.close()

            file = discord.File(fp=temp_file, filename="captcha.png")

            embed = discord.Embed(title="Verification", description="Solve the CAPTCHA to get verified!")
            await dm_channel.send(embed=embed, file=file)

            fail_count = 0
            timeout = 180 
            start_time = asyncio.get_event_loop().time()

            while (asyncio.get_event_loop().time() - start_time) < timeout:
                try:
                    response = await bot.wait_for('message', check=lambda m: m.author == member and isinstance(m.channel, discord.DMChannel), timeout=timeout)

                    if response.content == captchas[member.id]:
                        role = discord.utils.get(member.guild.roles, name="Verified")
                        await member.add_roles(role)
                        await dm_channel.send(f"Welcome {member.mention}, you are now verified and have been given the 'Verified' role!")
                        del captchas[member.id]
                        return
                    else:
                        fail_count += 1
                        if fail_count < 3:
                            await dm_channel.send(f"Sorry {member.mention}, that's incorrect. You have {3 - fail_count} attempts left. A new captcha will be sent after your remaining attempts run out.")
                        else:
                            await dm_channel.send(f"Sorry {member.mention}, that's incorrect. Generating a new CAPTCHA for you...")
                            break  # Exit the inner loop to generate a new CAPTCHA

                except asyncio.TimeoutError:
                    await dm_channel.send(f"Verification timed out. Please request a new CAPTCHA if you wish to verify.")
                    return

            os.remove(temp_file)


    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.event
    async def on_message(message):
        user = message.author
        content = message.content.lower().strip()
        if content.startswith("$add_task"):
            print(content)
            task_description = content.split(" ")[1:]
            output_message = queue.add_task(message.channel.id, " ".join(task_description))
            await message.channel.send(output_message)

        if content.startswith("$assign_task"):
            task_id = content.split(" ")[1]
            member = message.author  # Assuming the message sender is the member to assign the task
            output_message = queue.assign_task(message.channel.id, task_id, member)
            await message.channel.send(output_message)

        if content.startswith("$complete_task"):
            task_id = content.split(" ")[1]
            output_message = queue.complete_task(message.channel.id, task_id)
            await message.channel.send(output_message)
        if content.startswith("$list_tasks"):
            # Command to list tasks in the queue
            output_message = queue.list_tasks(ctx.channel.id)
            await message.channel.send(output_message)

        if content.startswith("$clear_tasks"):
            # Command to clear all tasks in the queue
            output_message = queue.clear_tasks(ctx.channel.id)
            await message.channel.send(output_message)

            
    

        # Define a list of channel IDs where you want the function to work
        allowed_channel_ids = [1157414659587063898, 1154875483553529981]  # Replace with your desired channel IDs

        # Check if the message is sent in one of the allowed channels
        if message.channel.id not in allowed_channel_ids:
            return  # Exit the function if it's not in an allowed channel
        # Convert the message content to lowercase for case-insensitive matching
        

        # Check if any word in the list is in the message content
        if message.author == bot.user:
            return
            
        if message.guild is None:
            return
  
        profanity = check_profanity(content)
        if(len(profanity) != 0 ) : 
            dm_channel = await user.create_dm()
            await message.delete()
            await dm_channel.send(
                f"Hello {message.author},\n"
                "\n"
                "We've noticed that you used inappropriate language in our Discord server. We take our community guidelines seriously to maintain a respectful and enjoyable environment for all members."
                "\n"
                "Please keep in mind our server rules:\n"
                "1. Be respectful to others.\n"
                "2. Avoid offensive language and slurs.\n"
                "3. No spamming or excessive caps.\n"
                "4. Follow channel-specific guidelines.\n"
                "You have received a warning for this violation. This warning is a reminder of our rules and a request to adhere to them. Repeated violations may lead to further actions, such as muting or removal from the server.\n"
                "If you have any questions or concerns, feel free to reach out to the server moderators or administrators. We encourage positive and respectful interactions among our members."
            )
        if message.author.id in captchas:
            if message.content == captchas[message.author.id]:
                await message.author.send(f"Welcome {message.author.mention}, you are now verified!")
                role = discord.utils.get(message.guild.roles, name="Verified")
                await message.author.add_roles(role)
                del captchas[message.author.id]
            else:
                await message.author.send(f"{message.author.mention}, that's incorrect. Please try again.")


    @bot.event
    async def on_member_join(member):
        await send_captcha(member)
    
        
    bot.run(token)
