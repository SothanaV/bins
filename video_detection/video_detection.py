import socketio
from utils import VideoCamera
from darknet.python import darknet as dn
from darknet.python.darknet import detect,nparray_to_image
from time import sleep
from datetime import timedelta,datetime
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("tcp://zmq:5559")

sio = socketio.Client()
sio.connect('http://server:5000')

thresh = 0.4

weights = 'darknet/models/bins/backup/yolo-v4-obj-train_last.weights'
netcfg  = 'darknet/models/bins/yolo/yolo-v4-obj-test.cfg'
data = 'darknet/models/bins/yolo/annotate/obj.data'

net  = dn.load_net(netcfg.encode('utf-8'), weights.encode('utf-8'), 0)
meta = dn.load_meta(data.encode('utf-8'))
camera = 0 # RTSP IP For ip-cam OR 0 For Default video-cam
accept_cls = ['glass','can','plastic']
pgm = {'glass':0,
    'can':1,
    'plastic':2
}
video_camera = None
def video_stream():
    global video_camera, net, meta,data
    count = 0
    alert_classes = [] # target classes
    alert_classes+=accept_cls
    current = datetime.now()
    if video_camera == None:
        video_camera = VideoCamera(camera=camera, alert_classes=alert_classes)
    while True:
        status = 0
        count+=1
        img = video_camera.get_frame(byte=False)
        if img is not None:
            detected_objects = detect(net, meta, img, thresh=thresh)
            for obj, confidence, rect in detected_objects:
                detected_class = obj.decode('utf-8')
                status = pgm[detected_class]
            frame, is_alert = video_camera.draw_yolo(detected_objects=detected_objects)
            data = {
                'frame': frame,
                'camera_id': 0, # fixed camera id (Int)
                'is_alert': is_alert,
            }
            if datetime.now() > (current+timedelta(seconds=1)):
                data['fps'] = count
                count=0
                current=datetime.now()
            zmq_socket.send_pyobj(data)
            sio.emit('class', status)
if __name__ == '__main__':
    video_stream()
