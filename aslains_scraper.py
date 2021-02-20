#!/usr/bin/env python
"""Automatically downloads the latest version of Aslain's Mod Pack for World of Warships.

Contains options for different programs to download, including Chrome, Firefox, Edge, and IDM. Also includes an option
for the user to specify another program.
"""

from collections.abc import Iterable
from lxml import html
from subprocess import call
import argparse
import os
import re
import requests
import sys

########################################################
## Original Code Credits & Information -- code has been updated since then.
''' 
__author__ = 'Liam Edwards'
__copyright__ = 'Copyright 2019, Liam Edwards'
__credits__ = ['Liam Edwards']

__license__ = 'GNU GPL v3.0'
__version__ = '1.0.1'
__maintainer__ = 'Liam Edwards'
__email__ = 'edwardsliam77@gmail.com'
__status__ = 'Production' '''
#########################################################

#########################################################
## Current Code Credits & Info for fork
__author__ = 'Chemputer'
__version__ = "1.3.0"
__maintainer__ = 'Chemputer'
__status__ = '\"Production\"'
__credits__ = ['Liam Edwards', 'Chemputer']
#########################################################


version_file = os.path.join(os.environ['localappdata'], 'AslainsScraper', 'latest')
link = 'https://aslain.com/index.php?/topic/2020-download-%E2%98%85-world-of-warships-%E2%98%85-modpack/'
vpath = '//*[@id="comment-10458_wrap"]/div[2]/div[1]/p[6]/span[2]/span/strong/text()'
adflypath = '//*[@id="comment-10458_wrap"]/div[2]/div[1]/p[9]/a/@href'
dlpath = '//*[@id="comment-10458_wrap"]/div[2]/div[1]/p[9]/span/a/@href'


def create_appdata_file():
    os.makedirs(os.path.dirname(version_file), exist_ok=True)
    if not os.path.exists(version_file):
        with open(version_file, 'w') as f:
            f.write('')


def get_last_download_version():
    with open(version_file, 'r') as f:
        return f.read()


def write_new_version(v):
    with open(version_file, 'w') as f:
        f.write(v)


def flatten(coll):
    for i in coll:
        if isinstance(i, Iterable) and not isinstance(i, str):
            yield from flatten(i)
        else:
            yield i


def run_latest_version(download_location, last_version):
    file = os.path.join(download_location, 'Aslains_WoWs_Modpack_Installer_'
                        + last_version.replace('#', '_').replace('v', 'v.') + '.exe')
    os.system(file)


parser = argparse.ArgumentParser(description='Downloads the latest Aslain\'s WoWS Mod Pack')
parser.add_argument('-P', '--program', help='Which program to use to download the mod pack (default: chrome)',
                    choices=['chrome', 'firefox', 'edge', 'idm', 'wget', 'other'], default='chrome')
parser.add_argument('-O', '--other', help='Specify a program to use to download the mod pack. Use the program\'s full '
                                          'path if not in the system PATH variable')
parser.add_argument('-A', '--args', help='Add other arguments when using another program. They will be called before '
                                         'the download link', dest='flags')
parser.add_argument('-D', '--downloaded', help='If the latest version has already been downloaded, run it. Specify the'
                                               ' download location (defaults to Windows Downloads folder)',
                    const=os.path.join('C:', os.environ['homepath'], 'Downloads'), nargs='?', dest='path')
parser.add_argument('-S', '--adfly', help='Use the ad.fly link to support Aslain. Does not work with IDM',
                    default=False, action='store_true')
parser.add_argument('-F', '--force', help='Forcefully download the latest version, even if it\'s already downloaded',
                    default=False, action='store_true')
parser.add_argument('-V', '--version', help='Doesn\'t download the mod pack. Just compare local version against latest',
                    default=False, action='store_true')
args = parser.parse_args()

create_appdata_file()

page = requests.get(link)
tree = html.fromstring(page.content)

version_release = re.sub(r'\s', '', ''.join(tree.xpath(vpath)[0][1:]))
print('Latest version:', version_release)
last_downloaded = get_last_download_version()
if last_downloaded == '': last_downloaded = 'No file downloaded'
print('Last downloaded:', last_downloaded)
if args.version:
    if version_release == last_downloaded:
        print('You are up to date')
    else:
        print('You are not up to date')
    sys.exit(0)
if version_release == last_downloaded and not args.force:
    print('You already have the most recent version!')
    if args.path is not None:
        print('Running the latest version now!')
        run_latest_version(args.path, last_downloaded)
    sys.exit(0)
if args.adfly and args.program == 'idm':
    print('Adfly links and IDM are not compatible with each other')
    sys.exit(2)

dl_link = tree.xpath(adflypath)[0] if args.adfly else tree.xpath(dlpath)[0]

prog_paths = {
    'chrome': os.path.join(os.environ['programfiles(x86)'], 'Google', 'Chrome', 'Application', 'chrome.exe'),
    'firefox': os.path.join(os.environ['programfiles'], 'Mozilla Firefox', 'firefox.exe'),
}

if args.program == 'chrome' or args.program == 'firefox':
    call([prog_paths[args.program], dl_link])
elif args.program == 'edge':
    call(['start', 'microsoft-edge:' + dl_link], shell=True)
elif args.program == 'idm':
    call(['idm', dl_link], shell=True)
elif args.program == "wget":
    call(['wget', dl_link], shell=True)
elif args.program == 'other':
    if args.other is None:
        print('Invalid syntax! Please specify what program you want to use by using --other')
        sys.exit(2)
    else:
        if args.flags is None:
            call([args.other, dl_link])
        else:
            call(list(flatten([args.other, args.flags.split(), dl_link])))

write_new_version(version_release)
