from abc import ABC, abstractmethod
from random import shuffle

# Default class
class SDeck(ABC):
    @abstractmethod
    def deal_card(self) -> str:
        pass
    @abstractmethod
    def check_for_cut(self) -> bool:
        pass

# Default class
class SGame(ABC):
    @abstractmethod
    def itterate(self) -> str:
        pass
    def get_game_number(self) -> int:
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
        self.decks_used += 1
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
    def get_used_cards(self):
        return self.__used_deck
    def reserve_dealer(self):
        self.dealer_card = self.__deck[-1]
        self.__deck.pop()
        return self.dealer_card
    def reveal_dealer(self):
        self.__used_deck.append(self.dealer_card)
        return self.dealer_card
    # Initial
    def __init__(self, deck_count=1) -> None:
        if deck_count not in self._VIABLE_DECKS:
            raise Exception(f"1")
        self.__deck_count = deck_count
        self._shuffle()
        self.decks_used = 0

# hand class to handle hands:
class Hand(object):
    # get the hand name
    def _sum_cards(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 0}
        for card in hand:
            if card not in values:
                raise Exception("2")
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
        self._cards.append(card)
    def get_cards(self):
        name = self._sum_cards(self._cards)
        return f"{name}"
    def clear(self):
        self.bet = 0
        self._cards = []
    def is_bust(self):
        name = self._sum_cards(self._cards)
        if int(name[1:]) > 21:
            return True
        return False
    def bet(self, sum):
        self.bet = sum
    # init
    def __init__(self) -> None:
        self._cards = []
        
class DealerHand(Hand):
    def get_upCard(self):
        return self._cards[0]

# main game class
class BlackJackGame(SGame):
    # constants
    _MAXIMUM_PLAYERS = 4
    
    def _check_players(self):
        if self.__player_count > self._MAXIMUM_PLAYERS or self.__player_count <=0:
            raise Exception(f"3") 
    
    # 1 step of game
    def itterate(self):
        if self.__roll == self.__player_count:
            self.__roll = 0
            # round up the last game: reveal delers card, check for win and push, clear all hands
            
            # TODO play the dealers cards
            self.__dealer_hand.add_to_hand(self.__game_deck.reveal_dealer())
            dealer_total = self.__dealer_hand.get_cards()[:1]
            for i in range(self.__player_count):
                player_total = self.__player_hands[i].get_cards()[1:]
                if player_total > dealer_total and not self.__player_hands[i].is_bust():
                    self.__players[i].funds += 2*self.__player_hands[i].bet
                elif player_total == dealer_total and not self.__player_hands[i].is_bust():
                    self.__players[i].funds += self.__player_hands[i].bet
                self.__player_hands[i].clear()
                # check if any players have 0 funds, if so kick from the game
                if self.__players[i].funds <= 0:
                    self.__kick(i)
            self.__dealer_hand.clear()
            self.__game_number += 1
            
            # check if there are players
            if self.__player_count == 0:
                raise Exception("0")
            
            # check for cut card and reshuffle if so
            self.__game_deck.check_for_cut()
            # deal new round: ask ewery player for new bets, deal to dealer and other hands
            for i in range(self.__player_count):
                info = self._get_info(i)
                self.__player_hands[i].bet(self.__players[i].get_bet(info))
            for i in range(self.__player_count):
                for j in range(2):
                    self.__player_hands[i].add_to_hand(self.__game_deck.deal_card())
            # deal for dealer
            self.__dealer_hand.add_to_hand(self.__game_deck.deal_card())
            
            if self.__dealer_hand._sum_cards([self.__dealer_hand.get_upCard, self.__game_deck.reserve_dealer()])[1:] == "21":
                
    
    def __kick(self, index):
        self.__players[index].kick(self.__game_number)
        self.__players.pop(index)
        self.__player_hands.pop(index)
        self.__player_count -= 1
    
    def _get_info(self, index):
        return [self.__game_deck.get_used_cards(), self.__player_hands[index], self.__dealer_hand.get_upCard, self.__player_count, index, self.__game_number]
    
    def get_game_number(self):
        return self.__game_number
    # initial
    def __init__(self, players, deck_count=1) -> None:
        # pre-build
        self.__game_number = 0
        self.__players = players
        self.__player_count = len(players)
        self._check_players() 
        self.__game_deck = Deck(deck_count)
        self.__player_hands = []
        # build
        self.__roll = 0
        for i in range(self.__player_count):
            self.__player_hands.append(Hand()) # initiate emty hands
        self.__dealer_hand = DealerHand()