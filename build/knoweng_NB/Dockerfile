# docker build -t knoweng_pipelines .
FROM knoweng_basenb
MAINTAINER Dan Lanier <lanier4@illinois.edu>

USER $NB_USER
USER root

RUN conda install Pillow
RUN conda install IPython

RUN pip install knpackage redis dispy

ENV BASE_LOC /home/jovyan/src
ENV DC_SRC_LOC $BASE_LOC/Data_Cleanup_Pipeline
ENV SC_SRC_LOC $BASE_LOC/Samples_Clustering_Pipeline
ENV DEV_SRC_LOC $BASE_LOC/knoweng_dev_tools

# install Data_Cleanup_Pipeline
RUN git clone https://github.com/KnowEnG/Data_Cleanup_Pipeline.git ${DC_SRC_LOC}

# install Samples_Clustering_Pipeline
RUN git clone https://github.com/KnowEnG-Research/Samples_Clustering_Pipeline.git ${SC_SRC_LOC}

# install development tools
RUN git clone https://github.com/dlanier/knoweng_dev_tools.git ${DEV_SRC_LOC}

USER $NB_USER
