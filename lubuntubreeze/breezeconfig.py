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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess
import sys
from pathlib import Path
from shutil import copyfile
from PyQt5.QtWidgets import (QWidget, QApplication, QDialogButtonBox)
from PyQt5.QtCore import (QDir, qDebug, QSettings)
from PyQt5 import uic
from gettext import gettext as _


class MainWindow(QWidget):
    def __init__(self, options=None):
        QWidget.__init__(self)
        if options is not None:
            self.datadir = options.datadir
            self.bindir = options.bindir
        else:
            self.datadir = '/usr/share/lubuntu-breeze-config'
            self.bindir = '/bin'
        uic.loadUi("%s/designer/main.ui" % self.datadir, self)
        self.confFile = Path(Path.home() / ".config/kdeglobals")
        self.schemeDir = "/usr/share/color-schemes/"
        self.rcFile = Path(Path.home() / ".config/breezerc")
        self.menuOpacity = 99
        self.initUI()

    def initUI(self):
        '''populate text and combobox needed with uic'''
        self.label.setText(_("Select Color Scheme for Breeze Qt Style:"))
        self.label2.setText(_("Menu Transparency"))
        self.label3a.setText(_("Transparent"))
        self.label3b.setText(_("Opaque"))
        t = _("Applications need to be restarted for changes to take effect.")
        t += "<br/>"
        t += _("In case of pcmanfm-qt, since it handles the desktop, ")
        t += _("a restart of the desktop is needed") + "<br/>"
        t += _("Easier, restart session.")
        t += "<br/>"
        t += _("Best results if a matching GTK Theme is selected.")
        t += "<br/>"
        t += _("Compton (or other compositor) needs to be enabled ")
        t += _("for transparency.")

        self.note.setText('<font size="-1">' + t + '</font>')
        sDir = QDir(self.schemeDir)
        self.files = sDir.entryList(sDir, sDir.Files)
        self.comboBox.clear()
        self.comboBox.addItem(_("None"))
        for f in self.files:
            settings = QSettings(self.schemeDir + f, QSettings.NativeFormat)
            self.comboBox.addItem(settings.value("ColorScheme"))
        self.comboBox.setCurrentText(self.checkCurrent())
        self.horizontalSlider.setValue(self.checkTransparency())
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

    def checkTransparency(self):
        '''check current transparency'''
        if self.rcFile.is_file():
            qDebug("exist: " + str(self.rcFile))
            settings = QSettings(str(self.rcFile), QSettings.NativeFormat)
            settings.beginGroup("Style")
            actual = settings.value("MenuOpacity")
            qDebug(actual)
            try:
                actual = int(actual)
            except ValueError:
                actual = 99
            qDebug(str(actual))
            return actual
        else:
            qDebug(str(self.rcFile) + " wasn't found")
            return 99

    def btnClk(self, btn):
        '''copy selected color-scheme to kdeglobals or close'''
        if btn == self.buttonBox.button(QDialogButtonBox.Apply):
            qDebug("apply")
            if self.comboBox.currentText() != "None":
                for f in self.files:
                    s = QSettings(self.schemeDir + f, QSettings.NativeFormat)
                    if(s.value("ColorScheme") == self.comboBox.currentText()):
                        copyfile(self.schemeDir + f, self.confFile)
            else:
                os.remove(self.confFile)
            if self.horizontalSlider.value != self.checkTransparency():
                settings = QSettings(str(self.rcFile), QSettings.NativeFormat)
                settings.beginGroup("Style")
                settings.setValue("MenuOpacity", self.horizontalSlider.value())

            filename = self.bindir + '/breeze-config'
            print(filename)
            # subprocess.Popen(filename)
            subprocess.Popen([filename, '--data-dir', self.datadir,
                              '--bin-dir', self.bindir])
            sys.exit(0)

        elif btn == self.buttonBox.button(QDialogButtonBox.Close):
            exit(0)


class App(QApplication):
    def __init__(self, options, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow(options)
        self.main.show()


def main(args, options):
    global app
    app = App(options, args)
    app.exec_()
