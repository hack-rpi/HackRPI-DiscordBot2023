from decouple import config
import discord
from discord.ext import commands


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

if __name__ =='__main__':
    # Define your intents
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.messages = True
    intents.message_content = True
    token = config("DISCORD_BOT_TOKEN")
    intents.members = True
    # Initialize the bot with the specified intents
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        global verified_members
        # Loop through members when the bot is ready

        for guild in bot.guilds:
            print(f'Listing members in server: {guild.name}\n')
            print(guild.member_count)
            for member in guild.members:
                # print("_" + member.name + "_\n")
                # print(member.roles)
                # if role in member.roles:
                #     print("This person is verified " + member.name)
                if any(role.name == "Verified" for role in member.roles):
                    print(f"{member.display_name} is already verified.")
                else:
                    print(f"{member.display_name} does not have the 'Verified' role. Sending a verification link...")

        print(f'Logged in as {bot.user.name}')
    

    @bot.event
    async def on_message(message):
        # Define a list of channel IDs where you want the function to work
        allowed_channel_ids = [1157414659587063898, 1154875483553529981]  # Replace with your desired channel IDs

        # Check if the message is sent in one of the allowed channels
        if message.channel.id not in allowed_channel_ids:
            return  # Exit the function if it's not in an allowed channel
        # Convert the message content to lowercase for case-insensitive matching
        content = message.content.lower().strip()

        # Check if any word in the list is in the message content
        if message.author == bot.user:
            return
        if content.startswith("!"):
            return
        profanity = check_profanity(content)
        if(len(profanity) != 0 ) : 
            user = message.author
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
    @bot.event
    async def on_member_join(member):
        print(member.name + "joined")

    bot.run(token)


