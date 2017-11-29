from database.card import Card
from typing import List, Tuple


class TempDatabase:

    def __init__(self, cards: List[Tuple[str, Card]]):
        self.cards = cards
