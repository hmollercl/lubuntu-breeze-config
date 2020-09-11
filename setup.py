#!/usr/bin/env python3
# coding=utf-8

# Copyright (C) 2019 Hans P. Möller <hmollercl@lubuntu.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
import subprocess
import os
from distutils.command.clean import clean


class MyClean(clean):
    def run(self):
        # Execute the classic clean command
        super().run()

        # Custom clean
        print("Removing translations")
        subprocess.run(['rm', '-rf', 'translations'])


def add_mo_files(data_files):
    app_name = 'lubuntu-breeze-config'
    mo = ''

    subprocess.run(['mkdir', 'translations/'])
    for f in os.listdir('po'):
        loc, ext = os.path.splitext(f)
        if ext == '.po':
            mo = app_name + '.mo'
            subprocess.run(['msgfmt', '-o', 'translations/' + mo,
                            'po/' + f], check=True)

            data_files.append(('share/locale/' + loc + '/LC_MESSAGES/',
                               ['translations/' + mo]))

    return data_files


data_files = [('share/applications/', ['data/breeze-config.desktop']),
              ('share/lubuntu-breeze-config/designer/',
               ['data/designer/main.ui'])]

setup(
    name="lubuntu-breeze-config",
    version="0.1.dev0",
    packages=['lubuntubreeze'],
    scripts=['breeze-config'],
    data_files=add_mo_files(data_files),
    test_suite="tests",
    cmdclass={'clean': MyClean}
)
