# Border Sum Sudoku Solver
# (Adapted from the Sudoku Solver example code)
# Adrian Dale
# 17/12/2017
from z3 import *

# Example puzzle:
# https://www.puzzler.com/FileDepository/Puzzles/Samples/BorderSumSudoku.pdf

# sudoku instance, we use '0' for empty cells
instance = (
(0,0,0,0,0,0,0,0,0),
(0,0,3,0,0,0,0,0,0),
(0,2,0,1,0,0,0,0,0),
(0,0,6,0,0,1,0,0,0),
(0,0,0,0,0,0,0,0,0),
(0,0,0,4,0,0,5,0,0),
(0,0,0,0,0,7,0,5,0),
(0,0,0,0,0,0,3,0,0),
(0,0,0,0,0,0,0,0,0))

TopRowSums = [22,9,14,10,19,16,19,11,15]
BottomRowSums = [17,20,8,22,6,17,8,21,16]
LeftColSums = [22,9,14,13,14,18,16,17,12]
RightColSums = [14,13,18,24,12,9,11,18,16]

# 9x9 matrix of integer variables
X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(9) ] 
      for i in range(9) ]

# each cell contains a value in {1, ..., 9}
cells_c  = [ And(1 <= X[i][j], X[i][j] <= 9) 
             for i in range(9) for j in range(9) ]

# each row contains a digit at most once
rows_c   = [ Distinct(X[i]) for i in range(9) ]

# each column contains a digit at most once
cols_c   = [ Distinct([ X[i][j] for i in range(9) ]) 
             for j in range(9) ]

# each 3x3 square contains a digit at most once
sq_c     = [ Distinct([ X[3*i0 + i][3*j0 + j] 
                        for i in range(3) for j in range(3) ]) 
             for i0 in range(3) for j0 in range(3) ]

# The extra border sum rules
sum_rules = []
for i in range(9):
	sum_rules.append(Sum(X[i][0], X[i][1], X[i][2]) == LeftColSums[i])
	sum_rules.append(Sum(X[i][6], X[i][7], X[i][8]) == RightColSums[i])
	sum_rules.append(Sum(X[0][i], X[1][i], X[2][i]) == TopRowSums[i])
	sum_rules.append(Sum(X[6][i], X[7][i], X[8][i]) == BottomRowSums[i])

sudoku_c = cells_c + rows_c + cols_c + sq_c + sum_rules

# Add in the given cells
instance_c = [ If(instance[i][j] == 0, 
                  True, 
                  X[i][j] == instance[i][j]) 
               for i in range(9) for j in range(9) ]

s = Solver()
s.add(sudoku_c + instance_c)
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ] 
          for i in range(9) ]
    print_matrix(r)
else:
    print "failed to solve"