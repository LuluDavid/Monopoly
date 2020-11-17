import unittest

from game.boxes import Street, Station, PublicCompany
from game.player import Player
from game.board import Board


class BoxTest(unittest.TestCase):

    def test_get_price(self):
        street = Street(1, "street", "Rue de Meudon", price=[60, 50], rent=[2, 10, 30, 90, 160, 250], color="yellow")
        station = Station(2, "station", "Gare de Dunkerque", price=200)
        company = PublicCompany(3, "public-service", "Centrale de Gravelines", price=40)
        self.assertEqual(60, street.price)
        self.assertEqual(200, station.price)
        self.assertEqual(40, company.price)

    def test_get_rent(self):
        chloe = Player("Chloe", 0)
        lucien = Player("Lucien", 1)
        gildas = Player("Gildas", 1)
        board = Board()
        chloe.buy_good(board.boxes[1])
        board.boxes[1].nb_houses = 2
        chloe.buy_good(board.boxes[3])
        board.boxes[3].nb_houses = 3
        chloe.buy_good(board.boxes[5])
        chloe.buy_good(board.boxes[6])
        chloe.buy_good(board.boxes[12])
        gildas.buy_good(board.boxes[15])
        gildas.buy_good(board.boxes[25])
        lucien.dices = [3, 4]
        self.assertEqual(0, board.boxes[1].get_rent(chloe))
        self.assertEqual(0, board.boxes[8].get_rent(chloe))
        self.assertEqual(0, board.boxes[16].get_rent(chloe))
        self.assertEqual(30, board.boxes[1].get_rent(lucien))
        self.assertEqual(180, board.boxes[3].get_rent(lucien))
        self.assertEqual(50, board.boxes[5].get_rent(lucien))
        self.assertEqual((3+4)*4, board.boxes[12].get_rent(lucien))
        self.assertEqual(0, board.boxes[13].get_rent(lucien))
        self.assertEqual(100, board.boxes[15].get_rent(lucien))


if __name__ == '__main__':
    unittest.main()
