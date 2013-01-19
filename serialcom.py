#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
#from serial import Serial
import serial
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import json, collections

from portsListener import PortsListener
from serialEvents import SerialEvents
import time


verbose = 1

_CODING_SERIAL = 'UTF-8'

class GenericPort:
	name = None
	description = None
	
	def __init__(self, _name, _desc):
		self.name = _name
		self.description = _desc
	
	def __repr__(self):
		return "'" + self.name + "'"
	
	def __str__(self):
		return self.name


class SerialCom(QObject):
	
	readyRead = QtCore.Signal()
	
	serial = None
	_serialEv = None
	
	_verbose = 0
	
	_dataRead = ''
	_jsonList = []
	
	def __init__(self, verbose = 0):
		QObject.__init__(self)

		# Serial port + serial events
		self.serial = serial.Serial()
		# self._serialEv = SerialEvents(self.serial, verbose=1)
		# self._serialEv.readyRead.connect(self._readSerial)


	def _multiSub(self, subs, subject):
		'''Simultaneously perform all substitutions on the subject string.'''
		pattern = '|'.join('(%s)' % re.escape(p) for p, s in subs)
		substs = [s for p, s in subs]
		replace = lambda m: substs[m.lastindex - 1]
		return re.sub(pattern, replace, subject)
	
	
	def __del__(self):
		self.disconnectPort()
	
	
	def ports(self):
		portslist = []
		for port in PortsListener.ports():
			portslist.append(GenericPort(port, ''))
		return portslist
	
	def portNames(self):
		return PortsListener.ports()
	
	
	def connectPort(self, portName):
		if self._verbose > 1:
			print('Opening serial port... (%s)' % portName)
			
		if self.isConnected():
			if self.disconnectPort() == -1:
				return -1
		
		if not self.isConnected():
			self.serial.port = portName
			try:
				self.serial.open()
				self.serial.flushInput()	# Flush buffer
				self.serial.flushOutput()
			
				# Threads are not restartable, we shall recreate one each time
				self._serialEv = SerialEvents(self.serial)
				self._serialEv.readyRead.connect(self._readSerial)
				self._serialEv.start()
				
				return True
				
			except serial.serialutil.SerialException as e:
				print('Exception:', e)
				return False
		else:
			print('Port unconnected! Unable to connect desired port.')
		
		return False
			
	
	@QtCore.Slot()
	def disconnectPort(self):
		
		# Stop thread if created
		if self._serialEv:
			self._serialEv.stop()
			
			self._serialEv.join(5.0)	# Wait for the thread to quit
			if self._serialEv.isAlive():
				print('Unable to stop thread!')
				return -1
		
		self.serial.close()
	
	
	def isConnected(self):
		return self.serial.isOpen()
		
	def portName(self):
		return self.serial.name
	
		
	def _readSerial(self):
		self._dataRead += self._serialEv.readAll().decode(_CODING_SERIAL)
		#print('SerialCom: ', self._dataRead)
		
		while True:	# Do .. while
			# Match JSON string encapsulated in < >
			match = re.search('^.*?(<({.*?})>)', self._dataRead)
			
			if match:
				self._jsonList.append(match.group(2))
				self._dataRead = self._dataRead[len(match.group(0)):]
				self.readyRead.emit()
			else:
				break
	
	
	def readAll(self):
		tmpList = self._jsonList
		self._jsonList = []
		return tmpList
		
	
	def readAllObjects(self):
			
		jsonObjects = []
		for jsonStr in self._jsonList:
			try:
				data = json.loads(jsonStr, object_pairs_hook=collections.OrderedDict)
				#print(data)
				jsonObjects.append(data)
			except:
				# Loading fail
				pass
		
		self._jsonList = []
		return jsonObjects
	
	
	def sendJSON(self, jsonData):
		try:
			return self.sendJSONStr(json.dumps(jsonData))
		except:
			print('JSON dump fail! Data not sent')
			return -1
	
	def sendJSONStr(self, jsonStr):
		
		invalid = [('\n','\\n'), ('\r','\\r'), ("'",'"')]

		json_str = self._multiSub(invalid, jsonStr)
		return self._sendStr(json_str)
	
	def _sendStr(self, string):
		if self.serial.isOpen():
			return self.serial.write(bytes('<' + string + '>', _CODING_SERIAL))
		return -1


	