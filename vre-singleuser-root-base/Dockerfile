FROM quay.io/jupyter/scipy-notebook:python-3.11
LABEL author="ESCAPE WP2 2024"
LABEL maintainer="VRE Team @ CERN 2024 - E. Garcia, G. Guerrieri"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

USER root

ENV LANG=C.UTF-8

ARG ROOT_BIN=root_v6.32.04.Linux-ubuntu24.04-x86_64-gcc13.2.tar.gz

WORKDIR /opt

COPY packages packages

RUN apt-get update -qq \
 && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
 && apt-get -y install rsync $(cat packages) wget\
 && rm -rf /var/lib/apt/lists/*\
 && wget https://root.cern/download/${ROOT_BIN} \
 && tar -xzvf ${ROOT_BIN} \
 && rm -f ${ROOT_BIN} \
 && echo /opt/root/lib >> /etc/ld.so.conf \
 && ldconfig

# Skip the post-start hook in the base image (https://github.com/vre-hub/vre/pull/299)
ENV SKIP_POSTSTART_HOOK true 

# Install ROOT
ENV ROOTSYS /opt/root
ENV PATH $ROOTSYS/bin:$PATH
ENV PYTHONPATH $ROOTSYS/lib:$PYTHONPATH
ENV CLING_STANDARD_PCH none


WORKDIR $HOME
USER $NB_UID

CMD ["start-notebook.sh"]