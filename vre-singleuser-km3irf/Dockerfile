FROM ghcr.io/vre-hub/vre-singleuser:sha-423e01a
LABEL author="Mikhail Smirnov"
LABEL maintainer="VRE Team @ CERN 22/23 - E. Garcia, E. Gazzarrini, D. Gosein"
LABEL org.opencontainers.image.source https://github.com/vre-hub/environments
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

# WORKDIR $HOME
USER $NB_UID

RUN pip install -U pip \
    && pip install gammapy==1.1 \
    && pip install km3net-testdata km3irf
