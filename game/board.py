import json
from game.boxes import Box, Street, Station, Tax, PublicService
from game.cards import Card


class Board:
    """A simple class to describe the board"""

    def __init__(self, boxes_filename="game/data/boxes.json", cards_filename="game/data/cards.json", parc_money = 0): # From Python Path
        self.boxes = self.make_boxes(boxes_filename)
        self.cards = self.make_cards(cards_filename)
        self.parc_money = parc_money

    @staticmethod
    def make_boxes(boxes_filename):
        with open(boxes_filename) as boxes_file:
            json_boxes = json.loads(boxes_file.read())
        boxes = {}
        for i, box in enumerate(json_boxes):
            if json_boxes[box]["type"] == "street":
                boxes[i] = Street(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["price"],
                    json_boxes[box]["rent"],
                    json_boxes[box]["color"]
                )
            elif json_boxes[box]["type"] == "station":
                boxes[i] = Station(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["price"]
                )
            elif json_boxes[box]["type"] == "tax":
                boxes[i] = Tax(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["rent"]
                )
            elif json_boxes[box]["type"] == "public-service":
                boxes[i] = PublicService(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"],
                    json_boxes[box]["price"]
                )
            else:
                boxes[i] = Box(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"]
                )
        return boxes

    def getBox(self, position):
        return self.boxes[position]
        
        
        
    @staticmethod
    def make_cards(cards_filename):
     with open(cards_filename) as cards_file:
         json_cards = json.loads(cards_file.read())
     card = []
     for com in json_cards:
         card.append(
             Card(
             int(com),
             json_cards[com]["name"],
             json_cards[com]["type"],
             json_cards[com]["value"]
             )
         )
     return card
        
        


if __name__ == "__main__":
    Board()
