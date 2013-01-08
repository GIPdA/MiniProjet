#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
#from serial import Serial
import serial
from PySide import QtGui, QtCore, QtDeclarative
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
import json

from portsListener import PortsListener
from serialEvents import SerialEvents
import time

from displays import Led, ProgressBar, QMLWidget


class Widget(QDeclarativeView):
	
	def __init__(self, title, qmlFile):
		QDeclarativeView.__init__(self)
		
		self.setWindowTitle(title)
		self.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
		
		# QML source file
		self.setSource(QUrl.fromLocalFile(qmlFile))
		# QML resizes to main window
		self.setResizeMode(QDeclarativeView.SizeRootObjectToView)
		


def main(args):
	
	def addSubWindow(widget):
		newSubWin = QMdiSubWindow()
		newSubWin.setWindowTitle(widget.id())
		mdiarea.addSubWindow(newSubWin)
		newSubWin.setWidget(widget)
		#subWindowList()
		return widget
	
	
	a = QtGui.QApplication(args)
	
	mainwindow = QMainWindow()
	mdiarea = QMdiArea()
	
	addSubWindow(QMLWidget('Test QML', 'TestQML.qml'))
	
	addSubWindow(Led('Blue LED', True))
	addSubWindow(Led('Red LED'))
	
	w = addSubWindow(ProgressBar('progressbar1', '> {0}', valueBefore = True))
	w.setValue(60)
	
	w2 = addSubWindow(ProgressBar('progressbar2', '< {0}'))
	w2.setValue(60)
	
	
	
	mainwindow.setCentralWidget(mdiarea)
	
	mainwindow.show()
	
	r = a.exec_()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
	