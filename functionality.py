#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore

class Functionality(QtCore.QObject):
	''' Base class for all action objects linked to a robot, called a functionality.
	Should be subclassed to implement desired objects (displays, actions...).
	Use signals for value changes or reimplement functions (don't forget to call mother's function)
	'''
	
	idChanged = QtCore.Signal(str)
	valueChanged = QtCore.Signal()
	valueChanged = QtCore.Signal(object)
	rangeChanged = QtCore.Signal(dict)
	
	
	_id = None
	_value = None
	_range = {'min': 0, 'max': 100}
	
	
	def __init__(self):
		QtCore.QObject.__init__(self)
		
		self._id = None
		self._value = None
		self._range = {'min': 0, 'max': 100}
	
	
	def setID(self, functionId):
		''' Set functionality ID (str) '''
		if isinstance(functionId, str):
			self._id = functionId
			self.idChanged.emit(self._id)
		else:
			raise TypeError
	
	def id(self):
		''' Functionality ID '''
		return self._id
	
	
	def setValue(self, value):
		''' Set internal functionality's value '''
		self._value = value
		self.valueChanged.emit(self._value)
	
	def value(self):
		''' Functionality's value '''
		return self._value
	
		
	def setValueRange(self, minValue, maxValue):
		''' Set internal functionality's value range '''
		if isinstance(minValue, str):
			minValue = int(minValue)
		if isinstance(maxValue, str):
			maxValue = int(maxValue)
		
		# Check range correctness. Set to None to don't change the value
		if (minValue < maxValue) or (minValue == None or maxValue == None):
			if minValue != None:
				self._range['min'] = minValue
			
			if maxValue != None:
				self._range['max'] = maxValue
			
			self.rangeChanged.emit(self._range)
			
		else:
			raise ValueError
	
	# def setValueRange(self, valueRange):
	# 	''' Provided for convenience.
	# 	Set the value range from list (min value, max value) or dict ('min':value, 'max':value)
	# 	'''
	# 	if isinstance(valueRange, dict):
	# 		self.setValueRange(valueRange['min'], valueRange['max'])
	# 	elif isinstance(valueRange, list):
	# 		self.setValueRange(valueRange[0], valueRange[1])
	# 	else:
	# 		raise TypeError
	
	def valueRange(self):
		''' Value range (dict {'min':value, 'max':value}) '''
		return self._range
	
	
	

if __name__ == "__main__":
	pass
	