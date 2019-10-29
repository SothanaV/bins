virtualenv env
source env/bin/activate
cd video_detection
pip install -r requirements.txt
git clone https://gitlab.com/SothanaV/darknet.git
cd darknet
wget https://pjreddie.com/media/files/yolov3.weights
make