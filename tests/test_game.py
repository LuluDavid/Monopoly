import unittest
from game.game import Game


class TestGame(unittest.TestCase):

    def test_init_player(self):
        game = Game({2532: "Gildas", 7429: "Lucien", 1734: "Chloe"})
        self.assertEqual({2532, 7429, 1734}, set(game.players_order))

    def test_next_player(self):
        game = Game({2532: "Gildas", 7429: "Lucien", 1734: "Chloe"})
        game.players_order = [7429, 1734, 2532]
        self.assertEqual(7429, game.players_order[game.current_player_turn])
        game.next_player()
        game.next_player()
        self.assertEqual(1734, game.players_order[game.current_player_turn])
        self.assertEqual(2532, game.players_order[game.current_player_turn])
        game.next_player()
        self.assertEqual(7429, game.players_order[game.current_player_turn])


if __name__ == '__main__':
    unittest.main()

