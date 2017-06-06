# docker build -t configged .
FROM local_user_notebook
MAINTAINER lanier4 <lanier4@illinois.edu>

ENTRYPOINT jupyter
CMD "notebook --no-browser --config-dir .jupyter" 

# docker run -v `pwd`:/home/local_user/test -it --rm -p 8888:8888 local_user_notebook
# WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
# docker exec -it xxxxxxxxxxxxx bash

# https://jupyter.readthedocs.io/en/latest/projects/jupyter-directories.html