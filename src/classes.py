# Those are the classes to represent the game

INITIAL_MONEY = 800
NB_CASES = 40


class User:
    """A simple class to describe the lambda monopoly player"""
    def __init__(self, name, money=INITIAL_MONEY, position=0, goods=None, inPrison = False, prisonTurn = None):
        self.name = name
        self.money = money
        self.position = position
        if goods is None:
            self.goods = []
        else:
            self.goods = goods
        self.inPrison = inPrison
        self.prisonTurn = prisonTurn
            
    def getUserName(self):
        return self.name
        
    def getMoney(self):
        return self.money
        
    def getPosition(self):
        return self.position
        
    def getGoods(self):
        return self.goods
        
    def getInPrison(self):
        return self.inPrison
        
    def getPrisonTurn(self):
        return self.prisonTurn
        
    def setPrisonTurn(self, value):
        self.prisonTurn = value
        
    def setPosition(self, position):
        self.position = position
        
    def setInPrison(self, boolean):
        self.inPrison = boolean
            
    def EarnMoney(self, earnMoney):
        self.money = self.money + earnMoney
        return self.money
        
    def LooseMoney(self, looseMoney):
        self.money = self.money - looseMoney
        return self.money
        
    def buyAStreet(self, street):
        position = self.getPosition()
        price = street.getPrice()[0]
        self.goods.append(street)
        street.owner = self 
        self.money = self.LooseMoney(price)
        
    def buyAStation(self, station):
        position = self.getPosition()
        price = station.getPrice()
        self.goods.append(station)
        station.owner = self 
        self.money = self.LooseMoney(price)


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


    def getBoxName(self):
        return self.name
    
    
    def getType(self):
        return self.box_type
        



class Street(Box):
    """"A simple class to describe a good on the board, like LES GALERIES LAFAYETTE"""
    def __init__(self, index,  box_type, name, price, rent,  color, players=None, owner=None, home=0):
        super().__init__(index,  box_type, name, players)
        self.owner = owner
        self.price = price
        self.rent = rent
        self.color = color
        self.home = home
        
    
    def getOwner(self):
        return self.owner
        
        
    def getPrice(self):
        return self.price
        
    def getColor(self):
        return self.color
        
    def getRent(self):
        return self.rent
        
    def getHome(self):
        return self.home
        
    def setHomes(self, number):
        self.home = self.home + number
        
    
        
        
class Station(Box):
    """"A simple class to describe a station on the board"""
    def __init__(self, index,  box_type, name, price, players=None, owner=None):
        super().__init__(index,  box_type, name, players)
        self.owner = owner
        self.price = price
    
    
    def getOwner(self):
        return self.owner
        
        
    def getPrice(self):
        return self.price
        

    def getRent(self):
        return self.rent
        

    
    


class Board:
    """A simple class to describe the board"""
    def __init__(self, boxes):
        self.boxes = boxes
        
    def getBox(self,position):
        return self.boxes[position]
        


class Game:
    """"A simple class to describe the game globally"""
    def __init__(self, players, board, turn, dice):
        self.players = players
        self.board = board
        self.turn = turn
        self.dice = dice
