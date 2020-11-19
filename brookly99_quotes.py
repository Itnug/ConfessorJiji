import random

from jiji_module import JijiModule
from games.brooklyn99 import B99

class B99Quotes(JijiModule):
    
    def on_message(self, message):
        print("> b99")
        print(message.content.lower())
        
        token = message.content.lower().split()
        print(token)

        if token[0] != 'jiji':
            return

        if token[1] != '99' and token[1] != 'b99':
            return
        
        if token[2]:
            if token[2] in B99:
                return random.choice(B99[token[2]])
        else:
            random.choice(B99[''])

if __name__ == "__main__":
    message = type('',(object,),{"content": 'jiji 99 amy'})()
    o = B99Quotes()
    print(o.on_message(message))