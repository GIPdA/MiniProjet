#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
from PySide import QtGui, QtCore, QtDeclarative
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
import json
from collections import OrderedDict

from serialCom import SerialCom
import time

#from BotConfigParser import BotConfigParser
#import importlib
#from displays import Led, ProgressBar, QMLWidget, Slider



def fullPath(path):
	return os.path.dirname(__file__) + '/' + path

class MainWindow(QtGui.QMainWindow):
	
	_objects = {}


	mdiarea = None
	functionalitiesMenu = None
	signalMapper = None
	
	configStream = '''{'__CONFIGURATION__':{'robot':{'name':'Wulka Bot'}, 'functionalities':{
	'sens_fl2':{'display':'Led', 'group':1, 'layout':'r0', 'disable':true},
	'sens_fl1':{'display':'Led', 'group':1, 'layout':'r0', 'disable':true},
	'sens_fm':{'display':'Led', 'group':1, 'layout':'r0', 'disable':true},
	'sens_fr1':{'display':'Led', 'group':1, 'layout':'r0', 'disable':true},
	'sens_fr2':{'display':'Led', 'group':1, 'layout':'r0', 'disable':true},
	
	'sens_rl1':{'display':'Led', 'group':2, 'layout':'r0', 'disable':true},
	'sens_rr1':{'display':'Led', 'group':2, 'layout':'r0', 'disable':true},
	
	'leftWheel':{'display':'Slider', 'group':3, 'layout':'r0', 'data':{'vertical':true, 'range':[-70, 70]}},
	'rightWheel':{'display':'Slider', 'group':3, 'layout':'r0', 'data':{'vertical':true, 'range':[-70, 70]}},
	
	'sfl2_value':{'display':'ProgressBar', 'group':4, 'layout':'r0', 'data':{'vertical':true}},
	'sfl1_value':{'display':'ProgressBar', 'group':4, 'layout':'r0', 'data':{'vertical':true}},
	'sfm_value':{'display':'ProgressBar', 'group':4, 'layout':'r0', 'data':{'vertical':true}},
	'sfr1_value':{'display':'ProgressBar', 'group':4, 'layout':'r0', 'data':{'vertical':true}},
	'sfr2_value':{'display':'ProgressBar', 'group':4, 'layout':'r0', 'data':{'vertical':true}},
	
	'srr1_value':{'display':'ProgressBar', 'group':5, 'layout':'r0', 'data':{'vertical':true}},
	'srl1_value':{'display':'ProgressBar', 'group':5, 'layout':'r0', 'data':{'vertical':true}},
	
	'robotDirWheelRotation':{'display':'Dial', 'data':{'range':[0, 360], 'vertical':true}}
	}}}'''
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		
		self._serialCom = SerialCom()
		self._serialCom.readyRead.connect(self.serialEvent)
		#print('Found ports:', self._serialCom.ports())
		
		self.createMenus()
		
		view = QDeclarativeView()
		
		widget = QWidget()
		
		lyt = QGridLayout(widget)
		lyt.addWidget(view, 0, 0)
		
		self.setCentralWidget(widget)
		
		
		self.setWindowTitle("Wulka Bot Simulator")
		view.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
		
		# Renders 'PyTerm.qml'
		view.setSource(QUrl.fromLocalFile('Robot.qml'))
		# QML resizes to main window
		view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
		
		
		self.root = view.rootObject()
		
		
		dirWheel = self.root.findChild(QtCore.QObject, 'robotDirWheelRotation')
		#dirWheel.setProperty('angle', 0)
		self._objects['robotDirWheelRotation'] = dirWheel
		
		v = self.root.findChild(QtCore.QObject, 'leftWheel')
		self._objects['leftWheel'] = v
		
		v = self.root.findChild(QtCore.QObject, 'rightWheel')
		self._objects['rightWheel'] = v
		
		
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
		
		
		self.resize(600, 550)
		
		# self.setSpeed_LeftWheel(-50)
		# self.setSpeed_LeftWheel(50)
		# self.setSpeed_RightWheel(50)
		
		#self.statusBar().showMessage('Open a robot configuration file...')
	
	
	def moveDirWheel(self, value):
		self._objects['robotDirWheelRotation'].setProperty('angle', value)

	def setSpeed_LeftWheel(self, speed):
		self._objects['leftWheel'].setSpeed(speed)
		
	def setSpeed_RightWheel(self, speed):
		self._objects['rightWheel'].setSpeed(speed)
	
	
	def sensorClicked(self, checked):
		#print('CLICKED', checked)
		#print('Value for', fobj.id(), ':', fobj.value())
		jsonData = {self.sender().objectName() : checked}
		self.commObject().sendJSON(jsonData)

	
	def sensorValueChanged(self, value):
		#print('SENSOR', int(value*100), self.sender().objectName())
		#print('Value for', fobj.id(), ':', fobj.value())
		jsonData = {self.sender().objectName() : int(value*100)}
		self.commObject().sendJSON(jsonData)
	
	
	
	def commObject(self):
		return self._serialCom
	
	def createMenus(self):
		''' Create the app default menus '''
		
		portSelectGroup = QActionGroup(self)
		portsMenu = self.menuBar().addMenu('&Ports')
		# Construct port list menu
		for port in self.commObject().ports():
			act = portsMenu.addAction(port.name)
			act.setCheckable(True)
			act.setToolTip(port.description)
			portSelectGroup.addAction(act)
			
		portSelectGroup.triggered.connect(self.changePort)
	
	
	
	def changePort(self, action):
		''' Use new port '''
		#print('Change port:', action.text())
		
		if self._serialCom.serial.isOpen():
			print('Disconnect from ' + self._serialCom.serial.name)
		
		self.commObject().connectPort(action.text())
		
		#self.configStream.replace("'", '"')
		
		data = json.loads(self.configStream.replace("'", '"'), object_pairs_hook=OrderedDict)
		#print(data)
		#print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
		
		print('>> Stream config file')
		self._serialCom.sendJSON(data)
		
		self.statusBar().showMessage('{} connected.'.format(action.text()), 6000)
	
	
	def serialEvent(self):
		''' JSON objects received '''
		
		jsonObjs = self.commObject().readAllObjects()
		
		#print('\nJSON data received:')
		for jsonObj in jsonObjs:
			#print(json.dumps(jsonObj, sort_keys=True, indent=2, separators=(',', ': ')))
			
			# Loop over all keys
			for fid in jsonObj:
				# Check if key is in stored functionalities
				if fid in self._objects:
					# Update value
					value = jsonObj[fid]
					
					if fid == 'robotDirWheelRotation':
						self.moveDirWheel(value)
					
					elif fid == 'leftWheel':
						self.setSpeed_LeftWheel(value)
					
					elif fid == 'rightWheel':
						self.setSpeed_RightWheel(value)
					
					print('Value: ', value, 'for display ', fid)
					
					self.statusBar().showMessage('Value for {} received ({}).'.format(fid, value), 2000)
	
	
	
	def closeEvent(self, event):
		self.commObject().disconnectPort()
		event.accept()


def main(args):
	
	a = QtGui.QApplication(args)
	
	mainwindow = MainWindow()
	mainwindow.show()
	
	#mainwindow.setFocus(Qt.MouseFocusReason)
	
	r = a.exec_()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
	