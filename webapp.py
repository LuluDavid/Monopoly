from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, emit, send
import random as rd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

GAMES = {}

@app.route('/')
def home():
    return render_template('home.html.jinja2')


@app.route('/game', methods=['POST'])
def play_game():
    try:
        if request.form.get('request_type') == "create":
            game_name = request.form.get('game_name')
            game_id = generate_id()
            while game_id in GAMES:
                game_id = generate_id()
            GAMES[game_id] = {
                "name": game_name,
                "players": {}
            }

        elif request.form.get('request_type') == "join":
            game_id = int(request.form.get('game_id'))
            if game_id in GAMES:
                game_name = GAMES[game_id]["name"]
            else:
                print("Game id does not exist")
                return redirect_home()
        else:
            return redirect_home()

        player_name = request.form.get('player_name')
        player_id = generate_id()
        while player_id in GAMES[game_id]["players"]:
            player_id = generate_id()
        GAMES[game_id]["players"][player_id] = {"name": player_name}

        print(GAMES)
        return render_template(
            'loby.html.jinja2',
            game_id=game_id,
            player_id=player_id,
            player_name=player_name,
            game_name=game_name
        )

    except ValueError:
        print("Impossible to create/join the room")
        return redirect_home()


@socketio.on('join')
def on_join(data):
    """Join a game"""
    game_id = data['game_id']
    if game_id in GAMES:
        join_room(game_id)
        new_player = GAMES[game_id]["players"][data['player_id']]
        players_in_game_names = [player["name"] for player in GAMES[game_id]["players"].values()]
        emit(
            'join_game',
            {"room": game_id, "new_player": new_player, "players_in_game_names": players_in_game_names},
            room=game_id
        )
    else:
        print("Unable to join room. Room does not exist.")
        emit('error', {'error': 'Unable to join room. Room does not exist.'})


def redirect_home():
    return redirect(url_for('home'))


def generate_id():
    return int("".join([str(rd.randint(1, 9)) for i in range(12)]))


if __name__ == '__main__':
    socketio.run(app, debug=True)
