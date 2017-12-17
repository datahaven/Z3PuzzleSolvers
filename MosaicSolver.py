# Mosaic Solver (from Beyond Sudoku magazine)
# https://www.puzzler.com/puzzles-a-z/mosaic
#
# Adrian Dale
# 09/12/2017
from z3 import *

# The puzzle definition
# https://www.puzzler.com/FileDepository/Puzzles/Samples/Mosaic.pdf
mosaic = (
"2-3-3-3-4554--0",
"---3-4-4-------",
"1-21223222--43-",
"--3-3-3-0----4-",
"------3----57--",
"5--7-6---2-----",
"--5-7553----541",
"5--7-7-----7---",
"--7--89--9--96-",
"5-7-8-7-9---87-",
"4---6---66---75",
"--6--56--------",
"-87--7-5-588--4",
"-87-----4-8-5-2",
"----3-5--------"
)

# Assume puzzles is correctly set up with all rows having the same
# number of columns
nr = len(mosaic)
nc = len(mosaic[0])

# matrix of ints for our puzzle
X = [ [Int("x_%s_%s" % (i+1,j+1)) for j in range(nc)] for i in range(nr)]

s = Solver()

# Cell contains either 0 for empty, or 1 for filled
s.add( [ Or(X[i][j] == 0, X[i][j] == 1) for j in range(nc) for i in range(nr)] )

# For each given cell, the sum of that cell's contents (0 or 1) plus its neighbours
# must add up to the given number
dx = [0,1,1,1,0,-1,-1,-1]
dy = [-1,-1,0,1,1,1,0,-1]
for i in range(nr):
	for j in range(nc):
		given_value = mosaic[i][j]
		if given_value != '-':
			given_value = ord(given_value) - ord('0')
			cellRefs = [X[i][j]]
			for d in range(len(dx)):
				neighbour_r = i+dy[d]
				neighbour_c = j+dx[d]
				if neighbour_r >= 0 and neighbour_r < nr and neighbour_c >= 0 and neighbour_c < nc:
					cellRefs.append(X[neighbour_r][neighbour_c])
			s.add(Sum(cellRefs) == given_value)

if s.check() == sat:
	m = s.model()
	r = [ [ m.evaluate(X[i][j]) for j in range(nc) ]
		for i in range(nr) ]
	print_matrix(r)
else:
	print "Failed to solve puzzle"
