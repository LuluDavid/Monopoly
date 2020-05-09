from game.globs import INITIAL_MONEY

class User:
    """A simple class to describe the lambda monopoly player"""

    def __init__(self, name, position=0, goods=None, inPrison=False, prisonTurn=None, money=INITIAL_MONEY):
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
        price = street.getPrice()[0]
        self.goods.append(street)
        street.owner = self
        self.money = self.LooseMoney(price)

    def buyAStation(self, station):
        price = station.getPrice()
        self.goods.append(station)
        station.owner = self
        self.money = self.LooseMoney(price)