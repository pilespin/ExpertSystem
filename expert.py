#!/usr/bin/python

import re

class Element(object):

	def __init__(self, name="none"):
		self._name = name
		self._status = False
		self._rules = []

	def addRule(self, rule):
		if (rule not in self._rules):
			self._rules.append(rule)
			# print "ADDED RULE: " + rule + " IN " + self._name

	def getName(self):
		return (self._name)

	def getStatus(self):
		return (self._status)

	def getRules(self):
		return (self._rules)

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

###############################################################################

def printAll():
	print "RULES:"
	for elt in rules:
		print(elt)
	print ""

	print "FACT:"
	for elt in facts:
		print(elt)
	print ""

	print "QUERIES:"
	for elt in queries:
		print(elt)
	print ""

def cleanLine(line):
	line = line.strip()
	end = line.find("#")
	if (end == -1):
		end = len(line)
	line = line[0:end]
	line = " ".join(line.split())
	line = line.strip()
	return (line)

def readFile(path):
	rules 	= []
	facts 	= []
	queries	= []

	with open(path) as f:
		for line in f:
			line = cleanLine(line)
			if (len(line) > 0 and line[0] != "#"):
				if (line[0] == "="):
					facts.append(line);
				elif (line[0] == "?"):
					queries.append(line);
				else:
					rules.append(line);
	return(rules, facts, queries)

def splitLogicOperator(string):
	return (re.split('\+|\||\^', string))

def initializeElement():
	elem = {}

	for s in rules:
		iff = False
		if (s.find("<=>") != -1):
			ret = s.split("<=>")
			iff = True
		elif (s.find("=>") != -1):
			ret = s.split("=>")
		else:
			print "ERROR: " + s + " Bad formulation"
			exit(1)

		if (len(ret) != 2):
			print "Error"
			exit(1)
		
		rule = ret[0].strip()
		implies = ret[1].strip()

		if (len(rule) <= 0 or len(implies) <= 0):
			print "Error: " + s
			exit(1)

		for n in splitLogicOperator(rule):
			n = n.strip()
			if (n not in elem):
				elem[n] = Element(n)

		for n in splitLogicOperator(implies):
			n = n.strip()
			if (n not in elem):
				elem[n] = Element(n)
			elem[n].addRule(rule)
	return (elem)

##############################
############ MAIN ############
##############################

rules, facts, queries = readFile('data')
elem = initializeElement()
# printAll()
# print rules

for i in elem:
	print elem[i].printInfoInLine()
