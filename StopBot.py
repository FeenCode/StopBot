import discord
import discord_components
import youtube_dl
import os
from requests import get
import random
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord_components import Button, Select, SelectOption, ComponentsBot
from youtube_dl import YoutubeDL


TOKEN = os.environ["TOKEN"]

#client = discord.Client()
#client = commands.Bot(command_prefix='$')
client = ComponentsBot(".")

recently_played = []
greetings = ['https://www.youtube.com/watch?v=eaEMSKzqGAg', 'https://youtu.be/JQ3Zn2Gtlt0?t=4', 'https://youtu.be/TRgdA9_FsXM?t=1', 'https://youtu.be/yoF2A_12pPk?t=2', 'https://youtu.be/lqYqyHBTZjg', 'https://www.youtube.com/watch?v=6Joyj0dmkug&ab_channel=CartmanHD']


#YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', skip_download: 'True'}
#FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'before_options': '-nostdin',
    'options': '-vn'
}



#Print log on startup
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))



##########ON_MESSAGE FUNCTIONS##############################################
#on_message events listens for key messsages and returns response
@client.event
async def on_message(message):
  ctx = await client.get_context(message)

  if message.author == client.user:
    return

  if message.content.startswith('ඞ!'):
    await message.channel.send('SUS!')
    await play(ctx, 'https://www.youtube.com/watch?v=_-CzeGEmfwQ&ab_channel=ManMadePancake')

  if message.content.startswith('!Rumble'):
    await play(ctx, 'The Rumbling by SiM')

  if message.content.startswith('Noly'):
    await message.channel.send('', file=discord.File('./Assets/no_bitches.jpg'))

  if message.content.startswith('You Turned Her Against Me'):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected() or voice.is_playing():
      await message.channel.send('You Have Done That Yourself!')
    else:
      url = 'https://www.youtube.com/watch?v=h5mEWVbQ_T8'

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
        await ctx.send("You Have Done That Yourself!")
        return

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

#bot will join the voice channel of the person who made the request and play a greeting
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

    greeting = '' #test greeting
    greeting = random.choice(greetings)
    

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(greeting, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return

@client.command(pass_context=True)
async def joinsimp(ctx):
  channel = ctx.message.author.voice.channel
  await channel.connect()

#bot will leave current voice channel
@client.command(pass_context=True)
async def leave(ctx):

    await ctx.voice_client.disconnect()

#bot will search youtube for search param and play top video
@client.command(pass_content=True)
async def play(ctx, *search):

    search = ' '.join(search)

    voice = get(client.voice_clients, guild=ctx.guild)
    
    if not voice:
      await joinsimp(ctx)
      voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
      await ctx.send("Already playing song")
      return

    
    if not isurl(search):
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]

      url = info['webpage_url']
    else:
      url = search

    recently_played.append(url)

    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
    ENCURL = info['formats'][0]['url']
    voice.play(FFmpegPCMAudio(ENCURL, **FFMPEG_OPTIONS))
    voice.is_playing()

    message = ctx.message
    await message.delete()

    message = await ctx.send('Now Playing: '+url)
    await message.add_reaction('⏯')
    await message.add_reaction('⏹')


    def check(reaction, user):
      return user == ctx.author

    reaction = None

    while True:
      if str(reaction) == '⏯':
        if voice.is_paused():
          await resume(ctx)
        elif voice.is_playing():
          await pause(ctx)
      elif str(reaction) == '⏹':
         await stop(ctx)
         break
      try:
            reaction, user = await client.wait_for('reaction_add', timeout = 10800.0, check = check)
            await message.remove_reaction(reaction, user)
      except:
            break

    await message.clear_reactions()


#bot will pause audio if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or voice.is_paused() or not voice.is_playing():
      await ctx.send("I'm not playing anything")
      return
    
    voice.pause()
    return
    

#bot will resume audio if it was paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
      await ctx.send("I'm not in a call")
      return

    elif not voice.is_paused():
      await ctx.send("I'm not paused")
      return
    
    voice.resume()
    return


#bot will leave and join again, stoppig what is playing
@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
      await ctx.send("I'm not in a call")
      return
    
    voice.stop()
    return


#bot replays the last url entered into the recently_played array
#BUG the replay plays the most recent played in any channel!!
@client.command(pass_content=True)
async def replay(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
      await ctx.send("I'm not in a call")
      return
    elif not recently_played:
      await ctx.send("I haven't played anything yet")
      return
    elif voice.is_playing():
      await ctx.send("Already playing song")
      return
    elif voice.is_paused():
      await ctx.send("I am currently playing a song, it's just paused")
      return

    url = recently_played[len(recently_played)-1]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    recently_played.append(url)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return


    return


#TEMP Prints a list of all URLS played during session. Needs to be revised bc there is a risk of spaming hundereds of urls.
#BUG the lop prints for all channels the bot has been in!!!!!!!
@client.command(pass_content=True)
async def lop(ctx):

    if not recently_played:
      await ctx.send("I haven't played anthing yet")
      return

    i = 0
    for url in recently_played:
      i = i + 1

      str1 = str(i)
      str2 = ") "

      ret = str1+str2+url

      await ctx.send(ret)
    
    return


#TESTING EMBEDEDPAGES NOT FOR USE
@client.command()
async def embedpages(ctx):
    page1 = discord.Embed (
        title = 'Video Game LOFI',
        description = 'https://www.youtube.com/watch?v=QlP3eE9Vlg8&t=1s',
        colour = discord.Colour.orange()
    )
    page2 = discord.Embed (
        title = 'Page 2/3',
        description = 'Description',
        colour = discord.Colour.orange()
    )
    page3 = discord.Embed (
        title = 'Page 3/3',
        description = 'Description',
        colour = discord.Colour.orange()
    )
    
    pages = [page1, page2, page3]

    message = await ctx.send(embed = page1)
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')


    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '▶':
            if i < 2:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '⏭':
            i = 2
            await message.edit(embed = pages[i])
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 120.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()

#Bot will say goodbye and shutdown
@client.command()
async def shutdown(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
      await leave(ctx)

    await ctx.send("Goodbye!")
    client.close()
    quit()





###################HELPER FUNCTIONS################################
def isurl(string):
  url = 'https://www.youtube.com/'
  if url in string:
    return True
  else:
    return False





#############################################################################################  
#############################################################################################  
client.run(TOKEN)
#############################################################################################  
#                                         #END#                                             #
 

