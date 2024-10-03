FROM jupyter/scipy-notebook:python-3.9.5
LABEL author="Image based on the work by Muhammad Aditya Hilmy - ESCAPE WP2 2020"
LABEL maintainer="VRE Team @ CERN 22/23 - E. Garcia, E. Gazzarrini, D. Gosein"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

RUN pip install --upgrade pip

USER $NB_UID

RUN conda install python=3.8 \
    && conda install -y -c conda-forge python-gfal2 \
    && conda clean --all -f -y

RUN pip install rucio-jupyterlab>=0.9.8 swanoauthrenew==1.0.1 PyJWT\
    && jupyter serverextension enable --py rucio_jupyterlab --sys-prefix \
    && jupyter serverextension enable --py swanoauthrenew --sys-prefix \
    && pip install reana-client

USER root

RUN apt update -y \
    && apt install -y build-essential curl \
    && apt install -y voms-clients-java software-properties-common \
    && apt clean -y \
    && rm /opt/conda/bin/voms-proxy-init \
    && ln -s /usr/bin/voms-proxy-init /opt/conda/bin/voms-proxy-init

# ESCAPE grid-security and VOMS setup
RUN wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | apt-key add -

RUN pip install ipykernel

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

# Auto load kernel extension when loading IPython
ENV IPYTHONDIR=/etc/ipython
ADD ipython_kernel_config.json /etc/ipython/profile_default/ipython_kernel_config.json
RUN chown -R $NB_UID /etc/ipython
ENV JUPYTER_ENABLE_LAB=yes

USER root

# Install ROOT
ENV LANG=C.UTF-8
ARG ROOT_BIN=root_v6.26.10.Linux-ubuntu20-x86_64-gcc9.4.tar.gz	

WORKDIR /opt

COPY packages packages

RUN apt-get update -qq \
    && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
    && apt-get -y install $(cat packages) wget\
    && rm -rf /var/lib/apt/lists/*\
    && wget https://root.cern/download/${ROOT_BIN} \
    && tar -xzvf ${ROOT_BIN} \
    && rm -f ${ROOT_BIN} \
    && echo /opt/root/lib >> /etc/ld.so.conf \
    && ldconfig

RUN apt-get -y install libxrootd-client-dev libxrootd-dev libxrootd-private-dev libxrootd-server-dev

ENV ROOTSYS /opt/root
ENV PATH $ROOTSYS/bin:$PATH
ENV PYTHONPATH $ROOTSYS/lib:$PYTHONPATH
ENV CLING_STANDARD_PCH none

RUN mkdir -p /opt/conda/share/jupyter/kernels/root \
    && cp -r /opt/root/etc/notebook/kernels/root/kernel.json /opt/conda/share/jupyter/kernels/root/kernel.json

 #RUN conda install -c conda-forge metakernel # conda complains, installing though pip
RUN pip install metakernel


WORKDIR $HOME
USER $NB_UID

CMD ["setup.sh", "start-notebook.sh"]
