#! /bin/bash

sudo apt update -y
sudo apt install -y docker.io
sudo apt install -y awscli

aws ecr get-login-password --region eu-central-1 | sudo docker login --username AWS --password-stdin 637423548204.dkr.ecr.eu-central-1.amazonaws.com


sudo docker pull 637423548204.dkr.ecr.eu-central-1.amazonaws.com/tsd-project/fastapi:latest

sudo docker pull 637423548204.dkr.ecr.eu-central-1.amazonaws.com/tsd-project/redis:latest

sudo docker pull 637423548204.dkr.ecr.eu-central-1.amazonaws.com/tsd-project/postgres:latest

