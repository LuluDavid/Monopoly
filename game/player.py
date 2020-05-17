import random
from deprecated import deprecated
from game.globs import INITIAL_MONEY, NUMBER_HOUSES_COLOR


class Player:
    """A simple class to describe the lambda monopoly player"""

    def __init__(self, name, player_id, position=0, goods=None, in_jail=False, jail_turn=None, money=INITIAL_MONEY, dices=None):
        self.name = name
        self.id = player_id
        self.money = money
        self.position = position
        self.goods = goods or []
        self.in_jail = in_jail
        self.jail_turn = jail_turn
        self.dices = dices

    @deprecated
    def getUserName(self):
        return self.name

    @deprecated
    def getMoney(self):
        return self.money

    @deprecated
    def getPosition(self):
        return self.position

    @deprecated
    def getGoods(self):
        return self.goods

    @deprecated
    def getInPrison(self):
        return self.in_jail

    @deprecated
    def getPrisonTurn(self):
        return self.jail_turn

    @deprecated
    def setPrisonTurn(self, value):
        self.jail_turn = value

    @deprecated
    def setPosition(self, position):
        self.position = position

    @deprecated
    def setInPrison(self, boolean):
        self.in_jail = boolean

    @deprecated
    def buyAStreet(self, street):
        price = street.price[0]
        self.goods.append(street)
        street.owner = self
        self.money = self.loose_money(price)

    @deprecated
    def buyAStation(self, station):
        price = station.getPrice()
        self.goods.append(station)
        station.owner = self
        self.money = self.loose_money(price)

    # ----------

    def throw_dices(self):
        self.dices = [random.randint(1, 6), random.randint(1, 6)]
        return self.dices

    def update_position(self, dices, board):
        if not self.in_jail:
            board.boxes[self.position].players.remove(self.id)
            self.position += sum(dices)
            if self.position > 39:
                self.money += 200
                self.position -= 40
            board.boxes[self.position].players.append(self.id)
            return self.position
        else:
            raise Exception("Player can't move because is in jail")

    def earn_money(self, amount):
        self.money = self.money + amount
        return self.money

    # TODO: Test if not enough money and make the player loose
    def loose_money(self, amount):
        self.money = self.money - amount
        return self.money

    def go_to_jail(self, board):
        board.boxes[self.position].players.remove(self.id)
        self.position = 10
        self.jail_turn = 0
        self.in_jail = True
        board.boxes[self.position].players.append(self.id)

    def leave_jail(self):
        self.in_jail = False

    def can_buy_good(self, good):
        return good.is_good and good.owner is None and self.money >= good.price

    def buy_good(self, good):
        if self.can_buy_good(good):
            self.goods.append(good)
            good.owner = self
            self.loose_money(good.price)
        else:
            if not good.is_good:
                raise Exception("Can't buy the good : not a good")
            elif good.owner is not None:
                raise Exception("Can't buy the good : owner is not None")
            elif self.money < good.price:
                raise Exception("Can't buy the good : not enough money")
            else:
                raise Exception("Can't buy the good")

    def has_full_color(self, color):
        count = sum([good.box_type == "street" and good.color == color for good in self.goods])
        return count == NUMBER_HOUSES_COLOR[color]

    def get_number_of_stations(self):
        return sum([good.box_type == "station" for good in self.goods])

    def get_number_of_companies(self):
        return sum([good.box_type == "public-company" for good in self.goods])

    def pay_player(self, player, amount):
        self.loose_money(amount)
        player.earn_money(amount)
