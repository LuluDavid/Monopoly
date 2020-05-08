import json
from game.boxes import Box, Street, Station
from game.cards import Card


class Board:
    """A simple class to describe the board"""

    def __init__(self, boxes_filename="game/data/boxes.json", community_funds_filename="game/data/community.json"): # From Python Path
        self.boxes = self.make_boxes(boxes_filename)
        self.community_funds = self.make_community_funds(community_funds_filename)

    @staticmethod
    def make_boxes(boxes_filename):
        with open(boxes_filename) as boxes_file:
            json_boxes = json.loads(boxes_file.read())
        boxes = []
        for box in json_boxes:
            if json_boxes[box]["type"] == "street":
                boxes.append(
                    Street(
                        int(box),
                        json_boxes[box]["type"],
                        json_boxes[box]["name"],
                        json_boxes[box]["price"],
                        json_boxes[box]["rent"],
                        json_boxes[box]["color"]
                    )
                )
            elif json_boxes[box]["type"] == "station":
                boxes.append(
                    Station(
                        int(box),
                        json_boxes[box]["type"],
                        json_boxes[box]["name"],
                        json_boxes[box]["price"]
                    )
                )
            else:
                boxes.append(
                    Box(
                        int(box),
                        json_boxes[box]["type"],
                        json_boxes[box]["name"]
                    )
                )
        return boxes

    def getBox(self, position):
        return self.boxes[position]
        
        
        
    @staticmethod
    def make_community_funds(community_funds_filename):
     with open(community_funds_filename) as community_file:
         json_community = json.loads(community_file.read())
     community = []
     for com in json_community:
         community.append(
             Card(
             int(com),
             json_community[com]["name"],
             json_community[com]["type"],
             json_community[com]["value"]
             )
         )
     return community
        
        


if __name__ == "__main__":
    Board()
