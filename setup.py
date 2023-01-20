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
import os
import shutil
import subprocess
import sys


BW_GITHUB_PATH = 'git@github.com:BourbonWarfare/potato_{}.git'
THIS_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_SYMLINK_PATH_UNFORMATTED = 'potato/{}'


def missing_requirements():
    '''Returns a list of missing requirements; the empty list is returned
    if all requirements are satisfied.'''

    reqs = ['git']

    res = []
    for req in reqs:
        if shutil.which(req) is None:
            res.append(req)
    return res


def is_path(potential_path):
    if os.path.isdir(potential_path):
        return potential_path

    raise NotADirectoryError(potential_path)


def link_directories(repo_path):
    try:
        is_path(repo_path)
    except NotADirectoryError:
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

    try:
        subprocess.run(['git', 'clone', BW_GITHUB_PATH.format(repository), repo_path],
                       check=False)
        link_directories(repo_path)
    except Exception as e:
        print("Error cloning {} to {}: {}!".format(
            BW_GITHUB_PATH.format(repository), repo_path, e))


def create_repo(clone_path, repository):
    print("Not implemented")


def link(args):
    link_directories(args.repositories[0])


def add(args):
    args.path = os.path.join(args.path, 'potato_field')

    for repo in args.repositories:
        if args.new:
            create_repo(args.path, repo)
        else:
            clone_repo(args.path, repo)


def main():
    missing = missing_requirements()
    if len(missing) > 0:
        print("The following requirements are missing:", missing)
        print("Exiting...")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        prog='setup.py',
        description='Manages the setup of any repository that falls under potato_field',
        epilog="""
        potato_field_manager  Copyright (C) 2022  Bailey Danyluk
        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions."""
    )

    parser.add_argument(
        'mode',
        choices=['link', 'add'],
        default='add',
        help='Whether to setup a new repository or link an existing one')
    parser.add_argument('repositories',
                        nargs='+',
                        help='Select which repositories to clone and setup')
    parser.add_argument('--path', '-p',
                        nargs=1,
                        required=False,
                        type=is_path,
                        default=os.path.dirname(os.path.realpath(__file__)),
                        help='The directory where the repository will be cloned to. If not \
                        specified, repository will be cloned within the directory this tool is run')
    parser.add_argument('--new',
                        required=False,
                        default=False,
                        help='Create the repository instead of cloning an existing repository')
    args = parser.parse_args()

    if args.mode == 'link':
        link(args)
    elif args.mode == 'add':
        add(args)


if __name__ == '__main__':
    main()
