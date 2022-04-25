#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
yum update -y


#aws s3 cp s3://sunnydays-webserver-zip-holing-s3-neu/webserver.zip /home/ec2-user/webserver.zip
wget https://sunnydays-webserver-zip-holing-s3-neu.s3.us-west-2.amazonaws.com/webserver.zip
cd /home/ec2-user/

unzip webserver.zip

chown -R ec2-user .
#sudo python3 -m venv venv
#sudo . venv/bin/activate
pip3 install Flask


export FLASK_APP=app
export FLASK_ENV=venv

cd webserver
sudo python3 app.py