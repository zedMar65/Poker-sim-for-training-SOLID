from abc import ABC, abstractmethod
import os
# clear later
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