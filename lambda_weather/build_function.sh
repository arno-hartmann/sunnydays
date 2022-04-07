#!/bin/bash
#Todocp Python-Files to lambda_weather/
#pip3 install --target ./package decimal



pip3 install --target ./package requests
#pip3 install --target ./package datetime


cd package
zip -r ../deploy-weather.zip .
cd ..
cd src

zip -r ../deploy-weather.zip .

cd ..