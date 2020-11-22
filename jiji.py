import os
import discord
from discord.ext import commands

from dotenv import load_dotenv
from hardcoded_reply import HardCodedReply
from magic_8ball import Magic8Ball
from brookly99_quotes import B99Quotes
from chess import Chess
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='!')

jiji_modules = [HardCodedReply(), Magic8Ball(), B99Quotes(), Chess()]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to the Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    for jiji_module in jiji_modules:
        print(type(jiji_module))
        print(message.content)
        reply = jiji_module.on_message(message)
        
        if reply:
            await message.channel.send(reply)
        
bot.run(TOKEN)