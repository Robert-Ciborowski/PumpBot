# Name: Discord Bot
# Author: Derek Wang, Robert Ciborowski
# Date: 14/04/2020
# Description: A Discord bot which sends alerts about pump and dumps.
#
#              Please! Do not put any mean words in here!

import discord
import csv
from random import randint
from discord.ext import commands, tasks
from itertools import cycle
import os

# for more https://discordpy.readthedocs.io/en/latest/index.html
client = commands.Bot(command_prefix='.')

status = cycle(['test status 1', 'test status 2'])

def update_bot_properties() -> str:
	TOKEN = ''

	try:
		with open('bot_properties.csv', mode='r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0

			# THIS IS BAD but it works!
			for row in csv_reader:
				if len(row) == 0:
					break
				elif line_count == 0:
					print(f'Column names are {", ".join(row)}')
				else:
					TOKEN = row[0]

				line_count += 1

	except csv.Error as e:
		print("You are missing bot_properties.csv. Please ask Robert (robert.ciborowski@mail.utoronto.ca) for help.")
		print(e)

	return TOKEN

TOKEN = update_bot_properties()

@client.event
async def on_ready():
	print("Bot is Online!")
	await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_remove(member):
	"""
	Prints to terminal when a member in discord leaves the server
	:param member: member object
	"""
	print(f'{member} has left the server')
	# await client.send(str(member) + " has left.")


@client.command()
async def ping(ctx):
	"""
	:param ctx:takes in a context
	"""
	await ctx.send(f'Latency: {round(client.latency * 1000)}ms')


@client.command()
async def talk(ctx):
	phrases = ["Test phrase 1", "Test phrase 2"]

	await ctx.send(phrases[randint(0, len(phrases) - 1)])


@client.event
async def on_message(message, ):
	if message.author.bot:
		return

	author = str(message.author)
	msg = message.content.lower()

	# We want to filter out bad words!
	if "wall street" in msg:
		await message.channel.send(str(message.author.mention) + " test!")
	elif "jp" in msg or "morgan" in msg:
		await message.channel.send(str(message.author.mention) + " test 2!")

	elif message.content.startswith("help"):
		if (author == "MuchoPotato#3835"):
			phrases = ["Test!!!", "TEST!!!!!!!!"]
			await message.channel.send(phrases[randint(0, len(phrases) - 1)])

	# Using in just in case he changes his #XXXX value.
	if ("MuchoPotato" in author):
		if "meme" in msg:
			await message.channel.send("!TSET")
	await client.process_commands(message)

@tasks.loop(minutes=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

client.run(TOKEN)
