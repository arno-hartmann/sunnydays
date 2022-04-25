#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
yum update -y
yum install pip -y

cd /home/ec2-user/
mkdir webserver
cd webserver
aws s3 cp s3://sunnydays-webserver-zip-holing-s3-neu/webserver.zip /home/ec2-user/webserver/webserver.zip

unzip webserver.zip

chown -R ec2-user .

pip3 install boto3
pip3 install Flask

export AWS_DEFAULT_REGION=us-west-2

python3 app.py