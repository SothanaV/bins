import socketio
import serial

sio = socketio.Client()
sio.connect('http://localhost:5000')
print('my sid is', sio.sid)

ser = serial.Serial('/dev/cu.wchusbserial1440',115200)


@sio.on('mcu')
def my_event(data):
    print('Received data: ', data)
    if data == 1:
        command = "180"
        ser.write(command.encode())
    elif data == 0:
        command = "0"
        ser.write(command.encode())
    s = ser.readline()
    s = s.decode('utf-8','ignore')
    print(s)
