import socketio
from utils import VideoCamera
from darknet.python import darknet as dn
from darknet.python.darknet import detect,nparray_to_image
from time import sleep
sio = socketio.Client()
sio.connect('http://socket:5000')
video_camera = None

thresh = 0.4
# weights = 'darknet/model/06/backup/yolo_v3_final.weights'
# netcfg  = 'darknet/model/06/yolo/yolo_v3.cfg'

weights = 'darknet/model/06/backup/yolo_v2_final.weights'
netcfg  = 'darknet/model/06/yolo/yolo_v2.cfg'


data = 'darknet/model/06/yolo/annotate/obj.data'

net  = dn.load_net(netcfg.encode('utf-8'), weights.encode('utf-8'), 0)
meta = dn.load_meta(data.encode('utf-8'))
camera = 0 # RTSP IP For ip-cam OR 0 For Default video-cam
accept_cls = ['glass','can']
def video_stream():
    global video_camera, net, meta,data
    count = 0
    alert_classes = [] # target classes
    alert_classes+=accept_cls

    if video_camera == None:
        video_camera = VideoCamera(camera=camera, alert_classes=alert_classes)
    while True:
        status = 0
        count+=1
        img = video_camera.get_frame(byte=False)
        if img is not None:
            detected_objects = detect(net, meta, img, thresh=.3)
            for obj, confidence, rect in detected_objects:
                detected_class = obj.decode('utf-8')
                if detected_class in accept_cls:
                    status = 1  
            frame, is_alert = video_camera.draw_yolo(detected_objects=detected_objects)
            sio.emit('image', {
                'image': frame,
                'camera_id': 0, # fixed camera id (Int)
                'is_alert': is_alert,
                })
        sio.emit('class',status)
        # if status==1:
        #     sleep(1)
if __name__ == '__main__':
    video_stream()
