import unittest

from game.player import Player
from game.board import Board
from game.globs import INITIAL_MONEY


class PlayerTest(unittest.TestCase):

    def test_throw_dices(self):
        chloe = Player("Chloe", 0)
        dices = chloe.throw_dices()
        self.assertTrue(2, len(dices))
        self.assertTrue(1 <= dices[0] <= 6)
        self.assertTrue(1 <= dices[1] <= 6)

    def test_earn_money(self):
        chloe = Player("Chloe", 0)
        earnings = 50
        self.assertEqual(INITIAL_MONEY + earnings, chloe.earn_money(earnings))

    def test_loose_money(self):
        chloe = Player("Chloe", 0)
        loss = 50
        self.assertEqual(INITIAL_MONEY - loss, chloe.loose_money(loss))

    def test_can_buy_good(self):
        chloe = Player("Chloe", 0, money=300)
        lucien = Player("Lucien", 0)
        board = Board()
        chloe.buy_good(board.boxes[3])
        lucien.buy_good(board.boxes[9])
        self.assertTrue(chloe.can_buy_good(board.boxes[1]))
        self.assertTrue(chloe.can_buy_good(board.boxes[5]))
        self.assertTrue(chloe.can_buy_good(board.boxes[12]))
        self.assertFalse(chloe.can_buy_good(board.boxes[2]))  # not a good
        self.assertFalse(chloe.can_buy_good(board.boxes[3]))  # chloe is owner
        self.assertFalse(chloe.can_buy_good(board.boxes[9]))  # lucien is owner
        self.assertFalse(chloe.can_buy_good(board.boxes[39]))  # not enough money

    def test_buy_good(self):
        chloe = Player("Chloe", 0)
        board = Board()
        chloe.buy_good(board.boxes[39])
        chloe.buy_good(board.boxes[1])
        chloe.buy_good(board.boxes[5])
        self.assertEqual(3, len(chloe.goods))
        self.assertEqual("Rue de la Paix", chloe.goods[0].name)
        self.assertEqual("Boulevard de Belleville", chloe.goods[1].name)
        self.assertEqual("Gare Montparnasse", chloe.goods[2].name)
        self.assertEqual(INITIAL_MONEY - sum([good.price for good in chloe.goods]), chloe.money)
        with self.assertRaises(Exception):
            chloe.buy_good(board.boxes[2])

    def test_has_full_color(self):
        chloe = Player("Chloe", 0)
        board = Board()
        chloe.buy_good(board.boxes[1])
        chloe.buy_good(board.boxes[3])
        chloe.buy_good(board.boxes[6])
        chloe.buy_good(board.boxes[8])
        chloe.buy_good(board.boxes[9])
        chloe.buy_good(board.boxes[11])
        self.assertTrue(chloe.has_full_color("brown"))
        self.assertTrue(chloe.has_full_color("light-blue"))
        self.assertFalse(chloe.has_full_color("pink"))
        self.assertFalse(chloe.has_full_color("green"))
        with self.assertRaises(KeyError):
            chloe.has_full_color("purple")

    def test_get_number_of_stations(self):
        chloe = Player("Chloe", 0)
        lucien = Player("Lucien", 1)
        gildas = Player("Gildas", 2)
        board = Board()
        chloe.buy_good(board.boxes[5])
        chloe.buy_good(board.boxes[15])
        lucien.buy_good(board.boxes[25])
        self.assertEqual(2, chloe.get_number_of_stations())
        self.assertEqual(1, lucien.get_number_of_stations())
        self.assertEqual(0, gildas.get_number_of_stations())

    def test_get_number_of_companies(self):
        chloe = Player("Chloe", 0)
        board = Board()
        chloe.buy_good(board.boxes[12])
        self.assertEqual(1, chloe.get_number_of_companies())

    def test_update_position(self):
        chloe = Player("Chloe", 1234)
        board = Board()
        board.boxes[0].players.append(1234)
        chloe.update_position([3, 4], board)
        self.assertEqual(7, chloe.position)
        self.assertNotIn(1234, board.boxes[0].players)
        self.assertIn(1234, board.boxes[7].players)
        chloe.update_position([35, 0], board)
        self.assertEqual(2, chloe.position)
        self.assertNotIn(1234, board.boxes[7].players)
        self.assertIn(1234, board.boxes[2].players)
        self.assertEqual(INITIAL_MONEY + 200, chloe.money)


if __name__ == '__main__':
    unittest.main()
