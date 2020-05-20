import unittest

from game.board import Board
from game.boxes import Street


class BoardTest(unittest.TestCase):

    def test_make_boxes(self):
        board = Board()
        self.assertEqual("street", board.boxes[32].box_type)
        self.assertEqual(Street, type(board.boxes[13]))
        self.assertEqual("Rue de la Fayette", board.boxes[29].name)
        self.assertEqual("dark-blue", board.boxes[39].color)
        self.assertEqual([2, 10, 30, 90, 160, 250], board.boxes[1].rent)
        self.assertEqual(200, board.boxes[5].price)


if __name__ == '__main__':
    unittest.main()
