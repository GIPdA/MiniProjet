#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
from PySide import QtGui, QtCore
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *



def main(args):
	
	a = QtGui.QApplication(args)
	
	# id type range display group
	settings = QSettings('mybot.bvc', QSettings.IniFormat);
	
	settings.beginGroup('robot')
	settings.setValue('name', 'Super Bot 1')
	settings.endGroup()
	
	settings.beginGroup('functionalities')
	
	settings.setValue('led1/display', 'Led')
	settings.setValue('led1/group', 0)
	settings.setValue('led1/showID', True)
	
	settings.setValue('led2/display', 'Led')
	settings.setValue('led2/group', 0)
	
	settings.setValue('d1/display', 'Dial')
	settings.setValue('d1/range', (0, 100))
	settings.endGroup()
	
	#r = a.exec_()
	return 0


if __name__ == "__main__":
	main(sys.argv)
	
	
	
	