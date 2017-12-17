# Stars Solver (from Beyond Sudoku magazine)
# https://www.puzzler.com/puzzles-a-z/stars
#
# Adrian Dale
# 08/12/2017
from z3 import *

# The puzzle definition
regions = (
"aabbaccdd",
"abbbacccd",
"aaaaaeeed",
"aaffffeed",
"afffddedd",
"gggfddddh",
"gffffdiih",
"gfgfddihh",
"gggfffihh"
)

# Assume regions is correctly set up with all rows having the same
# number of columns
puzRows = len(regions)
puzCols = len(regions[0])

# matrix of ints for our puzzle
X = [ [Int("x_%s_%s" % (i+1,j+1)) for j in range(puzCols)] for i in range(puzRows)]

s = Solver()

# Cell contains either 0 for empty, or 1 for a star
cells_c = [ Or(X[i][j] == 0, X[i][j] == 1) for j in range(puzCols) for i in range(puzRows)]
s.add(cells_c)

# Each row contains exactly two stars
row_count_rule = And( [Sum([X[i][j] for j in range(puzCols)]) == 2 for i in range(puzRows)])
s.add(row_count_rule)

# Each column contains exactly two stars
col_count_rule = And( [Sum([X[i][j] for i in range(puzRows)]) == 2 for j in range(puzCols)])
s.add(col_count_rule)

# Each region contains exactly two stars
region_dict = {}
for i in range(puzRows):
	for j in range(puzCols):
		region = regions[i][j]
		if region_dict.has_key(region):
			rde = region_dict[region]
			rde.append(X[i][j])
			region_dict[region] = rde
		else:
			region_dict[region] = [X[i][j]]

for region, region_cells in region_dict.items():
	region_rule = Sum(region_cells) == 2
	s.add(region_rule)

# Star cells cannot touch, even diagonally
# ie If cell is occupied then that implies that neighbours are not occupied
dx = [0,1,1,1,0,-1,-1,-1]
dy = [-1,-1,0,1,1,1,0,-1]
for i in range(puzRows):
	for j in range(puzCols):
		for d in range(8):
			nr = i+dy[d]
			nc = j+dx[d]
			if nr >= 0 and nr < puzRows and nc >= 0 and nc < puzCols:
				s.add(Implies(X[i][j] == 1, X[nr][nc] == 0))

if s.check() == sat:
	m = s.model()
	r = [ [ m.evaluate(X[i][j]) for j in range(puzCols) ]
		for i in range(puzRows) ]
	print_matrix(r)
else:
	print "Failed to solve puzzle"
