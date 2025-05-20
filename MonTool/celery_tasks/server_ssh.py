import paramiko
import logging
from queue import Queue

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MonTool.settings')

logger = logging.getLogger("celery")


def get_conn(host, username, password):
    """
    Establish connection to the server over SSH
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    return ssh
