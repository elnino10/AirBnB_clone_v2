#!/usr/bin/python3
"""
script generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack
"""
from datetime import datetime

from fabric.api import local


def do_pack():
    """function that generates a .tgz"""

    time_now = datetime.now()
    # format the file path with a .tgz extension
    archive_file = f"web_static_{time_now.strftime('%Y%m%d%H%M%S').tgz}"
    # create local directory
    local("mkdir -p versions")
    result = local(f"tar -czvf versions/{archive_file} web_static")
    # return file path if result was successful
    if result is not None:
        return archive_file
    return None
