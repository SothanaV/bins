from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins="*")

tmp = 0

@socketio.on('image')
def broadcast_image(data):
    camera_id = data['camera_id']
    broadcast_image_section = (camera_id // 12) + 1
    emit('broadcast-image-{}'.format(broadcast_image_section), data, broadcast=True)

@socketio.on('class')
def listen_detec(data):
    global tmp
    tmp = data
    emit('mcu',tmp,broadcast=True)

@app.route('/mcu')
def mcu_request():
    global tmp
    return str(tmp)

@socketio.on('fps_out')
def brod_fps(data):
    emit('fps_in',data,broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', )
