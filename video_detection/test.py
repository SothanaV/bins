import socketio
from utils import VideoCamera
import base64
sio = socketio.Client()
sio.connect('http://localhost:5000')

data_in = 0
camera = 0
video_camera = None
def data():
    global data_in
    while(data_in!=-99):
        data_in = int(input("Input : "))
        sio.emit('class',data_in)

def video_stream():
    global video_camera
    alert_classes = [] # target classes

    if video_camera == None:
        video_camera = VideoCamera(camera=camera, alert_classes=alert_classes)
        
    while True:
        # img = video_camera.get_frame(byte=False)
        img = video_camera.get_frame(byte=True)
        img = base64.b64encode(img)
        if img is not None:
            sio.emit('image', {
                'image': img,
                'camera_id': 0, # fixed camera id (Int)
                })
if __name__ == '__main__':
    video_stream()
    data()