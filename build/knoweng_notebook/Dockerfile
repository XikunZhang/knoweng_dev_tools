# docker build -t local_user_notebook .
FROM notebook_base
MAINTAINER lanier4<lanier4@illinois.edu>

USER root

ENV JUP_DIR /usr/local
ENV PATH $JUP_DIR/bin:$PATH
ENV NB_USER local_user
ENV NB_UID 1000

ENV BASE_LOC /home/$NB_USER

# Create local_user user with UID=1000 and in the 'users' group
# RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && mkdir -p $JUP_DIR && chown $NB_USER $JUP_DIR
# RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && chown $NB_USER $JUP_DIR && chown $NB_USER $BASE_LOC
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && chown $NB_USER $BASE_LOC

ENV DC_SRC_LOC $BASE_LOC/Data_Cleanup_Pipeline
ENV SC_SRC_LOC $BASE_LOC/Samples_Clustering_Pipeline
ENV DEV_SRC_LOC $BASE_LOC/knoweng_dev_tools

# install Data_Cleanup_Pipeline
RUN git clone https://github.com/KnowEnG/Data_Cleanup_Pipeline.git ${DC_SRC_LOC}

# install Samples_Clustering_Pipeline
RUN git clone https://github.com/KnowEnG-Research/Samples_Clustering_Pipeline.git ${SC_SRC_LOC}

# install development tools
RUN git clone https://github.com/dlanier/knoweng_dev_tools.git ${DEV_SRC_LOC}

EXPOSE 8888
WORKDIR ${BASE_LOC}
USER $NB_USER

RUN /usr/local/bin/jupyter notebook --generate-config

ENTRYPOINT jupyter
CMD "notebook"

# docker run -v `pwd`:/home/KnowEnG-Research -it --rm -p 8888:8888 local_user_notebook
# WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
# docker exec -it xxxxxxxxxxxxx bash
