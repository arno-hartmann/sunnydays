#!/bin/bash
#Todocp Python-Files to lambda_weather/
#pip3 install --target ./package decimal
pip3 install --target ./package requests
pip3 install --target ./package datetime


cd package
zip -r ../deployment-package-weather.zip .
cd ..
zip -g deployment-package-weather.zip lambda_weather_function.py

# deploy to AWS