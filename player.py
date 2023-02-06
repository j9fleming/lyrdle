import time

class Player:
	def __init__(self,name):
		self.name = name
		self.start_time = None
		self.elapsed_time = None
		self.answer = None

	def start(self):
		if self.start_time is not None:
			print("Timer is already running.")
		else:
			self.start_time = float(time.perf_counter())
	
	def stop(self):
		if self.start_time is None:
			print("Time hasn't started already.")
		else:
			#print(type(self.start_time))
			#print(type(time.perf_counter()))
			self.elapsed_time = time.perf_counter() - self.start_time

	def reset(self):
		self.start_time = None
		self.elapsed_time = None

	def change_answer(self, guess):
		self.answer = guess

	def compare_times(self, p2):
		if self.elapsed_time < p2.elapsed_time:
			return True
		return False

	def __str__(self):
		tostring = f"Name: {self.name}, Time: {self.elapsed_time:.3f} seconds"
		return tostring









