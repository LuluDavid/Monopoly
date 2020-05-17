import random
from deprecated import deprecated
from game.player import Player
from game.board import Board
import time


class Game:
    """"A simple class to describe the game globally"""
    def __init__(self, players):
        self.players = self.init_players(players)
        self.board = Board()
        self.players_order = self.order_players(self.players)
        self.current_player_turn = 0
        self.board.boxes[0].players = list(players.keys())

    @staticmethod
    def init_players(players):
        """Define the players at the beginning of the game"""
        if len(players) >= 0:  # 2:
            return {i: Player(players[i], i) for i in players}
        else:
            raise Exception("Not enough players to start the game")

    @staticmethod
    def order_players(players):
        """Choosing randomly what is the order of players"""
        order = list(players.keys())
        #random.shuffle(order)
        for i in range(len(order)):
            pass #print("Le joueur " + str(i+1) + " est " + self.players[order[i]].name)
        return order

    # Game

    @staticmethod
    @deprecated  # Done
    def launch_dices():
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        return [dice1, dice2]

    @deprecated  # Done
    def actualizePosition(self, player):
        dices = self.launch_dices()
        self.actualizePositionAux(player, dices)
        self.board.boxes[player.getPosition()].players.append(player.id)
        return player.getPosition()

    @deprecated  # Done
    def actualizePositionAux(self, player, dices):
        """
        Find the new position of the player after rolling dices
        Check that the player is not in jail, otherwise he can not move
        """

        oldPosition = player.getPosition()
        prison = player.getInPrison()
        totalDices = dices[0] + dices[1]
        prisonTurn = player.getPrisonTurn()
        player.dices = totalDices
        if (prison == False):
            self.board.boxes[player.getPosition()].players.remove(player.id)
            print("" + player.name + ", tu as fait " + str(totalDices))
            if (oldPosition + totalDices < 40):
                player.setPosition(oldPosition + totalDices)
            else:
                player.setPosition(oldPosition + totalDices - 40)
                player.earn_money(200)
                print("Vous passez la case Depart, vous gagnez 200 euros.")
        else:
            self.isInJail(player)

    @deprecated  # Done
    def playerHasAllColorStreets(self, player, streetPosition):
        """
        Check if a player has all the streets of the same color that the box on 'positionOfStreet'
        Example :chloe = User("Chloe"), position=39,
        return True if chloe has box 39 (Rue de la paix) and 37 (champs elysees) which are dark-blue
        """
        streetColor = self.board.get_box(streetPosition).getColor()
        if streetColor == "pink" or streetColor == "dark-blue":
            count = 0
            n = len(player.getGoods())
            for i in range(n):
                case_type = player.getGoods()[i].getType()
                if case_type == "street":
                    if player.getGoods()[i].getColor() == streetColor:
                        count = count + 1
            if count == 2:
                return True
            else:
                return False
        else:
            count = 0
            n = len(player.getGoods())
            for i in range(n):
                case_type = player.getGoods()[i].getType()
                if (case_type == "street"):
                    if (player.getGoods()[i].getColor() == streetColor):
                        count = count + 1
            if count == 3:
                return True
            else:
                return False

    @deprecated
    def putHomes(self, player):  # TODO : verify that owner has enough money to pay for houses

        """
        function to allow or not the player to add houses on the box (max houses is 5)
        check 1 : does the player has all the properties of the same color ?
        check 2 : can we still add more houses ? (if already 5 houses, we can't)
        """

        position = player.getPosition()
        numberOfHomes = self.board.get_box(position).getHome()
        priceOfHome = self.board.get_box(position).getPrice()[1]
        houseAvailable = 5 - numberOfHomes
        if (self.playerHasAllColorStreets(player, player.position) == True):
            if (houseAvailable != 0):
                choice = input("Vous pouvez placer " + str(
                    houseAvailable) + " maison(s) sur cette propriete, une maison coute " + str(
                    priceOfHome) + "euros. Souhaitez-vous construire ?")
                if (choice.lower() == "oui".lower()):
                    nbOfHouses = input("Combien de maison souhaitez-vous construire ?")
                    while (int(nbOfHouses) > houseAvailable):
                        nbOfHouses = input("Vous pouvez construire maximum " + str(
                            houseAvailable) + " maisons, combien souhaitez-vous en construire ?")
                    self.board.get_box(position).setHomes(int(nbOfHouses) + self.board.get_box(position).getHome())
                    player.loose_money(priceOfHome * int(nbOfHouses))
                    input("Vous avez construit" + str(nbOfHouses) + " maisons. Il vous reste " + str(
                        player.money) + "euros")
                else:
                    input("Vous avez choisi de ne pas construire de maison")

    ##Jail

    @deprecated
    def goToJail(self, player):

        """The player went on the box 'go to jail', he is sent to jail which is in position 10"""

        print("Vous allez directement en prison sans passer par la case depart")
        self.board.boxes[player.getPosition()].players.remove(player.identity)
        player.setPosition(10)
        self.board.boxes[10].players.append(player.identity)
        player.setInPrison(True)
        player.setPrisonTurn(0)

    @deprecated
    def jail_chooseToPay(self, player):

        """The player who is in jail chose to get out by paying 50euros"""

        print("Vous avez decide de payer 50euros, vous n'etes plus en prison")
        player.loose_money(50)
        player.setInPrison(False)
        player.setPrisonTurn(None)
        print("il vous reste " + str(player.getMoney()) + " euros")
        self.actualizePosition(player)

    @deprecated
    def jail_chooseDouble(self, player, dices):

        """The player in jail chose not to pay or had not enough money to pay, so he has to make a double to get        out"""

        # dices=launchDices()
        if (dices[0] == dices[1]):
            input("Bravo, vous avez fait un double " + str(
                dices[0]) + ". Vous etes sortis de prison et avancez de " + str(2 * dices[0]) + "")
            self.board.boxes[player.getPosition()].players.remove(player.identity)
            player.setPosition(10 + 2 * dices[0])
            self.board.boxes[player.getPosition()].players.append(player.identity)
            player.setInPrison(False)
            player.setPrisonTurn(None)
        else:
            input("Vous avez fait " + str(dices[0]) + " et " + str(
                dices[1]) + ". Ce n'est pas un double vous ne sortez pas de prison")
            player.setPrisonTurn(player.getPrisonTurn() + 1)  # one turn more in jail
            self.board.boxes[player.getPosition()].players.remove(player.identity)

    @deprecated
    def isInJail(self, player):
        dices = self.launch_dices()
        self.isInJailAux(player, dices)

    @deprecated
    def isInJailAux(self, player, dices):

        """
        The player is in jail,
        case 1 : he is in prison for less than 3 turns so he has to choose between paying or make a double
        case 2 : it's been 3 turns in prison so he gets out of jail and returns to normal game
        """

        turnInPrison = player.getPrisonTurn()  # how many turns since player is in jail ?
        if (turnInPrison < 3):
            if (player.getMoney() >= 50):
                choice = input(
                    "" + player.getUserName() + ", vous avez 2 options, la premiere est de payer 50euros pour sortir de prison. La deuxieme est d'essayer de faire des doubles, vous sortirez automatiquement au bout de 3 tours. Rq : vous pouvez payer 50 euros a chaque tour. Choisissez 1 ou 2")
                while (choice != "1" and choice != "2"):
                    choice = input(
                        "Vous devez choisir 1 ou 2. 1=payer 50euros, 2=attendre 3 tours en tentant de faire un double")
                if (choice == "1"):
                    self.jail_chooseToPay(player)
                else:
                    print("Vous avez choisi d'essayer de faire un double")
                    self.jail_chooseDouble(player, dices)
            else:
                input(
                    "" + player.getUserName() + "Vous n'avez pas assez d'argent pour sortir en payant 50euros, vous pouvez tenter de sortir en faisant un double")
                self.jail_chooseDouble(player, dices)
        else:
            print("Vous avez passe 3 tours en prison, vous sortez de prison")
            player.setInPrison(False)
            player.setPrisonTurn(None)
            self.actualizePosition(player)


    ## Cards

    @deprecated
    def card_earn_money(self, player, number):
        player.earn_money(self.board.cards[number].value)
        print("Vous recevez "+str(self.board.cards[number].value)+" euros.")

    @deprecated
    def card_loose_money(self, player, number):
        player.loose_money(self.board.cards[number].value)
        self.board.park_money = self.board.park_money + self.board.cards[number].value
        print("Vous perdez " + str(self.board.cards[number].value) + " euros.")

    @deprecated
    def card_moove_backwards(self, player, number):
        self.board.boxes[player.getPosition()].players.remove(player.identity)
        player.setPosition(self.board.cards[number].value)
        self.board.boxes[player.getPosition()].players.append(player.identity)
        self.onAStreetOrStation(player)
        print("Vous retournez a "+self.board.cards[number].name)

    @deprecated
    def card_moove_forward(self, player, number):
        value = self.board.cards[number].value
        pos = player.getPosition()
        self.board.boxes[player.getPosition()].players.remove(player.identity)
        if (pos<value):
            player.setPosition(value)
            self.board.boxes[player.getPosition()].players.append(player.identity)
            self.onAStreetOrStation(player)
        elif (value == 0):
            player.setPosition(value)
            self.board.boxes[player.getPosition()].players.append(player.identity)
            player.earn_money(200)
        else :
            player.setPosition(value)
            self.board.boxes[player.getPosition()].players.append(player.identity)
            self.onAStreetOrStation(player)
            player.earn_money(200)

    @deprecated
    def card_birthday(self, player, number):
        value = self.board.cards[number].value
        identity = player.identity
        n = len(self.players_order)
        player.earn_money(value * (n - 1))
        L = list(self.players.keys())
        L.remove(identity)
        for i in L:
            self.players[i].loose_money(value)

    @deprecated
    def card_community_or_chance(self, player, number):
        value = self.board.cards[number].value
        choice = input("Preferez vous payer "+str(value)+" euros : choix 1. Ou bien tirer une carte chance : choix 2")
        if choice == "1":
            self.card_loose_money(player, number)
        else:
            number = random.randint(17, 32)
            self.on_card_number(player, number)

    @deprecated
    def card_backwards(self, player, number):
        pos = player.getPosition()
        self.board.boxes[player.getPosition()].players.remove(player.identity)
        value = self.board.cards[number].value
        player.setPosition(pos - value)
        if player.getPosition() < 0:
            pos = player.getPosition()
            player.setPosition(pos + 40)
        self.board.boxes[player.getPosition()].players.append(player.identity)
        case = self.board.get_box(player.getPosition())
        if case.getType() == "station" or case.getType() == "street":
            self.onAStreetOrStation(player)
        elif case.getType() == "to-jail":
            self.goToJail(player)
        elif case.getType() == "chance" or case.getType() == "community-fund":
            self.on_card(player)
        elif case.getType() == "tax":
            self.on_tax(player)

    @deprecated
    def card_taxes(self, player, number):
        player_goods = player.getGoods()
        rent = self.board.cards[number].value
        n=len(player_goods)
        homes = 0
        hotels = 0
        for i in range(n):
            if player_goods[i].box_type == "street":
                case_home = player_goods[i].home
                if case_home < 5:
                    homes = homes + case_home
                elif case_home == 5:
                    hotels = hotels + 1
        money = homes*rent[0] + hotels*rent[1]
        player.loose_money(money)
        self.board.park_money = self.board.park_money + money

    @deprecated
    def on_card(self, player):
        card = self.board.cards
        if self.board.get_box(player.getPosition()).getType() == "community-fund":
            number = random.randint(0, 16)
        else:
            number = random.randint(17, 32)
        print("Vous tirez la carte : " + card[number].name)
        self.on_card_number(player, number)

    @deprecated
    def on_card_number(self, player, number):
        card = self.board.cards
        if card[number].card_type == "earn-money":
            self.card_earn_money(player, number)
        elif card[number].card_type == "loose-money":
            self.card_loose_money(player, number)
        elif card[number].card_type == "moove-backwards":
            self.card_moove_backwards(player, number)
        elif card[number].card_type == "go-to-jail":    #TODO tester cette partie la ?
            self.goToJail(player)
        elif card[number].card_type == "moove-forward":
            self.card_moove_forward(player, number)
        elif card[number].card_type == "birthday":
            self.card_birthday(player, number)
        elif card[number].card_type == "loose-money-or-chance":
            self.card_community_or_chance(player, number)
        elif card[number].card_type == "backwards":
            self.card_backwards(player, number)
        elif card[number].card_type == "taxes":
            self.card_taxes(player, number)
        else:
            print("type pas encore traite")

    @deprecated
    def on_tax(self, player):
        pos = player.getPosition()
        rent = self.board.get_box(pos).rent
        player.loose_money(rent)
        self.board.park_money = self.board.park_money + rent
        print("Vous perdez "+str(rent)+" euros.")

    # Others

    @deprecated  # Done
    def nbOfStations(self, owner):
        """
        How many stations does a player have ?
        """
        goods = owner.getGoods()
        nb = 0
        n = len(goods)
        for i in range(n):
            if (goods[i].getType() == "station"):
                nb = nb + 1
        return nb

    @deprecated  # Done
    def get_rent_public_service(self, player):
        pos = player.getPosition()
        owner = self.board.get_box(pos).getOwner()
        owner_goods = owner.getGoods()
        n = len(owner_goods)
        count = 0
        factor = 4
        for i in range(n):
            if owner_goods[i].box_type == "public-service":
                count = count + 1
        if count == 2:
            factor = 10
        dices = player.dices
        rent = factor*dices
        return rent

    @deprecated  # Done
    def getRentStreet(self, player):
        """
        The rent is different if their is homes in it or if the owner has all streets of the same color
        """
        pos = player.getPosition()
        numberOfHomes = self.board.get_box(pos).getHome()
        if (numberOfHomes != 0):
            rent = self.board.get_box(pos).getRent()[numberOfHomes]
            return rent
        else:
            rent = self.board.get_box(pos).getRent()[0]  # recup value of rent without houses to check if owner has
            streetColor = self.board.get_box(pos).getColor()  # all properties with the same color
            owner = self.board.get_box(pos).getOwner()
            hasAllColors = self.playerHasAllColorStreets(owner, pos)
            if (hasAllColors == True):
                rent = rent * 2
                return rent
            else:
                return rent

    @deprecated  # Done
    def getRentStation(self, player):
        """
        What is the rent to pay for the player on the station (position of station is player.position)
        """
        pos = player.getPosition()
        case = self.board.get_box(pos)
        owner = case.getOwner()
        nbStations = self.nbOfStations(owner)
        rent = 50 * nbStations
        return rent

    @deprecated
    def onAStreetOrStation(self, player):

        """
        The player is on a street, there is different cases

        case 1 : the street has no owner yet and the player has enough money to buy it, he has to choose if yes or
        not he wants it

        case 2 : the street has no owner yet but the player does not have enough money to buy it

        case 3 : the street belongs to the player, he can either do nothing or buy homes if possible

        case 4 : the street belongs to someone, we use 'getRentStreet' to know what is the rent to pay

        #check : if type = street price is a list, if type = station it is not. We factorize

        """

        pos = player.getPosition()
        case = self.board.get_box(pos)
        case_type = case.getType()
        price = case.getPrice()
        price = price[0] if case_type == "street" else price  # check
        if case.owner == None and player.money >= price:
            choice = input("Cette propriete est libre, son prix est de " + str(
                price) + " euros. Voulez-vous l'acheter ? (Il vous reste " + str(player.money) + " euros)")
            if choice.lower() == "oui".lower():
                player.buyAStreet(case) if case_type == "street" else player.buyAStation(case)  # check
                print("Vous venez d'acheter la propriete " + str(case.getBoxName()) + ". Il vous reste " + str(
                    player.getMoney()) + " euros.")
                # if case_type == "street":
                #     player.buyAStreet(case)
                if case_type == "street":
                    self.putHomes(player)
            else:
                print("Vous avez decide de ne pas acheter, vous avez toujours " + str(player.money) + " euros.")
        else:
            if case.getOwner() == None and player.getMoney() < price:
                print(
                    "Cette propriete est libre, malheureusement vous n'avez pas assez d'argent pour l'acheter.\ Il vous reste " + str(
                        player.money) + " euros et le prix est de " + str(price) + " euros.")
            else:  # the street belongs to someone
                ownerName = case.getOwner().getUserName()
                if case.getOwner() == player:
                    print("Cette propriete vous appartient")
                    if (case_type == "street"):
                        self.putHomes(player)
                else:
                    if case_type == "street":
                        rent = self.getRentStreet(player)
                    elif case_type == "station":
                        rent = self.getRentStation(player)
                    elif case_type == "public-service":
                        rent = self.get_rent_public_service(player)
                    print("Cette propriete appartient a " + ownerName + ", vous lui devez " + str(rent) + " euros.")
                    player.loose_money(rent)
                    print("Il vous reste " + str(player.money) + " euros.")
                    case.owner.earn_money(rent)
                    print("" + ownerName + " gagne " + str(rent) + " euros, il lui reste " + str(
                        case.owner.money) + " euros.")

    @deprecated
    def turn(self):
        """
        Simulates one turn :
        1-actualize position of the player
        2- different actions if on street station or jail
        3- if the player has not mony anymore --> he looses
        """
        numberOfPlayers = len(self.players_order)
        for i in range(numberOfPlayers):
            player = self.players[self.players_order[i]]
            self.actualizePosition(player)
            pos = player.getPosition()
            playerStreetPosition = self.board.get_box(pos).getBoxName()
            print("Tu es sur la case : " + playerStreetPosition)
            case = self.board.get_box(pos)
            if case.getType() == "station" or case.getType() == "street":
                self.onAStreetOrStation(player)
            elif case.getType() == "to-jail":
                self.goToJail(player)
            elif case.getType() == "chance" or case.getType() == "community-fund":
                self.on_card(player)
            elif case.getType() == "start":
                pass
            elif case.getType() == "tax":
                self.on_tax(player)
            elif case.getType() == "park":
                self.on_park(player)
            elif case.getType() == "jail":
                print("Vous etes en simple visite de la prison")
            elif case.getType() == "public-service":
                self.onAStreetOrStation(player)
            else:
                print("ce type de case n est pas encore traite")
            loosers = []
            if player.getMoney() < 0:
                print("" + player.getUserName() + ", tu as perdu! Tu n'as plus d'argent.")
                loosers.append(player)
            if len(loosers) > 0:
                for looser in loosers:
                    self.players_order.remove(looser)
        return self.players_order

    # JOINING WITH FRONT --------------------------------------------

    def game_to_json(self, action="play_turn", box_name=None, box_price=None):
        response = {
            "state_array": {
                i: [self.board.boxes[i].players, self.board.boxes[i].nb_houses] for i in list(self.board.boxes.keys())
            },
            "player_turn": self.players_order[self.current_player_turn],
            "action": action,
            "box_name": box_name,
            "box_price": box_price
        }
        return response

    def next_player(self):
        self.current_player_turn += 1
        if self.current_player_turn >= len(self.players_order):
            self.current_player_turn = 0

    def do_nothing(self):
        time.sleep(0.5)  # otherwise modal doesn't show
        self.next_player()
        return self.game_to_json()

    def landing_on_good(self, player, pos):
        if player.can_buy_good(pos):
            return self.game_to_json(action="ask_buy", box_name=pos.name, box_price=pos.price)
        elif pos.owner == player:
            pass  # TODO : ask_buy_house if possible
        elif pos.owner is not None:
            player.pay_player(pos.get_rent())
            time.sleep(0.5)
            return self.game_to_json()  # TODO: Message "X payed Y"
        else:
            return self.do_nothing()

    # TODO: Manage jail turn
    def jail_turn(self, player):
        return self.do_nothing()

    # TODO: card Class to manage everything
    def landing_on_card(self, player):
        return self.do_nothing()

    def landing_on_park(self, player):
        player.earn_money(self.board.park_money)
        self.board.park_money = 0
        time.sleep(0.5)
        return self.game_to_json()  # TODO: Message "X earned the park money"

    def play_turn(self, data):
        action = data["action"]
        player = self.players[self.players_order[self.current_player_turn]]

        if action == "play_turn":
            if player.in_jail:
                self.jail_turn(player)
            else:
                player.update_position(player.throw_dices(), self.board)
                new_pos = self.board.boxes[player.position]
                if new_pos.is_good:
                    return self.landing_on_good(player, new_pos)
                elif new_pos.box_type in ["community-fund", "chance"]:
                    return self.landing_on_card(player)
                elif new_pos.box_type == "park":
                    return self.landing_on_park(player)
                else:
                    return self.do_nothing()

        elif action == "buy":
            if data["action_value"]:
                player.buy_good(self.board.boxes[player.position])
            self.next_player()
            return self.game_to_json()
