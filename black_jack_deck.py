from enum import Enum
from typing import List
import random

class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"

class BlackJackCard:

    rank_values = {"2": 2, "3": 3,"4": 4,"5": 5,
                   "6": 6,"7": 7,"8": 8,"9": 9,"10": 10,
                   "J": 10, "Q": 10, "K": 10, "A": 1}

    def __init__(
            self,
            rank: str,
            suit: Suit
     ) -> None:
        if rank not in self.rank_values:
            raise ValueError(f"{rank} is not a valid rank.")
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit.value}"

    @property
    def hard(self) -> int:
        return self.rank_values[self.rank]
    
    @property
    def soft(self) -> int:
        if self.rank == "A":
            return 11
        else:
            return self.rank_values[self.rank]

class Deck():
    def __init__(self) -> None:
        self.deck = self.generate_deck()

    @classmethod
    def generate_deck(cls) -> List[BlackJackCard]:
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = [BlackJackCard(rank, suit) for suit in Suit for rank in ranks]
        return deck
    
    def pop(self) -> BlackJackCard:
        random_index = random.randint(0, len(self.deck) - 1)
        return self.deck.pop(random_index)

class Hand:
    def __init__(
        self,
        dealer_card: BlackJackCard,
        *cards: BlackJackCard
    ) -> None:
        self.dealer_card = dealer_card
        self._cards = list(cards)

    def __str__ (self) -> str:
        return ", ".join(map(str, self.card))

    def __repr__ (self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r}, "
            f"{', '.join(map(repr, self.card))})"
        )

class Hand_Lazy(Hand):
    @property
    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self._cards)
        hard_total = sum(c.hard for c in self ._cards)
        if hard_total + delta_soft <= 21:
            return hard_total + delta_soft
        return hard_total

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, aCard: BlackJackCard) -> None:
        self._cards.append(aCard)

    @card.deleter
    def card(self) -> None:
        self._cards.pop(-1)

def main():
    d = Deck()
    h = Hand_Lazy(d.pop(),d.pop(),d.pop())
    print(h)
    print(h.total)

if __name__ == '__main__':
    main()

