#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from PySide.QtCore import *
import threading
import serial
import time


class SerialEvents(QObject, threading.Thread):
	"""
	SerialEvents provide way to have asyncronous serial events 
	interfaced with Qt slots/signals system.
	"""
	
	## ## ## SIGNALS ## ## ##
	readyRead = QtCore.Signal(int)
	

	def __init__(self, serialObject, verbose = 0):
		QObject.__init__(self)
		threading.Thread.__init__(self)
		
		self._serialObject = serialObject
		self._stopEvent = threading.Event()
		
		self.verbose = verbose
		
		self._availableBytes = 0
	
	
	def readAll(self):
		""" Read all waiting bytes.
		Function provided for convenience
		"""
		return self._serialObject.read(self._serialObject.inWaiting())
	
	def setSerial(self, serialObject):
		self._serialObject = serialObject
	
	@QtCore.Slot()
	def stop(self):
		""" Stop all serial events """
		self._stopEvent.set()
		

	def run(self):
		""" Thread loop """
		
		if self.verbose:
			print('Entering Serial events loop...')
		
		#self._stopEvent.clear()
			
		while not self._stopEvent.isSet():
			# Check if data in buffer
			if self._serialObject.isOpen():
				
				wb = self._serialObject.inWaiting()
				if wb > 0 and wb != self._availableBytes:	# Emit readyRead signal only one time
					#string = self._serialObject.read(self._serialObject.inWaiting())
					
					# Emit signal with number of bytes to read
					self.readyRead.emit(self._serialObject.inWaiting())
					
					if self.verbose:
						print('Data available (', self._serialObject.inWaiting(), ')')
				
				# Store current number of waiting bytes
				self._availableBytes = self._serialObject.inWaiting()
				
				#time.sleep(0.1) # Wait 100ms
				self._stopEvent.wait(0.1)
				
			else:	# Not open, wait more
				#time.sleep(1)	# Wait 1s
				self._stopEvent.wait(1)
		
		if self.verbose:
			print('SerialEvents thread exited')


