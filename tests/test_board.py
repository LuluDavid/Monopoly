import unittest

from game.board import Board
from game.boxes import Street


class BoardTest(unittest.TestCase):

    def test_get_box(self):
        position = 39
        board = Board()
        self.assertEqual(board.boxes[position], board.getBox(position))

    def test_make_boxes(self):
        board = Board()
        self.assertEqual(board.boxes[32].box_type, "street")
        self.assertEqual(type(board.boxes[13]), Street)
        self.assertEqual(board.boxes[29].name, "Rue de la Fayette")
        self.assertEqual(board.boxes[39].color, "dark-blue")
        self.assertEqual(board.boxes[1].rent, [2, 10, 30, 90, 160, 250])
        self.assertEqual(board.boxes[5].price, 200)


if __name__ == '__main__':
    unittest.main()