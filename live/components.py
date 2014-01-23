from live.helpers import Timer
from bge import logic

from mathutils import Vector

def timed(fun, time, next_fun=None):
	"""A component that runs another component for a fixed length of time. Can optionally be given a follow-up component for chaining.

	   :param callable fun: The component to be run:
	   :param number time: The amount of time to run the component
	   :keyword callable next_fun: A component to run after the timed component is finished
	"""
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
	"""A component that suspends a component currently in the component list for a fixed length of time. Can optionally be given a different component to be run after the suspension is lifted.

	   :param number time: The amount of time to run the component
	   :keyword callable next_fun: A component to run after the suspension is lifted
	"""
	def suspend_callback(self, id):
		pass
	return timed(suspend_callback, time, next_fun )

def move_to(obj, target, **kwargs):
	"""Move the object to a target position. Can be done using speed, time, or acceleration, but no combination of them.
	   Note: object can still be moved by other applyMovement() calls.

	   :param KX_GameObject obj: The object to move
	   :param 3D Vector target: The world position to move to

	   :keyword number speed: The velocity to move at. In blender units per second

	   :keyword number time: How long you want the object to take to reach its target. In seconds. Speed will be automaticly calculated

	   :keyword number acceleration: How quickly you want the object to accelerate. In blender units per second per second.
	   :keyword number start_speed: (optional) (for acceleration) Initial speed for the object to move at. In blender units per second.
	   :keyword number max_speed: (optional) (for acceleration) Speed at which to stop acceleration. In blender units per second.
	"""
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
		return move_to(obj, target, accel=0, start_speed=speed, max_speed=speed)

	elif 'time' in kwargs:
		for key in kwargs:
			if key != 'time':
				raise TypeError('%s is an invalid keyword argument for this function' % key)
		speed = obj.getDistanceTo(target) / kwargs['time']
		return move_to(obj, target, speed=speed)

	return move_callback