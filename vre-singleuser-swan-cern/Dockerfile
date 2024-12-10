ARG VERSION_PARENT=v0.0.27

FROM gitlab-registry.cern.ch/swan/docker-images/jupyter/swan-cern:${VERSION_PARENT}
LABEL author="E. Garcia - 2024"
LABEL maintainer="VRE Team @ CERN 23/24 - E. Garcia, G. Guerrieri. escape-cern@cern.ch"

USER root 

RUN dnf update -y \
    && dnf install -y epel-release \
    && dnf install -y gfal2* \
    && dnf clean all \
    && rm -rf /var/cache/dnf

USER ${NB_UID}

RUN python -m pip install rucio-clients

# RUN conda install -y -c conda-forge python-gfal2 \
    # && conda clean --all -f -y

RUN python -m pip install --upgrade typing_extensions

RUN python -m pip install rucio-jupyterlab==1.0.0 \
    && jupyter serverextension enable --py rucio_jupyterlab --sys-prefix

# Add pre-hooks to be run before the jupyter server starts
COPY scripts/before-notebook.d/* /usr/local/bin/before-notebook.d/
COPY scripts/others/* /srv/singleuser

USER root

# RUN dnf install voms-clients-java -y \
#     && dnf clean all && \
#     rm -rf /var/cache/dnf

RUN mkdir -p /opt/rucio/etc \
#    && touch /opt/rucio/etc/rucio.cfg \
    && fix-permissions /opt/rucio/etc \
    && chown -R ${NB_UID}:${NB_GID} /opt/rucio/etc     

# Grant script execution permissions
RUN chmod +x /usr/local/bin/before-notebook.d/*
RUN fix-permissions /srv/singleuser/configure_rucio_jupyterlab.py \
    && chown -R ${NB_UID} /srv/singleuser/configure_rucio_jupyterlab.py \
    && chmod +x /srv/singleuser/configure_rucio_jupyterlab.py

# This should not be used as we are gonna be writing on $JUPYTER_CONFIG_DIR = '/home/$USER/.jupyter'
# RUN mkdir -p $HOME/.jupyter \
#     && fix-permissions $HOME/.jupyter \
#     && chown -R ${NB_UID} $HOME/.jupyter

RUN mkdir /certs \
    && touch /certs/rucio_ca.pem \
    && curl -fsSL 'https://cafiles.cern.ch/cafiles/certificates/CERN%20Root%20Certification%20Authority%202.crt' | openssl x509 -inform DER -out /tmp/cernrootca2.crt \
    && curl -fsSL 'https://cafiles.cern.ch/cafiles/certificates/CERN%20Grid%20Certification%20Authority(1).crt' -o /tmp/cerngridca.crt \
    && curl -fsSL 'https://cafiles.cern.ch/cafiles/certificates/CERN%20Certification%20Authority.crt' -o /tmp/cernca.crt \
    && cat /tmp/cernrootca2.crt >> /certs/rucio_ca.pem \
    && cat /tmp/cerngridca.crt >> /certs/rucio_ca.pem \
    && cat /tmp/cernca.crt >> /certs/rucio_ca.pem \
    && rm /tmp/*.crt \
    && update-ca-trust

USER ${NB_UID}
