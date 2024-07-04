import discord
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = ">"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

base_url = "https://ctftime.org/api/v1"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}

def top_teams():
    endpoint = "/top/"
    year = str(datetime.now().year)
    table_headers = ["Place", "Team", "Rating"]

    response = requests.get(base_url+endpoint, headers=headers)
    top_teams = json.loads(response.content)

    top_teams_list = []
    place = 1
    for top_team in top_teams[year]:
        team = [place, top_team["team_name"], top_team["points"]]
        top_teams_list.append(team)
        place += 1

    reply = tabulate(top_teams_list, table_headers, tablefmt="rounded_outline", floatfmt=".2f")
    reply = "```"+reply+"```"

    return reply

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == PREFIX+"hello":
        await message.channel.send("Hello!")

    if message.content == PREFIX+"top":
        reply = top_teams()
        await message.channel.send(reply)

client.run(TOKEN)