# InStockChecker
Web scraper to check if an item is available or not

Run below script within Docker installed Linux system

```bash
sudo docker run -it -p 8000:8888 -e JUPYTER_ENABLE_LAB=yes -e GRANT_SUDO=yes --user root -v "$PWD":/home/jovyan/work jupyter/scipy-notebook:latest /bin/bash
```

Run below script to download this repo:
```bash
git clone https://github.com/ElvinOuyang/OnlineStockChecker.git
```

Run below script to finish the setup:
```bash
cd ./OnlineStockChecker
source ./env_setup.sh 
```
