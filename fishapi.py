#!/usr/bin/python
"""Functions to share with modules isolated from the Fishbot object."""
import importer
import sys, os, time, string
import urllib, re
import chesterfield

#version - string set by main class
#execution_time - time set by main class

def getnick(s):
	"""Return an IRC nick from an IRC hostmask"""
	n = s.find("!")
	if n > -1:
		return s[:n]
	else:
		return s

def http_grep(url, regexp):
	"""Search the page returned by 'url' line by line for 'regexp'.

	Returns the first matching groups."""
	page = urllib.urlopen(url).readlines()
	for each in page:
		search = re.search(regexp, each, re.M)
		if search:
			return search.groups()

# Chesterfield derived objects
database = chesterfield.Chesterfield(user='fishbot', host='localhost', database='fishbot')
DatabaseObject = database.object
#ReadOnlyDatabaseObject = chesterfield.DatabaseObject(user='fishbotread', host='localhost', database='fishbot')

class Counter(DatabaseObject):
	"Count things!"
	name = "" # name of the counter
	count = 0 # the count
