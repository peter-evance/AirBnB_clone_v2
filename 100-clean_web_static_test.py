#!/usr/bin/python3
"""
Contain a function that deploys web_static to ubuntu servers.
"""
import os.path
from fabric.api import *
from datetime import datetime
from fabric.contrib import files


env.hosts = ["3.209.12.133", "18.208.159.16"]


def do_clean(number=0):
    """Deletes out of date archives from my local directory and servers"""
    number = int(number)
    if number == 0:
        number = 1
    fl_l = local("ls -t versions/* | awk 'NR>{}'".format(number), capture=True)
    fl_r = run("ls -t /data/w*/r*/ | awk 'NR>{}'".format(number))
    if fl_l:
        local("rm `ls -t versions/* | awk 'NR>{}'`".format(number))
    if fl_r:
        run("rm -rf `ls -dt /data/w*/r*/* | awk 'NR>{}'`".format(number))
