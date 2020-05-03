# Those are the classes to represent the game

import numpy as np
import random as rd

INITIAL_MONEY = 1500
NB_CASES = 40

class User:
    "A simple class to describe the lambda monopoly player"
    def __init__(self, name, money, position, goods):
        self.name = name
        self.money = money
        self.position = position
        self.goods = goods

    def __init__(self, name):
        self.name = name
        self.money = INITIAL_MONEY
        self.position = 0
        self.goods = []


class Box:
     "A simple class to describe each box"
     def __init__(self, players, street):
         self.players = players    #which player is on this box
         self.type = type

class Street(Box)
    "A simple class to describe a good on the board, like LES GALERIES LAFAYETTE"
    def __init__(self, owner, price, rent, color):
        self.owner = owner
        self.price = price
        self.rent = rent

    def __init__(self, price, rent, color):
        self.owner = None
        self.price = price
        self.rent = rent

class Board:
    "A simple class to describe the board"
    def __init__(self, boxes):
        self.boxes = boxes

class Game:
    "A simple class to describe the game globally"
    def __init__(self, players, board, turn, dice):
        this.players = players
        this.board = board
        this.turn = turn
        this.dice = dice