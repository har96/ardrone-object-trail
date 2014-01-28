from libardrone import libardrone

class Drone:
	def __init__(self, safe_offset):
		self.drone = libardrone.ARDrone()
		self.drone.set_speed(0.1)
		self.CAM_WIDTH = 640
		self.CAM_HEIGHT = 360
		self.CAM_CENTER = (320, 180)
		self.safe_offset = safe_offset
		self.prev_target = (0,0)
		self.state = "GROUNDED"

	def _get_center(self, rect):
		x, y w, h = rect
		return x + (w/2), y + (h/2)

	def launch(self):
		if self.state == "GROUNDED":
			self.drone.takeoff()
			self.state = "HOVER"

	def track_rect(self, rect):
		target = self._get_center(rect)

		if target[0] > (self.CAM_CENTER[0] + self.safe_offset):
			# target is to the right
			if self.state != "RIGHT":
				self.drone.turn_right()
				self.state = "RIGHT"
		elif target[0] < (self.CAM_CENTER[0] - self.safe_offset):
			# target is to the left
			if self.state != "LEFT":
				self.drone.turn_left()
				self.state = "LEFT"
		else:
			#target is dead on
			if self.state != "MOVING":
				self.drone.move_forward()
				self. state = "MOVING"

		self.prev_target = target

	def stop(self):
		if self.state != "HOVER":
			self.drone.hover()
			self.state = "HOVER"

	def done(self):
		if self.state != "GROUNDED":
			self.drone.hover()
			self.drone.land()
			self.state = "GROUNDED"

		self.drone.halt()
