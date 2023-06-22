#!/usr/bin/python3
"""
Contain a function that generates tar file of /web_static/ dir
"""
import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """Function that generates a tar of /web_static"""
    dt = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(dt)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local('tar -cvzf {} web_static'.format(file)).failed is True:
        return None
    return file
