#!/usr/bin/python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import time
import random
import re

client = commands.Bot(command_prefix='.')

# Events
@client.event
async def on_ready():
    print('Bot is ready.')


# Commands
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit=amount)

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(client.latency * 1000)))

@client.command()
async def flip(ctx, call=None):
    message = ''
    if(random.randint(0, 2) == 0):
        result = 'Heads'
    else:
        result = 'Tails'
    if(call is not None):
        if(str(call).lower() == result.lower()):
            message += f'You Win!\nResult: {result}'
        else:
            message += f'You Lose!\nResult: {result}'
    else:
        message = result
    await ctx.send(message)

@client.command()
async def roll(ctx, numOfDice=None, dice=None):
    message = ''
    try:
        if(numOfDice is None and dice is None):
            numOfDice = '1'
            dice = 'd20'
            message += 'Rolling a d20..\n'
        if(dice is not None):
            dice = int(str(dice)[1:])
            numOfDice = int(numOfDice)
        else:
            dice = int(str(numOfDice[1:]))
            numOfDice = 1
        rolls = []
        for i in range(numOfDice):
            rolls.append(random.randint(1, dice))
        result = sum(rolls)
        if(len(rolls) > 1):
            message += f'Rolls: {str(rolls)}\n'
        message += f'Result: {result}'
    except Exception:
        message = 'You typed it wrong, nerd.\nTry this format: \t.roll {number of dice} d{type of dice}\nExample(roll 3 six sided dice): \t.roll 3 d6 '
    await ctx.send(message)


client.run('Njk2ODYzNjY0NjQwMDk4MzY1.Xou65A.JP-g-XjFm8t3IfJaN9blE7D_vMw')