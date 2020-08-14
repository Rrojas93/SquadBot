#!/usr/bin/python3
# -*- coding: utf-8 -*-

# standard lib imports
import time, os, re, sys, logging as log 
log.basicConfig(filename='TicTacToe.log', level=log.DEBUG)

# custom modules
sys.path.insert(1, os.path.dirname(__file__))
from Game import BotGameInterface

def main():
    game = TicTacToe()
    game.newGame('')
    print(game.instructions())
    while(not(game._isGameOver())):
        os.system('cls')
        print(game.printBoard())
        move = input('Make your move Player({}): '.format('X' if game.turn else 'O'))
        game.makeMove(game.players[0 if game.turn else 1], int(move))
    print(game.printBoard())

class TicTacToe(BotGameInterface):
    def newGame(self, ctx, fake=False):
        '''
        Creates a new game of Tic Tac Toe.
        '''
        try:
            players = (ctx.author, ctx.message.mentions[0])
        except IndexError as e:
            err = 'Did not challenge anyone through mention after game name (example: .game new ttt @McLovin)'
            log.error(err)
            log.debug(str(e))
            raise ValueError(err)
        except Exception as e:
            log.error('Error occured when parsing user input data.')
            log.debug('Error: ' + str(e))
            print(str(e))
            raise Exception('Unexpected error occured. Couldn\'t start new game')

        self.name = 'Tic Tac Toe'
        self.players = players
        self.turn = True # two players only need boolean to keep turn order.
        self.board = []
        self._fillBoard()

    def startMessage(self):
        return 'Initiator of game goes first (X): \n' + self.printBoard()

    def _fillBoard(self, board=None, fill=False):
        if(board is None):
            board = self.board
        for i in range(10):
            if(fill):
                board.append(i)
            else:
                board.append(' ')

    def instructions(self):
        exampleBoard = list()
        self._fillBoard(board=exampleBoard, fill=True)
        msg = f'It\'s Tic Tac Toe... You know how this goes.\nUse the number pad on your keyboard as a guide to the Tic Tac Toe board. \nCommands for game: ".game " + any number from 1-9 (example: ".game 1")\nI know your gonna mess it up so here a picture:\n\n{self.printBoard(board=exampleBoard)}'
        return msg

    def clearBoard(self):
        self.board.clear()

    def response(self, ctx, command):
        if(ctx.author == self.players[0 if self.turn else 1]):
            if(re.match(r'[1-9]', command)):
                if(self.makeMove(ctx.author, int(command))):
                    gameOver = self._isGameOver()
                    if(gameOver[0]):
                        msg = self.printBoard()
                        if(gameOver[1] != 'Draw!'):
                            msg += '\n\nGame is over! Read \'em and wheep, bois.\n{} {}'.format(self.players[0 if not(self.turn) else 1].name, gameOver[1])
                        else:
                            msg += '\n\nDraw! Both pee shooters ran out of ammo..'
                        return msg
                    else:
                        return self.printBoard()
                else:
                    return "Nope, Can't do that."
            else:
                return "Tic Tac Toe does not understand your command: {}. Expecting a digit from 1-9.".format(command)
        elif(ctx.author not in self.players):
            return 'Stay out of this... This showdown is between {} and {}'.format(self.players[0].name, self.players[1].name)
        else:
            return 'It is not your turn {}!'.format(self.players[0 if not(self.turn) else 1].name)
            

    def makeMove(self, player, move):
        symbol = 'X' if self.turn else 'O'
        if(self.board[move] == ' '):
            self.board[move] = symbol
            self.turn = not(self.turn)
            return True
        else:
            return False

    def _isGameOver(self):
        if(self._winByColumn()):
            return (True, 'Won by Column!')
        elif(self._winByRow()):
            return (True, 'Won by Row!')
        elif(self._winByDiagnal()):
            return (True, 'Won by Diagnal!')
        elif(self._drawByFill()):
            return (True, 'Draw!')
        else:
            return (False, '')

    def _winByColumn(self):
        # win by column
        for cell in range(3):
            column = self.board[cell + 1::3]
            if(self._allInListSame(column)):
                print('Game is over by column.')
                return True
    
    def _winByRow(self):
        # win by Row
        for cell in range(4): # 1, 2, 3 | 1, 4, 7 diff 0, 2, 4 dev 2 
            if(cell == 0):
                continue
            start = cell + ((cell-1) * 2)
            row = self.board[start: start+3]
            if(self._allInListSame(row)):
                print('Game is over by row.')
                return True

    def _winByDiagnal(self):
        # win by diagnal
        diagnal = self.board[1:10:4]
        diagnal_2 = self.board[3:8:2]
        result = self._allInListSame(diagnal) or self._allInListSame(diagnal_2)
        if(result):
            print('Game is over by diagnal')
        return result

    def _allInListSame(self, inputList: list) -> bool:
        if(inputList[0] == ' '):
            return False
        return all([cell == inputList[0] for cell in inputList])

    def _drawByFill(self):
        return all([c != ' ' for c in self.board[1:]])

    def printBoard(self, board=None):
        if(board is None):
            board = self.board
        boardPrint = '{} | {} | {}\n_________\n{} | {} | {}\n_________\n{} | {} | {}'.format(
            board[7], board[8], board[9],
            board[4], board[5], board[6],
            board[1], board[2], board[3]
            )
        return f'```{boardPrint}```'


if __name__ == "__main__":
    main()