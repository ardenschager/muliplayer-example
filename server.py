from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random, colorsys

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# all connected players: { sid: { x, y, z, color } }
players = {}


def rand_color():
    # random hue, high saturation, decent brightness → vivid colors
    r, g, b = colorsys.hsv_to_rgb(random.random(), 0.75, 0.9)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def on_connect():
    players[request.sid] = {
        "x": random.uniform(-8, 8),
        "y": 0.5,
        "z": random.uniform(-8, 8),
        "color": rand_color(),
    }
    emit("players", players, broadcast=True)


@socketio.on("disconnect")
def on_disconnect():
    players.pop(request.sid, None)
    emit("players", players, broadcast=True)


# client sends { x, y, z } when it moves
@socketio.on("move")
def on_move(data):
    if request.sid in players:
        players[request.sid].update(data)
        emit("players", players, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
