virtualenv env
source env/bin/activate
pip install -r display/requirements.txt
cd video_detection
docker-compose up -d --build
docker-compose stop
cd ..