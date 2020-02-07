import requests
import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0',115200)

def my_event(data):
    print('Received data: ', data)
    if data == 1:
        command = "120"
        ser.write(command.encode())
    elif data == 0:
        command = "180"
        ser.write(command.encode())
    print(ser.readline())
    # print("read : {}  len : {}".format(ser.readline(),len(ser.readline())))

if __name__ == '__main__':
    print("hello")    
    while True:
        r = requests.get('http://localhost:5000/mcu').content.decode()
        my_event(r)
        sleep(1.0)

