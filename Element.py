#!/usr/bin/python

import re
from Common import Common

class Element(Common):

	def __init__(self, name="none", status=False):
		self._index = 0
		self._name = name
		self._status = status
		self._computed = False
		self._rules = []
		self._subRules = []
		self._elem = {}

	# def splitLogicOperator(self, string):
	# 	return (re.split(self.regexOperator, string))

	def addElement(self, name):
		if (name not in self._elem):
			self._elem[name] = Element(name)
			# if self.__isNegative(name):
				# if (name[1:] not in self._elem):
					# self._elem[name[1:]] = Element(name[1:])
			print "ADD " + name

	def getNewIndex(self):
		self._index = self._index + 1
		return ("_" + self.getName() + str(self._index))

	def getNextIndex(self):
		# self._index = self._index
		return ("_" + self.getName() + str(self._index + 1))

	def getSubParenthesis(self, rule):
		par = re.findall('\(.*\)', rule)
		if len(par) > 0:
			par = par[0]
		if (len(par) > 0):
			return (par);
		return (None)

	def createSubRule(self, rule):
		if self.checkLine(rule):
			par = self.getSubParenthesis(rule)
			if (par != None):
				newIndex = self.getNewIndex()
				if (self._index == 1):
					tmp = re.sub(re.escape(par), newIndex, rule)
					print " --- ADD RULE: " + tmp
					self._rules.append(tmp)
				
				elm = self.splitLogicOperator(self.removeParentese(rule))
				if self.getName() not in elm:
					pass
				else:
					print "Impliqued element \"" + self.getName() + "\" not have to be in rule: " + rule
					exit(8)
				
				rule = self.removeLastParentese(par)
				tmp = re.sub(re.escape(rule), newIndex, rule)
				nextIndex = self.getNextIndex()

				par = self.getSubParenthesis(rule)
				if (par != None):
					r = re.sub(re.escape(par), nextIndex, rule) 
					self._subRules.append(r + "=>" + newIndex)
					self.addElement(newIndex)
					self._elem[newIndex].addRule(r)
				else:
					self._subRules.append(rule + "=>" + newIndex)
					self.addElement(newIndex)
					self._elem[newIndex].addRule(rule)

				return (rule)
		return (None)

	def addRule(self, rule):
		par = re.findall('\(.*\)', rule)
		if len(par) > 0:
			print "ENTER SUB RULE"
			rule = self.createSubRule(rule)
			while rule != None:
				rule = self.createSubRule(rule)
		else:
			print "ENTER NORMAL RULE"
			if (rule not in self._rules):
				# rule = re.sub('\s+', '', rule)
				elm = self.splitLogicOperator(rule)
				if self.getName() not in elm:
					self._rules.append(rule)
				else:
					print "Impliqued element \"" + self.getName() + "\" not have to be in rule: " + rule
					exit(8)
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

	def getElement(self, index):
		# print "------------- IN ELEMENT GET " + index + " I'M IN " + self.getName()
		# print self._elem
		if index in self._elem:
			return (self._elem[index])
		else:
			print "Element Not found: " + index
			exit(6)

	def getSubRules(self):
		return (self._subRules)
	#############################

	########## SETTER ##########
	def setStatus(self, value=True, string=''):
		if len(string) > 0 and string[0] == "!":
			self._status = not value
			# print "set status" + string + str(self._status)
		else:
			self._status = value

	def setComputed(self, value=True):
		self._computed = value
	#############################

	def printInfo(self):
		print 	"Name:   \"" 	+ self.getName() + "\"" + \
				"	Status: " 	+ str(self.getStatus()) + \
				"	Rules: " 	+ str(self.getRules())	+ \
				"" 	+ str(self.getSubRules())

	def printAllInfo(self):
		print 	"Name:   \"" 	+ self.getName() + "\"" + \
				"	Status: " 	+ str(self.getStatus()) + \
				"	Rules: " 	+ str(self.getRules())	+ \
				"" 	+ str(self.getSubRules())
				# "" 	+ str(self._elem)
		if len(self._elem) > 0:
			print "---------- SUB of " + self.getName() + "-------------"
			for i in self._elem:
				self._elem[i].printInfo()
			print "--------------------------------"
