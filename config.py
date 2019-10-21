import configparser, os, sys
from pathlib import Path

_DEFAULT_CONFIG = "/etc/kattis/submit/kattisrc"

_CONFIG_NOT_FOUND_MSG = """\
I failed to read in a config file from your home directory or from the
same directory as this script. Please go to your Kattis installation
to download a .kattisrc file.

The file should look something like this:
[user]
username: yourusername
token: *********

[kattis]
loginurl: https://<kattis>/login
submissionurl: https://<kattis>/submit"""


def getConfig():
    cfg = configparser.ConfigParser()

    if os.path.exists(_DEFAULT_CONFIG):
        cfg.read(_DEFAULT_CONFIG)

    alternativeLocations = [
        os.path.join(str(Path.home()), ".kattisrc"),
        os.path.join(os.path.dirname(sys.argv[0]), ".kattisrc"),
    ]

    if not cfg.read(alternativeLocations):
        print(_CONFIG_NOT_FOUND_MSG)
        return -1

    return cfg
