# BlackJack class
---
### Overview
This library provides basic support to simulate a blackjack table, it also adds a default computer bot(basic strategy) and 2 human bots: with card count help and without.

---
### Instalation
Either
Download source code from Library dir and use freely
Or
* TODO: publish as python library

---
### Usage
* Using default bots:
```python
from bots import HumanBot

startingFunds = 500
name = "Human player"
player = HumanBot(startingFunds, name)
```
* Using BlackJack table:
```python
BlackJackGame(list_of_players, deck_count, False, 60)
```
---

### Code in a nutshell
---
##### Writing your own bots
* There are 3 default bots in the library:
`HumanBot <- a bot for a human to controll, no card counting help, possible to train card counting`
`HumanBotWithCount <- a bot with card counting help, imposible to train card counting`
`PlayerBot <- default self playing bot, follows the default strategy`
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
<br><br>

##### Undestarding BlackJackGame class
