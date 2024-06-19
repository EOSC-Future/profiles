#FROM quay.io/jupyter/minimal-notebook:python-3.11.7
FROM jupyter/minimal-notebook:python-3.10.11
LABEL author="Image based on the work by Muhammad Aditya Hilmy - ESCAPE WP2 2020"
LABEL maintainer="VRE Team @ CERN 2023 - E. Garcia"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

USER root

RUN pip install --upgrade jupyterlab jupyterlab_server jupyter_server traitlets nbformat

WORKDIR /opt

# ------------------------------------------------------
# Env python
# 05-10-2022 https://gitlab.com/wdfpipe/wdf/-/blob/master/dockers/env_python/Dockerfile

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Rome


# commenting 3rd line - using python already installed here:     python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel \ 
RUN apt-get update && apt-get install --no-install-recommends -y \
    tzdata wget git vim build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    cmake \
    libboost-all-dev \
    pybind11-dev python3-pybind11 \
    libfftw3-3 libfftw3-dev libfftw3-bin \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

## create and activate virtual environment
#RUN python3.9 -m venv /opt/venv
#ENV ENV_ROOT="/opt/venv"
#ENV PATH="/opt/venv/bin:$PATH"

## not using venv, instead we use the base conda env and fixing env vars
ENV LD_LIBRARY_PATH="/opt/conda/lib:$LD_LIBRARY_PATH"
ENV PYTHONPATH="/opt/conda/lib/python3.10:/opt/conda/lib/python3.10/site-packages:$PYTHONPATH"

## While the installation of pst4 and the use of `venv`, it is needed the `ENV_ROOT` env var
## > echo $ENV_ROOT/
## > /opt/venv/
ENV ENV_ROOT="/opt/conda"

# install requirements
COPY requirements.txt .
# Using installed version of pip
RUN echo "pip:"; pip -V && \
    echo "pip3:" pip3 -V
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt


# ------------------------------------------------------
# Env wdf
# 05-10-2022 https://gitlab.com/wdfpipe/wdf/-/blob/master/dockers/env_wdf/Dockerfile

#install GSL 
RUN set -ex \
    && wget https://mirror.ibcp.fr/pub/gnu/gsl/gsl-2.7.1.tar.gz\
    && tar -xzf gsl-2.7.1.tar.gz \
    && cd gsl-2.7.1\
    && ./configure \
    && make -j "$(nproc)" \
    && make install \
    && cd .. \
    && rm -rf gsl-2.7.1 \
    && rm gsl-2.7.1.tar.gz
#RUN apt-get update && apt-get install -y \
#    libgsl-dev  \
#    && apt-get clean && rm -rf /var/lib/apt/lists/*


#install FrameLib
RUN set -ex \
    && git clone https://git.ligo.org/virgo/virgoapp/Fr.git \
    && cd  Fr && cmake CMakeLists.txt \
    && make -j "$(nproc)" \
    && make install \
    && cd .. \
    && rm -rf Fr  

#install P4TSA
RUN git clone https://github.com/elenacuoco/p4TSA && cd p4TSA && cmake CMakeLists.txt \
    && make -j "$(nproc)" \
    && make install \
    && cd python-wrapper \
    && python setup.py  install \
    && cd .. \
    && cd .. \
    && rm -fr p4TSA

RUN /sbin/ldconfig 


# ------------------------------------------------------
# wdpipe
# 05-10-2022 https://gitlab.com/wdfpipe/wdf/-/blob/master/dockers/wdfpipe/Dockerfile

#install wdpipe
# Second line to be deleted when fixed in the wdfpipe repo 
RUN git clone https://gitlab.com/wdfpipe/wdf.git && cd wdf \
    && python setup.py  install \
    && cd .. \ 
    && rm -fr wdf


WORKDIR $HOME
USER $NB_UID

#RUN conda install -y -c conda-forge python-gfal2 \
#    && conda clean --all -f -y

# RUN pip install rucio-clients==1.31.0 \
#     && pip install ipykernel

USER root

RUN apt update -y \
    && apt install -y build-essential curl cmake

# RUN apt update -y \
#     && apt install -y build-essential curl voms-clients-java software-properties-common \
#     && apt clean -y \
#     && rm /opt/conda/bin/voms-proxy-init \
#     && ln -s /usr/bin/voms-proxy-init /opt/conda/bin/voms-proxy-init

RUN pip install reana-client==0.9.2

# ESCAPE grid-security and VOMS setup
# RUN wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | apt-key add -

# RUN apt update \
#     && add-apt-repository 'deb http://repository.egi.eu/sw/production/cas/1/current egi-igtf core' \
#     && apt -y install ca-policy-egi-core

RUN mkdir -p /etc/vomses \
    && wget https://indigo-iam.github.io/escape-docs/voms-config/voms-escape.cloud.cnaf.infn.it.vomses -O /etc/vomses/voms-escape.cloud.cnaf.infn.it.vomses \
    && mkdir -p /etc/grid-security/vomsdir/escape \
    && wget https://indigo-iam.github.io/escape-docs/voms-config/voms-escape.cloud.cnaf.infn.it.lsc -O /etc/grid-security/vomsdir/escape/voms-escape.cloud.cnaf.infn.it.lsc

# # Setup merged CERN CA file on Ubuntu based images.
# # This file is contained in the `CERN-bundle.pem` file downloaded using 
RUN mkdir /certs \
    && touch /certs/rucio_ca.pem \
    && curl -fsSL 'https://cafiles.cern.ch/cafiles/certificates/CERN%20Root%20Certification%20Authority%202.crt' | openssl x509 -inform DER -out /tmp/cernrootca2.crt \
    && curl -fsSL 'https://cafiles.cern.ch/cafiles/certificates/CERN%20Grid%20Certification%20Authority(1).crt' -o /tmp/cerngridca.crt \
    && curl -fsSL 'https://cafiles.cern.ch/cafiles/certificates/CERN%20Certification%20Authority.crt' -o /tmp/cernca.crt \
    && cat /tmp/cernrootca2.crt >> /certs/rucio_ca.pem \
    && cat /tmp/cerngridca.crt >> /certs/rucio_ca.pem \
    && cat /tmp/cernca.crt >> /certs/rucio_ca.pem \
    && rm /tmp/*.crt \
    && update-ca-certificates

RUN mkdir -p /opt/rucio \
    && chown -R $NB_UID /opt/rucio    

ENV IPYTHONDIR=/etc/ipython
ADD ipython_kernel_config.json /etc/ipython/profile_default/ipython_kernel_config.json
RUN chown -R $NB_UID /etc/ipython
ENV JUPYTER_ENABLE_LAB=yes

WORKDIR $HOME
USER $NB_UID


CMD ["start-notebook.sh"]