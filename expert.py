#!/usr/bin/python

import re
from Element import *

class Expert(object):

	def __init__(self, data):
		self.rules 		= []
		self.facts 		= []
		self.queries 	= []
		self.elem 		= {}

		self.readFile(data)
		self.initializeElement()

		if (len(self.queries) <= 0):
			print "Missing Queries"
			exit(1)

		self.facts = self.facts[0].split(" ")
		self.queries = self.queries[0].split(" ")

	def readFile(self, path):
		with open(path) as f:
			for line in f:
				line = self.cleanLine(line)
				if (len(line) > 0 and line[0] != "#"):
					if (line[0] == "="):
						self.facts.append(self.cleanLine(line[1:]));
					elif (line[0] == "?"):
						self.queries.append(self.cleanLine(line[1:]));
					else:
						self.rules.append(line);

	def initializeElement(self):
		for s in self.rules:
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

			for n in self.splitLogicOperator(rule):
				n = n.strip()
				if (n not in self.elem):
					self.elem[n] = Element(n)

			for n in self.splitLogicOperator(implies):
				n = n.strip()
				if (n not in self.elem):
					self.elem[n] = Element(n)
				self.elem[n].addRule(rule)

	def cleanLine(self, line):
		line = line.strip()
		end = line.find("#")
		if (end == -1):
			end = len(line)
		line = line[0:end]
		line = " ".join(line.split())
		line = line.strip()
		return (line)

	def splitLogicOperator(self, string):
		return (re.split('\+|\||\^', string))

	def printAll(self):
		print "RULES:"
		for elt in self.rules:
			print(elt)
		print ""

		print "FACT:"
		for elt in self.facts:
			print(elt)
		print ""

		print "QUERIES:"
		for elt in self.queries:
			print(elt)
		print ""	
