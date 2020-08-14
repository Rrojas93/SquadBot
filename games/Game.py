# standard lib imports
import time, abc

class BotGameInterface(metaclass=abc.ABCMeta):
    '''
    Provides an interface for a Discord text based game.
    '''
    def __init__(self, timeout_minutes=60):
        self.name = 'BotGame'
        self.startTime = time.time()
        self.timeout = timeout_minutes

    @abc.abstractclassmethod
    def newGame(self, ctx):
        '''
        Do any setup for the game here like setting inital vars. 
        '''
        raise NotImplementedError

    def instructions(self) -> str:
        '''
        Write any instructions to your game here and return it as a string. This will be 
        called when your game is first created.
        '''
        return None

    def startMessage(self):
        '''
        Implement this to return an initial message at the start of your game. This 
        will be called after instructions().
        '''
        return None

    @abc.abstractclassmethod
    def response(self, ctx, *response) -> str:
        '''
        This is the function that will handle any text responses from 
        the players and is the only function that is (and should be) called
        from the bot after initial setup.
        This should handle serving any commands to your game as well like "new" for 
        new game or "help" for the instructions.
        This function should also return a string with an updated message for your game.
        '''
        raise NotImplementedError

    def touch(self):
        '''
        Call this command to prevent your game from timing out. This will 
        set the start time to the current time as timeout checks the time 
        from the start of the game. 
        Effectively, this could make it so the timeout is reset after every
        move if called from response().
        '''
        self.startTime = time.time()

    def timedout(self):
        '''
        Tells the caller if the current game is still alive. If not, bot will 
        remove the game from context.
        '''
        if(self.timeout > 0):
            return time.time() > self.startTime + (self.timeout * 60)
        else:
            return False

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'newGame') and
                callable(subclass.newGame) and 
                hasattr(subclass, 'response') and
                callable(subclass.response)) 