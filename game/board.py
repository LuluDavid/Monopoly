import json
from deprecated import deprecated
from game.boxes import Box, Street, Station, Tax, PublicCompany
from game.card import Card


class Board:
    """A simple class to describe the board"""

    def __init__(self, park_money=0, boxes_filename="game/data/boxes.json", cards_filename="game/data/cards.json"):
        self.boxes = self.make_boxes(boxes_filename)
        self.cards = self.make_cards(cards_filename)
        self.park_money = park_money
        self.last_open_card = None

    @staticmethod
    def make_boxes(boxes_filename):
        with open(boxes_filename) as boxes_file:
            json_boxes = json.loads(boxes_file.read())
        boxes = {}
        for box in json_boxes:
            box_id = int(box)
            if json_boxes[box]["type"] == "street":
                boxes[box_id] = Street(
                    box_id,
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["price"],
                    json_boxes[box]["rent"],
                    json_boxes[box]["color"]
                )
            elif json_boxes[box]["type"] == "station":
                boxes[box_id] = Station(
                    box_id,
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["price"]
                )
            elif json_boxes[box]["type"] == "tax":
                boxes[box_id] = Tax(
                    box_id,
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["rent"]
                )
            elif json_boxes[box]["type"] == "public-company":
                boxes[box_id] = PublicCompany(
                    box_id,
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["price"]
                )
            else:
                boxes[box_id] = Box(
                    box_id,
                    json_boxes[box]["type"],
                    json_boxes[box]["name"]
                )
        return boxes
        
    @staticmethod
    def make_cards(cards_filename):
        with open(cards_filename) as cards_file:
            json_cards = json.loads(cards_file.read())
        cards = {}
        for card in json_cards:
            card_id = int(card)
            cards[card_id] = Card(
                card_id,
                json_cards[card]["name"],
                json_cards[card]["type"],
                json_cards[card]["value"]
            )
        return cards
