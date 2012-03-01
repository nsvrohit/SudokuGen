#!/usr/bin/env python

#
# Based upon Peter Norvig's Sudoku solver
#

def cross(xs, ys):
	return [x+y for x in xs for y in ys]

digits = '123456789'

rows = 'ABCDEFGHI'
cols = '123456789'
cells = cross(rows, cols)
rules = ([cross(rows, c) for c in cols] + 
	 [cross(r, cols) for r in rows] +
	 [cross(r, c) for r in ('ABC','DEF','GHI')
		      for c in ('123','456','789')])

groups = dict((c, [r for r in rules if c in r]) for c in cells)
connected = dict((c, set(sum(groups[c],[]))-set([c])) for c in cells)

def grid_values(grid):
	"Grid -> {cell : char}, where char is a digit, or empty (0 or .)"
	chars = [c for c in grid if c in digits or c in '0.']
	assert len(chars)==81
	return dict(zip(cells, chars))

def parse_grid(grid):
	"Converts a grid into a dictionary of cells to possible values."
	values = dict((c, digits) for c in cells)
	for c, d in grid_values(grid).items():
		if d in digits and not assign(values, s, d):
			# The grid contains a contradiction
			return False
	return values

def assign(values, c, d):
	"""Eliminate values other than d from values[c] and propagate.
	Return values, or False if a contradiction exists."""
	other_values = values[c].replace(d,'')
	if all(eliminate(values, c, d2) for d2 in other_values):
		return values
	else:
		return False

def eliminate(values, c, d):
	"""Eliminate d from values[c]; propagate when values or places <= 2.
	Return values, or False if a contradiction exists."""
	if d not in values[c]:
		return values # Already eliminated
	values[c] = values[c].replace(d, '')
	
	if len(values[c]) == 0:
		return False

	# 1) If a cell c is reduced to a single value, d2, then eliminate from connected cells
	elif len(values[c]) == 1:
		d2 = values[c]
		if not all(eliminate(values, c2, d2) for c2 in connected[c]):
			return False

	# 2) If a group is reduced to only one place for a value d, then place it there
	for g in groups[c]:
		dplaces = [c for c in g if d in values[c]]
		if len(dplaces) == 0:
			# No place for this value
			return False
		elif len(dplaces) == 1:
			# Can only be in one cell
			if not assign(values, dplaces[0], d):
				return False
	return values

if __name__ == '__main__':
	for rule in rules:
		print rule
