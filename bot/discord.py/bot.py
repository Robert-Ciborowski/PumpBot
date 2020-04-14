import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot is here!")

client.run('NjkyNTAyODY2NTcyNjA3NTM5.Xnvdwg.8boQM0hrhba4MiuXm5QvAKQ_TF4')