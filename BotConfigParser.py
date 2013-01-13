#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
from PySide import QtGui, QtCore
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import json
from collections import OrderedDict


class BotConfigParser:
	
	
	def loadConfigFile(self, configFileName):
		
		# id type range display group
		settings = QSettings(configFileName, QSettings.IniFormat);
		
		robotData = {}
		
		settings.beginGroup('robot')
		botName = settings.value('name')
		robotData['name'] = botName
		print('Robot name:', botName)
		settings.endGroup()
		
		settings.beginGroup('functionalities')
		
		funcData = OrderedDict()
		
		for group in settings.childGroups():
			settings.beginGroup(group)
			
			tmpDict = OrderedDict()
			
			for key in settings.childKeys():
				tmpDict[key] = settings.value(key)
				#print(group, key, settings.value(key))
			
			funcData[group] = tmpDict
			settings.endGroup()
		settings.endGroup()
		
		#print(funcData)
		return funcData, robotData




def main(args):
	a = QtGui.QApplication(args)
	
	bc = BotConfigParser()
	bc.loadConfigFile('mybot1.bvc')
	
	#r = a.exec_()
	return 0

if __name__ == "__main__":
	main(sys.argv)
	
	