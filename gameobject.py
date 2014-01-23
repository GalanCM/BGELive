from random import getrandbits
from functools import partial

from bge import logic, types, events
from mathutils import Vector, Matrix

from math import radians

class FunctionQueue():
	def __init__(self, owner, *args):
		self._queue = {}
		self._garbage = []
		self._owner = owner
		if (args):
			self.owner = args[0]

	def set(self, fun, *args, **kwargs):
		"""Set a component.

			:param function fun: function to use as component
			:keyword hashable id: [optional] a hashable value used to reference the component 
			Additional arguments to be used by the component may also be passed in. These arguments will be passed to the component each time it is called.

			:return: the reference id used for the component. If one is passed in by the user, this will be returned. Otherwise, it will be a randomly generated integer
			:rtype: int or other hashable
		"""
		if 'id' in kwargs:
			id = kwargs.pop('id')
		else:
			while True:
				id = getrandbits(32)
				if id not in self._queue:
					break
		self._queue[id] = ( partial(fun, self._owner, id), kwargs.get('pause_when') )
		return id

	def get(self, id):
		"""Retrieve a function from the component list

		:param hashable id: the id of the function to return

		:return: The function stored in the queue with the given id
		:rtype: function
		"""

		return self._queue[id][0].func

	def remove(self, id):
		"""Remove a function from the component list

		:param hashable id: the id of the function to remove
		"""
		self._garbage.append(id)

	def _run(self):
		"""Run the queue"""
		for queue_item in self._queue.values():
			pause_states = logic.getCurrentScene().get('pause_states')
			if pause_states == [] or pause_states == None:
				queue_item[0]()
			else:
				pause_this = False
				for state in pause_states:
					if state in queue_item:
						pause_this = True
				if not pause_this:
					queue_item[0]()
		for id in self._garbage:
			del self._queue[id]
		self._garbage = []

class Live_GameObject(types.KX_GameObject):
	def __init__(self, obj):
		self.logic_components = FunctionQueue(self)
		self.types = []

	def __del__(self):
		#remove the object from type lists
		scene = logic.getCurrentScene()
		for type_str in self.types:
			if self in scene['types'][type_str]:
				scene['types'][type_str].remove(self)
		#delete
		super().__del__()

	def run(self):
		"""Run the object's components"""
		self.logic_components._run()

	def set_type(self, type_str):
		"""Add a type to the object's .types list, and add it to a scene-wide list off object of the same type, stored in bge.logic.getCurrentScene()['types'][type_str]. Objects may have multiple types.

		:param string type_str: The name of the type to add to the object
		"""
		self.types += [type_str]
		scene = logic.getCurrentScene()
		if scene:
			if 'types' not in scene:
				scene['types'] = {}
				if type_str not in scene['types']:
					scene['types'][type_str] = set()
			scene['types'][type_str].add( self )

	def applyMovement(self, movement, *args, per_second=False):
		"""Sets the game object's movement

		:keyword boolean per_second: Whether or not the movement should be in blender units per second instead of per frame
		"""
		if per_second == True:
			movement = Vector(movement) / ( logic.getLogicTicRate() + 1 )
		else:
			raise TypeError
		super().applyMovement(movement, *args)

	def applyRotation(self, rotation, *args, per_second=False):
		"""Sets the game object's rotation

		:keyword per_second: if 'degrees' rotate in degrees per second. if 'radians' rotate in radians per second. If not set radians per frame
		"""
		if per_second == "radians" or per_second == "degrees" or per_second is True:
			rotation = Vector(rotation) / ( logic.getLogicTicRate() + 1 )
			if per_second == "degrees":
				rotation = [ radians(axis) for axis in rotation ]
		super().applyRotation(rotation, *args)

	def applyScale(self, scale, *args, per_second=False):
		"""Sets the game object's scale

		:keyword boolean per_second: Whether or not the scaling should be in blender units per second instead of per frame
		"""
		if per_second == True:
			scale = Vector(scale) / ( logic.getLogicTicRate() + 1 )
		if args[0] == True:
			self.localScale += Vector(scale)
		else:
			s = scale
			scale_matrix = Matrix([
				                   [s[0],   0,   0,   0],
				                   [   0,s[1],   0,   0],
				                   [   0,   0,s[2],   0],
				                   [   0,   0,   0,   1]  ])
			self.localTransform += scale_matrix * self.localOrientation.to_4x4()

def init():
	obj = logic.getCurrentController().owner
	Live_GameObject(obj)
def run():
	obj = logic.getCurrentController().owner
	obj.run()