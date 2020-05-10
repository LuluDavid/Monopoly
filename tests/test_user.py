import unittest

from game.user import User
from game.board import Board
from game.globs import INITIAL_MONEY


class UserTest(unittest.TestCase):

    """Test for class User"""

    def test_get_username(self):
        chloe = User("Chloe",0)
        lucien = User("Lucien",1)
        self.assertEqual(chloe.getUserName(), "Chloe")
        self.assertEqual(lucien.getUserName(), "Lucien")

    def test_set_in_jail(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        lucien = User("Lucien",2)
        chloe.setInPrison(True)
        gildas.setInPrison(False)
        self.assertTrue(chloe.getInPrison())
        self.assertFalse(gildas.getInPrison())
        self.assertFalse(lucien.getInPrison())

    def test_set_position(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        lucien = User("Lucien",2)
        chloe.setPosition(24)
        gildas.setPosition(0)
        self.assertEqual(chloe.getPosition(), 24)
        self.assertEqual(gildas.getPosition(), 0)
        self.assertEqual(lucien.getPosition(), 0)

    def test_earn_money(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        lucien = User("Lucien",2)
        chloe.EarnMoney(50)
        gildas.EarnMoney(0)
        self.assertEqual(chloe.getMoney(), INITIAL_MONEY + 50)
        self.assertEqual(gildas.getMoney(), INITIAL_MONEY)
        self.assertEqual(lucien.getMoney(), INITIAL_MONEY)

    def test_loose_money(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        lucien = User("Lucien",2)
        chloe.LooseMoney(50)
        gildas.LooseMoney(0)
        self.assertEqual(chloe.getMoney(), INITIAL_MONEY - 50)
        self.assertEqual(gildas.getMoney(), INITIAL_MONEY)
        self.assertEqual(lucien.getMoney(), INITIAL_MONEY)

    def test_buy_street(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        lucien = User("Lucien",2)
        board = Board()
        chloe.buyAStreet(board.boxes[39])
        chloe.buyAStreet(board.boxes[1])
        gildas.buyAStreet(board.boxes[3])
        self.assertEqual(len(lucien.getGoods()), 0)
        self.assertEqual(lucien.getMoney(), INITIAL_MONEY)
        self.assertEqual(len(gildas.getGoods()), 1)
        self.assertEqual(gildas.getGoods()[0].name, "Rue Lecourbe")
        self.assertEqual(board.boxes[3].owner, gildas)
        self.assertEqual(len(chloe.getGoods()), 2)
        self.assertEqual(chloe.getGoods()[0].name, "Rue de la Paix")
        self.assertEqual(chloe.getGoods()[1].name, "Boulevard de Belleville")
        self.assertEqual(chloe.getMoney(), INITIAL_MONEY - 400 - 60)

    def test_buy_station(self):
        chloe = User("Chloe",0)
        gildas = User("Gildas",1)
        lucien = User("Lucien",2)
        board = Board()
        chloe.buyAStation(board.boxes[5])
        chloe.buyAStation(board.boxes[15])
        gildas.buyAStation(board.boxes[25])
        self.assertEqual(len(lucien.getGoods()), 0)
        self.assertEqual(lucien.getMoney(), INITIAL_MONEY)
        self.assertEqual(len(gildas.getGoods()), 1)
        self.assertEqual(gildas.getGoods()[0].name, "Gare du Nord")
        self.assertEqual(board.boxes[25].owner, gildas)
        self.assertEqual(len(chloe.getGoods()), 2)
        self.assertEqual(chloe.getGoods()[0].name, "Gare Montparnasse")
        self.assertEqual(chloe.getGoods()[1].name, "Gare de Lyon")
        self.assertEqual(chloe.getMoney(), INITIAL_MONEY - 200 - 200)


if __name__ == '__main__':
    unittest.main()
