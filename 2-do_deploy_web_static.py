#!/usr/bin/python3
"""
script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from os.path import exists

from fabric.api import env, put, run

env.hosts = ["3.90.83.133", "54.146.60.136"]


def do_deploy(archive_path):
    """function that distributes an archive to web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run(f"mkdir -p {path}{no_extension}/")
        run(f"tar -xzf /tmp/{file_name} -C {path}{no_extension}/")
        run(f"rm /tmp/{file_name}")
        run(f"mv {path}{no_extension}/web_static/* {path}{no_extension}/")
        run(f"rm -rf {path}{no_extension}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {path}{no_extension}/ /data/web_static/current")
        return True
    except:
        return False
