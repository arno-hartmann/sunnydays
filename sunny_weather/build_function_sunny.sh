#!/bin/bash

pip3 install --target ./package -r requirement.txt
cd package
zip -r ../deploy-sunny.zip .
cd ..
cd src

zip -r ../deploy-sunny.zip .

cd ..


### requirements.txt : statistics == 1.0.3.5