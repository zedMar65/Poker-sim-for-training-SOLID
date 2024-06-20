#### This README is still not finished, if yo wish to use this class, good luck
# BlackJackTable
---
### Overview
This library provides basic support to simulate a blackjack table, it also adds a default computer bot(basic strategy) and 2 human bots: with card count help and without.

---
### Instalation
Either
* Download source code from Library dir and use freely
Or
* Install BlackJackTable with:
`
pip install BlackJackTable 
`

---
### Usage
* Using default bots:
```python
from BlackJackTable import HumanBot

startingFunds = 500
name = "Human player"
player = HumanBot(startingFunds, name)
```
- Creating own bots/Players:
   - [Go to section Code in a nutshell](#writing_bots)
* Using BlackJack table:
```python
from BlackJackTable import BlackJackGame as BJ
from BlackJackTable import HumanBot, PlayerBot

# vars
deck_count = 6
startingFunds = 500
# if logging is True it will print out some game desitions like player loosing all funds, if it is false that information can still be acceced with return codes
logging = True
# shuffle_procent decides how much procent of the deck should be used untill a reshuffle happens
shuffle_procent = 60
# initiating the player class
Player = HumanBot(startingFunds, "Player")
# initiating the standart bot that computer will play
Bot = PlayerBot(500, "BOT")
# adding our bots to a list
list_of_players = [Player, Bot, Bot]
# initiating the BJ class
BJ(list_of_players, deck_count, logging, shuffle_procent)
```
* Simplified:
```python
from BlackJackTable import BlackJackGame as BJ
from BlackJackTable import HumanBot, PlayerBot

table = BJ([], 6, False, 60)
table.add_player(HumanBot(500, "Human"))
table.add_player(PlayerBot(500, "BOT"))
table.add_player(PlayerBot(500, "BOT")) 
```
* CodeError function returns the error that an error code corresponds to. An error code is returned from something failing in the BlackJackGame itterate function:
```python
from BlackJackGame import CodeError

code = 2
print(CodeError(code)) # prints out "Can't split non-pair"
```
* Example of a working playable game:
```python
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
        print(info)
        time.sleep(2)
```
* Understanding BlackJackGame class
  - It derives from parent class SGame:
```python
class SGame(ABC):
    @abstractmethod
    def itterate(self) -> str:
        pass
    def get_game_number(self) -> int:
        pass
    def add_player(self, player) -> None:
        pass
    def normal_info(self) -> str:
        pass
    def __init__(self, players = [], deck_count=1, log=False, cut_procent = 60) -> None:
        pass
```
- It has 4 usable methods:
  - normal_info returns information about that table formated as:
    ```python
    f"
    Game number:  {gamenumber}
    Player count: {playercount}
    Deck count:   {deckcount}
    Alive Players:{aliveplayers's names}
    Players funds:{funds of alive players}
    Dead players: {deal players's names}
    Decks used:   {times shuffled}
    "
    ```
<ul>
    <ul>
        <li>
        get_game_number returns number of game played.
        </li>
        <li>
        add_player adds a new player into the game.
        </li>
        <li>
        itterate compleates 1 full game cycle by getting players bets, dealing the game, asking players desitions and giving out/taking money from bot class funds variable (Note: get_bet method in bot class MUST negte the chosen bet from its own funds).
        </li>
    </ul>
</ul>

---

### Code in a nutshell

<div id = "writing_bots"></div>

##### Writing your own bots
* There are 3 default bots in the library:
  - HumanBot <- a bot for a human to controll, no card counting help, possible to train card counting
  - HumanBotWithCount <- a bot with card counting help, imposible to train card counting
  - PlayerBot <- default self playing bot, follows the default strategy
* All bots must derive from a parent class Sbot:
```python
class SBot(ABC):
    @abstractmethod
    def __init__(self, funds, name):
        self.name = name
        self.funds = funds
    @abstractmethod
    def play(self, info) -> str:
        pass
    @abstractmethod
    def get_bet(self, info) -> int:
        # get_bet function MUST negate the bet from own funds
        bet = 0
        self.funds -= bet
        return bet
        pass
    @abstractmethod
    def kick(self, info) -> None:
        pass
    @abstractmethod
    def check_insurence(self, info) -> bool:
        pass
```
* All methods take in info variable which is a dictionary formated as:
```python
{
    "cards": self.__game_deck.get_used_cards(),        # Cards that at some point were on the table before resuffuling
    "p_cards": self.__player_hands[index].get_cards(), # The hand of the player formated as for example: B21, P8, H20, H10, P18, S18, S17, etc...
    "d_cards": self.__dealer_hand.get_cards(),         # Dealers hand formated in the same way
    "p_count": self.__player_count,                    # How many players playing
    "deck_game": self.__game_deck._deck_count,         # How many decks in the game
    "pos": index+1,                                    # Which position the player is sitting
    "num": self.__game_number,                         # Which game it is played
    "table_cards": self.table_cards                    # The cards that are currently on the table dealt
}
```
- The class can process the data howewer they want and must return:
  - play returns a play desition: H(hit), S(stand), D(double down), Y(split)
  - get_bet returns the bet amount
  - kick informs the class that it was kicked from the table
  - check_insurence returns either True to take insurence or False not to
* Writing your own bot is as simple as processing the info data. Example HumanBot:
```python
from BlackJackTable import SBot

class HumanBot(SBot):
    def __init__(self, funds, name):
        self.name = name
        self.funds = funds
        
    def play(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Your hand: {info['p_cards']}")
        print(f"Dealer's hand: {info['d_cards']}")
        print(f"Table cards: {info['table_cards']}")
        print(f"Funds: {self.funds}")
        action = input("Enter action (H(hit), S(stand), D(double), Y(split)): ")
        return action

    def get_bet(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Funds: {self.funds}")
        bet = int(input("Enter bet: "))
        self.funds -= bet
        return bet

    def kick(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Game over, round: {info}, funds: {self.funds}")
        
    def check_insurence(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Dealer's hand: {info['d_cards']}")
        print(f"Table cards: {info['table_cards']}")
        print(f"Funds: {self.funds}")
        action = input("Do you want to insure? (Y/N): ")
        return True if action == "Y" else False
```
* This class takes in input() as the choices that it makes
---

##### ToDo
- [ ] Publish v1.0
- [ ] Set up a python lybrary
- [ ] Set up docker

---