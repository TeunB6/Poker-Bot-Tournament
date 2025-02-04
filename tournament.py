# Credits to Mansur who wrote the bulk of this script for the ChessBot Tournament

import os
import time
import random
from src.judge import Judge

NUM_ROUNDS = 1000
HAND_LIMIT = 10


# rename all files in the "bots" directory to remove spaces and special characters
# remove all . before the extension
# this is necessary for the import to work

bots_dir = "bots"
for filename in os.listdir(bots_dir):
    if filename.endswith(".py"):
        new_filename = filename.replace(" ", "_") \
                                .replace(".", "_") \
                                .replace("-", "_") \
                                .replace("(", "_") \
                                .replace(")", "") \
                                .replace("__", "_")
        
        new_filename = new_filename[:-3] + ".py"
        # os.rename(os.path.join(bots_dir, filename), os.path.join(bots_dir, new_filename))
        print(f"{filename} -> {new_filename}")

bot_files = [bot_file for bot_file in os.listdir(bots_dir) if bot_file.endswith('.py')]
bot_files = sorted(bot_files)


# import bots from the files
from importlib import import_module, reload

bot_classes = []

for bot_file in bot_files:
    bot_name = bot_file[:-3]
    bot_module = reload(import_module(f"{bots_dir}.{bot_name}"))
    bot_class = getattr(bot_module, "PokerAgent")
    bot_class.name = bot_name
    
    bot_classes.append(bot_class())

print(bot_classes)

j = Judge(*bot_classes, time_limit=.1)
columns = [bot.name for bot in bot_classes]
r = [columns]
for i in range(NUM_ROUNDS):
    history, winner_id, winner_chips = j.run_game(hand_limit=HAND_LIMIT)
    r.append([p.chips for p in j.game.players])
