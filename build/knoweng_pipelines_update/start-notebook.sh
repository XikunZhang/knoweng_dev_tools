#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

cp -r /home/jovyan/pipelines/* /home/jovyan/work/

. /usr/local/bin/start.sh jupyter notebook $*
