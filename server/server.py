from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '@Q#VT#@%YWAE#%QBVY#QT'

socketio = SocketIO()
socketio.init_app(app, cors_allow_origins="*")

command = 0


@socketio.on('class')
def recv(data):
    global command
    command = data

@app.route('/mcu')
def mcu_request():
    global command
    return str(command)

if __name__ == '__main__':
    socketio.run(app , host='0.0.0.0')