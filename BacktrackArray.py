#!/usr/bin/env python

class BacktrackArray():
	"""A Bytearray that supports backtracking."""
	def __init__(self, initial = ''):
		self.stack = []
		self.storage = bytearray(initial)

	def set(self, index, value):
		initial = self.storage[index]
		self.stack.append((index, initial, value))
		self.storage[index] = value

	def undo(self):
		index, initial, value = self.stack.pop()
		assert chr(self.storage[index]) == value
		self.storage[index] = initial

	def __str__(self):
		return str(self.storage)

if __name__ == '__main__':
	print "Testing Backtrack Array..."
	init = "initial contents"
	ba = BacktrackArray(init)
	assert init == str(ba)
	ba.set(0, "z")
	changed = 'z' + init[1:]
	assert changed == str(ba)
	ba.undo()
	assert init == str(ba)
	print "Tests passed."

