import discord
import youtube_dl
from discord.ext import commands
import asyncio
from itertools import cycle

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

players = {}
queues = {}
currently_playing = "IDLE"
status = ['Ramses','Despacito','Racket', 'Daedalus','Code Blocks', 'Cesar']
def check_queue(id):
    if queue[id] != []:
        player = queue[id].pop(0)
        players[id] = player
        player.start()

@client.event
async def on_ready():
    print("The bot is ready!")

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def pissoff(ctx):
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

@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()


@client.command(pass_context = True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say("Video Queued")

@client.command(pass_context = True)
async def game(ctx, game):
    currently_playing = game

    if game == 'loop':
        async def change_status():
            games = cycle(status)
            while 1:
                current_status = next(games)
                await client.change_presence(game=discord.Game(name='{}'.format(current_status)))
                await asyncio.sleep(2)
    else:
        await client.change_presence(game=discord.Game(name='{}'.format(currently_playing)))

@client.event
async def on_member_join(member):
    role = dicord.utils.get(member.server.roles, name='servo')
    await client.add_roles(member, role)

client.run("NDk4MjYzMzU4OTA3MjE5OTY4.DprRmQ.dFGCwunjQ94FzEvOQAh9FdqHVfo")
