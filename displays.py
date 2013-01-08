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
	
	def __init__(self, displayID):
		Functionality.__init__(self)
		QWidget.__init__(self)
		
		# Create empty layout
		self._vbx = QtGui.QVBoxLayout(self)
		
		self.setID(displayID)
	
	
	def setWidget(self, widget):
		''' Private - Set widget to display '''
		self._vbx.removeWidget(self._widget) # Remove current widget ##TODO: is that necessary ??
		self._widget = widget
		self._vbx.addWidget(self._widget) # Add widget to layouts
	
	def widget(self):
		''' Display widget '''
		return self._widget



class Led(Display):
	''' Display a radio button as a LED '''
	
	def __init__(self, displayID, showID = False):
		''' displayID: object id
		showID: True to show id as radio button text
		'''
		Display.__init__(self, displayID)
		
		self.setWidget(QtGui.QRadioButton(self.id() if showID else ''))
	
	
	def setValue(self, value):
		''' Reimplement setValue to update the radio button.
		Raise TypeError if value not a bool.
		'''
		Display.setValue(self, value)
		
		if isinstance(value, bool):
			self.widget().setChecked(value)
		else:
			raise TypeError


class ProgressBar(Display):
	''' Display a progress bar '''
	
	def __init__(self, displayID, \
	             valueFormatting = None, valueBefore = False, valueRange = None, \
	             vertical = False):
		Display.__init__(self, displayID)
		
		if valueRange:
			self.setValueRange(valueRange)
		
		pgb = QtGui.QProgressBar()
		self.setWidget(pgb)
		
		pgb.setOrientation(Qt.Vertical if vertical else Qt.Horizontal)
		
		pgb.setMinimum(self.valueRange()['min'])
		pgb.setMaximum(self.valueRange()['max'])
		
		# Add text before or after
		if valueFormatting:	# ex. 'The value: {0}'
			self._textValue = QLabel()
			self._valueFormatting = valueFormatting
			self._vbx.setDirection(QBoxLayout.LeftToRight)
			
			if valueBefore:
				self._vbx.insertWidget(0, self._textValue)
			else:
				self._vbx.addWidget(self._textValue)
	
	
	def setValue(self, value):
		''' Reimplement setValue to update the progress bar.
		Raise TypeError if value not a int.
		'''
		Display.setValue(self, value)
		
		if isinstance(value, int):
			self.widget().setValue(value)
			if hasattr(self, '_textValue'):
				self._textValue.setText(self._valueFormatting.format(value))
		else:
			raise TypeError


class Slider(Display):
	''' Display a slider '''
	
	def __init__(self, displayID, \
	             valueFormatting = None, valueBefore = False, valueRange = None, \
	             vertical = False, \
	             tickInterval = None, invert = False):
		
		Display.__init__(self, displayID)
		
		if valueRange:
			self.setValueRange(valueRange)
		
		sld = QtGui.QSlider()
		sld.valueChanged.connect(self._sliderValueChanged)
		
		self.setWidget(sld)
		
		sld.setOrientation(Qt.Vertical if vertical else Qt.Horizontal)
		
		if invert:
			sld.setInvertedAppearance(True)
		
		sld.setMinimum(self.valueRange()['min'])
		sld.setMaximum(self.valueRange()['max'])
		
		# Add text before or after
		if valueFormatting:	# ex. 'The value: {0}'
			self._textValue = QLabel()
			self._valueFormatting = valueFormatting
			self._vbx.setDirection(QBoxLayout.LeftToRight)
			
			if valueBefore:
				self._vbx.insertWidget(0, self._textValue)
			else:
				self._vbx.addWidget(self._textValue)
	
	def _sliderValueChanged(self, value):
		''' Slider value changed (by user), update internal functionality's value '''
		self.setValue(value)
	
	def setValue(self, value):
		''' Reimplement setValue to update the slider.
		Raise TypeError if value not a int.
		'''
		Display.setValue(self, value)
		
		if isinstance(value, int):
			self.widget().setValue(value)
			if hasattr(self, '_textValue'):
				self._textValue.setText(self._valueFormatting.format(value))
		else:
			raise TypeError 


class QMLWidget(Display):
	
	def __init__(self, displayID, qmlFile):
		Display.__init__(self, displayID)
		
		qmlView = QDeclarativeView()
		
		qmlView.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
		
		# QML source file
		qmlView.setSource(QUrl.fromLocalFile(qmlFile))
		# QML resizes to main window
		qmlView.setResizeMode(QDeclarativeView.SizeRootObjectToView)
		
		self._vbx.setContentsMargins(0, 0, 0, 0)
		
		self.setWidget(qmlView)
	
	
	
	