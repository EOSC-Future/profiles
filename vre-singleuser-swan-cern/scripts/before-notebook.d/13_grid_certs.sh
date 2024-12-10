#!/bin/bash

if [[ -d /cvmfs/grid.cern.ch ]]
then
    ln -s /cvmfs/grid.cern.ch/etc/grid-security/certificates /etc/grid-security/certificates
    ln -s /cvmfs/grid.cern.ch/etc/grid-security/vomsdir /etc/grid-security/vomsdir
fi