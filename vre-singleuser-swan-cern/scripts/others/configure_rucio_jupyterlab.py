#!/usr/bin/env python
# Derived from https://gitlab.cern.ch/escape-wp2/docker-images/-/blob/master/datalake-singleuser/bin/configure.py (restricted access).

import os
import json

def write_jupyterlab_config():
    config_jupyterlab = os.environ['JUPYTER_CONFIG_DIR']
    file_path = config_jupyterlab + '/jupyter_server_config.json'

    if not os.path.isfile(file_path):
        os.makedirs( config_jupyterlab + '/.jupyter/', exist_ok=True)
    else:
        config_file = open(file_path, 'r')
        config_payload = config_file.read()
        config_file.close()

    try:
        config_json = json.loads(config_payload)
    except:
        config_json = {}

    escape_config = {
        "name": os.getenv('RUCIO_NAME', 'vre-rucio.cern.ch'),
        "display_name": os.getenv('RUCIO_DISPLAY_NAME', 'ESCAPE Rucio instance'),
        "rucio_base_url": os.getenv('RUCIO_BASE_URL', 'https://vre-rucio.cern.ch'),
        "rucio_auth_url": os.getenv('RUCIO_AUTH_URL', 'https://vre-rucio-auth.cern.ch'),
        "rucio_webui_url": os.getenv('RUCIO_WEBUI_URL', 'https://vre-rucio-ui.cern.ch'),
        "rucio_ca_cert": os.getenv('RUCIO_CA_CERT', '/certs/rucio_ca.pem'),
        "site_name": os.getenv('RUCIO_SITE_NAME', 'CERN'),
        "vo": os.getenv('RUCIO_VO', 'escape'),
        "voms_enabled": os.getenv('RUCIO_VOMS_ENABLED', '0') == '1',
        "voms_vomses_path": os.getenv('RUCIO_VOMS_VOMSES_PATH', '/etc/vomses'),
        "voms_certdir_path": os.getenv('RUCIO_VOMS_CERTDIR_PATH',),
        "voms_vomsdir_path": os.getenv('RUCIO_VOMS_VOMSDIR_PATH', '/etc/grid-security/vomsdir'),
        "destination_rse": os.getenv('RUCIO_DESTINATION_RSE', 'CERN-EOSPILOT'),
        "rse_mount_path": os.getenv('RUCIO_RSE_MOUNT_PATH', '/eos/eulake'),
        "replication_rule_lifetime_days": int(os.getenv('RUCIO_REPLICATION_RULE_LIFETIME_DAYS')) if os.getenv('RUCIO_REPLICATION_RULE_LIFETIME_DAYS') else None,
        "path_begins_at": int(os.getenv('RUCIO_PATH_BEGINS_AT', '5')),
        "mode": os.getenv('RUCIO_MODE', 'replica'),
        "wildcard_enabled": os.getenv('RUCIO_WILDCARD_ENABLED', '0') == '1',
        #"oidc_auth": os.getenv('RUCIO_OIDC_AUTH'),
        #"oidc_env_name": os.getenv('RUCIO_OIDC_ENV_NAME'),
        #"oidc_file_name": os.getenv('RUCIO_OIDC_FILE_NAME'),
    }
    atlas_config = {
        "name": os.getenv('ATLAS_RUCIO_NAME', 'https://voatlasrucio-server-prod.cern.ch'),
        "display_name": os.getenv('ATLAS_RUCIO_DISPLAY_NAME', 'ATLAS RUCIO'),
        "rucio_base_url": os.getenv('ATLAS_RUCIO_BASE_URL', 'https://voatlasrucio-server-prod.cern.ch:443'),
        "rucio_auth_url": os.getenv('ATLAS_RUCIO_AUTH_URL', 'https://atlas-rucio-auth.cern.ch:443'),
        "rucio_webui_url": os.getenv('ATLAS_RUCIO_WEBUI_URL', 'https://rucio-ui.cern.ch'),
        "rucio_ca_cert": os.getenv('RUCIO_CA_CERT', '/certs/rucio_ca.pem'),
        "site_name": os.getenv('ATLAS_RUCIO_SITE_NAME', 'CERN'),
        "vo": os.getenv('ATLAS_RUCIO_VO', 'atlas'),
        "voms_enabled": os.getenv('RUCIO_VOMS_ENABLED', '0') == '1',
        "voms_vomses_path": os.getenv('RUCIO_VOMS_VOMSES_PATH', '/etc/vomses'),
        "voms_certdir_path": os.getenv('RUCIO_VOMS_CERTDIR_PATH',),
        "voms_vomsdir_path": os.getenv('RUCIO_VOMS_VOMSDIR_PATH', '/etc/grid-security/vomsdir'),
        "destination_rse": os.getenv('ATLAS_RUCIO_DESTINATION_RSE', 'CERN-PROD_PHYS-TOP'),
        "rse_mount_path": os.getenv('ATLAS_RUCIO_RSE_MOUNT_PATH', '/eos/atlas/atlasscratchdisk/rucio'),
        "replication_rule_lifetime_days": int(os.getenv('ATLAS_RUCIO_REPLICATION_RULE_LIFETIME_DAYS')) if os.getenv('ATLAS_RUCIO_REPLICATION_RULE_LIFETIME_DAYS') else None,
        "path_begins_at": int(os.getenv('ATLAS_RUCIO_PATH_BEGINS_AT', '4')),
        "mode": os.getenv('ATLAS_RUCIO_MODE', 'replica'),
        "wildcard_enabled": os.getenv('ATLAS_RUCIO_WILDCARD_ENABLED', '0') == '1',
    }
    
    # Working atlas config
    # atlas_config = {
    #     "name": "https://voatlasrucio-server-prod.cern.ch",
    #     "display_name": "ATLAS RUCIO",
    #     "rucio_base_url": "https://voatlasrucio-server-prod.cern.ch:443",
    #     "rucio_auth_url": "https://atlas-rucio-auth.cern.ch:443",
    #     "rucio_ca_cert": "/certs/rucio_ca.pem",
    #     "site_name": "CERN",
    #     "vo": "atlas",
    #     "voms_enabled": os.getenv('RUCIO_VOMS_ENABLED', '0') == '1',
    #     "destination_rse": "CERN-PROD_PHYS-TOP",
    #     "rse_mount_path": "/eos/atlas/atlasscratchdisk/rucio",
    #     "path_begins_at": 4,
    #     "mode": "replica", 
    #     "wildcard_enabled": os.getenv('RUCIO_WILDCARD_ENABLED', '0') == '0'
    # }

    escape_config = {k: v for k,
                       v in escape_config.items() if v is not None}

    atlas_config = {k: v for k,
                       v in atlas_config.items() if v is not None}                       

    config_json['RucioConfig'] = {
        'instances': [escape_config, atlas_config], # cms, 
        "default_instance": os.getenv('RUCIO_DEFAULT_INSTANCE', escape_config['name']),
        "default_auth_type": os.getenv('RUCIO_DEFAULT_AUTH_TYPE', 'x509_proxy'),
    }

    config_file = open(file_path, 'w')
    config_file.write(json.dumps(config_json, indent=2))
    config_file.close()

