#!/usr/bin/python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import time, random, re
import logging as log
import secrets
from games import AvailableGames

mySecrets = secrets.Secrets()

log.basicConfig(filename='squadBot.log', level=log.DEBUG, filemode='a')
log.info('=== Beginning new log session ===')

currentGame = None

client = commands.Bot(command_prefix='.')

# Events
@client.event
async def on_ready():
    log.info('Bot is ready: ' + time.asctime(time.localtime(time.time())))
    print('Bot is ready.')

# Commands
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 2):
    log.info('Recieved clear command.')
    log.debug('Inputs: ' + str(amount))
    await ctx.channel.purge(limit=amount)

@client.command()
async def ping(ctx):
    log.info('Recieved ping command.')
    await ctx.send('Pong! {}ms'.format(round(client.latency * 1000)))

@client.command()
async def flip(ctx, call=None):
    log.info('Recieved flip command.')
    log.debug('Inputs: ' + str(call))
    message = ''
    log.info('Generating random ints from [0-1]')
    if(random.randint(0, 2) == 0):
        result = 'Heads'
    else:
        result = 'Tails'
    log.debug('Result: ' + result)
    if(call is not None):
        log.info('Checking if call was correct.')
        if(str(call).lower() == result.lower()):
            message += f'You Win!\nResult: {result}'
        else:
            message += f'You Lose!\nResult: {result}'
        log.debug('Result: ' + message)
    else:
        message = result
    log.info('Sending result..')
    await ctx.send(message)

commandFormat = '.roll [number of dice] d [type of dice] [operation (+ or -)(optional)] [modifier (number, required with operation)]\nExample (roll 3 six-sided dice, add 3): \t.roll 3d6+3'
@client.command()
async def roll(ctx, rollCommand=None):
    log.info('Recieved roll command.')
    log.debug('Input: ' + str(rollCommand))

    message = ''
    try:
        # parse the command
        if(rollCommand is None):
            log.info('Input empty, generating a default 1d20 roll.')
            numOfDice = 1
            dice = 20
            modifierNum = 0
            modifierOp = None
            message += 'Rolling a d20..\n'
        else:
            log.info('Detected input, creating a roll based on input.')

            # number of dice
            log.info('Looking for number of dice..')
            match = re.search(r'\d*(?=d)', rollCommand).group(0)
            log.debug('Number of Dice: ' + str(match))
            if (match is None):
                log.info('No number of dice found. Using 1 as default.')
                numOfDice = '1'
            else:
                
                if(str(match).isnumeric()):
                    log.info('Number of dice found, converting to integer.')
                    numOfDice = int(match)
                else:
                    log.info('Number of dice field empty. Using 1 as default.')
                    numOfDice = 1

            # dice type
            log.info('Looking for the dice type..')
            match = re.search(r'(?<=d)\d*(?=\+|\-)?', rollCommand).group(0) 
            if(match is None):
                log.info('No dice type found. Cannot continue, raising exception to return an error message.')
                raise Exception('Bad format.')
            else:
                log.info('Dice type found. Converting to integer.')
                dice = int(match)
                log.debug('Dice Type: ' + str(dice))

            # look for an operation
            log.info('Looking for an operation.')
            match = re.search(r'(?<=\-)*\+(?=\-)*', rollCommand) # look for + only
            match2 = re.search(r'(?<=\+)*\-(?=\+)*', rollCommand) # look for - only
            if(match or match2 and not(match and match2)): # eclusive or (must not contain + and -)
                log.info('Found a single operation')
                if(match):
                    modifierOp = match.group(0)
                else:
                    modifierOp = match2.group(0)
                log.debug('Operation: ' + str(modifierOp))

                # get modifer number
                log.info('Looking for a modifier number. Converting to int directly. If none found, exception will raise.')
                modifierNum = int(re.search(r'(?<=\+|\-)\d*', rollCommand).group(0)) # modifier number
                log.debug('Modifer Number: ' + str(modifierNum))
            elif(not(match) and not(match2)):
                log.info('No operation found.')
                modifierOp = None
            else:
                log.info('Detected more than 1 operator in the command string.')
                raise Exception ('More than 1 operator')

        rolls = []
        log.info('Generating rolls.')
        for i in range(numOfDice):
            rolls.append(random.randint(1, dice))
        log.debug('Rolls: ' + str(rolls))
        result = sum(rolls) 
        log.debug('Sum: ' + str(result))
        if(modifierOp):
            log.info('Executing optional operation for modifer.')
            log.debug('Operation: ' + modifierOp)
            log.debug('Modifier Number: ' + str(modifierNum))
            if(modifierOp == '+'):
                result += modifierNum
            else:
                result -= modifierNum
            log.info('Result: ' + str(result))
        if(len(rolls) > 1):
            log.info('More than 1 dice rolled, showing individual roll results.')
            message += f'Rolls: {str(rolls)}\n'
            if(modifierOp):
                log.info('Showing modifer changes.')
                message += f'Modifer: {modifierOp}{str(modifierNum)}\n'
                message += f'Sum before modifer: {str(sum(rolls))}\n'
        log.info('Showing final result.')
        message += f'Result: {str(result)}'
    except Exception as e:
        log.info('An error occured: \n' + str(e))
        message = f'You typed it wrong, nerd.\nI detected your input to be: "{rollCommand}"\nTry this format (no spaces except after ".roll"): \n\t{commandFormat}'
    await ctx.send(message)

