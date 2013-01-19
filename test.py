#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

from PySide import QtGui, QtCore, QtDeclarative
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

import time
import json, collections

verbose = 1


class Console(QtCore.QObject):
    @QtCore.Slot(str)
    def outputStr(self, s):
        print(s)


class Terminal(QWidget):
	
	_verbose = 0
	
	angle = 45
	
	configStream = '''{'robot':{'name':'Wulka Bot'}, 'functionalities':{
	'sens_fl2':{'display':'ProgressBar', 'group':1, 'layout':'r0'},
	'sens_fl1':{'display':'ProgressBar', 'group':1, 'layout':'r0'},
	'sens_fm':{'display':'ProgressBar', 'group':1, 'layout':'r0'},
	'sens_fr1':{'display':'ProgressBar', 'group':1, 'layout':'r0'},
	'sens_fr2':{'display':'ProgressBar', 'group':1, 'layout':'r0'},
	
	'sens_rl1':{'display':'ProgressBar', 'group':2, 'layout':'r0'},
	'sens_rr1':{'display':'ProgressBar', 'group':2, 'layout':'r0'},
	
	'leftWheel':{'display':'Slider', 'group':3, 'layout':'r0'},
	'rightWheel':{'display':'Slider', 'group':3, 'layout':'r0'},
	
	'sfl2_value':{'display':'Led', 'group':4, 'layout':'r0'},
	'sfl1_value':{'display':'Led', 'group':4, 'layout':'r0'},
	'sfm_value':{'display':'Led', 'group':4, 'layout':'r0'},
	'sfr1_value':{'display':'Led', 'group':4, 'layout':'r0'},
	'sfr2_value':{'display':'Led', 'group':4, 'layout':'r0'},
	
	'srr1_value':{'display':'Led', 'group':5, 'layout':'r0'},
	'srl1_value':{'display':'Led', 'group':5, 'layout':'r0'},
	
	'robotDirWheelRotation':{'display':'Dial'}
	}}'''
	
	
	def __init__(self, verbose = 0):
		QWidget.__init__(self)
		
		dial = QDial()
		dial.setMaximumHeight(100)
		dial.setMaximum(360)
		dial.setMinimum(0)
		dial.valueChanged.connect(self.moveDirWheel)
		
		view = QDeclarativeView()
		
		lyt = QVBoxLayout(self)
		lyt.addWidget(dial)
		lyt.addWidget(view)
		
		self.setWindowTitle("Robot")
		view.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
		
		# Renders 'PyTerm.qml'
		view.setSource(QUrl.fromLocalFile('Robot.qml'))
		# QML resizes to main window
		view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
		
		
		con = Console()
		context = view.rootContext()
		context.setContextProperty("con", con)

		
		self.root = view.rootObject()
		#print(root.children())
		#robot = root.findChild(QtCore.QObject, 'robotRotation')
		#robot.setProperty('angle', 45)
		
		self.objects = {}
		
		
		dirWheel = self.root.findChild(QtCore.QObject, 'robotDirWheelRotation')
		#dirWheel.setProperty('angle', 0)
		self.objects['robotDirWheelRotation'] = dirWheel
		
		v = self.root.findChild(QtCore.QObject, 'leftWheel')
		self.objects['leftWheel'] = v
		
		v = self.root.findChild(QtCore.QObject, 'rightWheel')
		self.objects['rightWheel'] = v
		
		
		v = self.root.findChild(QtCore.QObject,"sfm_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"sfl2_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"sfl1_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"sfr1_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"sfr2_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"srr1_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"srl1_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		

		v = self.root.findChild(QtCore.QObject,"sens_fm")
		v.checked.connect(self.sensorClicked)
		
		v = self.root.findChild(QtCore.QObject,"sens_fr2")
		v.checked.connect(self.sensorClicked)
		
		v = self.root.findChild(QtCore.QObject,"sens_fr1")
		v.checked.connect(self.sensorClicked)
		
		v = self.root.findChild(QtCore.QObject,"sens_fl1")
		v.checked.connect(self.sensorClicked)
		
		v = self.root.findChild(QtCore.QObject,"sens_fl2")
		v.checked.connect(self.sensorClicked)
		
		v = self.root.findChild(QtCore.QObject,"sens_rr1")
		v.checked.connect(self.sensorClicked)
		
		v = self.root.findChild(QtCore.QObject,"sens_rl1")
		v.checked.connect(self.sensorClicked)
		
		#print(self.configStream)
		data = json.loads(self.configStream.replace("'", '"'), object_pairs_hook=collections.OrderedDict)
		print(data)
		print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
		
		self.setSpeed_LeftWheel(50)
		self.setSpeed_RightWheel(-40)

	
	def moveDirWheel(self, value):
		dirWheel = self.root.findChild(QtCore.QObject, 'robotDirWheelRotation')
		dirWheel.setProperty('angle', value)

	def setSpeed_LeftWheel(self, speed):
		leftWheel = self.root.findChild(QtCore.QObject, 'leftWheel')
		leftWheel.setSpeed(speed)
		
	def setSpeed_RightWheel(self, speed):
		rightWheel = self.root.findChild(QtCore.QObject, 'rightWheel')
		rightWheel.setSpeed(speed)
	
	
	def sensorClicked(self, checked):
		print('CLICKED', checked)
		#print(self.sender())
	
	def sensorValueChanged(self, value):
		print('SENSOR', value, self.sender().objectName())



def main(args):
	
	
	a = QtGui.QApplication(args)
	
	term = Terminal()
	term.show()
	
	r = a.exec_()
	return r


if __name__ == "__main__":
	main(sys.argv)
	