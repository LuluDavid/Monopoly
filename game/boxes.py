from game.globs import FACTORS_PUBLIC_COMPANIES_RENT


class Box:

    def __init__(self, index, box_type, name, players=None):
        self.index = index
        self.box_type = box_type
        self.name = name
        self.players = players or []
        self.is_good = False
        self.nb_houses = 0


class Good(Box):

    def __init__(self, index, box_type, name, price, players=None, owner=None):
        super().__init__(index, box_type, name, players)
        self.is_good = True
        self.owner = owner
        self.price = price


class Street(Good):

    def __init__(self, index, box_type, name, price, rent, color, players=None, owner=None, nb_houses=0):
        super().__init__(index, box_type, name, price, players, owner)
        self.color = color
        self.nb_houses = nb_houses
        self.rent = rent
        self.price = price[0]
        self.price_house = price[1]

    def get_price_house(self):
        return self.price[1]

    def get_rent(self, player):
        if player == self.owner or self.owner is None:
            return 0
        elif self.nb_houses > 0:
            return self.rent[self.nb_houses]
        elif self.owner.has_full_color(self.color):
            return self.rent[0] * 2
        else:
            return self.rent[0]


class Station(Good):

    def __init__(self, index, box_type, name, price, players=None, owner=None):
        super().__init__(index, box_type, name, price, players, owner)

    def get_rent(self, player):
        if player == self.owner or self.owner is None:
            return 0
        else:
            return 50 * self.owner.get_number_of_stations()


class PublicCompany(Good):

    def __init__(self, index, box_type, name, price, players=None, owner=None):
        super().__init__(index, box_type, name, price, players, owner)

    def get_rent(self, player):
        if player == self.owner or self.owner is None:
            return 0
        else:
            return FACTORS_PUBLIC_COMPANIES_RENT[self.owner.get_number_of_companies()] * sum(player.dices)


class Tax(Box):

    def __init__(self, index, box_type, name, rent, players=None):
        super().__init__(index, box_type, name, players)
        self.rent = rent
