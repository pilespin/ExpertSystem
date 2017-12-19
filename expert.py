#!/usr/bin/python

import re
from Element import *

class Expert(object):

	def __init__(self, data):
		self._rules		= []
		self._facts		= []
		self._queries	= []
		self._elem		= {}

		self.__readFile(data)
		self.__initializeElement()

		if (len(self._queries) <= 0):
			print "Missing Queries"
			exit(1)

		self._facts = self._facts[0].split(" ")
		self._queries = self._queries[0].split(" ")

	def __readFile(self, path):
		with open(path) as f:
			for line in f:
				line = self.__cleanLine(line)
				if (len(line) > 0 and line[0] != "#"):
					if (line[0] == "="):
						self._facts.append(self.__cleanLine(line[1:]));
					elif (line[0] == "?"):
						self._queries.append(self.__cleanLine(line[1:]));
					else:
						self._rules.append(line);

	def __initializeElement(self):
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
				print "Error"
				exit(1)
			
			rule = ret[0].strip()
			implies = ret[1].strip()

			if (len(rule) <= 0 or len(implies) <= 0):
				print "Error: " + s
				exit(1)

			for n in self.__splitLogicOperator(rule):
				n = n.strip()
				self.__checkLine(n)
				if (n not in self._elem):
					self._elem[n] = Element(n)

			for n in self.__splitLogicOperator(implies):
				n = n.strip()
				self.__checkLine(n)
				if (n not in self._elem):
					self._elem[n] = Element(n)
				self._elem[n].addRule(rule)

	def __checkLine(self, line):
		if len(line) <= 0:
			print "Error"
			exit(1)

	def __cleanLine(self, line):
		line = line.strip()
		end = line.find("#")
		if (end == -1):
			end = len(line)
		line = line[0:end]
		line = " ".join(line.split())
		line = line.strip()
		return (line)

	def __splitLogicOperator(self, string):
		return (re.split('\+|\||\^', string))

	def initializeFact(self):
		for i in self._facts:
			self._elem[i].setStatus()

	def showQueries(self):
		for i in self._elem:
			if self._elem[i] and self._elem[i].getName()[0] != "!" and i in self._queries:
				print self._elem[i].getName() + " = " + str(self._elem[i].getStatus())

	def printElement(self):
		for i in self._elem:
			print self._elem[i].printInfoInLine()

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
