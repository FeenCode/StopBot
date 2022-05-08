import discord
import youtube_dl
import os
from discord.ext import commands

TOKEN = 
#client = discord.Client()
client = commands.Bot(command_prefix='ඞ')

#echo command returns the string that was sent
@client.command()
async def echo(ctx, message):
    await ctx.send(message)


#ping command used to make sure bot is working properly
@client.command()
async def ping(ctx):
    await ctx.send('pong')


#Print log on startup
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))



#on_message events listens for key messsages and returns response
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('ඞ!'):
    await message.channel.send('SUS!')

  if message.content.startswith('Noly'):
    await message.channel.send('', file=discord.File('./Assets/no_bitches.jpg'))

  await client.process_commands(message)





client.run(TOKEN)
