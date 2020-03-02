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
from argparse import ArgumentParser
from PyQt5.QtWidgets import (QWidget, QApplication, QDialogButtonBox)
from PyQt5.QtCore import (QDir, qDebug, QSettings)
from PyQt5 import uic
import gettext

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("data/designer/main.ui", self)
        self.confFile = Path(Path.home() / ".config/kdeglobals")
        self.schemeDir = "/usr/share/color-schemes/"
        self.initUI()

    def initUI(self):
        '''populate text and combobox needed with uic'''
        self.label.setText(_("Select Color Scheme for Breeze Qt Style:"))
        noteText =_("Applications need to be restarted for changes to take effect.")
        noteText += "<br/>"
        noteText += _("In case of pcmanfm-qt, since it handles the desktop, a restart of the desktop is needed")
        noteText += "<br/>"
        noteText += _("Easier, restart session.")
        noteText += "<br/>"
        noteText += _("Best results if a matching GTK Theme is selected.")

        self.note.setText('<font size="-1">' + noteText + '</font>')
        dir = QDir(self.schemeDir)
        self.files = dir.entryList(dir, dir.Files)
        self.comboBox.clear()
        self.comboBox.addItem("None")
        for f in self.files:
            settings = QSettings(self.schemeDir + f, QSettings.NativeFormat)
            self.comboBox.addItem(settings.value("ColorScheme"))
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
                    set = QSettings(self.schemeDir + f, QSettings.NativeFormat)
                    if(set.value("ColorScheme") == self.comboBox.currentText()):
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
    # app.setWindowIcon(QIcon.fromTheme("preferences-desktop-color"))
    app.exec_()


if __name__ == "__main__":
    _ = gettext.gettext
    parser = ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 0.1')
    options = parser.parse_args()
    # localesApp="software-properties"
    localesDir="/usr/share/locale"
    # gettext.bindtextdomain(localesApp, localesDir)
    # gettext.textdomain(localesApp)
    main(sys.argv)
