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
connected_cells = dict((c, set(sum(groups[c],[]))-set([c])) for c in cells)

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

if __name__ == '__main__':
	for rule in rules:
		print rule
