import random

from discord.ext import commands

from games.brooklyn99 import B99

bot = commands.Bot(command_prefix='!')

replies = {
    'yin': 'yang',
    'yang': 'yin',
    'ping': 'pong',
    'pong': 'ping',
    'toys': 'title of your sex tape'
}

eight_ball_answers = [
    'As I see it, yes.',
    'Ask again later.',
	'Better not tell you now.',
	'Cannot predict now.',
	'Concentrate and ask again.',
	'Don’t count on it.',
	'It is certain.',
	'It is decidedly so.',
	'Most likely.',
	'My reply is no.',
	'My sources say no.',
	'Outlook not so good.',
	'Outlook good.',
	'Reply hazy, try again.',
	'Signs point to yes.',
	'Very doubtful.',
	'Without a doubt.',
	'Yes.',
	'Yes – definitely.',
	'You may rely on it.',
]

@bot.event
async def on_ready():
    print(f'replybot is online')

@bot.command(name='jiji')
async def jiji(ctx, arg):
    if arg in replies:
        await ctx.send(replies[arg])
    
@bot.command(name='8ball')
async def magic8ball(ctx, arg):
    await ctx.send(random.choice(eight_ball_answers))

@bot.command(name='99', aliases=['b99'])
async def b99(ctx, arg):
    if arg and arg in B99:
        await ctx.send(random.choice(B99[arg]))
    else:
        await ctx.send(random.choice(B99['']))
