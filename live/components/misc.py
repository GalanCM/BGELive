from live.helpers import Timer

def timed(fun, time, next_fun=None):
	"""A component that runs another component for a fixed length of time. Can optionally be given a follow-up component for chaining.

	   :param callable fun: The component to be run:
	   :param number time: The amount of time to run the component
	   :keyword callable next_fun: A component to run after the timed component is finished
	"""
	timer = Timer(time)
	def timed_callback(self, id, *args):
		nonlocal timer
		if timer > 0.0:
			fun(self, id)
		else:
			if len(args) == 0:
				correct_queue = self.logic_components
			else:
				correct_queue = self.collision_components

			if next_fun:
				correct_queue.set(next_fun, id=id)
			else:
				correct_queue.remove(id)
	return timed_callback

def suspend(time, next_fun):
	"""A component that suspends a component currently in the component list for a fixed length of time. Can optionally be given a different component to be run after the suspension is lifted.

	   :param number time: The amount of time to run the component
	   :keyword callable next_fun: A component to run after the suspension is lifted
	"""
	def suspend_callback(self, id):
		pass
	return timed(suspend_callback, time, next_fun )