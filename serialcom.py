#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
#from serial import Serial
import serial
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import json

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
		self._serialEv = SerialEvents(self.serial)
		self._serialEv.readyRead.connect(self._readSerial)


	def _multiSub(self, subs, subject):
		'''Simultaneously perform all substitutions on the subject string.'''
		pattern = '|'.join('(%s)' % re.escape(p) for p, s in subs)
		substs = [s for p, s in subs]
		replace = lambda m: substs[m.lastindex - 1]
		return re.sub(pattern, replace, subject)
	
	
	def __del__(self):
		self._serialEv.stop()
		self.serial.close()
		pass
	
	
	def ports(self):
		portslist = []
		for port in PortsListener.ports():
			portslist.append(GenericPort(port, ''))
		return portslist
	
	
	def connectPort(self, portName):
		if self._verbose > 1:
			print('Opening serial port... (%s)' % portName)
		
		if not self.serial.isOpen():
			self.serial.port = portName
			self.serial.open()
			self._serialEv.start()
	
	@QtCore.Slot()
	def disconnectPort(self):
		self._serialEv.stop()
		self.serial.close()
	
	
		
	def _readSerial(self):
		self._dataRead += self._serialEv.readAll().decode(_CODING_SERIAL)
		#print('>', self._dataRead)
		
		while True:
			match = re.search('^.*?(<(.*?)>)', self._dataRead)
			
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
				data = json.loads(jsonStr)
				jsonObjects.append(data)
			except:
				# Loading fail
				pass
		
		self._jsonList = []
		return jsonObjects
	
	
	def sendJSON(self, jsonData):
		try:
			self.sendJSONStr(json.dumps(jsonData))
			return True
		except:
			return False
	
	def sendJSONStr(self, jsonStr):
		
		invalid = [('\n','\\n'), ('\r','\\r'), ("'",'"')]

		json_str = self._multiSub(invalid, jsonStr)
		self._sendStr(json_str)
	
	def _sendStr(self, string):
		if self.serial.isOpen():
			self.serial.write(bytes('<' + string + '>', _CODING_SERIAL))




def main(args):
	
	def quit():
		del sc
	
	def read():
		print('>> Reading data ')
		print(sc.readAllObjects()[0])
		
	
	def send():
		print('>> SEND ')
		print(te_inputData.toPlainText())
		sc.sendJSONStr(te_inputData.toPlainText())
		
		print(sc.ports())
		
	
	
	a = QtGui.QApplication(args)
	
	sc = SerialCom()
	sc.connectPort('/dev/tty.usbserial-A6008cB6')
	
	sc.readyRead.connect(read)
	
	pb_connect = QPushButton('Send JSON data')
	pb_connect.clicked.connect(send)
	
	te_inputData = QTextEdit()
	te_inputData.setPlainText('''{'musiques': ['Best Improvisation Ever 2', 'My Theory\n (Bonus)'], 'nom': 'MeshowRandom'}'''.replace("'", '"'))
	
	
	window = QWidget()
	layout = QVBoxLayout(window)
	
	layout.addWidget(te_inputData)
	layout.addWidget(pb_connect)
	
	window.show()
	
	r = a.exec_()
	#quit()
	del sc
	return r


if __name__ == "__main__":
	main(sys.argv)
	