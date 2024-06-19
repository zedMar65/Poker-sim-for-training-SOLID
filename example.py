from Library.game import BlackJackGame, CodeError
from Library.game import HumanBot, PlayerBot, HumanBotWithCount

import os
import time


try:
    print("Simple example of using the library")
    deck_count = int(input("Enter number of decks: "))
    funds = int(input("Enter funds: "))
    table = BlackJackGame([], deck_count, False, 60)
    if input("Play with card counting help or not? (y/n): ") == "y":
        table.add_player(HumanBotWithCount(funds, "You"))
    else:
        table.add_player(HumanBot(funds, "You"))
    number_of_bots = int(input("Enter number of bots: "))

    for i in range(number_of_bots):
        table.add_player(PlayerBot(500, f"Bot{i}"))
    while True:
        
        data = input("Enter action (i - next, q - quit, f - info): ")
        if data == "i":
            info = table.itterate()
            if isinstance(info, int):
                print(f"Game over, info: {CodeError(info)}")
                break
            command = 'cls' if os.name == 'nt' else 'clear'
            os.system(command)
            print(info)
        elif data == "q":
            break
        elif data == "f":
            print("\n"+table.normal_info())
except KeyboardInterrupt:
    print("\nGame over")
except Exception as e:
    print(e)
    time.sleep(10)
