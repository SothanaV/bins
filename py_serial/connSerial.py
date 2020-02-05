import socketio
import serial
from time import sleep

sio = socketio.Client()
sio.connect('http://localhost:5000')
print('my sid is', sio.sid)

ser = serial.Serial('/dev/cu.wchusbserial1420',115200)


@sio.on('mcu')
def my_event(data):
    print('Received data: ', data)
    if data == 1:
        command = "120"
        ser.write(command.encode())
    elif data == 0:
        command = "180"
        ser.write(command.encode())
    while len(ser.readline()) == 0:
        print("wait")
    s = ser.readline()
    s = s.decode('utf-8','ignore')
    print(s)
