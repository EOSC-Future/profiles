#!/usr/bin/env python
# Derived from https://gitlab.cern.ch/escape-wp2/docker-images/-/blob/master/datalake-singleuser/bin/configure.py (restricted access).

import os
import json
import configparser

HOME = '/home/jovyan'

def write_jupyterlab_config():
    file_path = HOME + '/.jupyter/jupyter_notebook_config.json'
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

    instance_config = {
        "name": os.getenv('RUCIO_NAME', "default"),
        "display_name": os.getenv('RUCIO_DISPLAY_NAME', "Default Instance"),
        "rucio_base_url": os.getenv('RUCIO_BASE_URL'),
        "rucio_auth_url": os.getenv('RUCIO_AUTH_URL'),
        "rucio_webui_url": os.getenv('RUCIO_WEBUI_URL'),
        "rucio_ca_cert": os.getenv('RUCIO_CA_CERT'),
        "site_name": os.getenv('RUCIO_SITE_NAME'),
        "vo": os.getenv('RUCIO_VO'),
        "voms_enabled": os.getenv('RUCIO_VOMS_ENABLED', '0') == '1',
        "voms_vomses_path": os.getenv('RUCIO_VOMS_VOMSES_PATH'),
        "voms_certdir_path": os.getenv('RUCIO_VOMS_CERTDIR_PATH'),
        "voms_vomsdir_path": os.getenv('RUCIO_VOMS_VOMSDIR_PATH'),
        "destination_rse": os.getenv('RUCIO_DESTINATION_RSE'),
        "rse_mount_path": os.getenv('RUCIO_RSE_MOUNT_PATH'),
        "replication_rule_lifetime_days": int(os.getenv('RUCIO_REPLICATION_RULE_LIFETIME_DAYS')) if os.getenv('RUCIO_REPLICATION_RULE_LIFETIME_DAYS') else None,
        "path_begins_at": int(os.getenv('RUCIO_PATH_BEGINS_AT', '0')),
        "mode": os.getenv('RUCIO_MODE', 'replica'),
        "wildcard_enabled": os.getenv('RUCIO_WILDCARD_ENABLED', '0') == '1',
        "oidc_auth": os.getenv('RUCIO_OIDC_AUTH'),
        "oidc_env_name": os.getenv('RUCIO_OIDC_ENV_NAME'),
        "oidc_file_name": os.getenv('RUCIO_OIDC_FILE_NAME'),
    }

    instance_config = {k: v for k,
                       v in instance_config.items() if v is not None}
    config_json['RucioConfig'] = {
        'instances': [instance_config],
        "default_instance": os.getenv('RUCIO_DEFAULT_INSTANCE'),
        "default_auth_type": os.getenv('RUCIO_DEFAULT_AUTH_TYPE'),
    }

    config_file = open(file_path, 'w')
    config_file.write(json.dumps(config_json, indent=2))
    config_file.close()

def write_rucio_config():
    
    rucio_config = configparser.ConfigParser()
    
    client_config = {
        'rucio_host': os.getenv('RUCIO_BASE_URL', 'https://rucio-intertwin-testbed.desy.de'),
        'auth_host': os.getenv('RUCIO_AUTH_URL', 'https://rucio-intertwin-testbed-auth.desy.de'),
        'ca_cert': os.getenv('RUCIO_CA_CERT', '/opt/conda/lib/python3.9/site-packages/certifi/cacert.pem'),
        'auth_type': os.getenv('RUCIO_AUTH_TYPE', 'oidc'), # 'x509' or 'oidc'
        'account': os.getenv('RUCIO_ACCOUNT', '$RUCIO_ACCOUNT'), # This is the RUCIO account name, need to be mapped from idp
        'oidc_polling': 'true',
        'oidc_scope': 'openid profile offline_access eduperson_entitlement',
        #'username': os.getenv('RUCIO_USERNAME', ''),
        #'password': os.getenv('RUCIO_PASSWORD', ''),
        'auth_token_file_path': '/tmp/rucio_egi.token',
        'request_retries': 3,
        'protocol_stat_retries': 6
    }
    client_config = dict((k, v) for k, v in client_config.items() if v)
    rucio_config['client'] = client_config
    
    with open('/opt/rucio/etc/rucio.cfg', 'w') as f:
        rucio_config.write(f)    
    
if __name__ == '__main__':
    write_jupyterlab_config()
    write_rucio_config()