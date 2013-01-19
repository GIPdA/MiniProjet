#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
from PySide import QtGui, QtCore, QtDeclarative
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
import json

from serialCom import SerialCom
import time

from BotConfigParser import BotConfigParser
from collections import OrderedDict
import importlib
#from displays import Led, ProgressBar, QMLWidget, Slider


class MdiSubWindow(QMdiSubWindow):
	''' Custom QMdiSubWindow implementing 'hided' signal.
	The default close event is overrided for hiding.
	'''
	
	hided = QtCore.Signal()
	
	def __init__(self):
		QMdiSubWindow.__init__(self)
	
	def closeEvent(self, event):
		event.ignore()
		self.hide()
		self.hided.emit()

def fullPath(path):
	return os.path.dirname(__file__) + '/' + path

class MainWindow(QtGui.QMainWindow):
	
	_fids = {}	# Functionalities display objects by functionality ID
	_wgtgrp = {}	# Widgets by group
	
	_layoutMatchString = r'(r(?P<row>\d+))?(c(?P<col>\d+))?(rs(?P<rowspan>\d+))?(cs(?P<colspan>\d+))?'
	
	mdiarea = None
	functionalitiesMenu = None
	signalMapper = None
	
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		self.loadSettings()
		#self.saveSettings()
		
		self._serialCom = SerialCom()
		self._serialCom.readyRead.connect(self.serialEvent)
		#print('Found ports:', self._serialCom.ports())
		
		self.createMenus()
		
		self.resize(800, 500)
		
		self.statusBar().showMessage('Open a robot configuration file...')
		
		#if self.recentFilesActs[0].data():
		#	self.recentFilesActs[0].triggered.emit()
		
		#self.setDockNestingEnabled(True)
	
	
	def commObject(self):
		return self._serialCom
	
	def createMenus(self):
		''' Create the app default menus '''
		
		fileMenu = self.menuBar().addMenu('&File')
		openAct = fileMenu.addAction('&Open Robot...', None, QKeySequence.Open)
		openAct.triggered.connect(self.openConfigFile)
		
		self.rfSeparatorAct = fileMenu.addSeparator()
		
		self.recentFilesActs = []
		for i in range(0, self.MaxRecentFiles):
			act = QAction(self)
			self.recentFilesActs.append(act)
			act.setVisible(False)
			act.triggered.connect(self.openRecentFile)
			
			fileMenu.addAction(act)
		
		self.updateRecentFilesActions()
		
		portSelectGroup = QActionGroup(self)
		portsMenu = self.menuBar().addMenu('&Ports')
		# Construct port list menu
		for port in self.commObject().ports():
			act = portsMenu.addAction(port.name)
			act.setCheckable(True)
			act.setToolTip(port.description)
			portSelectGroup.addAction(act)
			
		portSelectGroup.triggered.connect(self.changePort)
	
	
	def createSubWindowMenus(self):
		''' Create a menu containing the subWindows list '''
		
		subwActGroup = QActionGroup(self)
		subwActGroup.setExclusive(False)
		
		if not self.functionalitiesMenu:
			self.functionalitiesMenu = self.menuBar().addMenu('&Functionalities')
			
		subwMenu = self.functionalitiesMenu
		
		# Create subwindows list actions
		for subw in self.mdiarea.subWindowList():
			act = subwMenu.addAction(subw.windowTitle())
			act.setCheckable(True)
			act.setChecked(True)
			act.setData(subw)
			subw.hided.connect(act.toggle)
			subwActGroup.addAction(act)
		
		subwActGroup.triggered.connect(self.showSubWindow)
		
		subwMenu.addSeparator()
		
		# Add action to show all subwindows
		self._subWindowsActions = subwActGroup.actions()
		showall = subwMenu.addAction('Show All')
		showall.triggered.connect(self.showAllSubWindows)
	
	
	def openConfigFile(self, fileName = None):
		''' Open a dialog to get robot configuration file name, and load it '''
		
		stream = QApplication.keyboardModifiers() == Qt.ControlModifier
		
		if not fileName:
			fileName = QFileDialog.getOpenFileName(self, 'Open robot config file', '', 'BotVisor Config Files (*.bvc)')
			if fileName: fileName = fileName[0]
		
		if fileName:
			print('Open file:', fileName)
			self.setCurrentFile(fileName)
			
			if not stream:
				self.loadRobotFromConfigFile(fileName)
			else:
				self.streamRobotConfigFile(fileName)
	
	def openRecentFile(self):
		''' Called by recent files actions '''
		self.openConfigFile(self.sender().data())
	
	
	def loadRobotFromConfigFile(self, configFileName):
		''' Load a robot from configuration file '''
		
		# Load robot config file
		bc = BotConfigParser()
		data, botData = bc.loadConfigFile(configFileName)
		
		# fullData = OrderedDict()
		# fullData['__CONFIGURATION__'] = OrderedDict()
		# fullData['__CONFIGURATION__']['robot'] = botData
		# fullData['__CONFIGURATION__']['functionalities'] = data
		
		# print('>> Send JSON data')
		# self._serialCom.sendJSON(fullData)
		
		self.loadRobot(botData, data)
		
	
	def streamRobotConfigFile(self, configFileName):
		''' Stream a robot configuration file through com port '''
		
		# Load robot config file
		bc = BotConfigParser()
		data, botData = bc.loadConfigFile(configFileName)
		
		fullData = OrderedDict()
		fullData['__CONFIGURATION__'] = OrderedDict()
		fullData['__CONFIGURATION__']['robot'] = botData
		fullData['__CONFIGURATION__']['functionalities'] = data
		
		print('>> Stream config file')
		self._serialCom.sendJSON(fullData)
	
	
	def loadRobot(self, botData, functionalitiesData):
		''' Load a robot from configuration file '''
		
		self.clearRobot()
		
		self.mdiarea = QMdiArea()
		self.setCentralWidget(self.mdiarea)
		
		self.signalMapper = QSignalMapper()
		self.signalMapper.mapped[QObject].connect(self.functionalityValueChanged)
		
		
		self.setWindowTitle('BotVisor - ' + botData['name'])

		
		#print('All keys:', functionalitiesData.keys())
		#print(json.dumps(functionalitiesData, sort_keys=True, indent=2, separators=(',', ': ')))
		fnum = 0
		fnume = 0
		for fuKeys in functionalitiesData:
			#print(fuKeys)
			#print(functionalitiesData[fuKeys].keys())
			options = functionalitiesData[fuKeys]
			if 'display' in options.keys():
				self.loadFunctionality(fuKeys, options['display'], options)
				fnum = fnum+1
			else:
				print('Error: functionality', fuKeys, 'not loaded')
				fnume = fnume+1
		
		self.statusBar().showMessage('{} functionalities sucessfully loaded. {} failed.'.format(fnum, fnume), 6000)
		
		self.createSubWindowMenus()
	
	
	def clearRobot(self):
		''' Clear window, to load a robot '''
		
		if self.mdiarea:
			del self.mdiarea
		
		# Clear functionalities menu
		if self.functionalitiesMenu:
			self.functionalitiesMenu.clear()
		
		self._fids = {}
		self._wgtgrp = {}
		
		# Reset signal mapper
		if self.signalMapper:
			del self.signalMapper
		
	
	def showSubWindow(self, action):
		''' Show or hide a subWindow depending of action's state '''
		if action.isChecked():
			action.data().show()
		else:
			action.data().hide()
	
	def showAllSubWindows(self):
		''' Show all subWindows '''
		for act in self._subWindowsActions:
			act.data().show()
			act.setChecked(True)
	
	
	def changePort(self, action):
		''' Use new port '''
		#print('Change port:', action.text())
		
		if self._serialCom.serial.isOpen():
			print('Disconnect from ' + self._serialCom.serial.name)
		
		self._serialCom.connectPort(action.text())
		
		self.statusBar().showMessage('{} connected.'.format(action.text()), 6000)
	
	
	def serialEvent(self):
		''' JSON objects received '''
		
		jsonObjs = self._serialCom.readAllObjects()
		
		#print('\nJSON data received:')
		for jsonObj in jsonObjs:
			#print(json.dumps(jsonObj, sort_keys=True, indent=2, separators=(',', ': ')))
			
			if '__CONFIGURATION__' in jsonObj.keys():
				print('>> Streamed config file received')
				self.loadStreamedConfig(jsonObj['__CONFIGURATION__'])
			
			# Loop over all keys
			for fid in jsonObj:
				# Check if key is in stored functionalities
				if fid in self._fids:
					# Update value
					value = jsonObj[fid];
					self._fids[fid].setValue(value)
					print('Value: ', value, 'for display ', fid)
					
					self.statusBar().showMessage('Value for {} received ({}).'.format(fid, value), 2000)
	
	
	def loadStreamedConfig(self, jsonData):
		''' Load a config file streamed by a robot through com port '''
			
		if 'robot' not in jsonData or 'functionalities' not in jsonData:
			print('Streamed config file seems invalid ! (no functionalities in)')
			self.statusBar().showMessage('Streamed config file loading failed !', 6000)
			return
		
		self.loadRobot(jsonData['robot'], jsonData['functionalities'])
		
		self.statusBar().showMessage('Streamed config file loaded !', 6000)
	
	
	def addSubWindow(self, widget, title):
		''' Add a subwindow with title containing widget '''
		newSubWin = MdiSubWindow()
		newSubWin.setWindowTitle(title)
		self.mdiarea.addSubWindow(newSubWin)
		newSubWin.setWidget(widget)
		return widget
	
	def addDockWidget(self, widget, title):
		''' Add a dock with title containing widget '''
		newDock = QDockWidget(title)
		newDock.setWidget(widget)
		self.addDockWidget(Qt.LeftDockWidgetArea, newDock)
		return widget
	
	
	def loadFunctionality(self, fid, display, options):
		''' Load a functionality '''
		
		def availableLayoutPosition(layout, direction = 'r', start = (0,0) ):
			''' Return first available position in layout by incrementing on rows or cols '''
			r, c = start
			while layout.itemAtPosition(r, c):
				if direction == 'r':	# Search on rows
					r = r+1
				if direction == 'c':	# Search on cols
					c = c+1
			return r, c
		
		def loadClassFromModule(module_name, class_name):
			''' Dynamic class loading from a module '''
			# load the module, will raise ImportError if module cannot be loaded
			m = importlib.import_module(module_name)
			# get the class, will raise AttributeError if class cannot be found
			c = getattr(m, class_name)
			return c
		
		
		name = fid
		# Check for friendly name
		if 'name' in options:
			name = options['name']
		
		#print('Add display:', fid, '(' +display+ ')')
		
		# Load class instance
		classInstance = loadClassFromModule('displays', display)
		
		data = None
		if 'data' in options:
			data = options['data']
		
		if display == 'Led':
			c = classInstance(fid, name, True)
		elif display == 'ProgressBar':
			c = classInstance(fid, name, data=data, valueFormatting='{0}')
		elif display == 'Slider':
			c = classInstance(fid, name, data=data, valueFormatting='{0}')
		elif display == 'Dial':
			c = classInstance(fid, name, data=data, valueFormatting='{0}')
		elif display == 'Alphanum':
			c = classInstance(fid, name)
		else:
			raise TypeError('Unknown display type')
		
		
		# Connect signals
		c.valueChanged.connect(self.signalMapper.map)
		self.signalMapper.setMapping(c, c)
		
		# if 'range' in options:
		# 	c.setValueRange(int(options['range'][0]), int(options['range'][1]))
		
		if 'disable' in options:
			c.widget().setDisabled(options['disable'])
		
		# Save display by ID (to set values when JSON data received)
		self._fids[fid] = c
		
		# True to create a new subwindow.
		# False if the functionality is in an existing group.
		newsw = True
		
		# Check if group specified
		if 'group' in options:
			group = options['group']
			#print('Functionality in group', group)
			
			newsw = False
			# Group empty, create new widget with layout
			if group not in self._wgtgrp:
				w = QWidget()
				glyt = QGridLayout(w)
				self._wgtgrp[group] = w
				newsw = True
			else:
				self._wgtgrp[group].parent().setWindowTitle('Group '+str(group))
			
			widget = self._wgtgrp[group]
			
			# Layout position
			row, col = None, 0
			rowSpan, colSpan = 1, 1
			
			# Check if layout position specified
			if 'layout' in options:
				m = re.search(self._layoutMatchString, options['layout'])
				# Get values
				if m:
					gd = m.groupdict()
					#print(gd)
					row = int(gd['row']) if gd['row'] != None else None
					col = int(gd['col']) if gd['col'] != None else None
					
					rowSpan = int(gd['rowspan']) if gd['rowspan'] != None else 1
					colSpan = int(gd['colspan']) if gd['colspan'] != None else 1
					
					# Default if row & col to None
					if (row, col) == (None, None):
						col = 0
			
			# Get col number
			if col == None:
				row,col = availableLayoutPosition(widget.layout(), 'c', (row, 0))
			
			# Get row number
			if row == None:
				row,col = availableLayoutPosition(widget.layout(), 'r', (0, col))
			
			#print('Layout: ', row, col, rowSpan, colSpan)
			
			# Add the widget to the layout
			widget.layout().addWidget(c, row, col, rowSpan, colSpan)
			
		else:	# No group specified
			widget = c
		
		# Create new subwindow if needed
		if newsw:
			self.addSubWindow(widget, name)
			#self.addDockWidget(widget, name)
	
	
	def functionalityValueChanged(self, fobj):
		''' Send functionality value over comm port '''
		#print('Value for', fobj.id(), ':', fobj.value())
		jsonData = {fobj.id():fobj.value()}
		#print(json.dumps(jsonData, sort_keys=True, indent=2, separators=(',', ': ')))
		self._serialCom.sendJSON(jsonData)
		
		self.statusBar().showMessage('Value for {} sent ({}).'.format(fobj.id(), fobj.value()), 2000)


	def recentFilesList(self):
		''' Get recent files list from settings file '''
		se = QSettings(fullPath('BotVisor.conf'), QSettings.IniFormat)
		files = se.value('recentfiles', [])
		
		if isinstance(files, str):
			return [files]
		#if isinstance(files, list):
		#	return files
		return files
	
	
	def updateRecentFilesActions(self):
		''' Update recent files menu actions '''
		recentFiles = self.recentFilesList()
		
		numRecentFiles = min(len(recentFiles), self.MaxRecentFiles)
		
		for i in range(0, numRecentFiles):
			self.recentFilesActs[i].setText(QFileInfo(recentFiles[i]).fileName())
			self.recentFilesActs[i].setData(recentFiles[i])
			self.recentFilesActs[i].setVisible(True)
		
		for i in range(numRecentFiles, self.MaxRecentFiles):
			self.recentFilesActs[i].setVisible(False)
		
		self.rfSeparatorAct.setVisible(numRecentFiles > 0)
		
	
	def setCurrentFile(self, fileName):
		''' Update recent files '''
		recentFiles = self.recentFilesList()
		
		# Remove occurences of fileName
		while recentFiles.count(fileName):
			recentFiles.remove(fileName)
		
		# Prepend file
		recentFiles.insert(0, fileName)
		
		# Remove old files
		if len(recentFiles) > self.MaxRecentFiles:
			recentFiles = recentFiles[self.MaxRecentFiles:]
		
		# Save recent files list
		se = QSettings(fullPath('BotVisor.conf'), QSettings.IniFormat)
		se.setValue('recentfiles', recentFiles)
		
		self.updateRecentFilesActions()
		
	
	def loadSettings(self):
		''' Load settings '''
		se = QSettings(fullPath('BotVisor.conf'), QSettings.IniFormat)
		
		#recentFiles = se.value('recentfiles')
		self.MaxRecentFiles = int(se.value('maxrecentfiles', 10))
		
		
	def saveSettings(self):
		''' Save settings '''
		#se = QSettings(fullPath('BotVisor.conf'), QSettings.IniFormat)
		pass
	
	def closeEvent(self, event):
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
	
	