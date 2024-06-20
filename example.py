from BlackJackTable import BlackJackGame, CodeError
from BlackJackTable import HumanBot, PlayerBot
import time

table = BlackJackGame([
    HumanBot(500, "me"), 
    PlayerBot(500, "bot"), 
    PlayerBot(500, "bot"), 
    PlayerBot(500, "bot")], 
    1, True, 70)

while True:
    info = table.itterate()
    if isinstance(info, int):
        print(f"Game over, info: {CodeError(info)}")
        if CodeError(info) != "Deck has been reshuffled" or CodeError(info) != "Dealer has blackjack, new game":
            break
    else:
        print("\n\n\n"+info)
        input()