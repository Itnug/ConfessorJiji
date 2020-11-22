import os
import asyncio
import chessbot, replybot

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

loop = asyncio.get_event_loop()
loop.create_task(chessbot.bot.start(TOKEN))
loop.create_task(replybot.bot.start(TOKEN))
loop.run_forever()
