#!/usr/bin/python

import re
from Element import *

class Compute(object):

	def __init__(self):
		pass

	def computeQueries(self, allElem, elem):
		rules1 = self.getElement(elem).getRules()
		self.computeNaturalRule(elem, rules1)

		rules2 = None
		if ("!" + elem in allElem):
			# print "OPOSITE EXIST"
			rules2 = self.getElement("!" + elem).getRules()
			self.computeNaturalRule("!" + elem, rules2)
			# print self.getElement("!" + elem).getStatus()
			if self.getElement("!" + elem).getStatus() == True:
				self.getElement(elem).setStatus(False)

			# print "COMPUTED"

			# if ret1 == True and ret2 == True:
			# 	print "Conflict with element " + elem
			# 	exit(7)

	def computeNaturalRule(self, elem, rules):
		# print elem + " --- " + str(rules)
		for i in rules:
			ret = self.computeSimpleNaturalRule(i)
			# print elem
			# print ret
			if ret == True:
				self.getElement(elem).setStatus()
				# self.getElement(elem).setStatus(string=elem)
				self.getElement(elem).setComputed()
				# return True
		# return False

	def computeSimpleNaturalRule(self, rule):
		# print "Rule: " + rule
		ret = self.splitLogicOperator(rule)
		# print ret
		if len(ret) == 1:
			# print ret[0]
			A = self.getElement(ret[0])
			if (self.getElement(A.getName(), negative=False).getComputed() == False):
				self.computeQueries(self._elem, A.getName())
			ret = A.getStatus(ret[0])
			# print str(A.getName())
			# print ret
			# ret = self.getElement(ret[0]).getStatus(ret[0])
			# print ret
		elif len(ret) >= 3:
			ret = self.parseLongRule(rule)
			# return False
		else:
			A, operator, B = self.parseSimpleRule(rule)
			ret = self.compute(A, operator, B)
		# print ret
		return ret

	def parseLongRule(self, rule):
		elm = self.splitLogicOperator(rule)
		opr = re.findall(self.regexOperator, rule)

		if (len(elm) <= 1 and len(opr) <= 0 and len(opr) != len(elm) - 1):
			print "Error when parsing: " + rule
			exit(7)

		ret = self.getElement(elm[0], negative=False).getStatus(elm[0])

		for i in range(len(opr)):

			cur = elm[i]
			nxt = elm[i+1]

			# A, operator, B = self.parseSimpleRule(cur + opr[i] + nxt)
			# A = self.getElement(cur)
			B = self.getElement(nxt, negative=False).getStatus(nxt)
			# print "COMPUTE: " + opr[i] + nxt
			# print "COMPUTE: " + str(ret) + opr[i] + str(B)
			ret = self.compute(ret, opr[i], B)
		
		# print elm
		# print opr
		# print ret

		return ret

	def parseSimpleRule(self, rule):
		ret = self.splitLogicOperator(rule)
		operator = re.findall(self.regexOperator, rule)
		if (len(operator) <= 0):
			print "Error when parsing: " + rule
			exit(1)
		operator = operator[0]
		if (len(ret) != 2 and operator is not None):
			print "Error when parsing: " + rule
			exit(1)
		A = self.getElement(ret[0], negative=False)
		B = self.getElement(ret[1], negative=False)
		# print str(A.getName()) + " " + operator + " " + str(B.getName())
		# print str(A.getStatus()) + " " + operator + " " + str(B.getStatus())
		# print A.getName()
		# print A.getStatus(ret[0])
		# print B.getName()
		# print B.getStatus(ret[1])
		if (A.getComputed() == False):
			self.computeQueries(self._elem, A.getName())
		if (B.getComputed() == False):
			self.computeQueries(self._elem, B.getName())
			# print A.getStatus(ret[0])
			# print B.getStatus(ret[1])
		return (A.getStatus(ret[0]), operator, B.getStatus(ret[1]))

	def compute(self, A, operator, B):
		if operator == '+':
			if A == True and B == True:
				return True
			else:
				return False
		if operator == '|':
			if A == True or B == True:
				return True
			else:
				return False
		if operator == '^':
			if A == True and B == False:
				return (True)
			if A == False and B == True:
				return True
			else:
				return False
		else:
			print "Operator not found"
			exit(4)
