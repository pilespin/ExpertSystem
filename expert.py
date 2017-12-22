#!/usr/bin/python

import re
from Element import Element
from Compute import Compute
from Common import Common

class Expert(Compute, Common):

	def __init__(self):
		self._rules		= []
		self._facts		= []
		self._queries	= []
		self._elem		= {}

	def getAllElement(self):
		return (self._elem)

	def readFile(self, path):
		with open(path) as f:
			for line in f:
				line = self.__cleanLine(line)
				if (len(line) > 0 and line[0] != "#"):
					if (line[0] == "="):
						self.__addFact(self.__cleanLine(line[1:]))
					elif (line[0] == "?"):
						self.__addQueries(self.__cleanLine(line[1:]))
					else:
						self.__addRule(self.__cleanLine(line));

	def __addRule(self, rule):
		left = re.findall('\(', rule)
		right = re.findall('\)', rule)
		if len(left) != len(right):
			print "Bad parenthesis in rule: " + rule
			exit(9)
		self._rules.append(rule);

	def __addFact(self, line):
		if line.find(',') != -1:
			s = line.split(',')
			self.__checkLine(s, "Error when getting fact")
			for x in s:
				self._facts.append(x);
		else:
			for i in line:
				self._facts.append(i);

	def __addQueries(self, line):
		if line.find(',') != -1:
			s = line.split(',')
			self.__checkLine(s, "Error when getting fact")
			for x in s:
				self._queries.append(x);
		else:
			for i in line:
				self._queries.append(i);

	def initialize(self):
		for s in self._rules:
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
				print "Error:"
				exit(1)
			
			rule = ret[0].strip()
			implies = ret[1].strip()

			if (len(rule) <= 0 or len(implies) <= 0):
				print "Error: " + s
				exit(1)

			a = re.findall('\||\^', implies)
			if len(a) >= 1:
				print "implies not allow \"|\" or \"^\" in: " + s
				exit(11)
				
			for n in self.splitLogicOperator(rule):
				n = self.removeParentese(n)
				n = n.strip()
				self.__checkLine(n, rule)
				self.addElement(n)

			for n in self.splitLogicOperator(implies):
				n = n.strip()
				self.__checkLine(n, rule)
				self.addElement(n)
				self.getElement(n).addRule(rule)

			# if iff == True:
			# 	a = re.findall('\||\^', rule)
			# 	if len(a) >= 1:
			# 		print "Biconditional rules not allow \"|\" or \"^\" in: " + s
			# 		exit(11)
			# 	else:
			# 		for n in self.splitLogicOperator(implies):
			# 			n = self.removeParentese(n)
			# 			n = n.strip()
			# 			self.__checkLine(n, implies)
			# 			self.addElement(n)

			# 		# for n in self.splitLogicOperator(rule):
			# 			n = rule.strip()
			# 			self.__checkLine(n, implies)
			# 			self.addElement(n)
			# 			self.getElement(n).addRule(implies)

	def checkQueriesExist(self):
		err = False
		for q in self._queries:
			if q not in self._elem:
				print "Querie not reconized: " + q
				err = True
		if err == True:
			exit(3)

		if (len(self._queries) <= 0):
			print "Missing Queries"
			exit(1)

	def checkFactsExist(self):
		err = False
		for q in self._facts:
			if q not in self._elem:
				print "Fact not reconized: " + q
				err = True
		if err == True:
			exit(3)

	def checkConflict(self):
		conflit = False
		for i in self._elem:
			if self._elem[i].getName()[0] != "!":
				if "!" + i in self._elem:
					for j in self._elem[i].getRules():
						if j in self._elem["!" + i].getRules():
							print "Conflict with rule: " + j + " in " + i
							conflit = True
		if conflit == True:
			exit(2)

	def addElement(self, name):
		if (name not in self._elem):
			self._elem[name] = Element(name)
			if self.__isNegative(name):
				if (name[1:] not in self._elem):
					self._elem[name[1:]] = Element(name[1:])

	def __isNegative(self, name):
		if (len(name) >= 2):
			if name[0] == "!":
				return True
		return False

	def __checkLine(self, line, append):
		if len(line) <= 0:
			print "Error:" + " " + append
			exit(1)

	def __cleanLine(self, line):
		line = line.strip()
		line = re.sub('\s+', '', line)
		line = re.sub('\++', '+', line)
		line = re.sub('\|+', '|', line)
		line = re.sub('\^+', '^', line)
		end = line.find("#")
		if (end == -1):
			end = len(line)
		line = line[0:end]
		line = " ".join(line.split())
		line = line.strip()
		return (line)

	def getElement(self, index, negative=True):

		tmp = re.findall('\_(.*)\_', index)
		if len(tmp) > 0:
			if tmp[0] in self._elem:
				A = self._elem[tmp[0]]
				return(A.getElement(index))
			else:
				print "Element Not found1: " + index
				exit(6)

		if negative == False:
			if len(index) >= 2:
				if index[0] == "!":
					index = index[1:]

		if index in self._elem:
			return (self._elem[index])
		else:
			print "Element Not found2: " + index
			exit(6)

	def setInitialFact(self):
		for i in self._facts:
			self._elem[i].setStatus()
			self._elem[i].setComputed(False)
			self._elem[i].setBeginComputed(False)

	def setInitialFactToFalse(self):
		for i in self._facts:
			self._elem[i].setStatus(False)
			self._elem[i].setComputed(False)

	def showQueries(self):
		for i in sorted(self._elem):
			if self._elem[i].getName()[0] != "!" and i in self._queries:
				self.setInitialFact()
				self.computeQueries(self._elem, i)
				print self._elem[i].getName() + " = " + str(self._elem[i].getStatus())
				self.setInitialFactToFalse()

	def printElement(self):
		for i in sorted(self._elem):
			self._elem[i].printAllInfo()
		print ""

	def printAll(self):
		print "RULES:"
		for elt in self._rules:
			print(elt)
		print ""

		print "FACT:"
		for elt in self._facts:
			print(elt)
		print ""

		print "QUERIES:"
		for elt in self._queries:
			print(elt)
		print ""
