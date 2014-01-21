from bge import logic
from time import time

import re
name_suffix_regex = re.compile('\.[0-9]{3}$')

class Timer():
	'''a timer that takes in time in seconds, and counts down to zero. Returns time remain in seconds, or 0.0 if finished.'''
	
	def __init__(self, seconds = 0.0):
		self._time_of_end = time() + seconds #set the time() at which the timer == 0.0

	def __get__(self):
		if self._time_of_end - time() > 0:
			return self._time_of_end - time()
		else:
			return 0.0
	def __str__(self):
		return str( self.__get__() )

	def __repr__(self):
		return self.__str__()

	def __gt__(self, other):
		return self.__get__() > other
	def __lt__(self, other):
		return self.__get__() < other
	def __eq__(self, other):
		return self.__get__() == other
	def __float__(self):
		return float(self.__get__())

		

get_scene = logic.getCurrentScene

####### TEST!!! #######
def get_owner():
	return logic.getCurrentController().owner

def clean_name(obj):
	if name_suffix_regex.search(obj.name) != None:
		return obj.name[0:-4]

def find_object(name, list=get_scene().objects):
	for obj in list:
		if name == obj.name or name == clean_name(obj):
			return obj
	return None

def find_objects(name, list=get_scene().objects):
	results = []
	for obj in list:
		if name == obj.name or name == clean_name(obj):
			results += [obj]
	if results != []:
		return results
	else:
		return None