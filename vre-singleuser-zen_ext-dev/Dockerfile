FROM quay.io/jupyter/scipy-notebook:python-3.11.8
LABEL author="Image based on the work by Muhammad Aditya Hilmy - ESCAPE WP2 2020"
LABEL maintainer="VRE Team @ CERN 23/24 - E. Garcia, G. Guerrieri"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

RUN python -m pip install --upgrade pip

USER $NB_UID

RUN conda install -y -n base mamba \
    && mamba install -y -c conda-forge python-gfal2 \
        nodejs \
        jupyterlab">4,<5" \
        notebook"<7" \
        jupyterhub \
        jsonschema>4 \
        jupyterlab_server \
        jupyter_server \
        traitlets \
        nbformat \
        ipykernel \
        PyJWT \
        ipywidgets \
    && conda clean --all -f -y

# # Install jupyterlab extensions
# RUN python -m pip install rucio-jupyterlab==1.0.0 \
#     && jupyter server extension enable --py rucio_jupyterlab --sys-prefix 

# RUN python -m pip install swanoauthrenew==1.0.1 \ 
#     && jupyter server extension enable --py swanoauthrenew --sys-prefix 

# RUN python -m pip install reana-jupyterlab \
#     && jupyter server extension enable --py reana_jupyterlab --sys-prefix

RUN git clone https://github.com/vre-hub/zenodo-jupyterlab-extension.git \
    && cd zenodo-jupyterlab-extension \
    && git checkout dev \
    && python -m pip install . \
    && jupyter server extension enable --py zenodo_jupyterlab.server --sys-prefix \
    && cd .. \
    && rm -rf zenodo-jupyterlab-extension
    
# Custom version of reana-client due to the jsonschema problem
#RUN python -m pip install git+https://github.com/mdonadoni/reana-client.git@vre-summer-24

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
    && apt -y install ca-policy-egi-core

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
COPY configure-vre.py /usr/local/bin/
RUN chmod +x /usr/local/bin/configure-vre.py
COPY configure-vre.sh /usr/local/bin/before-notebook.d/

RUN mkdir -p /opt/rucio/etc \
    && chown -R $NB_UID /opt/rucio/etc 

ENV JUPYTER_ENABLE_LAB=yes
ENV JUPYTERHUB_SINGLEUSER_APP=jupyter-server

WORKDIR $HOME
USER $NB_UID

CMD ["start-notebook.py"]
