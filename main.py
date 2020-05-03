# This is an attempt to recreate the game Monopoly, because we do not want to pay
# for it on Steam, and mostly because we are very bored during this quarantine.

import json
from src.classes import User, Board, Street, Box, Game


def initGame():

    with open("boxes.json") as boxes_file:
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
        else:
            boxes.append(
                Box(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"]
                )
            )
    return Board(boxes)


if __name__ == "__main__":
    board = initGame()
    for box in board.boxes:
        print("{} - TYPE : {} \t\t NAME : {}".format(box.index, box.box_type, box.name))



































