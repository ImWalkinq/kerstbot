import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import youtube_dl
import json
import os

TOKEN = 'NTAwOTMwODcyODkxOTMyNjcz.DqSAPg.Jam4ieVZ5qMzaN3zbmaFcoaIIP4'

client = commands.Bot(command_prefix = '?')
status = ['met sneeuwvlokjes', 'met kerststerren', 'met sneeuwengeltjes']
client.remove_command('help')
os.chdir(r'C:\Users\Gebruiker\Desktop\Kerstbot')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(60)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='met sneeuwvlokjes'))
    print('Bot is online.')

@client.command()
async def regels():
    await client.say('Word nog uitgewerkt.')

@client.command()
async def ping():
    await client.say('Pong.')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name= '|KerstElf')
    await client.add_roles(member, role)

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Succesvol berichten verwijderd.')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour= discord.Colour.red()
    )

    embed.set_author(name='Kerst Community Help')
    embed.add_field(name='?regels', value='Laat je de regels zien.', inline=False)
    embed.add_field(name='?ping', value='Reageerd met Pong.', inline=False)
    embed.add_field(name='?join', value='Laat de bot je channel joinen.', inline=False)
    embed.add_field(name='?leave', value='Laat de bot je channel leaven.', inline=False)

    await client.send_message(author, embed=embed)

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Music queued.')

@client.command(pass_context=True)
async def q(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Music queued.')

@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, userName: discord.User):
    await client.ban(userName)
    print ('Gebruiker is succesvol verbannen.')

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    await client.kick(userName)
    print ('Gebruiker is succesvol gekickt.')

client.loop.create_task(change_status())
client.run(TOKEN)
