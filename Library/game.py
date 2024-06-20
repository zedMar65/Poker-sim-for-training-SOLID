from abc import ABC, abstractmethod
from random import shuffle
import os


def CodeError(code):
    if code == 0:
        return "Not enough funds for double"
    elif code == 1:
        return "Can't double after hit"
    elif code == 2:
        return "Can't split non-pair"
    elif code == 3:
        return "Not enough funds for split"
    elif code == 4:
        return "Invalid action"
    elif code == 5:
        return "Dealer has blackjack, new game"
    elif code == 6:
        return "Deck has been reshuffled"
    elif code == 7:
        return "Game over"
    else:
        return "Unknown error"
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
    def add_player(self, player) -> None:
        pass
    def normal_info(self) -> str:
        pass
    def __init__(self, players = [], deck_count=1, log=False, cut_procent = 60) -> None:
        pass

def HLcount(cards):
    count = 0
    for card in cards:
        if card in ['2', '3', '4', '5', '6']:
            count += 1
        elif card in ['10', 'J', 'Q', 'K', 'A']:
            count -= 1
    return count

# default class
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
        bet = 0
        self.funds -= bet
        pass
    @abstractmethod
    def kick(self, info) -> None:
        pass
    @abstractmethod
    def check_insurence(self, info) -> bool:
        pass

class DealerBot():
    def play(hand):
        hand_type = hand[0]
        total = int(hand[1:])

        if hand_type == 'S':  # Soft hand
            if total < 18:  # Soft 17 rule (stand on soft 17 or higher)
                return "H"
            else:
                return "S"
        else:
            if total < 17:
                return "H"
            else:
                return "S"

class PlayerBot(SBot):
    def __init__(self, funds, name):
        self.name = name
        self.funds = funds
        # Strategy mappings
        self.hard_totals = {
            17: "S", 16: "S", 15: "S", 14: "S", 13: "S", 12: "H",
            11: "D", 10: "D", 9: "H", 8: "H"
        }
        self.soft_totals = {
            19: "S", 18: "S", 17: "H", 16: "H", 15: "H", 14: "H", 13: "H"
        }
        self.pair_splitting = {
            "A": "Y", "T": "N", "9": "Y", "8": "Y", "7": "Y", "6": "H",
            "5": "N", "4": "H", "3": "H", "2": "H"
        }

    def play(self, info):
        player_hand = info["p_cards"]
        dealer_hand = info["d_cards"]
        dealer_total = int(dealer_hand[1:])
        player_type = player_hand[0]
        player_total = int(player_hand[1:])

        if player_type == 'H':  # Hard hand
            return self._get_hard_action(player_total, dealer_total)
        elif player_type == 'S':  # Soft hand
            return self._get_soft_action(player_total, dealer_total)
        elif player_type == 'P':  # Pair hand
            pair_value = player_hand[1]
            return self._get_pair_action(pair_value, dealer_total)
        else:
            raise ValueError("Invalid hand type")
    def get_bet(self, info):
        bet = self.funds/100
        self.funds -= bet
        self.last_bet = bet
        return bet
    def _get_hard_action(self, player_total, dealer_total):
        if player_total >= 17:
            return "S"
        elif player_total == 16:
            return "S" if dealer_total < 7 else "H"
        elif player_total == 15:
            return "S" if dealer_total < 7 else "H"
        elif player_total == 14:
            return "S" if dealer_total < 7 else "H"
        elif player_total == 13:
            return "S" if dealer_total < 7 else "H"
        elif player_total == 12:
            return "H" if dealer_total in [2, 3, 7, 8, 9, 10, 11] else "S"
        elif player_total == 11:
            if self.last_bet >= self.funds:
                return "D"
            else:
                return "H"
        elif player_total == 10:
            if self.last_bet >= self.funds:
                return "D" if dealer_total < 10 else "H"
            else:
                return "H"
        elif player_total == 9:
            if self.last_bet >= self.funds:
                return "D" if dealer_total in [3, 4, 5, 6] else "H"
            else:
                return "H"
        else:
            return "H"

    def _get_soft_action(self, player_total, dealer_total):
        if player_total >= 19:
            return "S"
        elif player_total == 18:
            if dealer_total in [2, 7, 8]:
                return "S"
            elif dealer_total in [3, 4, 5, 6]:
                return "S"
            else:
                return "H"
        elif player_total == 17:
            return "S" if dealer_total in [3, 4, 5, 6] else "H"
        elif player_total == 16:
            if self.last_bet >= self.funds:
                return "D" if dealer_total in [4, 5, 6] else "H"
            else:
                return "H"
        elif player_total == 15:
            if self.last_bet >= self.funds:
                return "D" if dealer_total in [4, 5, 6] else "H"
            else:
                return "H"
        elif player_total == 14:
            if self.last_bet >= self.funds:
                return "D" if dealer_total in [4, 5, 6] else "H"
            else:
                return "H"
        elif player_total == 13:
            if self.last_bet >= self.funds:
                return "D" if dealer_total in [4, 5, 6] else "H"
            else:
                return "H"
        else:
            return "H"

    def _get_pair_action(self, pair_value, dealer_total):
        if pair_value == "A":
            if self.last_bet <= self.funds:
                return "Y" if dealer_total < 7 else "H"
            else:
                return "H"
        elif pair_value == "T":
            if self.last_bet <= self.funds:
                return "D"
            else:
                return "H"
        elif pair_value == "8":
            return "H"
        elif pair_value == "6":
            if dealer_total < 7 and self.last_bet <= self.funds:
                return "Y"
            else:
                return "H"
        elif pair_value == "4":
            if dealer_total < 7 and self.last_bet <= self.funds:
                return "Y"
            else:
                return "H"
        else:
            return "H"
    def kick(self, info):
        print(f"Run out of funds: {info}")
    def check_insurence(self, info):
        return False
        pass

