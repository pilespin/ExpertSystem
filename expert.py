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

###############################################################################

def printAll():
	print "RULES:"
	for elt in enumerate(rules):
		print(elt[1])
	print ""

	print "FACT:"
	for elt in enumerate(facts):
		print(elt[1])
	print ""

	print "QUERIES:"
	for elt in enumerate(queries):
		print(elt[1])
	print ""

def readFile(path):
	rules 	= []
	facts 	= []
	queries	= []

	with open(path) as f:
		for line in f:
			line = line.strip()
			line = line[0:line.find("#")]
			if (len(line) > 0 and line[0] != "#"):
				line = " ".join(line.split())
				line = line.strip()
				if (line[0] == "="):
					facts.append(line);
				elif (line[0] == "?"):
					queries.append(line);
				else:
					rules.append(line);
	return(rules, facts, queries)

def initializeElement():
	elem = {}

	for elt in enumerate(rules):
		s = str(elt[1])
		if (s.find("<=>") != -1):
			ret = s.split("<=>")
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

		tab = re.split('\+|\||\^', rule)
		for n in enumerate(tab):
			n = n[1].strip()
			if (n not in elem):
				elem[n] = Element(n)

		tab = re.split('\+|\||\^', implies)
		for n in enumerate(tab):
			n = n[1].strip()
			if (n not in elem):
				elem[n] = Element(n)
			# print "-----INPL: " + rule
			elem[n].addRule(rule)
	return (elem)

##############################
############ MAIN ############
##############################

rules, facts, queries = readFile('data')
elem = initializeElement()
printAll()
print elem

print elem["A"].printInfo()
print elem["B"].printInfo()
print elem["C"].printInfo()
print elem["D"].printInfo()
