# standard lib imports
import os, sys

# custom modules
sys.path.insert(1, os.path.dirname(__file__))
import TicTacToe


Games = {
    'ttt': TicTacToe.TicTacToe
}

def getPrettyGameList():
    return '\n'.join(list(Games.keys()))

if __name__ == "__main__":
    print(Games)