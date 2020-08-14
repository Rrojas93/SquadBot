# SquadBot
## By the squad, for the squad!

### Description

SquadBot is a Discord bot which provides some useful utilities for managing and using a discord chat channel 
as well as fun interactions between the bot and the users. 

### Available Commands:
* **.clear**: Clears a certain amount of messages in the channel it was typed in. Input argument is the number of messages to delete. If no argument is given, will only delete the last message.
    * Example: ".clear 10" > deletes the last 10 messages.
* **.ping**: Returns the response time from the server.
* **.flip**: Flips a coin (Settle it between a friend with a flip of a coin!). Can call the flip so the winner is clear and in ink!
    * Example: ".flip heads" 
* **.roll**: Rolls a dice with as many dice and sides needed. A modifier can also be added to the command.
    * Example: To roll 5 20-sided dice and add 16 to the total: ".roll 5d20+16"
* **.howtoroll**: Gives detailed instructions on how the roll command works and how to use it.
* **.game**: Can start a game from a list of available games. Just enter the command with no arguments to see a list of games. To start a new game use "new" as the first argument followed by the name of the game as the second argument.
    * Example: ".game new ttt @your_friend" > will result in the start of a new Tic Tac Toe game and challenges a user you mentioned with "@". 
        * Note: the "@your_friend" argument is a game specific argument that is required by the game "Tic Tac Toe"

### Gallery
.help Command:
![.help Command](/images/gallery/command_help.png)

.roll Command:
![.roll Command](/images/gallery/command_roll.png)

.game Command:
![.game Command](/images/gallery/command_game_ttt.png)