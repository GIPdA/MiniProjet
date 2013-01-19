#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore, QtDeclarative
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from functionality import Functionality


class Display(Functionality, QWidget):
	''' Base class for display objects '''
	
	_widget = None
	_vbx = None
	name = ''
	
	def __init__(self, displayID, friendlyName):
		Functionality.__init__(self)
		QWidget.__init__(self)
		
		# Create empty layout
		self._vbx = QtGui.QGridLayout(self)
		self._vbx.setContentsMargins(0, 0, 0, 0)
		self._vbx.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		
		self.setID(displayID)
		self.name = friendlyName
	
	
	def setWidget(self, widget, row=1, col=1):
		''' Private - Set widget to display '''
		self._vbx.removeWidget(self._widget) # Remove current widget ##TODO: is that necessary ??
		self._widget = widget
		self._vbx.addWidget(self._widget, row, col) # Add widget to layout
	
	def widget(self):
		''' Display widget '''
		return self._widget



class Led(Display):
	''' Display a radio button as a LED '''
	
	def __init__(self, displayID, friendlyName, showID = False):
		''' displayID: object id
		showID: True to show id as radio button text
		'''
		Display.__init__(self, displayID, friendlyName)
		
		self.setWidget(QtGui.QRadioButton(friendlyName if showID else ''))
		
		self.widget().toggled.connect(self._ledStateChanged)
	
	
	def _ledStateChanged(self, state):
		self.setValue(state, _emitChange=True)	# Emit valueChanged signal
	
	def setValue(self, value, _emitChange=False):
		''' Reimplement setValue to update the radio button.
		Raise TypeError if value not a bool.
		'''
		Display.setValue(self, value, _emitChange)
		
		if isinstance(value, bool):
			if not _emitChange:	# If not called from _ledStateChanged
				self.widget().blockSignals(True)
				self.widget().setChecked(value)
				self.widget().blockSignals(False)
		else:
			raise TypeError(str(value.__class__) + ' type not allowed fo Led')


class ProgressBar(Display):
	''' Display a progress bar '''
	
	def __init__(self, displayID, friendlyName, data = None, \
	             valueFormatting = None, valueBefore = False):
		Display.__init__(self, displayID, friendlyName)
		
		
		pgb = QtGui.QProgressBar()
		self.setWidget(pgb)
		
		if 'vertical' in data:
			pgb.setOrientation(Qt.Vertical if data['vertical'] else Qt.Horizontal)
		
		if 'range' in data:
			self.setValueRange(data['range'][0], data['range'][1])
			
		pgb.setMinimum(self.valueRange()['min'])
		pgb.setMaximum(self.valueRange()['max'])
		
		# Add text before or after
		if valueFormatting:	# ex. 'The value: {0}'
			self._textValue = QLabel()
			self._textValue.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
			self._valueFormatting = valueFormatting
			
			if 'vertical' in data and not data['vertical']:
				if valueBefore:
					self._vbx.addWidget(self._textValue, 1, 0)
				else:
					self._vbx.addWidget(self._textValue, 1, 2)
			else:
				if valueBefore:
					self._vbx.addWidget(self._textValue, 0, 1)
				else:
					self._vbx.addWidget(self._textValue, 2, 1)
			
			self.setValue(0)
	
	
	def setValue(self, value):
		''' Reimplement setValue to update the progress bar.
		Raise TypeError if value not a int.
		'''
		Display.setValue(self, value, emitChange=False)
		
		if isinstance(value, int):
			self.widget().setValue(value)
			if hasattr(self, '_textValue'):
				self._textValue.setText(self._valueFormatting.format(value))
		else:
			raise TypeError(str(value.__class__) + ' type not allowed fo ProgressBar')
	
	def setValueRange(self, minValue, maxValue):
		
		self.widget().setMinimum(minValue)
		self.widget().setMaximum(maxValue)
		
		Display.setValueRange(minValue, maxValue)


class Slider(Display):
	''' Display a slider '''
	
	def __init__(self, displayID, friendlyName, data = None, \
	             valueFormatting = None, valueBefore = False):
	             #invert = False):
		
		Display.__init__(self, displayID, friendlyName)
		
		
		sld = QtGui.QSlider()
		self.setWidget(sld)
		
		if 'vertical' in data:
			sld.setOrientation(Qt.Vertical if data['vertical'] else Qt.Horizontal)
		
		# if invert:
		# 	sld.setInvertedAppearance(True)
		
		if 'range' in data:
			self.setValueRange(data['range'][0], data['range'][1])
			
		sld.setMinimum(self.valueRange()['min'])
		sld.setMaximum(self.valueRange()['max'])
		
		# Connection
		sld.valueChanged.connect(self._sliderValueChanged)
		
		# Add text before or after
		if valueFormatting:	# ex. 'The value: {0}'
			self._textValue = QLabel()
			self._textValue.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
			self._valueFormatting = valueFormatting
			
			if 'vertical' in data and not data['vertical']:
				if valueBefore:
					self._vbx.addWidget(self._textValue, 1, 0)
				else:
					self._vbx.addWidget(self._textValue, 1, 2)
			else:
				if valueBefore:
					self._vbx.addWidget(self._textValue, 0, 1)
				else:
					self._vbx.addWidget(self._textValue, 2, 1)
			
			self.setValue(0)
	
	def _sliderValueChanged(self, value):
		''' Slider value changed (by user), update internal functionality's value '''
		self.setValue(value, _emitChange=True)
	
	def setValue(self, value, _emitChange=False):
		''' Reimplement setValue to update the slider.
		Raise TypeError if value not a int.
		'''
		Display.setValue(self, value, _emitChange)
		
		if isinstance(value, int):
			if not _emitChange:	# If not called from _sliderValueChanged
				self.widget().blockSignals(True)
				self.widget().setValue(value)
				self.widget().blockSignals(False)
			if hasattr(self, '_textValue'):
				self._textValue.setText(self._valueFormatting.format(value))
		else:
			raise TypeError 
	
	def setValueRange(self, minValue, maxValue):
		
		self.widget().setMinimum(minValue)
		self.widget().setMaximum(maxValue)
		
		Display.setValueRange(self, minValue, maxValue)


