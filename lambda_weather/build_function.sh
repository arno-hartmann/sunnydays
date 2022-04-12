#!/bin/bash



pip3 install --target ./package requests


cd package
zip -r ../deploy-weather.zip .
cd ..
cd src

zip -r ../deploy-weather.zip .

cd ..