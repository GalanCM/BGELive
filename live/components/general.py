from live.helpers import Timer, clean_name

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
				self.logic_components.add(next_fun, id=id)
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

def uncollide(targets, function):
	''':param targets: Can be str or GameObject
	'''
	def uncollide_callback(self, id):
		for obj in self.hitObjectList:
			for target in targets:
				if type(target) == str and obj.name == target:
					return
				elif type(target) != str and obj.name == target.name:
					return

		function(self, id)

	return uncollide_callback

# def uncollide(obj, targets, callback):
# 	class collision_callback():
# 		def __init__(self, targets):
# 			self._targets = targets
# 			self._hit = False
# 		def __call__(self, obj, id, collider):
# 			for target in self._targets:
# 				print(clean_name(collider))
# 				if collider == target or clean_name(collider) == target:
# 					self._hit = True

# 	class logic_callback():
# 		def __init__(self, callback, collision_id):
# 			self._collision_id = collision_id
# 			self._callback = callback
# 		def __call__(self, obj, id):
# 			if not obj.collision_components.get(self._collision_id)._hit:
# 				self._callback(obj, id)
# 			obj.collision_components.get(self._collision_id)._hit = False



# 	collision_id = obj.collision_components.add( collision_callback(targets) )
# 	return logic_callback(callback, collision_id)