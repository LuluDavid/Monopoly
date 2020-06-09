import random
from game.player import Player
from game.board import Board
from game.globs import JAIL_FEE
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
        return order

    def game_to_json(self, action="play_turn",
                     box_name=None,
                     box_price=None,
                     house_price=None,
                     buyable_houses=None,
                     card_type=None,
                     card_message=None,
                     changed_players=None,
                     bought=None
                     ):
        player_turn_id = self.players_order[self.current_player_turn]
        response = {
            "state_array": {
                i: [self.board.boxes[i].players, self.board.boxes[i].nb_houses] for i in list(self.board.boxes.keys())
            },
            "player_turn": player_turn_id,
            "player_money": self.players[player_turn_id].money,
            "is_in_jail": self.players[player_turn_id].in_jail,
            "jail_turn": self.players[player_turn_id].jail_turn,
            "card_leave_jail": self.players[player_turn_id].card_leave_jail,
            "action": action,
            "box_name": box_name,
            "box_price": box_price,
            "house_price": house_price,
            "buyable_houses": buyable_houses,
            "card_type": card_type,
            "card_message": card_message,
            "changed_players": changed_players,
            "bought": bought
        }
        return response

    def next_player(self):
        time.sleep(0.5)  # otherwise modal doesn't show
        self.current_player_turn += 1
        if self.current_player_turn >= len(self.players_order):
            self.current_player_turn = 0

    def jail_turn(self, player, choice):
        if choice == "double":
            dices = player.throw_dices()
            if dices[0] == dices[1]:
                player.leave_jail()
                player.update_position(dices, self.board)
                return self.landing_on_position(player, self.board.boxes[player.position])
            else:
                player.loose_money(JAIL_FEE)
                player.jail_turn += 1
                self.next_player()
                return self.game_to_json()
        elif choice == "pay" and player.money > JAIL_FEE:
            player.leave_jail()
            player.update_position(player.throw_dices(), self.board)
            return self.landing_on_position(player, self.board.boxes[player.position])
        elif choice == "card" and player.card_leave_jail > 0:
            player.card_leave_jail -= 1
            player.leave_jail()
            player.update_position(player.throw_dices(), self.board)
            return self.landing_on_position(player, self.board.boxes[player.position])
        else:
            raise Exception("Failed to execute the following choice for jail turn : ", choice)

    def landing_on_position(self, player, pos, new_turn=False, changed_players=None):
        if changed_players is None:
            changed_players = {}
        if pos.is_good:
            return self.landing_on_good(player, pos, new_turn, changed_players=changed_players)
        elif pos.box_type in ["community-fund", "chance"]:
            return self.landing_on_card(pos, player, changed_players=changed_players)
        elif pos.box_type == "tax":
            return self.landing_on_tax(player, pos, changed_players=changed_players)
        elif pos.box_type == "park":
            return self.landing_on_park(player, changed_players=changed_players)
        else:
            return self.do_nothing(player, new_turn, changed_players=changed_players)

    def do_nothing(self, player=None, new_turn=False, changed_players=None):
        if changed_players is None:
            changed_players = {}
        self.next_player()
        if player is not None and new_turn:
            changed_players[player.id] = {"money": player.money}
        return self.game_to_json(changed_players=changed_players)

    def landing_on_good(self, player, pos, new_turn=False, changed_players=None):
        if changed_players is None:
            changed_players = {}
        if new_turn:
            changed_players[player.id] = {"money": player.money}
        if player.can_buy_good(pos):
            return self.game_to_json(action="ask_buy", box_name=pos.name,
                                     box_price=pos.price, changed_players=changed_players)
        elif pos.owner == player and pos.box_type == "street":
            nb_houses_buyable = player.can_buy_houses(pos)
            if nb_houses_buyable > 0:
                return self.game_to_json(
                    action="ask_buy_houses",
                    box_name=pos.name,
                    house_price=pos.price,
                    buyable_houses=nb_houses_buyable,
                    changed_players=changed_players)
            else:
                return self.do_nothing(player, new_turn)
        elif pos.owner is not None:
            player.pay_player(pos.owner, pos.get_rent(player))
            self.next_player()
            changed_players[player.id] = {"money": player.money}
            return self.game_to_json(changed_players=changed_players)  # TODO: Message "X payed Y"
        else:
            return self.do_nothing()

    def landing_on_card(self, pos, player=None, new_turn=False, changed_players=None):
        if changed_players is None:
            changed_players = {}
        if pos.box_type == "community-fund":
            card_id = random.randint(0, 16)
        else:
            card_id = random.randint(17, 32)
        card = self.board.cards[card_id]
        self.board.last_open_card = card
        if player is not None and new_turn:
            changed_players[player.id] = {"money": player.money}
        return self.game_to_json(action="draw_card", card_type=pos.box_type,
                                 card_message=card.name, changed_players=changed_players)

    def landing_on_tax(self, player, pos, changed_players=None):
        if changed_players is None:
            changed_players = {}
        player.loose_money(pos.rent)
        self.board.park_money += pos.rent
        self.next_player()
        changed_players[player.id] = {"money": player.money}
        return self.game_to_json(changed_players=changed_players)

    def landing_on_park(self, player, changed_players=None):
        if changed_players is None:
            changed_players = {}
        player.earn_money(self.board.park_money)
        self.board.park_money = 0
        self.next_player()
        changed_players[player.id] = {"money": player.money}
        return self.game_to_json(changed_players=changed_players)
        # TODO: Message "X earned the park money"

    def play_turn(self, data):
        action = data["action"]
        player = self.players[self.players_order[self.current_player_turn]]
        if action == "play_turn":
            if player.in_jail:
                player.jail_turn += 1
                if player.jail_turn > 3:
                    player.leave_jail()
                    new_turn = player.update_position(player.throw_dices(), self.board)
                    return self.landing_on_position(player, self.board.boxes[player.position],
                                                    new_turn=new_turn)
                else:
                    return self.jail_turn(player, data["action_value"])
            else:
                new_turn = player.update_position(player.throw_dices(), self.board)
                return self.landing_on_position(player, self.board.boxes[player.position],
                                                new_turn=new_turn)

        elif action == "buy":
            changes = {}
            bought = {}
            if data["action_value"]:
                bought_box = self.board.boxes[player.position]
                bought[player.id] = bought_box.name
                player.buy_good(bought_box)
                changes["money"] = player.money
                if bought_box.box_type == "street":
                    color = bought_box.color
                    changes[color] = player.get_number_of_color(color)
                elif bought_box.box_type == "station":
                    changes["station"] = player.get_number_of_stations()
                elif bought_box.box_type == "public-company":
                    # TODO: ugly fix to come...
                    if player.position == 12:
                        changes["electricity"] = 1
                    else:
                        changes["water"] = 1
            changed_players = {player.id: changes}
            self.next_player()
            return self.game_to_json(changed_players=changed_players, bought=bought)

        elif action == "buy_houses":
            changed_players = None
            nb_houses = int(data["action_value"])
            if nb_houses > 0:
                player.buy_houses(self.board.boxes[player.position], nb_houses)
                changed_players = {player.id: {"money": player.money}}
                # TODO: display number of houses on sidebar ?
            self.next_player()
            return self.game_to_json(changed_players=changed_players)

        elif action == "execute_card":
            init_pos = player.position
            changed_players = self.board.last_open_card.execute(player, self.players, self.board)
            new_pos = player.position
            if init_pos != new_pos and not player.in_jail:
                return self.landing_on_position(player, self.board.boxes[new_pos], changed_players=changed_players)
            else:
                self.next_player()
                return self.game_to_json(changed_players=changed_players)
