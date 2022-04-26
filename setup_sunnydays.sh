#!/bin/bash
cd lambda_weather
sh build_function.sh
cd ..

cd sunny_weather
sh build_function_sunny.sh
cd ..

cd get_flight
sh build_function_flight.sh
cd ..

cd webserver
zip -r webserver.zip static/* templates/* app.py run-api.sh
cd ..

aws s3api create-bucket --bucket sunnydays-webserver-zip-holing-s3-neu --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2

echo "waiting for 20 seconds for S3 to be created"
sleep 20

aws s3 cp webserver/webserver.zip s3://sunnydays-webserver-zip-holing-s3-neu/webserver.zip --acl public-read-write

terraform init
terraform plan
terraform apply

echo "waiting for 20 seconds for EC2 to download .zip from S3"
sleep 20


cd create_sunnydays
python3 write_cities_to_dynamodb.py
cd ..


cd lambda_weather
rm -rf package
rm -rf deploy-weather.zip
cd ..

cd sunny_weather
rm -rf package
rm -rf deploy-sunny.zip
cd ..

cd get_flight
rm -rf deploy-flight.zip
cd ..

cd webserver
rm -rf webserver.zip
cd ..


aws s3 rb s3://sunnydays-webserver-zip-holing-s3-neu/ --force

echo "sunnydays is ready"
