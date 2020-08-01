#!/usr/bin/python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import time
import random
import re
import logging as log

log.basicConfig(filename='squadBot.log', level=log.DEBUG, filemode='a')
log.info('=== Beginning new log session ===')

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


'''
    THE FOLLOWING FUNCTIONS ARE HELPER FUNCTIONS NOT RELATED TO BOT COMMANDS.
'''




client.run('Njk2ODYzNjY0NjQwMDk4MzY1.Xou65A.JP-g-XjFm8t3IfJaN9blE7D_vMw')