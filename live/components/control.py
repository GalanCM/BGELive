from bge import logic, render

from math import radians

def _mouselook_core(self, id):
	deadzone = 0.001 # used to prevent floating when mouse isn't moving
	screen_x = 0.5 - logic.mouse.position[0]
	if -deadzone < screen_x < deadzone:
		screen_x = 0
	screen_y = 0.5 - logic.mouse.position[1]
	if -deadzone < screen_y < deadzone:
		screen_y = 0

	self.applyRotation([screen_y*sensitivity_x, 0, screen_x*sensitivity_y], True, per_second=True)

	render.setMousePosition(int(render.getWindowWidth() / 2), int(render.getWindowHeight() / 2))

def mouselook_6dof(self, id):
	_mouselook_core(self, id)


def mouselook_6dof_planar(self, id):
	euler = self.worldOrientation.to_euler()
	if euler.y > radians(30):
		euler.y = radians(30)
	elif euler.y < radians(-30):
		euler.y = radians(-30)
	elif euler.y < -0.01:
		euler.y += 0.002
	elif euler.y > 0.01:
		euler.y -= 0.002
	self.worldOrientation = euler.to_matrix()

	_mouselook_core(self, id)


def make_mouselook_fps():
	sensitivity_x = 30
	sensitivity_y = 40
	def mouselook_fps_callback(self, id):
		_mouselook_core(self,id)

		euler = self.worldOrientation.to_euler()
		euler.y = 0
		self.worldOrientation = euler.to_matrix()

	return mouselook_fps_callback
