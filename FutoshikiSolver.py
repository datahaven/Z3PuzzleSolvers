# Futoshiki Solver (from Beyond Sudoku magazine)
# https://www.puzzler.com/puzzles-a-z/futoshiki
#
# Adrian Dale
# 09/12/2017
from z3 import *

# The puzzle definition
# https://www.puzzler.com/FileDepository/Puzzles/Samples/Futoshiki.pdf

givens = (
(0,4,0,0),
(0,0,0,0),
(0,0,3,0),
(1,0,0,0)
)

# Assume puzzles is correctly set up with all rows having the same
# number of columns
nr = len(givens)
nc = len(givens[0])

# matrix of ints for our puzzle
X = [ [Int("x_%s_%s" % (i+1,j+1)) for j in range(nc)] for i in range(nr)]

s = Solver()

# The puzzle rules - it's easier to simply write these in code, than
# to come up with a scheme for specifying them in data.
# Which, of course, is what I ought to do!
s.add(X[0][3] > X[1][3])
s.add(X[2][1] > X[1][1])
s.add(X[2][2] > X[2][3])

# Cell contains a digit from 1 .. puzzle size
s.add( [ And(X[i][j] >= 1, X[i][j] <= nr) for j in range(nc) for i in range(nr)] )

# Solution contains our given answers
s.add( [ If(givens[i][j] == 0, True, X[i][j] == givens[i][j]) for j in range(nc) for i in range(nr) ] )

# Each row must contain distinct digits
s.add( [ Distinct(X[i]) for i in range(nr)])

# Each column must contain distinct digits
s.add( [Distinct([X[i][j] for i in range(nr) ]) for j in range(nc)] )

if s.check() == sat:
	m = s.model()
	r = [ [ m.evaluate(X[i][j]) for j in range(nc) ]
		for i in range(nr) ]
	print_matrix(r)
else:
	print "Failed to solve puzzle"
