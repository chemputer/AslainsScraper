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

__author__ = 'Liam Edwards'
__copyright__ = 'Copyright 2019, Liam Edwards'
__credits__ = ['Liam Edwards']

__license__ = 'GNU GPL v3.0'
__version__ = '1.0.0'
__maintainer__ = 'Liam Edwards'
__email__ = 'edwardsliam77@gmail.com'
__status__ = 'Production'

version_file = os.path.join(os.environ['localappdata'], 'AslainsScraper', 'latest')
link = 'https://aslain.com/index.php?/topic/2020-0891-aslains-wows-modpack-installer-wpicture-preview/'
vpath = '//*[@id="comment-10458_wrap"]/div[2]/div[1]/p[5]/span/span/strong/text()'
dlpath = '//*[@id="comment-10458_wrap"]/div[2]/div[1]/p[6]/strong/span[2]/a/@href'


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


parser = argparse.ArgumentParser(description='Downloads the latest Aslain\'s WoWS Mod Pack')
parser.add_argument('-P', '--program', help='Which program to use to download the mod pack (default: chrome)',
                    choices=['chrome', 'firefox', 'edge', 'idm', 'other'], default='chrome')
parser.add_argument('-O', '--other', help='Specify a program to use to download the mod pack. Use the program\'s full '
                                          'path if not in the system PATH variable')
parser.add_argument('-A', '--args', help='Add other arguments when using another program. They will be called before '
                                         'the download link', dest='flags')
parser.add_argument('-F', '--force', help='Forcefully download the latest version, even if it\'s already downloaded',
                    default=False, action='store_true')
args = parser.parse_args()

create_appdata_file()

page = requests.get(link)
tree = html.fromstring(page.content)

version_release = re.sub(r'\s', '', ''.join(tree.xpath(vpath)[1:]))
print('Latest version:', version_release)
last_downloaded = get_last_download_version()
if last_downloaded == '': last_downloaded = 'No file downloaded'
print('Last downloaded:', last_downloaded)
if version_release == last_downloaded and not args.force:
    print('You already have the most recent version!')
    sys.exit(0)

dl_link = tree.xpath(dlpath)[0]

prog_paths = {
    'chrome': os.path.join(os.environ['programfiles(x86)'], 'Google', 'Chrome', 'Application', 'chrome.exe'),
    'firefox': os.path.join(os.environ['programfiles'], 'Mozilla Firefox', 'firefox.exe'),
    'idm': os.path.join(os.environ['programfiles(x86)'], 'Internet Download Manager', 'IDMan.exe')
}

if args.program == 'chrome' or args.program == 'firefox':
    call([prog_paths[args.program], dl_link])
elif args.program == 'edge':
    call(['start', 'microsoft-edge:' + dl_link], shell=True)
elif args.program == 'idm':
    call([prog_paths[args.program], '/n', '/d', dl_link])
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
