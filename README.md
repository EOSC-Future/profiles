[![Docker automatic build and publish](https://github.com/vre-hub/environments/actions/workflows/env-build.yaml/badge.svg?branch=main)](https://github.com/vre-hub/environments/actions/workflows/env-build.yaml)

# Environments

VRE related and user environment images for workflows and notebooks.

## VRE user environments

We strongly recommend that every user enviroment image uses the latests `vre-singleuser` image as a base layer (the `FROM` command in the `Dockerfile`). For example:
```Dockerfile
FROM ghcr.io/vre-hub/vre-singleuser:sha-423e01a
```
or 
```Dockerfile
FROM ghcr.io/vre-hub/vre-singleuser-py38:sha-7ed7d80
```
  - It is advisable to use the `:sha-<SHA>` tagging rather than the `:latest` one.
    - Check the latest version of the `vre-singleuser` image [here](https://github.com/vre-hub/environments/pkgs/container/vre-singleuser).
    - And the latest version of the `vre-singleuser-py38` image [here](https://github.com/vre-hub/environments/pkgs/container/vre-singleuser-py38).

Within your PR: 
 - Add a folder per environments, the directory needs to contain a valid `Dockerfile`. Once your PR is merged, the CI will detect the changes in the repository and will trigger the building of the image.
 - Add a `README.md` file describing the environment and its usage.
 - We strongly recommend to add the following lines to any new user environment (thus in a `Dockerfile`)
 
```Dockerfile
# After the `FROM` and any other `LABEL` commands
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE
```
  - The above lines will "label" the image with the time it was build by the CI.
