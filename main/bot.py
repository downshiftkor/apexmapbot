import discord
import requests
from bs4 import BeautifulSoup as bs
import re
import os
import json

def minute_change(minute):
    ss = int(minute)
    hours, remainder = divmod(ss, 60)
    seconds, minutes = divmod(remainder, 3600)
    result = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    return result

def apex_map():
    map_list = {'Olympus':'올림푸스', 'Storm Point':'스톰 포인트', 'Kings Canyon':'킹스 캐니언', "World's Edge":'세상의 끝'}
    
    url = 'https://api.mozambiquehe.re/maprotation?version=2&auth=b7U7qjwNBU5e2m9WjwCS'
    html = requests.get(url)
    soup = bs(html.text, "html.parser")
    jsonObj = json.loads(soup.text)

    c_map = jsonObj['battle_royale']['current']['map']
    c_map_dura = jsonObj['battle_royale']['current']['remainingTimer']

    next_map = jsonObj['battle_royale']['next']['map']
    next_map_dura = jsonObj['battle_royale']['next']['DurationInMinutes']

    result = f'```현재 맵 : {map_list[c_map]} {c_map_dura} 남음\n다음 맵 : {map_list[next_map]} {minute_change(next_map_dura)}```'

    return result
    
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.offline)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!맵'):
        a = apex_map()
        await message.channel.send(a)

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
