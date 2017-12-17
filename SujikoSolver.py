# Sujiko Solver (from Beyond Sudoku magazine)
# https://www.puzzler.com/puzzles-a-z/sujiko
#
# Adrian Dale
# 17/12/2017
from z3 import *
import itertools

# The puzzle definition
# https://www.puzzler.com/FileDepository/Puzzles/Samples/Sujiko.pdf
sums = (10, 21, 18, 20)

givens = (
(0,0,0),
(0,0,0),
(8,0,7)
)

# Sujiko puzzles are always 3x3
nr = 3
nc = 3

# matrix of ints for our puzzle
X = [ [Int("x_%s_%s" % (i+1,j+1)) for j in range(nc)] for i in range(nr)]

s = Solver()

# Cell contains the piece (if any) given in the definition
s.add( [ If(givens[i][j] == 0, True, X[i][j] == givens[i][j]) for j in range(nc) for i in range(nr) ] )

# Cell contains integer between 1 and 9
s.add( [ And(X[i][j] >= 1, X[i][j] <= 9) for j in range(nc) for i in range(nr)] )

# Each digit is used exactly once
s.add( Distinct(list(itertools.chain(*X)) ) )

# The sums must add up
s.add( Sum(X[0][0], X[0][1], X[1][0], X[1][1]) == sums[0] )
s.add( Sum(X[0][1], X[0][2], X[1][1], X[1][2]) == sums[1] )
s.add( Sum(X[1][0], X[1][1], X[2][0], X[2][1]) == sums[2] )
s.add( Sum(X[1][1], X[1][2], X[2][1], X[2][2]) == sums[3] )

if s.check() == sat:
	m = s.model()
	r = [ [ m.evaluate(X[i][j]) for j in range(nc) ]
		for i in range(nr) ]
	print_matrix(r)
else:
	print "Failed to solve puzzle"
