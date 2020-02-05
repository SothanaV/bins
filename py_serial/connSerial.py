import socketio
import serial
from datetime import datetime,timedelta
sio = socketio.Client()
sio.connect('http://localhost:5000')
print('my sid is', sio.sid)

ser = serial.Serial('/dev/ttyUSB0',115200)
current = datetime.now()

@sio.on('mcu')
def my_event(data):
    
    print('Received data: ', data)
    if data == 1:
        print("Close")
        command="180"
    elif data == 0:
        print("Open")
        command="140"
    command+='\n'
    ser.write(command.encode())
    sio.sleep(2)
        
