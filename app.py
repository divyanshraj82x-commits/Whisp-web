from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

online_users = set()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join(data):
    username = data["username"]

    if username in online_users:
        emit("username_taken")
        return

    online_users.add(username)

    # Send success only to new user
    emit("join_success", {"online": list(online_users)})

    # Update others
    emit("update_online", {"online": list(online_users)}, broadcast=True, include_self=False)

@socketio.on("message")
def handle_message(data):
    data["timestamp"] = datetime.now().strftime("%H:%M")
    emit("new_message", data, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    # We don't know username directly, so we track by request.sid if needed, 
    # but simple method requires client to send username before closing
    pass

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
