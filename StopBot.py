import discord
import youtube_dl
import os
from discord.ext import commands

TOKEN = os.environ["TOKEN"]

#client = discord.Client()
client = commands.Bot(command_prefix='ඞ')

players = {}

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


###########COMMANDS#########################################################
#echo command returns the string that was sent
@client.command()
async def echo(ctx, message):
    await ctx.send(message)


#ping command used to make sure bot is working properly
@client.command()
async def ping(ctx):
    await ctx.send('pong')

#bot will join the voice channel of the person who made the request 
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

#bot will leave current voice channel
@client.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()


#OUTDATED CODE: takes in a URL and has the bot start playing the youtube video url
#@client.command(pass_context=True)
#async def play(ctx, url):
    #server = ctx.message.server
    #voice_client = client.voice_client_in(server)
    #player = await voice_client.create_ytdl_player(url)
    #players[server.id] = player
    #player.start()


client.run(TOKEN)
