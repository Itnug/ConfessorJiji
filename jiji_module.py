class JijiModule:
    '''abstract class. do not instantiate.'''

    def on_message(self, message):
        ''' extend in subclass '''
        raise NotImplementedError