class Dial(Display):
	''' Display a dial '''
	
	def __init__(self, displayID, friendlyName, data = None, \
	             valueFormatting = None, valueBefore = False):#, \
	             #invert = False):
		
		Display.__init__(self, displayID, friendlyName)
		
		
		dial = QtGui.QDial()
		
		self.setWidget(dial)
		
		if 'vertical' in data:
			dial.setOrientation(Qt.Vertical if data['vertical'] else Qt.Horizontal)
		
		# if invert:
		# 	dial.setInvertedAppearance(True)
			
		if 'range' in data:
			self.setValueRange(data['range'][0], data['range'][1])
		
		dial.setMinimum(self.valueRange()['min'])
		dial.setMaximum(self.valueRange()['max'])
		
		# Connection
		dial.valueChanged.connect(self._dialValueChanged)
		
		# Add text before or after
		if valueFormatting:	# ex. 'The value: {0}'
			self._textValue = QLabel()
			self._textValue.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
			self._valueFormatting = valueFormatting
			
			if 'vertical' in data and not data['vertical']:
				if valueBefore:
					self._vbx.addWidget(self._textValue, 1, 0)
				else:
					self._vbx.addWidget(self._textValue, 1, 2)
			else:
				if valueBefore:
					self._vbx.addWidget(self._textValue, 0, 1)
				else:
					self._vbx.addWidget(self._textValue, 2, 1)
			
			self.widget().blockSignals(True)
			self.setValue(0)
			self.widget().blockSignals(False)
	
	
	def _dialValueChanged(self, value):
		''' Dial value changed (by user), update internal functionality's value '''
		self.setValue(value, _emitChange=True)
	
	def setValue(self, value, _emitChange=False):
		''' Reimplement setValue to update the dial.
		Raise TypeError if value not a int.
		'''
		Display.setValue(self, value, _emitChange)
		
		if isinstance(value, int):
			if not _emitChange:	# If not called from _dialValueChanged
				self.widget().blockSignals(True)
				self.widget().setValue(value)
				self.widget().blockSignals(False)
			if hasattr(self, '_textValue'):
				self._textValue.setText(self._valueFormatting.format(value))
		else:
			raise TypeError 
	
	def setValueRange(self, minValue, maxValue):
		
		self.widget().setMinimum(minValue)
		self.widget().setMaximum(maxValue)
		
		Display.setValueRange(self, minValue, maxValue)
	
	# def setValueRange(self, valueRange):
	# 	Display.setValueRange(self, valueRange)
		
	# 	self.widget().setMinimum(self.valueRange['min'])
	# 	self.widget().setMaximum(self.valueRange['max'])


class Alphanum(Display):
	''' Display an alphanumeric "screen" '''
	
	def __init__(self, displayID, friendlyName):
		
		Display.__init__(self, displayID, friendlyName)
		
		te = QTextEdit()
		
		self.setWidget(te)
		self.widget().setMaximumHeight(60)
		
		self._vbx.setVerticalSpacing(1)
		
		self._wordCount = QLabel()
		self._vbx.addWidget(self._wordCount, 2, 1)
		
		# Connection
		te.textChanged.connect(self._textChanged)
	
	
	def _textChanged(self):
		''' Text changed (by user), update internal functionality's value '''
		Display.setValue(self, self.widget().toPlainText())
		self._wordCount.setText('Word count: ' + str(len(self.widget().toPlainText())))
	
	def setValue(self, value):
		''' Reimplement setValue to update the dial.
		Raise TypeError if value not a int.
		'''
		Display.setValue(self, value, emitChange=False)
		
		if isinstance(value, str):
			self.widget().blockSignals(True)
			self.widget().setText(value)
			self.widget().blockSignals(False)
		else:
			raise TypeError('"str" is the only type allowed.')



class QMLWidget(Display):
	
	def __init__(self, displayID, friendlyName, qmlFile):
		Display.__init__(self, displayID, friendlyName)
		
		qmlView = QDeclarativeView()
		
		qmlView.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
		
		# QML source file
		qmlView.setSource(QUrl.fromLocalFile(qmlFile))
		# QML resizes to main window
		qmlView.setResizeMode(QDeclarativeView.SizeRootObjectToView)
		
		self._vbx.setContentsMargins(0, 0, 0, 0)
		
		self.setWidget(qmlView)


