# docker build -t notebook_base .
FROM knowengdev/base_image:11_09_2016
MAINTAINER Dan Lanier<lanier4@illinois.edu>

RUN apt-get update && apt-get install python3-dev python3-setuptools
RUN apt-get update && apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

RUN pip3 install Pillow
RUN pip3 install -I knpackage redis dispy
RUN pip3 install IPython
RUN pip3 install jupyter




