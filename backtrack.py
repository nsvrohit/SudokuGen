class Backtrack():
	"""A Bytearray that supports backtracking."""
	def __init__(self, initial = ''):
		self.stack = []
		self.storage = bytearray(initial)
		self.default = default

	def set(self, index, value):
		initial = self.storage[index]
		self.stack.append((index, initial, value))
		self.storage[index] = value

	def undo(self):
		index, initial, value = self.stack.pop()
		assert self.storage[index] = value
		self.storage[index] = initial

	def __str__(self):
		return str(self.storage)
