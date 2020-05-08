import json
from boxes import Box, Street, Station


class Board:
    """A simple class to describe the board"""

    def __init__(self, boxes_filename="./data/boxes.json"):
        self.boxes = self.make_boxes(boxes_filename)

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


if __name__ == "__main__":
    Board()
