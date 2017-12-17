# Suguru Solver (from Beyond Sudoku magazine)
# https://www.puzzler.com/puzzles-a-z/suguru
#
# Adrian Dale
# 09/12/2017
from z3 import *

# The puzzle definition
regions = (
"abbbbc",
"dbeccc",
"deeefc",
"dgehff",
"dghhhf",
"ggghii"
)

givens = (
(0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,3,0,0,4,0),
(0,2,0,0,0,0),
(0,5,0,5,0,0),
(0,0,0,0,0,0)
)

# Assume puzzles is correctly set up with all rows having the same
# number of columns
nr = len(regions)
nc = len(regions[0])

# matrix of ints for our puzzle
X = [ [Int("x_%s_%s" % (i+1,j+1)) for j in range(nc)] for i in range(nr)]

s = Solver()

# Cell contains the piece (if any) given in the definition
s.add( [ If(givens[i][j] == 0, True, X[i][j] == givens[i][j]) for j in range(nc) for i in range(nr) ] )

# Cell contains integer greater than 0
s.add( [ X[i][j] > 0 for j in range(nc) for i in range(nr)] )

# Each region contains distinct integers from 1..regionsize
region_dict = {}
for i in range(nr):
	for j in range(nc):
		region = regions[i][j]
		if region_dict.has_key(region):
			rde = region_dict[region]
			rde.append(X[i][j])
			region_dict[region] = rde
		else:
			region_dict[region] = [X[i][j]]

for region, region_cells in region_dict.items():
	region_sum = len(region_cells)*(len(region_cells)+1) / 2
	region_rule = And( Distinct(region_cells), Sum(region_cells) == region_sum )
	s.add(region_rule)

# No same digit appears in neighbouring cells, not even diagonally
dx = [0,1,1,1,0,-1,-1,-1]
dy = [-1,-1,0,1,1,1,0,-1]
for i in range(nr):
	for j in range(nc):
		for d in range(len(dx)):
			neighbour_r = i+dy[d]
			neighbour_c = j+dx[d]
			if neighbour_r >= 0 and neighbour_r < nr and neighbour_c >= 0 and neighbour_c < nc:
				region_size = len(region_dict[regions[i][j]])
				for rd in range(region_size):
					s.add(Implies(X[i][j] == rd+1, X[neighbour_r][neighbour_c] != rd+1))

if s.check() == sat:
	m = s.model()
	r = [ [ m.evaluate(X[i][j]) for j in range(nc) ]
		for i in range(nr) ]
	print_matrix(r)
else:
	print "Failed to solve puzzle"
