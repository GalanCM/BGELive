from live.helpers import Timer
from bge import logic

from mathutils import Vector
from math import degrees

def timed(fun, time, next_fun=None):
	timer = Timer(time)
	def timed_callback(self, id):
		nonlocal timer
		if timer > 0.0:
			fun(self, id)
		else:
			if next_fun:
				self.logic_components.set(next_fun, id=id)
			else:
				self.logic_components.remove(id)
	return timed_callback

def suspend(time, next_fun):
	def suspend_callback(self, id):
		pass
	return timed(suspend_callback, time, next_fun )

def move_to(self, target, **kwargs):
	if 'accel' in kwargs:
		for key in kwargs.keys():
			if key not in ('accel', 'start_speed', 'max_speed'):
				raise TypeError('%s is an invalid keyword argument for this function' % key)
		accel = kwargs['accel']
		current_speed = kwargs['start_speed'] if 'start_speed' in kwargs else 0.0
		max_speed = kwargs['max_speed'] if 'max_speed' in kwargs else False

		target = Vector(target)
		stop_next = False
		def move_callback(self, id):
			nonlocal stop_next, current_speed

			if not stop_next:
				if max_speed == False or current_speed < max_speed:
					current_speed += accel / (logic.getLogicTicRate()+1.0)
				elif current_speed > max_speed:
					current_speed = max_speed
				self.applyMovement( self.getVectTo(target)[1] * current_speed )
				if self.getDistanceTo(target) - current_speed < 0.0:
					stop_next = True
			else:
				self.worldPosition = target
				current_speed = 0.0
				self.logic_components.remove(id)

	elif 'speed' in kwargs:
		for key in kwargs:
			if key != 'speed':
				raise TypeError('%s is an invalid keyword argument for this function' % key)
		speed = kwargs['speed'] / (logic.getLogicTicRate()+1.0)
		return move_to(self, target, accel=0, start_speed=speed, max_speed=speed)

	elif 'time' in kwargs:
		for key in kwargs:
			if key != 'time':
				raise TypeError('%s is an invalid keyword argument for this function' % key)
		speed = self.getDistanceTo(target) / kwargs['time']
		return move_to(self, target, speed=speed)

	return move_callback