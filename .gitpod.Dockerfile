ARG GITPOD_IMAGE=gitpod/gitpod/workspace-python-3.8:latest
FROM ${GITPOD_IMAGE}

## Update the packet cache
RUN sudo apt update

## Install libsndfile-dev
RUN sudo apt-get install -y libsndfile-dev

## Install ovhai client
RUN curl https://cli.gra.training.ai.cloud.ovh.net/install.sh | bash