# def write_rucio_config():
    
#     rucio_config = configparser.ConfigParser()
    
#     client_config = {
#         'rucio_host': os.getenv('RUCIO_BASE_URL'),
#         'auth_host': os.getenv('RUCIO_AUTH_URL'),
#         'auth_type': os.getenv('RUCIO_AUTH_TYPE', 'userpass'), # it could be gss, x509_proxy, ssh
#         'username': os.getenv('RUCIO_USERNAME', 'ddmlab'),
#         'password': os.getenv('RUCIO_PASSWORD', 'secret'),
#         'ca_cert': os.getenv('RUCIO_CA_CERT'),
#         'client_cert': os.getenv('X509_USER_CERT'),
#         'client_key': os.getenv('X509_USER_KEY'),
#         'client_x509_proxy': os.getenv('X509_USER_PROXY'),
#         'ssh_private_key': os.getenv('SSH_PRIVATE_KEY', '$HOME/.ssh/id_rsa'),
#         'account': os.getenv('RUCIO_ACCOUNT', 'root'),
#         'request_retries': 3,
#         'protocol_stat_retries': 6
#     }
#     client_config = dict((k, v) for k, v in client_config.items() if v)
    
#     rucio_config['client'] = client_config
#     with open('/opt/rucio/etc/rucio.cfg', 'w') as f:
#         rucio_config.write(f)
    
if __name__ == '__main__':
    write_jupyterlab_config()
    #write_rucio_config()