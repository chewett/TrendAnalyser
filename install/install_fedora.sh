#!/bin/bash

sudo rm -rf TwitterAPI
git clone https://github.com/geduldig/TwitterAPI.git
cd TwitterAPI
sudo python setup.py install
cd ..

sudo yum install python-pip -y
sudo pip install requests

sudo rm -rf requests-oauthlib
git clone https://github.com/requests/requests-oauthlib.git
cd requests-oauthlib
sudo python setup.py install
