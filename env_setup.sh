#! /bin/bash

# install shell apps
Y | apt-get update && apt-get install tmux && apt-get install nano

# set up github
git config --global user.name "ElvinOuyang"
git config --global user.email "elvin.ouyang@gmail.com"
git config credential.helper store

# install Chrome for selenium
apt-get install -y curl
curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
dpkg -i /chrome.deb || apt-get install -yf
rm /chrome.deb

# install chrome driver for selenium
curl https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip -o /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver

# install python packages
pip install selenium

# set up notebook password
jupyter notebook password

# execution to fire up the env
tmux new -d -s jupyter_session 'jupyter lab --notebook-dir="$PWD" --ip 0.0.0.0 --no-browser --allow-root'
