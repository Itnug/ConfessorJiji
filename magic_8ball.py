import random

from jiji_module import JijiModule

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

class Magic8Ball(JijiModule):

    def on_message(self, message):
        print("> 8ball")
        print(message.content.lower())
        
        token = message.content.lower().split()
        print(token)

        if token[0] != 'jiji':
            return

        if token[1] != '8ball':
            return

        return random.choice(eight_ball_answers)

if __name__ == "__main__":
    message = type('',(object,),{"content": 'jiji 8ball where?'})()
    magic_8ball = Magic8Ball()
    print(magic_8ball.on_message(message))