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

import os
import sys
from pathlib import Path
from shutil import copyfile
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QVBoxLayout,
                             QComboBox, QDialogButtonBox)
from PyQt5.QtCore import (QDir, qDebug, QSettings)
from PyQt5.QtGui import QIcon
# from PyQt5 import uic
# from PyQt5 import QtX11Extras


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # uic.loadUi("designer/main.ui", self)
        self.confFile = Path(Path.home() / ".config/kdeglobals")
        self.schemeDir = "/usr/share/color-schemes/"
        self.initUI()

    def initUI(self):
        '''set UI not needed first part if uic is used'''
        self.label = QLabel()
        self.note = QLabel()
        self.comboBox = QComboBox()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Apply
                                          | QDialogButtonBox.Close)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.comboBox)
        vbox.addWidget(self.note)
        vbox.addWidget(self.buttonBox)
        self.label.setText("Select Color Scheme for Breeze Qt Style:")
        noteText = '''
        <font size="-1">
        Applications need to be restarted for changes to take effect.<br/>
        In case of pcmanfm-qt, since it handles the desktop,<br/>
        a restart of the desktop is needed.<br/>
        Easier, restart session.<br/>
        Best results if a matching GTK Theme is selected.
        </font>
        '''
        self.note.setText(noteText)
        self.setLayout(vbox)
        self.setWindowTitle("Lubuntu Breeze Config")

        '''populate combobox needed with uic'''
        dir = QDir(self.schemeDir)
        self.files = dir.entryList(dir, dir.Files)
        self.comboBox.clear()
        self.comboBox.addItem("None")
        for f in self.files:
            settings = QSettings(self.schemeDir + f, QSettings.NativeFormat)
            set = settings.value("ColorScheme")
            self.comboBox.addItem(set)
        self.comboBox.setCurrentText(self.checkCurrent())

        self.buttonBox.clicked.connect(self.btnClk)

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
        if self.confFile.is_file():
            qDebug("exist: " + str(self.confFile))
            settings = QSettings(str(self.confFile), QSettings.NativeFormat)
            set = settings.value("ColorScheme")
            qDebug(set)
            if set != "":
                return(set)
            else:
                return("None")
        else:
            qDebug(str(self.confFile) + " wasn't found")
            return("None")

    def btnClk(self, btn):
        '''copy selected color-scheme to kdeglobals or close'''
        if btn == self.buttonBox.button(QDialogButtonBox.Apply):
            qDebug("apply")
            if self.comboBox.currentText() != "None":
                for f in self.files:
                    settings = QSettings(self.schemeDir + f, QSettings.NativeFormat)
                    set = settings.value("ColorScheme")
                    if(set == self.comboBox.currentText()):
                        copyfile(self.schemeDir + f, self.confFile)
            else:
                os.remove(self.confFile)
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

        elif btn == self.buttonBox.button(QDialogButtonBox.Close):
            exit(0)


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
