#!/usr/bin/env python

#
# Based upon Peter Norvig's Sudoku solver
#

import time
import random

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

def display(values):
	"Display the values in a grid"
	width = 1 + max(len(values[c]) for c in cells)
	line = '+'.join(['-'*(width*3)]*3)
	for r in rows:
		print ''.join(values[r+c].center(width) + 
				('|' if c in '36' else '')
				for c in cols)
		if r in 'CF':
			print line
	print

def some(seq):
	"Return some element of seq that is true."
	for e in seq:
		if e:
			return e
	return False

def search(values):
	"Using depth-first search and propagation, try all possible values."
	if values is False:
		return False
	if all(len(values[c]) == 1 for c in cells):
		return Values

	# Choose unfilled cell c with the fewest possibilities
	n, c = min((len(values[c]), c) for c in squares if len(values[c]) > 1)

	return some(search(assign(values.copy(), s, d)) for d in values[c])


def solve(grid):
	return search(parse_grid(grid))

def solve_all(grids, name='', showif=0.0):
	"""Attempt to solve a sequence of grids. Report results.
	When showif is a number of seconds, display puzzles that take longer.
	When showif is None, don't display any puzzles."""
	def time_solve(grid):
		start = time.clock()
		values = solve(grid)
		t = time.clock() - start

		if showif is not None and t > showif:
			display(grid_values(grid))
			if values:
				display(values)
			print '(%.2f seconds)\n' % t
		return (t, solved(values))
	times, results = zip(*[time_solve(grid) for grid in grids])
	N = len(grids)
	if N > 1:
		print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values):
	"A puzzle is solved if each unit is a permutation of the digits 1 to 9."
	def group_solved(group):
		return set(values[c] for c in group) == set(digits)
	return values is not False and all(group_solved(group) for group in groups)

def from_file(filename, sep='\n'):
	"Parse a file into a list of strings, separated by sep."
	return file(filename).read().strip().split(sep)

def shuffled(seq):
	"Return a randomly shuffled copy of the input sequence."
	seq = list(seq)
	random.shuffle(seq)
	return seq

def random_puzzle(N=17):
	"""Make a random puzzle with N or more assignments. Restart on contradictions. Note the resulting puzzle is not guaranteed to be solvable, but empirically about 99.8% of them are. Some have multiple solutions."""
	values = dict((c, digits) for c in cells)
	for c in shuffled(cells):
		if not assign(values, c, random.choice(values[c])):
			break
		ds = [values[c] for c in cells if len(values[c]) == 1]
		if len(ds) >= N and len(set(ds)) >= 8:
			return ''.join(values[c] if len(values[c]) == 1 else '.' for c in cells)
	return random_puzzle(N) # Give up, try again

if __name__ == '__main__':
	test()
	solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
