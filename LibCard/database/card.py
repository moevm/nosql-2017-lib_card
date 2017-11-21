from typing import List, Dict


class HistoryRecord:

    def __init__(self, reader: str, date_from: str, date_to: str):
        self.reader = reader
        self.date_from = date_from
        self.date_to = date_to

    @staticmethod
    def create_from_list(obj: List[Dict[str, str]]):
        return [HistoryRecord(i['reader'], i['from'], i['to']) for i in obj] if obj else None


class Card:

    def __init__(self, title: str, author: str, year: str, history: List[HistoryRecord]):
        self.title = title
        self.author = author
        self.year = year
        self.history = history

    def __str__(self):
        return f'Card({self.title} {self.author} {self.year})'

    @staticmethod
    def create_from_dict(obj) -> 'Card':
        return Card(obj['title'], obj['author'], obj['year'], HistoryRecord.create_from_list(obj['history']))
