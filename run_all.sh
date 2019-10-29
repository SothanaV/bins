docker-compose up -d --build
source env/bin/activate
cd video_detection
python video_detection.py
# python test.py