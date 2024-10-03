FROM jupyter/scipy-notebook:python-3.9.13
LABEL author="Image based on the work by Muhammad Aditya Hilmy - ESCAPE WP2 2020"
LABEL maintainer="VRE Team @ CERN 2024 - E. Garcia"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

RUN pip install --upgrade pip

USER $NB_UID

RUN pip install reana-client ipykernel 

USER root

RUN mkdir -p /certs
RUN mkdir -p /opt/rucio \
    && chown -R $NB_UID /opt/rucio 
RUN fix-permissions $HOME/.jupyter    

ENV JUPYTER_ENABLE_LAB=yes
# ENV JUPYTERHUB_SINGLEUSER_APP=jupyter-server

ENV JUPYTER_ENABLE_LAB=yes

WORKDIR $HOME
USER $NB_UID

CMD ["start-notebook.sh"]
