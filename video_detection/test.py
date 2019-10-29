import socketio
sio = socketio.Client()
sio.connect('http://localhost:5000')

data_in = 0

while(data_in!=-99):
    data_in = int(input("Input : "))
    sio.emit('class',data_in)