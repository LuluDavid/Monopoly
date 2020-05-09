import unittest
from game.game import Game
from game.user import User
from game.globs import INITIAL_MONEY
from game.board import Board


class TestGame(unittest.TestCase):

    def test_player_has_all_colors_streets(self):
        players = {0: "Chloe", 1: "Lucien"}
        game = Game(players)
        chloe = game.players[0]
        lucien = game.players[1]
        chloe.buyAStreet(game.board.getBox(37))
        chloe.buyAStreet(game.board.getBox(39))
        lucien.buyAStreet(game.board.getBox(34))
        lucien.buyAStreet(game.board.getBox(32))
        lucien.buyAStreet(game.board.getBox(31))
        lucien.buyAStreet(game.board.getBox(29))
        self.assertTrue(game.playerHasAllColorStreets(chloe, 37))
        self.assertFalse(game.playerHasAllColorStreets(chloe, 34))
        self.assertTrue(game.playerHasAllColorStreets(lucien, 34))
        self.assertFalse(game.playerHasAllColorStreets(lucien, 29))

    def test_go_to_jail(self):
        players = {0: "Chloe", 1: "Lucien"}
        game = Game(players)
        chloe = game.players[0]
        chloe.setPosition(25)
        game.goToJail(chloe)
        self.assertEqual(chloe.getPosition(), 10)
        self.assertTrue(chloe.getInPrison())
        self.assertEqual(chloe.getPrisonTurn(), 0)

    def test_nb_of_stations(self):
        players = {0: "Chloe", 1: "Lucien", 2: "Gildas"}
        game = Game(players)
        chloe = game.players[0]
        lucien = game.players[1]
        gildas = game.players[2]
        chloe.buyAStation(game.board.getBox(5))
        chloe.buyAStation(game.board.getBox(15))
        lucien.buyAStation(game.board.getBox(25))
        self.assertEqual(game.nbOfStations(chloe), 2)
        self.assertEqual(game.nbOfStations(lucien), 1)
        self.assertEqual(game.nbOfStations(gildas), 0)

    def test_get_rent_street(self):
        players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
        game = Game(players)
        chloe = game.players[0]
        lucien = game.players[1]
        gildas = game.players[2]
        camille = game.players[3]
        gildas.setPosition(1)
        lucien.setPosition(6)
        camille.setPosition(8)
        chloe.buyAStreet(game.board.getBox(1))
        chloe.buyAStreet(game.board.getBox(3))
        chloe.buyAStreet(game.board.getBox(6))
        chloe.buyAStreet(game.board.getBox(8))
        game.board.getBox(6).setHomes(2)
        self.assertEqual(game.getRentStreet(gildas), 4)  # double rent
        self.assertEqual(game.getRentStreet(lucien), 90)  # rent with 2 houses
        self.assertEqual(game.getRentStreet(camille), 6)  # normal rent

    def test_get_rent_station(self):
        players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
        game = Game(players)
        chloe = game.players[0]
        lucien = game.players[1]
        gildas = game.players[2]
        camille = game.players[3]
        camille.setPosition(5)
        lucien.setPosition(15)
        chloe.buyAStation(game.board.getBox(5))
        gildas.buyAStation(game.board.getBox(15))
        gildas.buyAStation(game.board.getBox(25))
        gildas.buyAStation(game.board.getBox(35))
        self.assertEqual(game.getRentStation(camille), 50)
        self.assertEqual(game.getRentStation(lucien), 150)

    def test_make_cards(self):
        board = Board()
        self.assertEqual(board.cards[0].name, "Vous heritez 100 euros.")
        self.assertEqual(board.cards[0].card_type, "earn-money")
        self.assertEqual(board.cards[0].value, 100)
        self.assertEqual(len(board.cards), 33)
        self.assertEqual(board.cards[-1].value, 150)

    def test_card_earn_money(self):
        players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
        game = Game(players)
        chloe = User(players[0])
        chloe.setPosition(2)
        game.card_earn_money(chloe, 15)
        self.assertEqual(chloe.getMoney(), INITIAL_MONEY + 10)

    def test_card_loose_money(self):
        players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
        game = Game(players)
        chloe = User(players[0])
        chloe.setPosition(2)
        game.card_loose_money(chloe, 7)
        self.assertEqual(chloe.getMoney(), INITIAL_MONEY - 100)
        self.assertEqual(game.board.parc_money, 100)





if __name__ == '__main__':
    unittest.main()
