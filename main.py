from decouple import config
import discord

def check_profanity(sentence):
	if():
		return True
	return False


token = config("DISCORD_BOT_TOKEN")


bot = discord.Client()


@bot.event
async def on_message(message):
	word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	if message.content.lower() == "hello":
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("hey testing 123")
          

        

bot.run(token)
