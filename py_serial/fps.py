import socketio
import serial
from time import sleep
import os

sio = socketio.Client()
sio.connect('http://localhost:5000')
print('my sid is', sio.sid)

@sio.on('fps_in')
def my_event(data):
    os.system('clear')
    print('FPS : ', data)
    