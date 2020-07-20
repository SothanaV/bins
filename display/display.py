import cv2
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PULL)
zmq_socket.connect("tcp://127.0.0.1:5560")


while(True):
    data = zmq_socket.recv_pyobj()
    frame = data['frame']
    cv2.imshow('frame',frame)
    if 'fps' in data:
        print("FPS : {}".format(data['fps']))
    cv2.waitKey(1)
cv2.destroyAllWindows()     