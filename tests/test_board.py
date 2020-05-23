import unittest

from game.board import Board
from game.boxes import Street
from game.card import Card


class BoardTest(unittest.TestCase):

    def test_make_boxes(self):
        board = Board()
        self.assertEqual("street", board.boxes[32].box_type)
        self.assertEqual(Street, type(board.boxes[13]))
        self.assertEqual("Rue de la Fayette", board.boxes[29].name)
        self.assertEqual("dark-blue", board.boxes[39].color)
        self.assertEqual([2, 10, 30, 90, 160, 250], board.boxes[1].rent)
        self.assertEqual(200, board.boxes[5].price)

    def test_make_cards(self):
        board = Board()
        self.assertEqual("earn-money", board.cards[0].card_type)
        self.assertEqual("Payez votre Police d'Assurance s'elevant a 50 euros", board.cards[1].name)
        self.assertEqual(50, board.cards[4].value)
        self.assertEqual(Card, type(board.cards[13]))


if __name__ == '__main__':
    unittest.main()
