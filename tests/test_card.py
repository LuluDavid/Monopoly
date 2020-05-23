import unittest

from game.player import Player
from game.card import Card
from game.board import Board
from game.game import Game
from game.globs import INITIAL_MONEY, MONEY_START_BOX, JAIL_POSITION


class CardsTest(unittest.TestCase):

    def test_earn_money(self):
        chloe = Player("Chloe", 0)
        card = Card(card_id="666", name="", card_type="earn-money", value=100)
        card.execute(chloe, None, None)
        self.assertEqual(INITIAL_MONEY + 100, chloe.money)

    def test_loose_money(self):
        chloe = Player("Chloe", 0)
        board = Board()
        card = Card(card_id="666", name="", card_type="loose-money", value=100)
        card.execute(chloe, None, board)
        self.assertEqual(INITIAL_MONEY - 100, chloe.money)
        self.assertEqual(board.park_money, 100)

    def test_taxes(self):
        chloe = Player("Chloe", 0)
        board = Board()
        chloe.buy_good(board.boxes[1])
        chloe.buy_good(board.boxes[3])
        chloe.buy_good(board.boxes[6])
        chloe.buy_good(board.boxes[8])
        chloe.buy_good(board.boxes[9])
        chloe.buy_houses(board.boxes[1], 5)
        chloe.buy_houses(board.boxes[3], 3)
        chloe.buy_houses(board.boxes[6], 5)
        chloe.buy_houses(board.boxes[8], 2)
        money_before_taxes = chloe.money
        card = Card(card_id="666", name="", card_type="taxes", value=[20, 50])
        card.execute(chloe, None, board)
        tax = 5*20 + 2*50
        self.assertEqual(money_before_taxes - tax, chloe.money)
        self.assertEqual(board.park_money, tax)

    def test_backwards(self):
        chloe = Player("Chloe", 0)
        lucien = Player("Lucien", 1)
        board = Board()
        board.boxes[3].players.append(0)
        chloe.position = 3
        board.boxes[20].players.append(1)
        lucien.position = 20
        card = Card(card_id="666", name="", card_type="backwards", value=4)
        card.execute(chloe, None, board)
        card.execute(lucien, None, board)
        self.assertEqual(39, chloe.position)
        self.assertEqual(16, lucien.position)

    def test_move_forward_to(self):
        chloe = Player("Chloe", 0)
        lucien = Player("Lucien", 1)
        board = Board()
        board.boxes[3].players.append(0)
        chloe.position = 3
        board.boxes[20].players.append(1)
        lucien.position = 20
        card = Card(card_id="666", name="", card_type="move-forward-to", value=5)
        card.execute(chloe, None, board)
        card.execute(lucien, None, board)
        self.assertEqual(5, chloe.position)
        self.assertEqual(5, lucien.position)
        self.assertEqual(INITIAL_MONEY, chloe.money)
        self.assertEqual(INITIAL_MONEY + MONEY_START_BOX, lucien.money)

    def test_move_backward_to(self):
        chloe = Player("Chloe", 0)
        lucien = Player("Lucien", 1)
        board = Board()
        board.boxes[3].players.append(0)
        chloe.position = 3
        board.boxes[20].players.append(1)
        lucien.position = 20
        card = Card(card_id="666", name="", card_type="move-backward-to", value=5)
        card.execute(chloe, None, board)
        card.execute(lucien, None, board)
        self.assertEqual(5, chloe.position)
        self.assertEqual(5, lucien.position)
        self.assertEqual(INITIAL_MONEY, chloe.money)
        self.assertEqual(INITIAL_MONEY, lucien.money)

    def test_go_to_jai(self):
        chloe = Player("Chloe", 0)
        board = Board()
        board.boxes[3].players.append(0)
        chloe.position = 3
        card = Card(card_id="666", name="", card_type="go-to-jail", value=-1)
        card.execute(chloe, None, board)
        self.assertTrue(chloe.in_jail)
        self.assertEqual(JAIL_POSITION, chloe.position)

    def test_birthday(self):
        game = Game({0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Emile"})
        chloe = game.players[0]
        lucien = game.players[1]
        gildas = game.players[2]
        emile = game.players[3]
        card = Card(card_id="666", name="", card_type="birthday", value=50)
        card.execute(chloe, game.players, game.board)
        self.assertEqual(INITIAL_MONEY + 3*50, chloe.money)
        self.assertEqual(INITIAL_MONEY - 50, lucien.money)
        self.assertEqual(INITIAL_MONEY - 50, gildas.money)
        self.assertEqual(INITIAL_MONEY - 50, emile.money)

    def test_loose_money_or_chance(self):
        chloe = Player("Chloe", 0)
        board = Board()
        card = Card(card_id="666", name="", card_type="loose-money-or-chance", value=100)
        card.execute(chloe, None, board)
        self.assertEqual(INITIAL_MONEY - 100, chloe.money)
        self.assertEqual(board.park_money, 100)


if __name__ == '__main__':
    unittest.main()
