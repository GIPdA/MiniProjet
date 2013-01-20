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
	
	lastComPort = None
	
	configStream = '''{'__CONFIGURATION__':{'robot':{'name':'Wulka Bot'},
	'groups':{'1':'Capteurs avants', '2':'Capteurs arrières', '3':'Roues', '4':'Télémètres avants', '5':'Télémètres arrières'},
	
	'functionalities':{
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
	
	'srl1_value':{'display':'ProgressBar', 'group':5, 'layout':'r0', 'data':{'vertical':true}},
	'srr1_value':{'display':'ProgressBar', 'group':5, 'layout':'r0', 'data':{'vertical':true}},
	
	'robotDirWheelRotation':{'display':'Dial', 'name':'Direction', 'data':{'range':[0, 360], 'vertical':true}}
	}}}'''
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		self.loadSettings()
		
		self._serialCom = SerialCom()
		self._serialCom.readyRead.connect(self.serialEvent)
		#print('Found ports:', self._serialCom.ports())
		
		self.createMenus()
		
		view = QDeclarativeView()
		
		widget = QWidget()
		
		lyt = QGridLayout(widget)
		lyt.setContentsMargins(0, 0, 0, 0)
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
		
		v = self.root.findChild(QtCore.QObject,"srl1_value")
		v.progressValueChanged.connect(self.sensorValueChanged)
		
		v = self.root.findChild(QtCore.QObject,"srr1_value")
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
		self.setFixedHeight(550)
		self.setFixedWidth(600)
		
		# self.setSpeed_LeftWheel(-50)
		# self.setSpeed_LeftWheel(50)
		# self.setSpeed_RightWheel(50)
		
		self.statusBar().showMessage('Choose a port to stream configuration')

		# Open last port if possible
		if self.lastComPort:
			if self.lastComPort in self.commObject().portNames():
				print('>> Loading saved port config:', self.lastComPort)
				self.changeComPort(self.lastComPort)
			else:
				print('Saved com port not available.')
		else:
			print('No com port saved.')
	
	
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
		self.portsMenu = self.menuBar().addMenu('&Ports')
		# Construct port list menu
		for port in self.commObject().ports():
			act = self.portsMenu.addAction(port.name)
			act.setCheckable(True)
			act.setToolTip(port.description)
			portSelectGroup.addAction(act)
			
		portSelectGroup.triggered.connect(self._changePort)
		
		configMenu = self.menuBar().addMenu('&Configuration')
		streamAct = configMenu.addAction('&Stream configuration')
		streamAct.triggered.connect(self.streamConfiguration)
	
	
	def streamConfiguration(self):
		
		if not self.commObject().isConnected():
			print('Port unconnected, unable to stream data.')
			self.statusBar().showMessage('Open a port to stream data!', 6000)
			#return
		
		print('>> Stream config file')
		
		data = json.loads(self.configStream.replace("'", '"'), object_pairs_hook=OrderedDict)
		#print(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))
		
		if self.commObject().sendJSON(data):
			self.statusBar().showMessage('Configuration streamed!', 6000)
		else:
			self.statusBar().showMessage('Error: data not sent', 6000)
	
	
	def _changePort(self, action):
		''' Use new port '''
		#print('Change port:', action.text())
		
		self.changeComPort(action.text())
	
	
	def changeComPort(self, portName):
		''' Try to connect to 'portName' '''
		
		if self.commObject().isConnected():
			print('Disconnect from', self.commObject().portName())
		
		if not self.commObject().connectPort(portName):
			self.statusBar().showMessage('Unable to connect {}.'.format(portName), 6000)
			return
		
		# Stream our robot config file
		self.streamConfiguration()
		
		# Update last port
		self.lastComPort = portName
		
		# Check menu action for current port
		for act in self.portsMenu.actions():
			if act.text() == portName:
				act.setChecked(True)
		
		self.statusBar().showMessage('{} connected.'.format(portName), 6000)
		
	
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
	
	
	
	def loadSettings(self):
		''' Load settings '''
		se = QSettings(fullPath('wulkabot.conf'), QSettings.IniFormat)
		
		se.beginGroup('commport')
		self.lastComPort = se.value('lastport', '')
		se.endGroup()
		
		
	def saveSettings(self):
		''' Save settings '''
		se = QSettings(fullPath('wulkabot.conf'), QSettings.IniFormat)
		
		se.beginGroup('commport')
		se.setValue('lastport', self.lastComPort)
		se.endGroup()
	
	
	def closeEvent(self, event):
		''' App closing request '''
		self.saveSettings()
		
		self._serialCom.disconnectPort()
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
	
	