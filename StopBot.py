import discord
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

TOKEN = os.environ["TOKEN"]

#client = discord.Client()
client = commands.Bot(command_prefix='$')

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


#bot will play the audio of the youtube video that it sent via URL
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return


#TEMP bot will leave and join again, stoppig what is playing
@client.command(pass_context=True)
async def stop(ctx):
     await ctx.voice_client.disconnect()
     channel = ctx.message.author.voice.channel
     await channel.connect()


client.run(TOKEN)
