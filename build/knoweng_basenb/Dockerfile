# docker build -t knoweng_basenb .
FROM jupyter/base-notebook
MAINTAINER Dan Lanier <lanier4@illinois.edu>

USER $NB_USER

USER root

# Install packages and their dependencies
RUN apt-get update && apt-get install -y vim python3-pip git libblas-dev liblapack-dev libatlas-base-dev gfortran libfreetype6-dev libxft-dev
RUN conda install numpy==1.11.1 pandas==0.18.1 scipy==0.18.0 scikit-learn==0.17.1 pyyaml

RUN apt-get update && apt-get install python3-dev python3-setuptools

RUN conda install Pillow
RUN conda install IPython

USER $NB_USER
