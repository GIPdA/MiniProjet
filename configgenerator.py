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
	settings = QSettings('mybot1.bvc', QSettings.IniFormat);
	
	settings.beginGroup('robot')
	settings.setValue('name', 'Super Bot 1')
	settings.endGroup()
	
	settings.beginGroup('functionalities')
	
	settings.setValue('led1/display', 'Led')
	settings.setValue('led1/group', 0)
	
	settings.setValue('led2/display', 'Led')
	settings.setValue('led2/group', 0)
	settings.endGroup()
	
	#r = a.exec_()
	return 0


if __name__ == "__main__":
	main(sys.argv)
	
	
	
	