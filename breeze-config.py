#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020 Hans P. Möller <hmollercl@lubuntu.me>
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

import sys
from pathlib import Path
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QVBoxLayout,
                             QComboBox, QDialogButtonBox)
from PyQt5.QtCore import (QDir, qDebug)
from PyQt5.QtGui import QIcon
# from PyQt5 import uic
# from PyQt5 import QtX11Extras


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # uic.loadUi("designer/main.ui", self)
        self.initUI()

    def initUI(self):
        '''set UI not needed first part if uic is used'''
        self.label = QLabel()
        self.comboBox = QComboBox()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Apply
                                          | QDialogButtonBox.Cancel)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.comboBox)
        vbox.addWidget(self.buttonBox)
        self.label.setText("Select Color Scheme")
        self.setLayout(vbox)
        self.setWindowTitle("Lubuntu Breeze Config")

        '''populate combobox needed with uic'''
        dir = QDir("/usr/share/color-schemes/")
        files = dir.entryList(dir, dir.Files)
        self.comboBox.clear()
        self.comboBox.addItem("None")
        for f in files:
            self.comboBox.addItem(f.split(".")[0])
        self.comboBox.setCurrentText(self.checkCurrent())

        self.center()

    def center(self):
        '''centers UI'''
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def checkCurrent(self):
        '''check current used theme'''
        confFile = Path(str(Path.home()) + "/.config/kdeglobals")
        if confFile.is_file():
            qDebug("exist: " + str(confFile))
            with open(str(confFile)) as f:
                for line in f:
                    item = line.split("=")
                    if item[0] == "ColorScheme":
                        current = item[1].replace("\n", "")  # remove \n
                        current = current.replace(" ", "")  # remove spaces
                        qDebug("current scheme: " + current)
                        return(current)
                qDebug("No Color Scheme found on file")
                return("None")
        else:
            qDebug(str(confFile) + "wasn't found")
            return("None")

    def apply(self):
        '''copy selected color-scheme to kdeglobals'''


class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.main.show()


def main(args):
    global app
    app = App(args)
    app.setWindowIcon(QIcon.fromTheme("preferences-desktop-color"))
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
