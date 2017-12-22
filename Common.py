#!/usr/bin/python

import re
# from Element import Element

class Common(object):

	regexOperator = '\+|\||\^'

	def __init__(self):
		pass

	def removeLastParentese(self, rule):
		rule = re.sub("\)$", "", rule)
		rule = re.sub("^\(", "", rule)
		return (rule)

	def removeParentese(self, rule):
		rule = re.sub("\)", "", rule)
		rule = re.sub("\(", "", rule)
		return (rule)

	def splitLogicOperator(self, string):
		if self.checkLine(string):
			# print "SPLIT: " + string
			return (re.split(self.regexOperator, string))
		return ([])

	def checkLine(self, string):
		if string != None and len(string) >= 1:
			return(string)
		else:
			return(None)

