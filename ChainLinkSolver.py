# Chain Link Solver (from Beyond Sudoku magazine)
# https://www.puzzler.com/puzzles-a-z/chain-link
#
# Adrian Dale
# 09/12/2017
from z3 import *

# The puzzle definition
# https://www.puzzler.com/FileDepository/Puzzles/Samples/Chainlink.pdf
regions = (
"aa---bbb",
"aaacb-bb",
"ddacccb-",
"d-acc--b",
"d-ac-c--",
"deeeee--",
"defee-ff",
"dd-fffff"
)

givens = (
(0,0,0,7,0,0,0,0),
(5,0,4,0,2,0,0,6),
(0,5,0,0,0,6,0,2),
(0,0,0,1,0,0,0,5),
(4,0,6,0,0,5,0,0),
(0,0,0,3,0,7,0,0),
(0,6,1,0,0,2,0,3),
(0,1,0,0,0,4,0,0)
)

# Assume puzzles is correctly set up with all rows having the same
# number of columns
nr = len(regions)
nc = len(regions[0])

# matrix of ints for our puzzle
X = [ [Int("x_%s_%s" % (i+1,j+1)) for j in range(nc)] for i in range(nr)]

s = Solver()

# Cell contains a digit from 1 .. puzzle size
s.add( [ And(X[i][j] >= 1, X[i][j] <= nr) for j in range(nc) for i in range(nr)] )

# Solution contains our given answers
s.add( [ If(givens[i][j] == 0, True, X[i][j] == givens[i][j]) for j in range(nc) for i in range(nr) ] )

# Each row must contain distinct digits
s.add( [ Distinct(X[i]) for i in range(nr)])

# Each column must contain distinct digits
s.add( [Distinct([X[i][j] for i in range(nr) ]) for j in range(nc)] )

# Each region contains distinct integers from 1..regionsize
region_dict = {}
for i in range(nr):
	for j in range(nc):
		region = regions[i][j]
		if region != '-':
			if region_dict.has_key(region):
				rde = region_dict[region]
				rde.append(X[i][j])
				region_dict[region] = rde
			else:
				region_dict[region] = [X[i][j]]

for region, region_cells in region_dict.items():
	s.add( Distinct(region_cells) )
	
if s.check() == sat:
	m = s.model()
	r = [ [ m.evaluate(X[i][j]) for j in range(nc) ]
		for i in range(nr) ]
	print_matrix(r)
else:
	print "Failed to solve puzzle"
