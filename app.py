from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
