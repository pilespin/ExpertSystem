#!/usr/bin/python

import re

class Element(object):

	def __init__(self, name="none", status=False):
		self._name = name
		self._status = status
		self._computed = False
		self._rules = []

	def addRule(self, rule):
		if (rule not in self._rules):
			# rule = re.sub('\s+', '', rule)
			self._rules.append(rule)
			# print "ADDED RULE: " + rule + " IN " + self._name

	########## GETTER ##########

	def getComputed(self):
		return (self._computed)

	def getName(self):
		return (self._name)

	def getStatus(self, string=''):
		if len(string) > 0 and string[0] == "!":
			return (not self._status)
		return (self._status)

	def getRules(self):
		return (self._rules)
	#############################

	########## SETTER ##########
	def setStatus(self, value=True):
		self._status = value

	def setComputed(self, value=True):
		self._computed = value
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
