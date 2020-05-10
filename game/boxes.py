
class Box:

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



class Public_services(Box):
    def __init__(self, index, box_type, name, price, owner=None, players=None):
        super().__init__(index, box_type, name, players)
        self.price = price
        self.owner = owner

    def getOwner(self):
        return self.owner

    def getPrice(self):
        return self.price


class Tax(Box):

    def __init__(self, index, box_type, name, rent, players=None):
        super().__init__(index, box_type, name, players)
        self.rent = rent


class Street(Box):

    def __init__(self, index, box_type, name, price, rent, color, players=None, owner=None, home=0):
        super().__init__(index, box_type, name, players)
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
        self.home = number


class Station(Box):

    def __init__(self, index, box_type, name, price, players=None, owner=None):
        super().__init__(index, box_type, name, players)
        self.owner = owner
        self.price = price

    def getOwner(self):
        return self.owner

    def getPrice(self):
        return self.price
