""" Custom commands to be added here for fbs """
from fbs.cmdline import command
from os.path import dirname
import subprocess

import fbs.cmdline
project_dir = dirname(__file__)


@command
def ui_files():
    subprocess.call([project_dir + "src/scripts/build_ui_files.sh"])

if __name__ == '__main__':
    fbs.cmdline.main(project_dir)