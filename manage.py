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

parser = argparse.ArgumentParser(
        prog = 'manage.py',
        description = 'Manages admin work for every plant and field',
        epilog = """
    potato_field_manager  Copyright (C) 2022  Bailey Danyluk
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions."""
)

args = parser.parse_args()
