# Those are the classes to represent the game

import numpy as np
import random as rd

INITIAL_MONEY = 1500
NB_CASES = 40

class User:
    "A simple class to describe the lambda monopoly player"
    def __init__(self, name, money = INITIAL_MONEY, position = 0, goods = []):
        self.name = name
        self.money = money
        self.position = position
        self.goods = goods

class Box:
     "A simple class to describe each box"
     def __init__(self, name, players):
         self.name = name
         self.players = players    #which player is on this box
         self.type = type

class Street(Box):
    "A simple class to describe a good on the board, like LES GALERIES LAFAYETTE"
    def __init__(self, name, price, rent, players = [], owner = None, color = 0):
        super().__init__(name, players)
        self.owner = owner
        self.price = price
        self.rent = rent
        self.color = color

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
