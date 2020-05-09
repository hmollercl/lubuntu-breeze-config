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
from PyQt5.QtGui import (QPalette, QColor)
from PyQt5 import uic
from gettext import gettext as _  # better than in main "_ = gettext.gettext" for testing


class MainWindow(QWidget):
    def __init__(self, options = None):
        QWidget.__init__(self)
        if options is not None:
            self.datadir = options.datadir
            self.scriptdir = options.scriptdir
            self.restart = options.restart
        else:
            self.datadir = 'data'
            self.scriptdir = ''
        uic.loadUi("%s/designer/main.ui" % self.datadir, self)
        self.confFile = Path(Path.home() / ".config/kdeglobals")
        self.schemeDir = "/usr/share/color-schemes/"
        self.initUI()

    def initUI(self):
        '''populate text and combobox needed with uic'''
        self.label.setText(_("Select Color Scheme for Breeze Qt Style:"))
        noteText =_("Applications need to be restarted for changes to take effect.")
        noteText += "<br/>"
        noteText += _("In case of pcmanfm-qt, since it handles the desktop, ")
        noteText += _("a restart of the desktop is needed") + "<br/>"
        noteText += _("Easier, restart session.")
        noteText += "<br/>"
        noteText += _("Best results if a matching GTK Theme is selected.")

        self.note.setText('<font size="-1">' + noteText + '</font>')
        dir = QDir(self.schemeDir)
        self.files = dir.entryList(dir, dir.Files)
        self.comboBox.clear()
        self.comboBox.addItem(_("None"))
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

    def getColor(self, data):
        if type(data) is list:
            color = QColor(int(data[0]), int(data[1]), int(data[2]))
        return(color)

    def updateWindow(self, selected):
        if self.restart == 1:
            filename = self.scriptdir + '/breeze-color'
            print(filename)
            subprocess.Popen(filename)
            sys.exit(0)

        else:
            nSettings = QSettings(selected, QSettings.NativeFormat)
            nPalette = QPalette(app.style().standardPalette())

            nSettings.beginGroup("Colors:Window")
            color = self.getColor(nSettings.value("BackgroundNormal"))
            nPalette.setColor(QPalette.Window, color)
            color = self.getColor(nSettings.value("ForegroundNormal"))
            nPalette.setColor(QPalette.WindowText, color)
            color = self.getColor(nSettings.value("ForegroundLink"))
            nPalette.setColor(QPalette.Link, color)
            nSettings.endGroup()

            nSettings.beginGroup("Colors:View")
            color = self.getColor(nSettings.value("BackgroundNormal"))
            nPalette.setColor(QPalette.Base, color)
            color = self.getColor(nSettings.value("ForegroundNormal"))
            nPalette.setColor(QPalette.Text, color)
            nSettings.endGroup()

            nSettings.beginGroup("Colors:Button")
            color = self.getColor(nSettings.value("BackgroundNormal"))
            nPalette.setColor(QPalette.Button, color)
            color = self.getColor(nSettings.value("ForegroundNormal"))
            nPalette.setColor(QPalette.ButtonText, color)
            nSettings.endGroup()

            nSettings.beginGroup("Colors:Tooltip")
            color = self.getColor(nSettings.value("BackgroundNormal"))
            nPalette.setColor(QPalette.ToolTipBase, color)
            color = self.getColor(nSettings.value("ForegroundNormal"))
            nPalette.setColor(QPalette.ToolTipText, color)
            nSettings.endGroup()

            nSettings.beginGroup("Colors:Selection")
            color = self.getColor(nSettings.value("BackgroundNormal"))
            nPalette.setColor(QPalette.Highlight, color)
            color = self.getColor(nSettings.value("ForegroundNormal"))
            nPalette.setColor(QPalette.HighlightedText, color)
            nSettings.endGroup()

            app.setPalette(nPalette)
            app.setStyleSheet("QPushButton:pressed {background-color: #2a82da}")


        # TODO "modificar los colores de botones seleccionados
        """darkPalette.setColor(QPalette::Link, QColor(42, 130, 218));

    darkPalette.setColor(QPalette::Highlight, QColor(42, 130, 218));
    darkPalette.setColor(QPalette::Highlig        self.repaint()
        self.show()
        app.setStyle('Fusion')
        app.setStyle('Breeze')
        '''htedText, Qt::black);"""

        '''self.hide()
        self.repaint()
        self.show()
        app.setStyle('Fusion')
        app.setStyle('Breeze')
        '''

    def btnClk(self, btn):
        '''copy selected color-scheme to kdeglobals or close'''
        if btn == self.buttonBox.button(QDialogButtonBox.Apply):
            qDebug("apply")
            if self.comboBox.currentText() != "None":
                for f in self.files:
                    set = QSettings(self.schemeDir + f, QSettings.NativeFormat)
                    if(set.value("ColorScheme") == self.comboBox.currentText()):
                        selected = self.schemeDir + f
                        copyfile(selected, self.confFile)
            else:
                os.remove(self.confFile)
            self.updateWindow(selected)

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
    # app.setWindowIcon(QIcon.fromTheme("preferences-desktop-color"))
    app.exec_()
