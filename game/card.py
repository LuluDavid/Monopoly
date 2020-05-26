from game.globs import NB_BOXES


class Card:
    
    def __init__(self, card_id, name, card_type, value):
        self.id = card_id
        self.name = name
        self.card_type = card_type
        self.value = value

    def execute(self, player, players, board):
        if self.card_type == "earn-money":
            player.earn_money(self.value)

        elif self.card_type == "loose-money":
            player.loose_money(self.value)
            board.park_money += self.value

        elif self.card_type == "taxes":
            nb_houses, nb_hotels = player.get_number_of_buildings()
            amount = nb_houses * self.value[0] + nb_hotels * self.value[1]
            player.loose_money(amount)
            board.park_money += amount

        elif self.card_type == "backwards":
            player.update_position([-self.value], board)

        elif self.card_type == "move-backward-to":
            player.update_position([-((player.position - self.value) % NB_BOXES)], board)

        elif self.card_type == "move-forward-to":
            player.update_position([(self.value - player.position) % NB_BOXES], board)

        elif self.card_type == "go-to-jail":
            player.go_to_jail(board)

        elif self.card_type == "birthday":
            for payer in filter(lambda p: p != player, players.values()):
                payer.pay_player(player, self.value)

        elif self.card_type == "loose-money-or-chance":
            # TODO: or chance ?
            player.loose_money(self.value)
            board.park_money += self.value

        elif self.card_type == "leave_jail":
            player.card_leave_jail += 1

        else:
            raise Exception("This card type does not exist : ", self.card_type)
