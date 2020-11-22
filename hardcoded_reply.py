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
        if type(message) == type(''):
            return self.reply(message)
        else:
            token = message.content.lower().split()
            if token[0] != 'jiji':
                return
            return self.reply(token[1])

    def reply(self, q):
        if q in self.replies:
            return self.replies[q]
    
if __name__ == '__main__':
    test_string = 'jiji  yin'
    print(test_string.split())