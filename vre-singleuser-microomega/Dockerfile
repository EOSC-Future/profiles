FROM ghcr.io/vre-hub/vre-singleuser:sha-423e01a
LABEL author="VRE Team @ CER 22/23 -  - E. Garcia, E. Gazzarrini, D. Gosein"
LABEL maintainer="VRE Team @ CERN 22/23 - E. Garcia, E. Gazzarrini, D. Gosein"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

USER root

# GCC compiler
RUN apt update -y \
    && apt install -y build-essential

WORKDIR /opt

COPY environment.yaml environment.yaml

RUN conda install conda=4.12.0 && \
    conda install mamba -n base -c conda-forge && \
    mamba env create -f environment.yaml && \
    conda clean --all -f -y

ENV PATH /opt/conda/envs/microomega/bin:$PATH
ENV CONDA_DEFAULT_ENV microomega

RUN echo "conda activate microomega" >> ~/.bashrc

RUN conda install -p /opt/conda/envs/microomega -c fermi fermitools 

WORKDIR $HOME
USER $NB_UID
