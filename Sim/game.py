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
        self.__deck = self._DECK * self._deck_count
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
            raise Exception(f"Deck count is {deck_count} and should be in {self._VIABLE_DECKS}.")
        self._deck_count = deck_count
        self.decks_used = 0
        self._shuffle()
        

# hand class to handle hands:
class Hand(object):
    # get the hand name
    def _sum_cards(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 0}
        for card in hand:
            if card not in values:
                raise Exception(f"Invalid card: {card}")
        total_value = sum(values[card] for card in hand)
        has_ace = 'A' in hand

        # Check for pairs
        if len(hand) == 2 and hand[0] == hand[1]:
            if hand[0] == 'A':
                return "P2"
            return "P" + str(total_value)
        if has_ace and total_value == 10 and len(hand) == 2:
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
    def bet_m(self, sum):
        self.bet += sum
    def count(self):
        return len(self._cards)
    # init
    def __init__(self) -> None:
        self.bet = 0
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
            raise Exception(f"Player count is {self.__player_count} and should be between 1 and 4.")
    
    # 1 step of game
    def itterate(self):
        self.table_cards = []
        # check if there are players
        if self.__player_count == 0:
            return "Game over"
        
        # check for cut card and reshuffle if so
        if self.__game_deck.check_for_cut():
            return "Cut card reached, reshuffling."
        # deal new round: ask ewery player for new bets, deal to dealer and other hands
        for i in range(self.__player_count):
            info = self._get_info(i)
            self.__player_hands[i].bet_m(self.__players[i].get_bet(info))
        for i in range(self.__player_count):
            for j in range(2):
                card = self.__game_deck.deal_card()
                self.__player_hands[i].add_to_hand(card)
                self.table_cards += card
            if self.__player_hands[i].get_cards()[1:] == "21":
                # TODO idk this is a bug
                self.__players[i].funds += self.__player_hands[i].bet/2*3
        # deal for dealer
        self.__dealer_hand.add_to_hand(self.__game_deck.deal_card())
        self.table_cards += self.__dealer_hand.get_upCard()
        self.__game_deck.reserve_dealer()
        if self.__dealer_hand.get_upCard() == "A":
            if self.__insurence_scam101():
                self.__dealer_hand.add_to_hand(self.__game_deck.reveal_dealer())
                # start a new game if dealer has blackjack
                return "BJ Loss"
        return_str = ""
        # play the game: ask ewery player for action, deal cards if needed
        for i in range(self.__player_count):
            player = self.__players[i]
            hand1 = self.__player_hands[i]
            hand2 = None
            # play the players turn with hand
            for hand in [hand1, hand2]:
                if hand is None:
                    continue
                while not hand.is_bust() and hand.get_cards()[1:] != "21" and hand.get_cards() != "B21":
                    choice = player.play(self._get_info(i))
                    if choice == "H":
                        card = self.__game_deck.deal_card()
                        hand.add_to_hand(card)
                        self.table_cards += card
                    elif choice == "S":
                        i += 1
                        break
                    elif choice == "D":
                        if player.funds < hand.bet:
                            print(f"Player {player.name}, not enough funds for double. Try again.")
                            i -= 1
                            break
                        if hand.count() > 2:
                            print(f"Player {player.name}, can't double after hit. Try again.")
                            i -= 1
                            break
                        card = self.__game_deck.deal_card()
                        hand.add_to_hand(card)
                        self.table_cards += card
                        hand.bet_m(hand.bet)
                        player.funds -= hand.bet
                        break
                    elif choice == "Y":
                        if hand.get_cards()[0] != "P":
                            print(f"Player {player.name}, can't split non-pair. Try again.")
                            i -= 1
                            break
                        if player.funds < hand.bet:
                            print(f"Player {player.name}, not enough funds for split. Try again.")
                            i -= 1
                            break
                        hand2 = Hand()
                        hand2.add_to_hand(self.__game_deck.deal_card())
                        hand2.add_to_hand(self.__game_deck.deal_card())
                        self.table_cards += hand2._cards[0]
                        self.table_cards += hand2._cards[1]
                        hand2.bet_m(hand.bet)
                        player.funds -= hand.bet
                    else:
                        print(f"Player {player.name}, invalid action. Try again.")
                        i -= 1
                        break
        # round up the last game: reveal delers card, check for win and push, clear all hands
        
        # reveal dealer cards
        self.__dealer_hand.add_to_hand(self.__game_deck.reveal_dealer())
        
        # play dealer
        while not self.__dealer_hand.is_bust() or self.__dealer_hand.get_cards()[1:] != "21" or self.__dealer_hand.get_cards() != "B21":
            if int(self.__dealer_hand.get_cards()[1:]) > 16 and self.__dealer_hand.get_cards()[0] != "S":
                break
            if int(self.__dealer_hand.get_cards()[1:]) > 17:
                break
            self.__dealer_hand.add_to_hand(self.__game_deck.deal_card())
        # check for win and push
        dealer_total = int(self.__dealer_hand.get_cards()[:1])
        if self.__dealer_hand.is_bust():
            dealer_total = 0
        for i in range(self.__player_count):
            player_total = int(self.__player_hands[i].get_cards()[1:])
            if player_total > dealer_total and not self.__player_hands[i].is_bust():
                self.__players[i].funds += 2*self.__player_hands[i].bet
                return_str += f"Player {self.__players[i].name} has: {self.__player_hands[i]._cards} and won {2*self.__player_hands[i].bet}.\n"
            elif player_total == dealer_total and not self.__player_hands[i].is_bust():
                self.__players[i].funds += self.__player_hands[i].bet
                return_str += f"Player {self.__players[i].name} has: {self.__player_hands[i]._cards} and pushed {self.__player_hands[i].bet}.\n"
            else:
                return_str += f"Player {self.__players[i].name} has: {self.__player_hands[i]._cards} and lost {self.__player_hands[i].bet}.\n"
            self.__player_hands[i].clear()
            # check if any players have 0 funds, if so kick from the game
            if self.__players[i].funds <= 0:
                return_str += f"Player {self.__players[i].name} has run out of funds.\n"
                self.__kick(i)
        return_str += f"Dealer has: {self.__dealer_hand._cards}\n"
        self.__dealer_hand.clear()
        self.__game_number += 1
        return_str += f"Game number: {self.__game_number}\n"
        return_str += f"The table cards are: {self.table_cards}\n"
        return return_str
                
    def __insurence_scam101(self):
        insured_indexes = []
        for i in range(self.__player_count):
            if self.__players[i].check_insurence(self._get_info(i)):
                insured_indexes.append(i)
        if self.__dealer_hand._sum_cards([self.__dealer_hand.get_upCard(), self.__game_deck.dealer_card])[1:] == "21":
            for i in range(self.__player_count):
                if i in insured_indexes:
                    self.__players[i].funds += self.__player_hands[i].bet
            return True
        else:
            for i in range(self.__player_count):
                if i in insured_indexes:
                    self.__players[i].funds -= self.__player_hands[i].bet/2
            return False
    def __kick(self, index):
        self.__players[index].kick(self.normal_info())
        print(f"Player {self.__players[index].name} has been kicked from the game.")
        self.__dead_players.append(self.__players[index])
        self.__players.pop(index)
        self.__player_hands.pop(index)
        self.__player_count -= 1
        self._check_players()
        
    
    def _get_info(self, index):
        return {
            "cards": self.__game_deck.get_used_cards(), 
            "p_cards": self.__player_hands[index].get_cards(), 
            "d_cards": self.__dealer_hand.get_cards(), 
            "p_count": self.__player_count,
            "deck_game": self.__game_deck._deck_count,
            "pos": index+1, 
            "num": self.__game_number,
            "table_cards": self.table_cards
            }
    
    def get_game_number(self):
        return self.__game_number
    # initial
    def add_player(self, player):
        self.__players.append(player)
        self.__player_count += 1
        self._check_players()
        self.__player_hands.append(Hand())
    def normal_info(self):
        info_str = ""
        info_str += f"Game number: {self.__game_number}\n"
        info_str += f"Player count: {self.__player_count}\n"
        info_str += f"Deck count: {self.__game_deck._deck_count}\n"
        info_str += f"Alive Players: {', '.join([player.name for player in self.__players])}\n"
        info_str += f"Players funds: {', '.join([str(player.funds) for player in self.__players])}\n"
        info_str += f"Dead players: {', '.join([player.name for player in self.__dead_players])}\n"
        info_str += f"Decks used: {self.__game_deck.decks_used}\n"
        return info_str
    def __init__(self, players = [], deck_count=1) -> None:
        # pre-build
        self.table_cards = []
        self.__dead_players = []
        self.__game_number = 0
        self.__players = players
        self.__player_count = len(players)
        self.__game_deck = Deck(deck_count)
        self.__player_hands = []
        # build
        for i in range(self.__player_count):
            self.__player_hands.append(Hand()) # initiate emty hands
        self.__dealer_hand = DealerHand()