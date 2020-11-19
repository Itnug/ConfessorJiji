from jiji_module import JijiModule

class HardCodedReply(JijiModule):

    replies = {
        'yin': 'yang',
        'yang': 'yin',
        'ping': 'pong',
        'pong': 'ping',
        'toys': 'title of your sex tape'
    }

    def on_message(self, message):
        token = message.content.lower().split()
        
        if token[0] != 'jiji':
            return
        
        if token[1] in self.replies:
            return self.replies[token[1]]
    
if __name__ == '__main__':
    test_string = 'jiji  yin'
    print(test_string.split())