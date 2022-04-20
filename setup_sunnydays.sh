#!/bin/bash
cd lambda_weather
sh build_function.sh
cd ..
terraform init
terraform plan
terraform apply

cd create_sunnydays
python3 write_cities_to_dynamodb.py
cd ..

cd lambda_weather
rm -rf package
#rm -rf deploy-weather.zip
cd ..
pwd