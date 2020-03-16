#!/usr/bin/python3
# coding=utf-8

import unittest
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir, QSettings
# from PyQt5.QtTest import QTest
from pathlib import Path
from gettext import gettext as _  # better than in main "_ = gettext.gettext" for testing


# from lubuntuBreezeConfig import lubuntuBreeze
# import lubuntuBreezeConfig
# help(lubuntuBreezeConfig)

sys.path.insert(0, "")
import lubuntuBreeze


app = QApplication(sys.argv)

class LubuntuBreezeTest(unittest.TestCase):

    def setUp(self):
        self.form = lubuntuBreeze.MainWindow()
        dir = QDir(self.form.schemeDir)
        self.files = dir.entryList(dir, dir.Files)
        self.confFile = Path(Path.home() / ".config/kdeglobals")

    def testText(self):
        '''Test GUI in default state'''
        label = _("Select Color Scheme for Breeze Qt Style:")
        noteText =_("Applications need to be restarted for changes to take effect.")
        noteText += "<br/>"
        noteText += _("In case of pcmanfm-qt, since it handles the desktop, ")
        noteText += _("a restart of the desktop is needed") + "<br/>"
        noteText += _("Easier, restart session.")
        noteText += "<br/>"
        noteText += _("Best results if a matching GTK Theme is selected.")

        self.assertEqual(self.form.label.text(), label)
        self.assertEqual(self.form.note.text(), '<font size="-1">' + noteText + '</font>')

    def testComoboxPopulation(self):
        '''test if combobox is populated with same entries as number of files
        (+1 because on None)'''
        len(self.files)
        self.assertEqual(self.form.comboBox.count(), len(self.files) + 1)

    def testComoboxSelected(self):
        '''test if comobox select the actual'''
        if self.confFile.is_file():
            settings = QSettings(str(self.confFile), QSettings.NativeFormat)
            set = settings.value("ColorScheme")
            self.assertEqual(self.form.comboBox.currentText(), set)
        else:
            self.assertEqual(self.form.comboBox.currentText(), _("None"))


    """def testSelectApply(self):
        '''check if '''
        if self.form.comboBox.currentText() == "None":
            # select something else
            for f in self.files:
                set = QSettings(self.form.schemeDir + f, QSettings.NativeFormat)
                if(set.value("ColorScheme") == self.form.comboBox.currentText()):
                    settings = QSettings(str(self.confFile), QSettings.NativeFormat)
                    set = settings.value("ColorScheme")
                    self.assertEqual(self.form.comboBox.currentText(),set)
                    # copyfile(self.schemeDir + f, self.confFile)
        else:
            # select NONE and see if file is removed



    def testClose(self):
        '''test apply'''
    """

if __name__ == "__main__":
    unittest.main()
