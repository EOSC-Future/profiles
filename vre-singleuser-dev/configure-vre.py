#!/usr/bin/env python
# Derived from https://gitlab.cern.ch/escape-wp2/docker-images/-/blob/master/datalake-singleuser/bin/configure.py (restricted access).

import os
import json

HOME = '/home/jovyan'

def write_jupyterlab_config():
    file_path = HOME + '/.jupyter/jupyter_server_config.json'
    if not os.path.isfile(file_path):
        os.makedirs(HOME + '/.jupyter/', exist_ok=True)
    else:
        config_file = open(file_path, 'r')
        config_payload = config_file.read()
        config_file.close()

    try:
        config_json = json.loads(config_payload)
    except:
        config_json = {}


# Looking to the rucio-jupyterlab configuration; https://github.com/rucio/jupyterlab-extension/blob/master/rucio_jupyterlab/config/schema.py#L101
#  either ("destination_rse", "rse_mount_path") either ("rucio_ca_cert") are required env vars, even if they are defined in the jhub manifest.
# Adding 'rucio_base_url' too - from debugging experience

    escape_config = {
        "name": os.getenv('RUCIO_NAME', 'default'),
        "display_name": os.getenv('RUCIO_DISPLAY_NAME', 'Default Instance'),
        "rucio_base_url": os.getenv('RUCIO_BASE_URL', 'DEFAULT rucio base url'),
        "rucio_auth_url": os.getenv('RUCIO_AUTH_URL'),
        "rucio_webui_url": os.getenv('RUCIO_WEBUI_URL'),
        "rucio_ca_cert": os.getenv('RUCIO_CA_CERT'),
        "site_name": os.getenv('RUCIO_SITE_NAME'),
        "vo": os.getenv('RUCIO_VO'),
        "voms_enabled": os.getenv('RUCIO_VOMS_ENABLED', '0') == '1',
        "voms_vomses_path": os.getenv('RUCIO_VOMS_VOMSES_PATH'),
        "voms_certdir_path": os.getenv('RUCIO_VOMS_CERTDIR_PATH'),
        "voms_vomsdir_path": os.getenv('RUCIO_VOMS_VOMSDIR_PATH'),
        "destination_rse": os.getenv('RUCIO_DESTINATION_RSE', 'DEFAULT rse destination'),
        "rse_mount_path": os.getenv('RUCIO_RSE_MOUNT_PATH', 'DEFAULT rse mount path'),
        "replication_rule_lifetime_days": int(os.getenv('RUCIO_REPLICATION_RULE_LIFETIME_DAYS')) if os.getenv('RUCIO_REPLICATION_RULE_LIFETIME_DAYS') else None,
        "path_begins_at": int(os.getenv('RUCIO_PATH_BEGINS_AT', '0')),
        "mode": os.getenv('RUCIO_MODE', 'replica'),
        "wildcard_enabled": os.getenv('RUCIO_WILDCARD_ENABLED', '0') == '1',
        "oidc_auth": os.getenv('RUCIO_OIDC_AUTH'),
        "oidc_env_name": os.getenv('RUCIO_OIDC_ENV_NAME'),
        "oidc_file_name": os.getenv('RUCIO_OIDC_FILE_NAME'),
    }

    atlas_config = {
        "name": "https://voatlasrucio-server-prod.cern.ch",
        "display_name": "ATLAS RUCIO",
        "rucio_base_url": "https://voatlasrucio-server-prod.cern.ch:443",
        "rucio_auth_url": "https://atlas-rucio-auth.cern.ch:443",
        "rucio_ca_cert": "/certs/rucio_ca.pem",
        "site_name": "CERN",
        "vo": "atlas",
        "voms_enabled": os.getenv('RUCIO_VOMS_ENABLED', '0') == '1',
        "destination_rse": "CERN-PROD_PHYS-TOP",
        "rse_mount_path": "/eos/atlas/atlasscratchdisk/rucio",
        "path_begins_at": 4,
        "mode": "replica", 
        "wildcard_enabled": os.getenv('RUCIO_WILDCARD_ENABLED', '0') == '0'
      }

    escape_config = {k: v for k,
                    v in escape_config.items() if v is not None}

    atlas_config = {k: v for k,
                    v in atlas_config.items() if v is not None}


    config_json['RucioConfig'] = {
        'instances': [escape_config, atlas_config],
        "default_instance": os.getenv('RUCIO_DEFAULT_INSTANCE', escape_config['name']),
        "default_auth_type": os.getenv('RUCIO_DEFAULT_AUTH_TYPE', 'oidc'),
    }

    config_file = open(file_path, 'w')
    config_file.write(json.dumps(config_json, indent=2))
    config_file.close()

def write_ipython_config():
    file_path = HOME + '/.ipython/profile_default/ipython_kernel_config.json'
    extension_module = 'rucio_jupyterlab.kernels.ipython'

    if not os.path.isfile(file_path):
        os.makedirs(HOME + '/.ipython/profile_default/', exist_ok=True)
    else:
        config_file = open(file_path, 'r')
        config_payload = config_file.read()
        config_file.close()

    try:
        config_json = json.loads(config_payload)
    except:
        config_json = {}

    if 'IPKernelApp' not in config_json:
        config_json['IPKernelApp'] = {}

    ipkernel_app = config_json['IPKernelApp']

    if 'extensions' not in ipkernel_app:
        ipkernel_app['extensions'] = []

    if extension_module not in ipkernel_app['extensions']:
        ipkernel_app['extensions'].append(extension_module)

    config_file = open(file_path, 'w')
    config_file.write(json.dumps(config_json, indent=2))
    config_file.close()    
    
if __name__ == '__main__':
    write_jupyterlab_config()
    write_ipython_config()
