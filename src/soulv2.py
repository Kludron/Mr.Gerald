import os, sys
import logging
from datetime import datetime

from dotenv import load_dotenv
from discord import (
    Intents,
    Client,
    Message
)

load_dotenv()

# Set up API token
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    logging.error('Discord API Token not found') 
    exit()

# Set up Logging
LOGDIR = os.getenv('DISCORD_LOGDIR')
LOGFILE = 'discord.log'
if not LOGDIR:
    LOGDIR = 'logs'

# This is for the qotd for the FFBC Youth Server
QOTD_ROLE = "<@&941465848873386004>"

class MrGerald(Client):

    intents = Intents.default()
    intents.message_content = True 

    def __init__(self, questions:list, startdate:datetime) -> None:
        # self.handler = logging.FileHandler(filename=os.path.join(LOGDIR, LOGFILE), encoding='utf-8', mode='a')
        self.handler = logging.StreamHandler()
        self.questions = questions
        self.startdate = startdate

    # def __call__(self) -> None:
    #     self.run(TOKEN, log_handler=self.handler)
    # self.start(TOKEN, reconnect=True)

    async def on_message(self, message):
        if message.author == self.client.user: return
        if self.client.user in message.mentions:
            await self.run_command(message.channel, message.author, message.content)

    async def run_command(self, channel:Message.channel, author:Message.author, content:str):
        cmd = content.strip(self.client.user.mention).strip()
        reply = str()
        if cmd == "qotd":
            try:
                question = self.questions[(self.startdate-datetime.now()).days]
            except IndexError:
                question = "I'm all out of questions!"

            reply += QOTD_ROLE + ' ' + question
        if reply:
            await channel.send(reply)

if __name__ == '__main__':
    questions = [q.strip() for q in open('data/qotd.list', 'r').readlines()]
    startdate = datetime(day=9, month=10, year=2022)

    bot = MrGerald(questions=questions, startdate=startdate)
    bot.run(TOKEN, log_handler=logging.StreamHandler())
