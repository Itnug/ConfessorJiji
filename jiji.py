import os
import discord

from dotenv import load_dotenv
from hardcoded_reply import HardCodedReply
from magic_8ball import Magic8Ball
from brookly99_quotes import B99Quotes

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

jiji_modules = [HardCodedReply(), Magic8Ball(), B99Quotes()]

@client.event
async def on_ready():
    print(f'{client.user} has connected to the Discord!')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    for jiji_module in jiji_modules:
        print(type(jiji_module))
        print(message.content)
        reply = jiji_module.on_message(message)
        
        if reply:
            await message.channel.send(reply)
        
client.run(TOKEN)