"""
    potato_field_manager - any and all managing of the codebases of potato_plant and potato_field
    Copyright (C) 2022  Bailey Danyluk

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
import shutil
import os
import subprocess

BW_GITHUB_PATH = 'git@github.com:BourbonWarfare/potato_{}.git'
THIS_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_SYMLINK_PATH_UNFORMATTED = 'potato/{}'

def has_requirements():
    if shutil.which('git') is None:
        return False

    return True

def is_path(potential_path):
    if os.path.isdir(potential_path):
        return potential_path
    else:
        raise NotADirectoryError(potential_path)

def link_directories(repo_path):
    try:
        is_path(repo_path)
    except:
        print('"{}" is not a valid path to symlink!'.format(repo_path))
        return

    if repo_path.endswith('/') or repo_path.endswith('\\'):
        repo_path = repo_path[:-1]

    symlink_path = os.path.join(THIS_PATH, REPO_SYMLINK_PATH_UNFORMATTED.format(os.path.basename(repo_path)))

    print('Linking "{}" to "{}"'.format(repo_path, symlink_path)) 
    os.symlink(repo_path, symlink_path)

def clone_repo(clone_path, repository):
    repo_name = "potato_" + repository
    repo_path = os.path.join(clone_path, repo_name)

    subprocess.run(['git', 'clone', BW_GITHUB_PATH.format(repository), repo_path])
    link_directories(repo_path)

def create_repo(clone_path, repository):
    print("Not implemented")

def link(args):
    link_directories(args.repositories[0])
    
def add(args):
    args.path = os.path.join(args.path, 'potato_field')

    for repo in args.repositories:
        clone_repo(args.path, repo)

if not has_requirements():
    exit()

parser = argparse.ArgumentParser(
        prog = 'setup.py',
        description = 'Manages the setup of any repository that falls under potato_field',
        epilog = """
    potato_field_manager  Copyright (C) 2022  Bailey Danyluk
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions."""
)

parser.add_argument('mode', choices=['link', 'add'], default='add', help='Whether to setup a new repository or link an existing one')
parser.add_argument('repositories', nargs='+', help='Select which repositories to clone and setup')
parser.add_argument('--path', '-p', required=False, type=is_path, default=os.path.dirname(os.path.realpath(__file__)), help='The directory where the repository will be cloned to. If not specified, repository will be cloned within the directory this tool is run')
args = parser.parse_args()

if args.mode == 'link':
    link(args)
elif args.mode == 'add':
    add(args)


