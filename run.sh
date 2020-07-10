cd video_detection
docker-compose up -d --build
cd ..
source env/bin/activate
python display/display.py