# playable class
class HumanBotWithCount(SBot):
    def __init__(self, funds, name):
        self.name = name
        self.funds = funds
        
    def play(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Your hand: {info['p_cards']}")
        print(f"Dealer's hand: {info['d_cards']}")
        print(f"Count: {HLcount(info['cards'])}")
        print(f"Decks remaining: {int(info['deck_game'] - len(info['cards'])/52)}")
        print(f"Funds: {self.funds}")

        action = input("Enter action (H(hit), S(stand), D(double), Y(split)): ")
        return action

    def get_bet(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Count: {HLcount(info['cards'])}")
        print(f"Decks remaining: {int(info['deck_game'] - len(info['cards'])/52)}")
        print(f"Funds: {self.funds}")
        bet = int(input("Enter bet: "))
        self.funds -= bet
        return bet

    def kick(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Game over, info: \n{info}\nFunds: {self.funds}")
        
    def check_insurence(self, info):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)
        print(f"Dealer's hand: {info['d_cards']}")
        print(f"Count: {HLcount(info['cards'])}")
        print(f"Decks remaining: {int(info['deck_game'] - len(info['cards'])/52)}")
        print(f"Funds: {self.funds}")
        action = input("Do you want to insure? (Y/N): ")
        return True if action == "Y" else False
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

class Deck(SDeck):
    # Constants
    _DECK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']*4
    
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
        if len(self.__used_deck) / (len(self.__used_deck) + len(self.__deck)) * 100 > self.cut_procent:
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
    def __init__(self, deck_count=1, cut_procent = 60) -> None:
        self._deck_count = deck_count
        self.cut_procent = cut_procent
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
    
    # 1 step of game
    def itterate(self):
        self.table_cards = []
        # check if there are players
        if self.__player_count == 0:
            if self.log:
                print("Game over")
            return 7
        
        # check for cut card and reshuffle if so
        if self.__game_deck.check_for_cut():
            if self.log:
                print("Deck has been reshuffled.")
            return 6
        # deal new round: ask ewery player for new bets, deal to dealer and other hands
        for i in range(self.__player_count):
            info = self._get_info(i)
            self.__player_hands[i].bet_m(self.__players[i].get_bet(info))
        for i in range(self.__player_count):
            for j in range(2):
                card = self.__game_deck.deal_card()
                self.__player_hands[i].add_to_hand(card)
                self.table_cards += card
        # deal for dealer
        self.__dealer_hand.add_to_hand(self.__game_deck.deal_card())
        self.table_cards += self.__dealer_hand.get_upCard()
        self.__game_deck.reserve_dealer()
        if self.__dealer_hand.get_upCard() == "A":
            if self.__insurence_scam101():
                self.__dealer_hand.add_to_hand(self.__game_deck.reveal_dealer())
                # start a new game if dealer has blackjack
                if self.log:
                    print("Dealer has blackjack, new game.")
                return 5
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
                            if self.log:
                                print(f"Player {player.name}, not enough funds for double")
                            return 0
                        if hand.count() > 2:
                            if self.log:
                                print(f"Player {player.name}, can't double after hit.")
                            return 1
                        card = self.__game_deck.deal_card()
                        hand.add_to_hand(card)
                        self.table_cards += card
                        hand.bet_m(hand.bet)
                        player.funds -= hand.bet
                        break
                    elif choice == "Y":
                        if hand.get_cards()[0] != "P":
                            if self.log:
                                print(f"Player {player.name}, can't split non-pair.")
                            return 2
                        if player.funds < hand.bet:
                            if self.log:
                                print(f"Player {player.name}, not enough funds for split.")
                            return 3
                        hand2 = Hand()
                        hand2.add_to_hand(self.__game_deck.deal_card())
                        hand2.add_to_hand(self.__game_deck.deal_card())
                        self.table_cards += hand2._cards[0]
                        self.table_cards += hand2._cards[1]
                        hand2.bet_m(hand.bet)
                        player.funds -= hand.bet
                    else:
                        if self.log:
                            print(f"Player {player.name}, invalid action.")
                        return 4
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
        dealer_total = int(self.__dealer_hand.get_cards()[1:])
        if self.__dealer_hand.is_bust():
            dealer_total = 0
        for i in range(self.__player_count):
            player_total = int(self.__player_hands[i].get_cards()[1:])
            if self.__player_hands[i].get_cards() == "B21":
                self.__players[i].funds += int(2.5*self.__player_hands[i].bet)
                return_str += f"Player {self.__players[i].name} has: {self.__player_hands[i]._cards} and won {int(2.5*self.__player_hands[i].bet)}.\n"
                break
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
        if self.log:
            print(f"Player {self.__players[index].name} has been kicked from the game.")
        self.__dead_players.append(self.__players[index])
        self.__players.pop(index)
        self.__player_hands.pop(index)
        self.__player_count -= 1
        
    
    def _get_info(self, index):
        return {
    "cards": self.__game_deck.get_used_cards(),        # Cards that at some point were on the table before resuffuling
    "p_cards": self.__player_hands[index].get_cards(), # The hand of the player formated as for example: B21, P8, H20, H10, P18, S18, S17, etc...
    "d_cards": self.__dealer_hand.get_cards(),         # Dealers hand formated in the same way
    "p_count": self.__player_count,                    # How many players playing
    "deck_game": self.__game_deck._deck_count,         # How many decks in the game
    "pos": index+1,                                    # Which position the player is sitting
    "num": self.__game_number,                         # Which game it is played
    "table_cards": self.table_cards                    # The cards that are currently on the table dealt
            }
    
    def get_game_number(self):
        return self.__game_number
    # initial
    def add_player(self, player):
        self.__players.append(player)
        self.__player_count += 1
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
    def __init__(self, players = [], deck_count=1, log=False, cut_procent = 60) -> None:
        # pre-build
        
        self.log = log
        self.table_cards = []
        self.__dead_players = []
        self.__game_number = 0
        self.__players = players
        self.__player_count = len(players)
        self.__game_deck = Deck(deck_count, cut_procent)
        self.__player_hands = []
        # build
        for i in range(self.__player_count):
            self.__player_hands.append(Hand()) # initiate emty hands
        self.__dealer_hand = DealerHand()