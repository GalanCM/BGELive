from random import getrandbits
from functools import partial

from bge import logic, types, events
from mathutils import Vector, Matrix

from live.helpers import get_scene

from math import radians

class FunctionQueue():
	def __init__(self, owner, *args):
		self._queue = {}
		self._garbage = []
		self._owner = owner
		if (args):
			self.owner = args[0]

	def set(self, fun, *args, **kwargs):
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
		return self._queue[id][0].func

	def remove(self, id):
		self._garbage.append(id)

	def _run(self):
		for queue_item in self._queue.values():
			pause_states = get_scene().get('pause_states')
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
		scene = get_scene()
		for type_str in self.types:
			if self in scene['types'][type_str]:
				scene['types'][type_str].remove(self)
		super().__del__()

	def run(self):
		self.logic_components._run()

	def set_type(self, type_str):
		self.types += [type_str]
		scene = get_scene()
		if scene:
			if 'types' not in scene:
				scene['types'] = {}
				if type_str not in scene['types']:
					scene['types'][type_str] = set()
			scene['types'][type_str].add( self )

	def applyMovement(self, movement, *args, per_second=False):
		if per_second == True:
			movement = Vector(movement) / ( logic.getLogicTicRate() + 1 )
		else:
			raise TypeError
		super().applyMovement(movement, *args)

	def applyRotation(self, rotation, *args, per_second=False):
		if per_second == "radians" or per_second == "degrees" or per_second is True:
			rotation = Vector(rotation) / ( logic.getLogicTicRate() + 1 )
			if per_second == "degrees":
				rotation = [ radians(axis) for axis in rotation ]
		super().applyRotation(rotation, *args)

	def applyScale(self, scale, *args, per_second=False):
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