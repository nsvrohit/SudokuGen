#!/usr/bin/env python

#
# Based upon Peter Norvig's Sudoku solver
#

def cross(xs, ys):
	return [x+y for x in xs for y in ys]

rows = 'ABCDEFGHI'
cols = '123456789'
cells = cross(rows, cols)
rules = ([cross(rows, c) for c in cols] + 
	 [cross(r, cols) for r in rows] +
	 [cross(r, c) for r in ('ABC','DEF','GHI')
		      for c in ('123','456','789')])


if __name__ == '__main__':
	for rule in rules:
		print rule
