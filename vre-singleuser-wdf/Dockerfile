# Based on same strategy as the one done at 
# https://gitlab.in2p3.fr/escape2020/virtual-environment/docker-images/-/blob/master/datalake-singleuser-wdf/Dockerfile



# Very extremely  and not at all optimaise way of building the image, just testing purposes with py3.11


FROM jupyter/base-notebook:python-3.11
LABEL author="Image based on the work by Muhammad Aditya Hilmy on the DLaaS - ESCAPE WP2 2020"
LABEL maintainer="VRE Team @ CERN 22/23 - E. Garcia, E. Gazzarrini, D. Gosein"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

USER root

RUN pip install --upgrade pip

# GCC compiler before installing everything
RUN apt update -y \
    && apt install -y build-essential

USER $NB_UID

RUN conda install -y -c conda-forge python-gfal2 \
   && conda clean --all -f -y

RUN pip install jupyter_contrib_nbextensions 
RUN jupyter contrib nbextension install --user
RUN pip install rucio-jupyterlab>=0.9.8 
RUN pip install swanoauthrenew==1.0.1
RUN pip install PyJWT 
RUN jupyter serverextension enable --py rucio_jupyterlab --sys-prefix
RUN jupyter serverextension enable --py swanoauthrenew --sys-prefix 
RUN pip install reana-client>=0.9.0 
RUN pip install ipykernel

USER root

RUN apt update -y \
    && apt install -y build-essential curl voms-clients-java software-properties-common \
    && apt clean -y \
    && rm /opt/conda/bin/voms-proxy-init \
    && ln -s /usr/bin/voms-proxy-init /opt/conda/bin/voms-proxy-init

# ESCAPE grid-security and VOMS setup
RUN wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | apt-key add -

RUN apt update \
    && add-apt-repository 'deb http://repository.egi.eu/sw/production/cas/1/current egi-igtf core' \
    && apt -y install ca-certificates ca-policy-egi-core

RUN mkdir -p /etc/vomses \
    && wget https://indigo-iam.github.io/escape-docs/voms-config/voms-escape.cloud.cnaf.infn.it.vomses -O /etc/vomses/voms-escape.cloud.cnaf.infn.it.vomses \
    && mkdir -p /etc/grid-security/vomsdir/escape \
    && wget https://indigo-iam.github.io/escape-docs/voms-config/voms-escape.cloud.cnaf.infn.it.lsc -O /etc/grid-security/vomsdir/escape/voms-escape.cloud.cnaf.infn.it.lsc

# Setup merged CERN CA file on Ubuntu based images.
# This file is contained in the `CERN-bundle.pem` file downloaded using 
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

# Setup extension Rucio instance config
ADD configure.py /opt/setup-rucio-jupyterlab/configure.py
ADD setup.sh /usr/local/bin/setup.sh
RUN fix-permissions /opt/setup-rucio-jupyterlab \
    && fix-permissions /usr/local/bin/setup.sh \
    && sed -i -e 's/\r$/\n/' /usr/local/bin/setup.sh \
    && chmod +x /usr/local/bin/setup.sh

RUN mkdir -p /opt/rucio \
    && chown -R $NB_UID /opt/rucio \
    && /usr/local/bin/setup.sh \
    && chown -R $NB_UID /etc/jupyter/jupyter_notebook_config.json \
    && chown -R $NB_UID /etc/jupyter/jupyter_notebook_config.py

ENV IPYTHONDIR=/etc/ipython
ADD ipython_kernel_config.json /etc/ipython/profile_default/ipython_kernel_config.json
RUN chown -R $NB_UID /etc/ipython
ENV JUPYTER_ENABLE_LAB=yes

WORKDIR $HOME
USER $NB_UID


# ------------------------------------------------------
# Env wdf-python
# https://gitlab.com/wdfpipe/createwdfenv/-/blob/main/dockers/env_python/Dockerfile

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Rome

# create and activate virtual environment
RUN python3.11 -m venv /opt/venv
ENV ENV_ROOT="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
ENV LD_LIBRARY_PATH="/opt/venv/lib:$LD_LIBRARY_PATH"
ENV PYTHONPATH="/opt/venv/lib/python3.11:/opt/venv/lib/python3.11/site-packages:$PYTHONPATH"


# install requirements
COPY requirements.txt .  
RUN pip3 install -r requirements.txt

# env wdf
# https://gitlab.com/wdfpipe/createwdfenv/-/blob/main/dockers/env_wdf/Dockerfile

# runtime dependencies to install wdf
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
	cmake \
    libboost-all-dev \
    pybind11-dev python3-pybind11 \
    libfftw3-3 libfftw3-dev libfftw3-bin \
    libgsl-dev; \
	rm -rf /var/lib/apt/lists/*
  
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

# env wdfpipe
# https://gitlab.com/wdfpipe/wdf/-/blob/master/dockers/wdfpipe/Dockerfile

RUN https://gitlab.com/wdfpipe/wdf.git && cd wdf
RUN mkdir tmp1/
ADD . tmp1/
RUN cd tmp1/ && python setup.py  install &&\
    cd .. && rm -fr tmp1/ 


CMD ["setup.sh", "start-notebook.sh"]
