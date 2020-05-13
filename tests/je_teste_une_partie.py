from game.game import Game
from game.user import User
from game.globs import INITIAL_MONEY
from game.board import Board

if __name__ == '__main__':
    #players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game({0: "Chloe", 1: "Samy"})
    order = game.orderOfPlayers(game.players)
    while len(order) > 1:
        game.turn()
