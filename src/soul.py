from calendar import month
import os
import discord
import dotenv
from datetime import datetime

dotenv.load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CMD_PREFIX = "$mg"

questions = [q.strip() for q in open('data/qotd.list', 'r').readlines()]
questions.reverse()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if client.user in message.mentions:
        await run_command(message.channel, message.author, message.content)

@client.event
async def on_scheduled_event_create(event):
    pass

async def run_command(channel: discord.Message.channel, author: discord.Message.author, content: discord.Message.content):
    cmd = content.strip("@Mr. Gerald").strip()
    print(f"Command: {cmd}")
    if cmd == "hi":
        await channel.send(f"Hello {author.nick}!")
    elif cmd == "qotd":
        start = datetime(day=9, month=10, year=2022)

        try:
            question = questions[(start - datetime.now()).days]
        except IndexError:
            question = "I'm all out of questions!"

        print(f"Sending QOTD: {question}")
        await channel.send(question)
    else:
        await channel.send("I don't know that command...")

client.run(TOKEN)
