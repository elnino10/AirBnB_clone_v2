#!/usr/bin/python3
"""
Write a Fabric script (based on the file 2-do_deploy_web_static.py) that
creates and distributes an archive to your web servers, using the function deploy
"""

from datetime import datetime
from os.path import exists

from fabric.api import env, local, put, run

env.hosts = ["3.90.83.133", "54.146.60.136"]


def do_pack():
    """function that generates a .tgz"""

    time_now = datetime.now()
    # format the file path with a .tgz extension
    archive_file = f"web_static_{time_now.strftime('%Y%m%d%H%M%S')}.tgz"
    # create local directory
    local("mkdir -p versions")
    result = local(f"tar -czvf versions/{archive_file} web_static")
    # return file path if result was successful
    if result is not None:
        return archive_file
    return None


def do_deploy(archive_path):
    """function that distributes an archive to web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        # Upload the archive to the /tmp/
        put(archive_path, "/tmp/")
        run(f"mkdir -p {path}{no_extension}/")
        # Uncompress the archive to designated folder
        run(f"tar -xzf /tmp/{file_name} -C {path}{no_extension}/")
        run(f"rm /tmp/{file_name}")
        run(f"mv {path}{no_extension}/web_static/* {path}{no_extension}/")
        run(f"rm -rf {path}{no_extension}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {path}{no_extension}/ /data/web_static/current")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def deploy():
    """
    function generates a '.tgz' and distributes archive files to web servers
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
