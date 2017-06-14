FROM knowengdev/jupyter_notebooks:base_image
MAINTAINER Dan Lanier <lanier4@illinois.edu>

USER root
ENV BASE_LOC /home/jovyan/pipelines
RUN mkdir $BASE_LOC
RUN chown $NB_USER $BASE_LOC

RUN pip install --upgrade pip
RUN pip install knpackage redis dispy

# define a directory structure relative to the notebooks
ENV DC_SRC_LOC $BASE_LOC/Data_Cleanup_Pipeline
ENV SC_SRC_LOC $BASE_LOC/Samples_Clustering_Pipeline
ENV GP_SRC_LOC $BASE_LOC/Gene_Prioritization_Pipeline
ENV GSC_SRC_LOC $BASE_LOC/GeneSet_Characterization_Pipeline

ENV DEV_SRC_LOC $BASE_LOC/knoweng_dev_tools

# install Data_Cleanup_Pipeline
RUN git clone https://github.com/KnowEnG/Data_Cleanup_Pipeline.git ${DC_SRC_LOC}

# install Samples_Clustering_Pipeline
RUN git clone https://github.com/KnowEnG-Research/Samples_Clustering_Pipeline.git ${SC_SRC_LOC}

# install Gene_Prioritization_Pipeline
RUN git clone https://github.com/KnowEnG-Research/Gene_Prioritization_Pipeline.git ${GP_SRC_LOC}

# install GeneSet_Characterization_Pipeline
RUN git clone https://github.com/KnowEnG-Research/GeneSet_Characterization_Pipeline.git ${GSC_SRC_LOC}

# install notebook development tools
RUN git clone https://github.com/dlanier/knoweng_dev_tools.git ${DEV_SRC_LOC}

USER $NB_USER

# docker build -t knoweng_pipelines .
# rooted: https://github.com/jupyter/docker-stacks (base-notebook)