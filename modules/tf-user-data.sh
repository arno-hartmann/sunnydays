#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
yum update -y

cd /home/ec2-user/

chown -R ec2-user .
#sudo python3 -m venv venv
#sudo . venv/bin/activate
pip3 install Flask

mkdir webserver
cd webserver
export FLASK_APP=app
export FLASK_ENV=venv


#sudo python3 app.py