import socketio
import serial
from time import sleep
import eventlet
sio = socketio.Client()
sio.connect('http://localhost:5000')
print('my sid is', sio.sid)

ser = serial.Serial('/dev/ttyUSB0',115200)

# @sio.on('mcu')
def my_event(data):
    
    print('Received data: ', data)
    if data == 1:
        command = "120"
        ser.write(command.encode())
    elif data == 0:
        command = "180"
        ser.write(command.encode())
    print("read : {}  len : {}".format(ser.readline(),len(ser.readline())))
    socketio.sleep(0.1)
    while len(ser.readline()) == 0:
        print("wait")
    s = ser.readline()
    s = s.decode('utf-8','ignore')
    print(s)
    eventlet.sleep(1)

if __name__ == '__main__':
    print("hello")    
    sio.on('mcu',my_event)