@client.command()
async def howtoroll(ctx):
    log.info('Recieved howtoroll command.')
    log.info('Showing instructions message.')
    msg = f'Enter a command (no spaces except after ".roll"): \n\t{commandFormat}'
    await ctx.send(msg)

@client.command()
async def game(ctx, *args):
    log.info('Recieved game command.')
    log.debug('Input arguments: ' + str(args))
    retMsg = None
    if(args):
        if (args[0] == 'new'):
            if(len(args) == 1):
                retMsg = 'No game selected. Enter name of game after "new". List of games: \n{}'.format(AvailableGames.getPrettyGameList())
            else:
                log.info('Grabbing game.')
                g = AvailableGames.Games.get(args[1])
                if(g):
                    g = g()
                    retMsg = 'Starting Game: {}\n'.format(g.name)
                    log.info('Game found.')
                    log.debug('Game: ' + str(g.name))

                    log.info('Adding instructions and start message to output string.')
                    global currentGame
                    currentGame = g
                    instr = g.instructions()
                    if(instr):
                        retMsg += instr + '\n'
                    try:
                        g.newGame(ctx)
                    except Exception as e:
                        log.error('Encountered an error when attempting to start new game from bot.')
                        log.debug('New Game Error: ' + str(e))
                        await ctx.send('Couldn\'t start new game: ' + str(e))
                        return
                    startM = g.startMessage()
                    if(startM):
                        retMsg += startM + '\n'
                else:
                    log.error('Game was not found.')
                    retMsg = 'Game not found. List of games: \n{}'.format(AvailableGames.getPrettyGameList())
        elif(currentGame is None):
            log.error('Unknown arguments given with no game loaded.')
            retMsg = 'No game has been loaded. Please load a game with "new"'
        else:
            log.info('Unknown arguments given, passing args to game.')
            try:
                retMsg = currentGame.response(ctx, *args)
            except Exception as e:
                retMsg = 'An error occured in the game while handling your input.'
                log.error('Error occured when game was handling response.')
                log.debug('Error: ' + str(e))
    else:
        log.error('No input argumnets detected.')
        await ctx.send('.game command needs more input! Use "new" to start a new game. List of games: \n{}'.format(AvailableGames.getPrettyGameList()))

    if(retMsg is not None):
        log.info('Return message detected, sending response.')
        await ctx.send(retMsg)
    else:
        log.info('Return message was not filled. Forgoing a reply.')

'''
    THE FOLLOWING FUNCTIONS ARE HELPER FUNCTIONS NOT RELATED TO BOT COMMANDS.
'''

client.run(mySecrets.discordBotKey)