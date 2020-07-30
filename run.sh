#!/bin/bash

echo "Installing Brew"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

echo "Installing Python"
brew install python

echo "Installing PIP"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

echo "Installing dependencies"
pip install -r requirements.txt

#echo "Running the application"
#python main.py