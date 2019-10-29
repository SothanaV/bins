import socketio
from utils import VideoCamera
from darknet.python import darknet as dn
from darknet.python.darknet import detect,nparray_to_image

sio = socketio.Client()
sio.connect('http://localhost:5000')
video_camera = None

weights = 'darknet/yolov3.weights'
netcfg  = 'darknet/cfg/yolov3.cfg'
data = 'darknet/cfg/coco.data'

net  = dn.load_net(netcfg.encode('utf-8'), weights.encode('utf-8'), 0)
meta = dn.load_meta(data.encode('utf-8'))

camera = None # RTSP IP For ip-cam OR 0 For Default video-cam
accept_cls = []
def video_stream():
    global video_camera, net, meta,data
    alert_classes = [] # target classes
    alert_classes+=accept_cls

    if video_camera == None:
        video_camera = VideoCamera(camera=camera, alert_classes=alert_classes)
        
    while True:
        img = video_camera.get_frame(byte=False)
        if img is not None:
            detected_objects = detect(net, meta, img, thresh=.30)
            for obj, confidence, rect in detected_objects:
                detected_class = obj.decode('utf-8')
                if detected_class in accept_cls:
                    sio.emit('class',1)
                else:
                    sio.emit('class',0)
            frame, is_alert = video_camera.draw_yolo(detected_objects=detected_objects)
            sio.emit('image', {
                'image': frame,
                'camera_id': 0, # fixed camera id (Int)
                'is_alert': is_alert,
                })
if __name__ == '__main__':
    video_stream()
