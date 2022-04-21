#!/bin/bash


pip3 install --target ./package -r src/requirements.txt
#pip3 install --target ./package statistics
cd package
zip -r ../deploy-sunny.zip .
cd ..
cd src

zip -r ../deploy-sunny.zip .

cd ..