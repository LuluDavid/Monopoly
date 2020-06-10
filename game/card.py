from game.globs import NB_BOXES


class Card:
    
    def __init__(self, card_id, name, card_type, value):
        self.id = card_id
        self.name = name
        self.card_type = card_type
        self.value = value

    def execute(self, player, players, board):
        changed_players = None
        if self.card_type == "earn-money":
            player.earn_money(self.value)
            changed_players = {player.id: {"money": player.money}}

        elif self.card_type == "loose-money":
            player.loose_money(self.value)
            changed_players = {player.id: {"money": player.money}}
            board.park_money += self.value

        elif self.card_type == "taxes":
            nb_houses, nb_hotels = player.get_number_of_buildings()
            amount = nb_houses * self.value[0] + nb_hotels * self.value[1]
            player.loose_money(amount)
            changed_players = {player.id: {"money": player.money}}
            board.park_money += amount

        elif self.card_type == "backwards":
            player.update_position([-self.value], board)

        elif self.card_type == "move-backward-to":
            player.update_position([-((player.position - self.value) % NB_BOXES)], board)

        elif self.card_type == "move-forward-to":
            new_turn = player.update_position([(self.value - player.position) % NB_BOXES], board)
            if new_turn:
                changed_players = {player.id: {"money": player.money}}

        elif self.card_type == "go-to-jail":
            player.go_to_jail(board)

        elif self.card_type == "birthday":
            changed_players = {}
            for payer in filter(lambda p: p != player, players.values()):
                payer.pay_player(player, self.value)
                changed_players[player.id] = {"money": player.money}

        elif self.card_type == "loose-money-or-chance":
            # TODO: or chance ?
            player.loose_money(self.value)
            changed_players = {player.id: {"money": player.money}}
            board.park_money += self.value

        elif self.card_type == "leave-jail":
            player.card_leave_jail += 1

        return changed_players
        # else:
        #    raise Exception("This card type does not exist : ", self.card_type)
