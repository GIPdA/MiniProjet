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
	

class MainWindow(QtGui.QMainWindow):
	
	_fids = {}	# Functionalities display objects by functionality ID
	_wgtgrp = {}	# Widgets by group
	
	_layoutMatchString = r'(r(?P<row>\d+))?(c(?P<col>\d+))?(rs(?P<rowspan>\d+))?(cs(?P<colspan>\d+))?'
	
	mdiarea = None
	functionalitiesMenu = None
	signalMapper = None
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		
		self._serialCom = SerialCom()
		self._serialCom.readyRead.connect(self._serialEvent)
		#print('Found ports:', self._serialCom.ports())
		
		self.createMenus()
		
		self.resize(800, 500)
		
		self.statusBar().showMessage('Open a robot configuration file...')
		
		#self.setDockNestingEnabled(True)
	
	
	def commObject(self):
		return self._serialCom
	
	def createMenus(self):
		''' Create the app default menus '''
		
		fileMenu = self.menuBar().addMenu('&File')
		openAct = fileMenu.addAction('&Open Robot...', None, QKeySequence.Open)
		openAct.triggered.connect(self.openConfigFile)
		
		portSelectGroup = QActionGroup(self)
		portsMenu = self.menuBar().addMenu('&Ports')
		# Construct port list menu
		for port in self.commObject().ports():
			act = portsMenu.addAction(port.name)
			act.setCheckable(True)
			act.setToolTip(port.description)
			portSelectGroup.addAction(act)
			
		portSelectGroup.triggered.connect(self._changePort)
		
		# Functionalitites menu
		#self.createFunctionalitiesMenu()
	
	
	def createSubWindowMenu(self):
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
		
		subwActGroup.triggered.connect(self._showSubWindow)
		
		subwMenu.addSeparator()
		
		# Add action to show all subwindows
		self._subWindowsActions = subwActGroup.actions()
		showall = subwMenu.addAction('Show All')
		showall.triggered.connect(self._showAllSubWindows)
	
	
	def openConfigFile(self):
		''' Open a dialog to get robot configuration file name, and load it '''
		
		fileName = QFileDialog.getOpenFileName(self, 'Open robot config file', '', 'BotVisor Config Files (*.bvc)')
		
		if fileName:
			print('Open file:', fileName)
			self.loadRobot(fileName[0])
	
	
	def loadRobot(self, configFileName):
		''' Load a robot from configuration file '''
		
		self.clearRobot()
		
		self.mdiarea = QMdiArea()
		self.setCentralWidget(self.mdiarea)
		
		self.signalMapper = QSignalMapper()
		self.signalMapper.mapped[QObject].connect(self.functionalityValueChanged)
		
		# Load robot config file
		bc = BotConfigParser()
		data, botData = bc.loadConfigFile(configFileName)
		
		self.setWindowTitle('BotVisor - ' + botData['name'])
		
		#print('All keys:', data.keys())
		#print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
		fnum = 0
		fnume = 0
		for fuKeys in data:
			#print(fuKeys)
			#print(data[fuKeys].keys())
			options = data[fuKeys]
			if 'display' in options.keys():
				self.loadFunctionality(fuKeys, options['display'], options)
				fnum = fnum+1
			else:
				print('Error: functionality', fuKeys, 'not loaded')
				fnume = fnume+1
		
		self.statusBar().showMessage('{} functionalities sucessfully loaded. {} failed.'.format(fnum, fnume), 6000)
		
		self.createSubWindowMenu()
	
	
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
		
	
	def _showSubWindow(self, action):
		''' Show or hide a subWindow depending of action's state '''
		if action.isChecked():
			action.data().show()
		else:
			action.data().hide()
	
	def _showAllSubWindows(self):
		''' Show all subWindows '''
		for act in self._subWindowsActions:
			act.data().show()
			act.setChecked(True)
	
	
	def _changePort(self, action):
		''' Use new port '''
		print('Change port:', action.text())
		
		self.statusBar().showMessage('Port changed for {}.'.format(action.text()), 6000)
	
	
	def _serialEvent(self):
		''' JSON objects received '''
		
		jsonObjs = self._serialCom.readAllObjects()
		
		print('\nJSON data received:')
		for jsonObj in jsonObjs:
			print(json.dumps(jsonObj, sort_keys=True, indent=2, separators=(',', ': ')))
			
			# Loop over all keys
			for fid in jsonObj:
				# Check if key is in stored functionalities
				if fid in self._fids:
					# Update value
					value = jsonObj[fid];
					self._fids[fid].setValue(value)
					
					self.statusBar().showMessage('Value for {} received ({}).'.format(fid, value), 2000)
	
	
	
	def addSubWindow(self, widget, title):
		''' Add a subwindow with title containing widget '''
		newSubWin = MdiSubWindow()
		newSubWin.setWindowTitle(title)
		self.mdiarea.addSubWindow(newSubWin)
		newSubWin.setWidget(widget)
		return widget
	
	def _addDockWidget(self, widget, title):
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
		
		if display == 'Led':
			c = classInstance(fid, name, True)
		elif display == 'ProgressBar':
			c = classInstance(fid, name, '{0}')
		elif display == 'Slider':
			c = classInstance(fid, name, '{0}')
		elif display == 'Dial':
			c = classInstance(fid, name, '{0}')
		elif display == 'Alphanum':
			c = classInstance(fid, name)
		else:
			raise TypeError('Unknown display type')
		
		
		# Connect signals
		c.valueChanged.connect(self.signalMapper.map)
		self.signalMapper.setMapping(c, c)
		
		if 'range' in options:
			c.setValueRange(int(options['range'][0]), int(options['range'][1]))
		
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
			#self._addDockWidget(widget, name)
	
	
	def functionalityValueChanged(self, fobj):
		''' Send functionality value over comm port '''
		#print('Value for', fobj.id(), ':', fobj.value())
		jsonData = {fobj.id():fobj.value()}
		#print(json.dumps(jsonData, sort_keys=True, indent=2, separators=(',', ': ')))
		#self._serialCom.sendJSON(jsonData)
		
		self.statusBar().showMessage('Value for {} sent ({}).'.format(fobj.id(), fobj.value()), 2000)



def main(args):
	
	a = QtGui.QApplication(args)
	
	mainwindow = MainWindow()
	mainwindow.show()
	
	r = a.exec_()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
	