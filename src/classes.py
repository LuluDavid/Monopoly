# Those are the classes to represent the game

INITIAL_MONEY = 800
NB_CASES = 40


class User:
    """A simple class to describe the lambda monopoly player"""
    def __init__(self, name, money=INITIAL_MONEY, position=0, goods=None):
        self.name = name
        self.money = money
        self.position = position
        if goods is None:
            self.goods = []
        else:
            self.goods = goods


class Box:
    """A simple class to describe each box"""

    def __init__(self, index, box_type, name, players=None):
        self.index = index
        self.box_type = box_type
        self.name = name
        if players is None:
            self.players = []
        else:
            self.players = players 


class Street(Box):
    """"A simple class to describe a good on the board, like LES GALERIES LAFAYETTE"""
    def __init__(self, index,  box_type, name, price, rent,  color, players=None, owner=None, home=0):
        super().__init__(index,  box_type, name, players)
        self.owner = owner
        self.price = price
        self.rent = rent
        self.color = color
        self.home = home


class Board:
    """A simple class to describe the board"""
    def __init__(self, boxes):
        self.boxes = boxes


class Game:
    """"A simple class to describe the game globally"""
    def __init__(self, players, board, turn, dice):
        self.players = players
        self.board = board
        self.turn = turn
        self.dice = dice
