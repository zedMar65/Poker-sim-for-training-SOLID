from abc import ABC, abstractmethod
from random import shuffle

# Default class
class SDeck(ABC):
    @abstractmethod
    def deal_card(self):
        pass
    @abstractmethod
    def check_for_cut(self):
        pass

class Deck(SDeck):
    # Constants
    _DECK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']*4
    _SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
    _SLICE_PERCENT = 60
    _VIABLE_DECKS = [1, 2, 4, 6, 8]
    
    # General functions
    def _shuffle(self):
        self.__deck = self._DECK * self.__deck_count
        shuffle(self.__deck)
        self.__used_deck = []
    
    def deal_card(self):
        card = self.__deck[-1]
        self.__used_deck.append(self.__deck[-1])
        self.__deck.pop()
        return card
    
    def check_for_cut(self):
        # Check if above set percentage of cards are already used
        if len(self.__used_deck) / (len(self.__used_deck) + len(self.__deck)) * 100 > self._SLICE_PERCENT:
            self._shuffle()
            return True
        return False
    
    # Initial
    def __init__(self, deck_count=1) -> None:
        if deck_count not in self._VIABLE_DECKS:
            raise Exception(f"{deck_count} is not a valid deck")
        self.__deck_count = deck_count
        self._shuffle()

# hand class to handle hands:
class hand:
    # get the hand name
    def _sum_cards(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 0}
        for card in hand:
            if card not in values:
                raise Exception("Soething went wrong with card mapping")
        total_value = sum(values[card] for card in hand)
        has_ace = 'A' in hand

        # Check for pairs
        if len(hand) == 2 and hand[0] == hand[1]:
            if hand[0] == 'A':
                return "P2"
            return "P" + str(total_value)
        if has_ace and total_value == 10:
            return "B21"
        if has_ace and total_value <= 10:
            return "S" + str(total_value+11)
        if has_ace:
            total_value+=1
        return "H" + str(total_value)
    def add_to_hand(self, card):
        self.__cards.append(card)
    def get_cards(self):
        name = self._sum_cards(self.__cards)
        return f"{name} {self.__cards}"
    def is_bust(self):
        name = self._sum_cards(self.__cards)
        if int(name[1:]) > 21:
            return True
        return False
    # init
    def __init__(self, cards, funds) -> None:
        self.__cards = cards
        self.funds = funds

# Default class
class SGame(ABC):
    @abstractmethod
    def itterate(self, action=None):
        pass

# main game class
class BlackJackGame(SGame):
    # constants
    _MAXIMUM_PLAYERS = 4
    
    def _check_players(self):
        if self.__player_count > self._MAXIMUM_PLAYERS or self.__player_count <=0:
            raise Exception(f"Maximum number of players exceeded: {self.__player_count}") 
    
    # 1 step of game
    def itterate(self, action=None):
        # \\TODO: ALL OF THIS PART GOD HELP ME
                
                    
        
    # initial
    def __init__(self, deck_count=1, player_count=1, funds = [0]) -> None:
        # pre-build
        self.__player_count = player_count
        self._check_players() 
        self.__game_deck = Deck(deck_count)
        self.__player_hands = []
        # build
        self.__roll = 0
        for i in range(self.__player_count):
            self.__player_hands.append(hand([], 0)) # initiate emty hands
        self.__dealer_hand = hand([], 0)