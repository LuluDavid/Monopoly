from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO, join_room, emit
import random as rd
from game.game import Game


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

GAMES = {}
PLAYERS = {}


@app.route('/')
def home():
    return render_template('home.html.jinja2')


@app.route('/game', methods=['GET', 'POST'])
def play_game():
    if request.method == 'POST':
        try:
            if request.form.get('request_type') == "create":
                game_id = generate_id()
                while game_id in GAMES:
                    game_id = generate_id()
                GAMES[game_id] = {
                    "game": None,
                    "players": {}
                }

            elif request.form.get('request_type') == "join":
                game_id = int(request.form.get('game_id'))
                if game_id not in GAMES:
                    print("Game id does not exist")
                    return redirect_home()
            else:
                return redirect_home()

            player_name = request.form.get('player_name')
            player_id = generate_id()
            while player_id in GAMES[game_id]["players"]:
                player_id = generate_id()
            GAMES[game_id]["players"][player_id] = player_name
            PLAYERS[player_id] = (player_name, game_id)
            resp = make_response(render_template(
                'lobby.html.jinja2',
                game_id=game_id,
                player_id=player_id,
                player_name=player_name
            ))
            resp.set_cookie('uid', str(player_id))
            return resp
        except ValueError:
            print("Impossible to create/join the room")
            return redirect_home()
    pid = request.cookies.get('uid')
    if pid is None or not isinstance(pid, str):
        redirect_home()
    player_id = int(pid)
    player_name, gid = PLAYERS[player_id]
    game_id = int(gid)
    print("Redirecting ", player_name, " in room ", player_id)
    return render_template(
        'lobby.html.jinja2',
        game_id=game_id,
        player_id=player_id,
        player_name=player_name
    )


@socketio.on('join')
def on_join(data):
    game_id = data['game_id']
    if game_id in GAMES:
        join_room(game_id)
        new_player = {"id": data['player_id'], "name": GAMES[game_id]["players"][data['player_id']]}
        players_in_game = GAMES[game_id]["players"]
        emit(
            'join_game',
            {"room": game_id, "new_player": new_player, "players_in_game": players_in_game},
            room=game_id
        )
    else:
        print("Unable to join room. Room does not exist.")
        emit('error', {'error': 'Unable to join room. Room does not exist.'})


@socketio.on("offer")
def on_offer(data):
    game_id = data["game_id"]
    emit("offer", data, room=game_id)


@socketio.on("accepted")
def on_accepted(data):
    game_id = data["game_id"]
    response = GAMES[game_id]["game"]\
        .trade(data["sender"], data["receiver"], data["offered"], data["wanted"], int(data["money"]))
    emit("trade", response, room=game_id)


@socketio.on('start_game')
def on_start_game(data):
    game_id = data["game_id"]
    GAMES[game_id]["game"] = Game(GAMES[game_id]["players"])
    game_state = GAMES[game_id]["game"].game_to_json()
    player_id = data["player_id"]
    player_name = data["player_name"]
    response = {"newPlayer": {"id": player_id, "name": player_name}, "gameState": game_state}
    emit("start_game", response, room=game_id)


@socketio.on('play_turn')
def on_play_turn(data):
    game_id = data["game_id"]
    response = GAMES[game_id]["game"].play_turn(data)
    emit("play_turn", response, room=game_id)


@socketio.on('new_msg')
def on_new_msg(data):
    player_name = data['player_name']
    msg = data['msg']
    game_id = data['game_id']
    if game_id in GAMES:
        emit(
            'print_new_msg',
            {"room": game_id, "player_name": player_name, "msg": msg},
            room=game_id
        )
    else:
        print("Unable to post in room. Room does not exist.")
        emit('error', {'error': 'Unable to post in room. Room does not exist.'})


def redirect_home():
    return redirect(url_for('home'))


def generate_id():
    return int("".join([str(rd.randint(1, 9)) for i in range(12)]))


if __name__ == '__main__':
    socketio.run(app)
