#!/env/Python3.8.10
#!/MobCat (2022)

import discord      # Discord bot api
import os		    # Basic os funcions like task kill and load files..
import sys, getopt  # for command line varibal things
#import datetime     # Get date and time from system

# User variables
# Where is your Discord bot API token file stored.
BotKey = "Discord.key"
# Absolute file path for if your running the bot from somewhere else.
#BotKey = "F:\\Python\\Discord\\Navi\\Discord.key"
# What is the default bot channel when not useing the -c command
BotChannel = "bots"

#!DO NOT UPLOAD YOUR Discord.key FILE!##############
#!DO NOT UPLOAD YOUR Discord.key FILE!#########################################
#!DO NOT UPLOAD YOUR Discord.key FILE!##############
try:
	with open(BotKey, 'r') as f:
		# It's assumed our file contains a single line,
		# with our API key
		BotToken = f.read().strip()
except FileNotFoundError:
	print ('Discord.key file not found')
	os._exit(1)
# Kinda shitty check bu it will do
if BotToken == '':
	print ('You need to add your bot API Token into the Discord.key file\nhttps://discord.com/developers/applications')
	os._exit(1)

#!DO NOT UPLOAD YOUR Discord.key FILE!##############
#!DO NOT UPLOAD YOUR Discord.key FILE!#####################################
#!DO NOT UPLOAD YOUR Discord.key FILE!##############

# Bot invite link
#https://discord.com/api/oauth2/authorize?client_id=YOURIDHERE&permissions=2147798080&scope=bot

#########################################################################################################################
#Def for procuessing command input
def CMDArgs(argv):
	global commandMsg, BotChannel, BotServer
	commandMsg = BotServer = "" # default set to nothing

	try:
		opts, args = getopt.getopt(argv,"hc:m:s:") # X: needs input. X No input needed.
	except getopt.GetoptError:
		print ('Bad command argument. Try Navi.py -h')
		sys.exit(2)

	for opt, arg in opts:
			if opt == '-h':
				print ('''Discord python message bot
20230331 - MobCat

Navi.py -h
Will display this help screen

Navi.py -m "Your messages" 
Will send "Your messages" to the default server and channel.
Default channel is set to "bots" by default.
It can be changed in the code if you like, look for User variables
at the top.

Navi.py -m "Your message\\nis really\\nreally\\nlong"
Placing a "\\n" In your message will send a multi line message
In this case to the default server and channel.
Your message
is really
really
long

Navi.py -c general -m "Your messages"
Will send "Your messages" to the "general" channel on the default server.
You can set -c to any valid channel on your server. Even NSFW.
please note, channel names are case sensitive.

Navi.py -s 1 -c general -m "Your messages"
Will send "Your messages" to the "general" channel to the server ID 1.

Navi.py
(No command arguments supplied)
Will log into the bot and print out the current settings of the bot
and a list of server IDs to be used with the -s command.
These IDs are normally in order of which servers you invited the bot to first.

Navi.py -s 1 -c general
Will show the same settings menu from above
but now you can see your channel and server IDs are set to custom ones.''')
				os._exit(1)

			elif opt in "-m":
				commandMsg = arg

			elif opt in "-c":
				BotChannel = arg

			elif opt in "-s":
				try:
					BotServer = int(arg)
				except ValueError:
					print("ERROR: -s must be set to a number... You dingus.")
					os._exit(1)

# Chech comand vars, Needs to run first
CMDArgs(sys.argv[1:])

# If no -s command was used. set the defuilt ID to be 0
# which if you only have one server that should be it.
if BotServer == "":
	print("Default server ID was set.")
	BotServer = 0


# New and tasty
# This will find a \n if it was included in our -m messages
# Then split each message block up and chuck it in a list. 
# Then it will send that list with it's own newline chars
# It sounds stupid but if you don't do this, the \n will be
# treated as plain text by the discord api.
# as we are passing it inside a string, not outside.
bufferMsg = []
bufferMsg = commandMsg.split("\\n")
commandMsg = '\n'.join(bufferMsg)


# Our push message to discord thing
async def sendMessage(channel, commandMsg):
	try:
		await channel.send(commandMsg)
	except AttributeError:
		print("ERROR: Please check the spelling of your -c channel. It is case sensitive")

#########################################################################################################################
# Setup the bot
print("Starting the bot.")
bot = discord.Client()

# Our main do shit def
async def main(commandMsg):
	# Set time
	# I kinda wanna use this. but kinda dont need to... just leaving it here.
	#current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	
	# Set the server and channel to talk in
	try:
		channel = discord.utils.get(bot.guilds[BotServer].channels, name=BotChannel)
	except (UnboundLocalError, IndexError) as e:
		print(f"ERROR: -s {BotServer} is not a valid server ID.\nPlease run Navi.py with no args to see a list of server IDs.")
		os._exit(1)

	#print(f"Bot is typing...\n{current_time} | {commandMsg}")
	print(f"Bot is typing...\n{commandMsg}")
	await sendMessage(channel, commandMsg)

	# Murder the bot in silence
	print("Bot done.")
	os._exit(1)

##########################################################################################################################
# Run the bot and login
@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))


	# Check if there was no input, then print a list of server ids we are appart of
	if commandMsg == "":
		print("[Settings]")
		print(f'Your default channel to speek on is set to "{BotChannel}"')
		print(f"Current server ID is {BotServer}")
		print("Your bot can talk on these servers\n")
		ID = 0
		for i in bot.guilds:
			print(f"ID={ID} Server={i}")
			ID +=1
		print("\nPlease copy paste the server ID you want to send messages to.\nRun Navi.py -h for more info.")
		os._exit(1)
	
	await main(commandMsg)

print("Logging into Discord...")
try:
	bot.run(BotToken)

except RuntimeError:
	print("This error for crtl+c is broken")
	os._exit(1)