#!/usr/bin/python3
"""
Contain a function that deploys web_static to ubuntu servers.
"""
import os.path
from fabric.api import *
from datetime import datetime
from fabric.contrib import files


env.hosts = ["3.209.12.133", "18.208.159.16"]


@runs_once
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


def do_deploy(archive_path):
    """Deploys webstatic to all my ubuntu servers"""
    if os.path.isfile(archive_path) is True:
        put('{}'.format(archive_path), '/tmp/')
        archive_split = archive_path.split('.')
        archive_name_split = archive_split[0].split("/")
        arc_name = archive_name_split[1]
        data_path = "/data/web_static/releases/{}".format(arc_name)
        path_web = "/data/web_static/releases/{}/web_static/*".format(arc_name)
        if files.exists(data_path) is False:
            run('mkdir {}'.format(data_path))
        run('tar -xvzf /tmp/{}.tgz -C {}'.format(arc_name, data_path))
        run('mv {} {}'.format(path_web, data_path))
        run('rm /tmp/{}.tgz'.format(arc_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(data_path))
        return True
    else:
        return False


def deploy():
    """Creates and deploys archives to my web servers"""
    archive_name = do_pack()

    if archive_name is None:
        return False
    return do_deploy(archive_name)
