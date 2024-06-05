from abc import ABC, abstractmethod

# default class
class SBot(ABC):
    @abstractmethod
    def play(hand) -> str:
        pass

class DealerBot(SBot):
    @staticmethod
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
    def __init__(self, funds):
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

    def play(self, player_hand, dealer_hand):
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
            return "D"
        elif player_total == 10:
            return "D" if dealer_total < 10 else "H"
        elif player_total == 9:
            return "D" if dealer_total in [3, 4, 5, 6] else "H"
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
            return "D" if dealer_total in [4, 5, 6] else "H"
        elif player_total == 15:
            return "D" if dealer_total in [4, 5, 6] else "H"
        elif player_total == 14:
            return "D" if dealer_total in [4, 5, 6] else "H"
        elif player_total == 13:
            return "D" if dealer_total in [4, 5, 6] else "H"
        else:
            return "H"

    def _get_pair_action(self, pair_value, dealer_total):
        if pair_value == "A":
            return "Y"
        elif pair_value == "T":
            return "N"
        elif pair_value == "9":
            return "Y" if dealer_total != 7 and dealer_total != 10 and dealer_total != 11 else "S"
        elif pair_value == "8":
            return "Y"
        elif pair_value == "7":
            return "Y" if dealer_total < 8 else "H"
        elif pair_value == "6":
            return "Y" if dealer_total < 7 else "H"
        elif pair_value == "5":
            return "D" if dealer_total < 10 else "H"
        elif pair_value == "4":
            return "H" if dealer_total in [5, 6] else "H"
        elif pair_value == "3":
            return "H" if dealer_total < 8 else "H"
        elif pair_value == "2":
            return "H" if dealer_total < 8 else "H"
        else:
            return "H"