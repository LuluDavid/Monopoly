# Those are the classes to represent the game

INITIAL_MONEY = 1500
NB_CASES = 40


class User:
    """A simple class to describe the lambda monopoly player"""
    def __init__(self, name, money=INITIAL_MONEY, position=0, goods=[]):
        self.name = name
        self.money = money
        self.position = position
        self.goods = goods


class Box:
    """A simple class to describe each box"""

    def __init__(self, index, box_type, name, players=[]):
        self.index = index
        self.box_type = box_type
        self.name = name
        self.players = players  # which players are on this box


class Street(Box):
    """"A simple class to describe a good on the board, like LES GALERIES LAFAYETTE"""
    def __init__(self, index,  box_type, name, price, rent, players=[], owner=None, color=0):
        super().__init__(index,  box_type, name, players)
        self.owner = owner
        self.price = price
        self.rent = rent
        self.color = color


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
