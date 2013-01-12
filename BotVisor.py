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
from displays import Led, ProgressBar, QMLWidget, Slider


class MainWindow(QtGui.QMainWindow):
	
	_fids = {}	# Functionalities display objects by functionality ID
	_wgtgrp = {}	# Widgets by group
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		self.mdiarea = QMdiArea()
		
		self.signalMapper = QSignalMapper()
		self.signalMapper.mapped[QObject].connect(self.functionalityValueChanged)
		
		
		self._serialCom = SerialCom()
		self._serialCom.readyRead.connect(self._serialEvent)
		
		print('Found ports:', self._serialCom.ports())
		
		# w = self.addSubWindow(Slider('progressbar1', '{0}', valueBefore = True))
		# w.setValue(60)
		# w.valueChanged.connect(self.valc)
		
		
		bc = BotConfigParser()
		data = bc.loadConfigFile('mybot1.bvc')
		
		#print(data)
		
		print('All keys:', data.keys())
		
		print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
		
		for fuKeys in data:
			#print(fuKeys)
			#print(data[fuKeys].keys())
			options = data[fuKeys]
			if 'display' in options.keys():
				self.loadFunctionality(fuKeys, options['display'], options)
			else:
				print('Error: functionality', fuKeys, 'not loaded')

		
		
		self.setCentralWidget(self.mdiarea)
	
	
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
					
	
	
	def addSubWindow(self, widget, title):
		''' Add a subwindow with title containing widget '''
		newSubWin = QMdiSubWindow()
		newSubWin.setWindowTitle(title)
		self.mdiarea.addSubWindow(newSubWin)
		newSubWin.setWidget(widget)
		#subWindowList()
		return widget
	
	
	def loadClassFromModule(self, module_name, class_name):
		''' Dynamic class loading from a module '''
		# load the module, will raise ImportError if module cannot be loaded
		m = importlib.import_module(module_name)
		# get the class, will raise AttributeError if class cannot be found
		c = getattr(m, class_name)
		return c
	
	
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
		
		
		name = fid
		# Check for friendly name
		if 'name' in options:
			name = options['name']
		
		print('Add display:', fid, '(' +display+ ')')
		
		# Load class instance
		classInstance = self.loadClassFromModule('displays', display)
		
		if display == 'Led':
			c = classInstance(name, True)
		elif display == 'ProgressBar':
			c = classInstance(name, '{0}')
		elif display == 'Slider':
			c = classInstance(name, '{0}')
		elif display == 'Dial':
			c = classInstance(name, '{0}')
		elif display == 'Alphanum':
			c = classInstance(name)
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
			
			# Check if layout position specified
			if 'layout' in options:
				m = re.search(r'(r(?P<row>\d+))?(c(?P<col>\d+))?', options['layout'])
				# Get values
				if m:
					gd = m.groupdict()
					row = gd['row']
					col = gd['col']
					
					if row != None:
						row = int(row)
					if col != None:
						col = int(col)
					
					# Default if row & col to None
					if (row, col) == (None, None):
						col = 0
			
			# Get col number
			if col == None:
				row,col = availableLayoutPosition(widget.layout(), 'c', (row, 0))
			
			# Get row number
			if row == None:
				row,col = availableLayoutPosition(widget.layout(), 'r', (0, col))
			
			#print('Layout: ', row, col)
			
			# Add the widget to the layout
			widget.layout().addWidget(c, row, col)
			
		else:	# No group specified
			widget = c
		
		# Create new subwindow if needed
		if newsw:
			self.addSubWindow(widget, name)
	
	
	def functionalityValueChanged(self, fobj):
		''' Send functionality value over comm port '''
		print('Value for', fobj.id(), ':', fobj.value())
		jsonData = {fobj.id():fobj.value()}
		#print(json.dumps(jsonData, sort_keys=True, indent=2, separators=(',', ': ')))
		#self._serialCom.sendJSON(jsonData)



def main(args):
	
	
	a = QtGui.QApplication(args)
	
	mainwindow = MainWindow()
	
	
	mainwindow.show()
	
	r = a.exec_()
	return r


if __name__ == "__main__":
	main(sys.argv)
	
	