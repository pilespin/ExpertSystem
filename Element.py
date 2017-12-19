#!/usr/bin/python

import re

class Element(object):

	def __init__(self, name="none"):
		self._name = name
		self._status = False
		self._rules = []

	def addRule(self, rule):
		if (rule not in self._rules):
			# rule = re.sub('\s+', '', rule)
			self._rules.append(rule)
			# print "ADDED RULE: " + rule + " IN " + self._name

	########## GETTER ##########
	def getName(self):
		return (self._name)

	def getStatus(self):
		return (self._status)

	def getRules(self):
		return (self._rules)
	#############################

	########## SETTER ##########
	def setStatus(self, value=True):
		self._status = value
	#############################

	def printInfo(self):
		print "Name:   \"" + self._name + "\""
		print "Status: " + str(self._status)
		print "Rules: "
		print self._rules
		print ""

	def printInfoInLine(self):
		print 	"Name:   \"" 	+ self.getName() + "\"" + \
				"	Status: " 	+ str(self.getStatus()) + \
				"	Rules: " 	+ str(self.getRules())
