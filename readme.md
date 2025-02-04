## General

Welcome to the first edition of the IlluminaTee PokerBot Tournament. This repository contains everything you need to get started creating your own Poker Agents to compete in the tournament. A quick overview of what can be found here: 

- src/judge.py: This contains the class required to run a game/hand with a set of agents. The class contains various methods which can be used to gather data or train agents. In addition to being able to visiualize runs it is possible to run a large amount of runs which can be used to train reinforcement learning agents, should this be something you wish to try. 

- src/formatting.py: This is used by the Judge class to format the information given to the agents. The information is passed in the form of a dictionary. There also exists a version to format it into a string should you want this. The information contained in this dictionary is explained in the rules section.

- src/poker_agent.py: This class contains the ABC your poker bot class should inherit from. Additionally, a few very small examples can be found showcasing some of the basic functionality of the libraries used. 

- tournament.py: This is the file which will be used to run your bots in the final showdown of the tournament. 

- allowed.txt: Libraries allowed to be used in the tournament.

- requirements.txt: Libraries required to run the Judge Class

In the next section, we will discuss the exact rules your implementation must follow. If you have any questions about the rules, the libraries used, the code made or anything you want to discuss relating to the tournament you can do so in the pokerbot tournament discord channel in the Cover Discord server. Any communication/announcements about the tournament will also happen here. Should you have a private inquiry you can of course also send an email to illuminatee@svcover.nl.

For the tournament, the main Python package used for the implementation of poker is the texasholdem library. More info on this can be found here: https://github.com/SirRender00/texasholdem/tree/main. The more broad "poker" package is also in the allowed list if you wish to use it.

We wish you the best of luck in the tournament.
 
-llluminaTee

## Rules
- All bots need to be written in Python. 

- To submit a bot to the tournament you can use this [Google Form](https://forms.gle/gHeN5dmtSCD6Rz1v9).
    - The Python file submitted should contain a copy of the PokerAgentABC class from src/poker_agent in this repo and a class named PokerAgent inheriting from it.
    - Submitting multiple times is allowed/encouraged as this enables us to release multiple rankings throughout the block. In the tournament, we will only take your newest submission into account.
    - Use your University email to submit to the Google Form
- The only allowed libraries can be found in the allowed.txt file in the repository, these are the exact libraries that will be imported during official runs of the tournament.
    - The included libraries make it possible to use basically any AI technique for your bot.

- Work submitted should be your own. 

- Running the tournament:
    - The tournament will be run using the included tournament.py script.
    - All submitted bots will be imported and placed on a single large poker table.
    - After playing a large amount of games with a fixed hand limit, the agent with the most total chips summed across all games (with buyin * num_games subtracted for clarity), will be crowned the winner.
    - A game is defined as a series of hands played with each agent starting with the same amount of chips (the buy-in). A game ends either when the hand limit (100) is reached or when there is only one agent who still has any chips.
    - The tournament will be run using standard Texas Holdem Rules.

- Running your bot:
    - Your bot will be run in the Judge class environment.
    - An action will be picked using your bot's choose_action method. This action has a time-limit of 0.2s
    - Your bot will have a private attribute which is its id, this is its index in the list of players. So when supplied with a list containing information about all players. The information pertaining to your bot can be found at that index.

- The choose_action method of your bot is supplied with the following information:
    1. The game state which contains the following facts about the game:
        - The PlayerState for all players. This signifies whether a player has folded, is in the current round, whether they still need to call or if they are all in.
        - The two cards in your hand.
        - The cards on the table at this time.
        - The amount of chips each player has.
        - The amount of chips each player has at stake, i.e. the amount of chips they stand to gain should they win this hand.
        - The move history: A list containing every action taken by a player in the current hand.

    2. An available_moves MoveIterator. This is an iterator over the legal moves allowed at this time for the current player (i.e. your bot). It supports "in" checks.
