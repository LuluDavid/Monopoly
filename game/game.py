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
        return order

    ##Jail

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
        if dices[0] == dices[1]:
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

    def game_to_json(self, action="play_turn",
                     box_name=None,
                     box_price=None,
                     house_price=None,
                     buyable_houses=None,
                     card_type=None,
                     card_message=None):
        response = {
            "state_array": {
                i: [self.board.boxes[i].players, self.board.boxes[i].nb_houses] for i in list(self.board.boxes.keys())
            },
            "player_turn": self.players_order[self.current_player_turn],
            "action": action,
            "box_name": box_name,
            "box_price": box_price,
            "house_price": house_price,
            "buyable_houses": buyable_houses,
            "card_type": card_type,
            "card_message": card_message
        }
        return response

    def next_player(self):
        time.sleep(0.5)  # otherwise modal doesn't show
        self.current_player_turn += 1
        if self.current_player_turn >= len(self.players_order):
            self.current_player_turn = 0

    # TODO: Manage jail turn
    def jail_turn(self, player):
        return self.do_nothing()

    def landing_on_position(self, player, pos):
        if pos.is_good:
            return self.landing_on_good(player, pos)
        elif pos.box_type in ["community-fund", "chance"]:
            return self.landing_on_card(pos)
        elif pos.box_type == "tax":
            return self.landing_on_tax(player, pos)
        elif pos.box_type == "park":
            return self.landing_on_park(player)
        else:
            return self.do_nothing()

    def do_nothing(self):
        self.next_player()
        return self.game_to_json()

    def landing_on_good(self, player, pos):
        if player.can_buy_good(pos):
            return self.game_to_json(action="ask_buy", box_name=pos.name, box_price=pos.price)

        elif pos.owner == player:
            nb_houses_buyable = player.can_buy_houses(pos)
            if nb_houses_buyable > 0:
                return self.game_to_json(
                    action="ask_buy_houses",
                    box_name=pos.name,
                    house_price=pos.price,
                    buyable_houses=nb_houses_buyable)
            else:
                return self.do_nothing()

        elif pos.owner is not None:
            player.pay_player(pos.get_rent(player))
            self.next_player()
            return self.game_to_json()  # TODO: Message "X payed Y"

        else:
            return self.do_nothing()

    def landing_on_card(self, pos):
        if pos.box_type == "community-fund":
            card_id = random.randint(0, 16)
        else:
            card_id = random.randint(17, 32)
        card = self.board.cards[card_id]
        self.board.last_open_card = card
        return self.game_to_json(action="draw_card", card_type=pos.box_type, card_message=card.name)

    def landing_on_tax(self, player, pos):
        player.loose_money(pos.rent)
        self.board.park_money += pos.rent
        self.next_player()
        return self.game_to_json()

    def landing_on_park(self, player):
        player.earn_money(self.board.park_money)
        self.board.park_money = 0
        self.next_player()
        return self.game_to_json()  # TODO: Message "X earned the park money"

    def play_turn(self, data):
        action = data["action"]
        player = self.players[self.players_order[self.current_player_turn]]

        if action == "play_turn":
            if player.in_jail:
                return self.jail_turn(player)
            else:
                # player.update_position([1, 1], self.board)
                player.update_position(player.throw_dices(), self.board)
                return self.landing_on_position(player, self.board.boxes[player.position])

        elif action == "buy":
            if data["action_value"]:
                player.buy_good(self.board.boxes[player.position])
            self.next_player()
            return self.game_to_json()

        elif action == "buy_houses":
            nb_houses = int(data["action_value"])
            if nb_houses > 0:
                player.buy_houses(self.board.boxes[player.position], nb_houses)
            self.next_player()
            return self.game_to_json()

        elif action == "execute_card":
            init_pos = player.position
            self.board.last_open_card.execute(player, self.players, self.board)
            new_pos = player.position
            if init_pos != new_pos:
                return self.landing_on_position(player, self.board.boxes[new_pos])
            else:
                self.next_player()
                return self.game_to_json()
