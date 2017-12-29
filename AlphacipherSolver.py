# Alphacipher Solver (from puzzler.com)
# https://www.puzzler.com/puzzles-a-z/alphacipher
#
# Adrian Dale
# 29/12/2017
from z3 import *

# The puzzle definition
# https://www.puzzler.com/FileDepository/Puzzles/Samples/Alphacipher.pdf

givens = (
("ANGELOU", 45),
("ATWOOD", 55),
("BALZAC", 59),
("BRAINE", 47),
("CONRAD", 59),
("EVELYN", 63),
("FORESTER", 58),
("GASKELL", 47),
("GOGOL", 41),
("HAMSUN", 53),
("HELLER", 35),
("JEROME", 53),
("KAFKA", 74),
("LESSING", 45),
("NESBIT", 45),
("PARKER", 58),
("POTTER", 47),
("PROUST", 42),
("QUENEAU", 56),
("RANSOME", 45),
("RENAULT", 40),
("SALINGER", 55),
("SHUTE", 37),
("SYMONS", 50),
("WALTON", 49)
)

# Variables A-Z for our puzzle
X = [Int("x_%s" % i) for i in range(26)]

s = Solver()

# Each letter must contain a distinct value
s.add( Distinct(X) )

# Letter values should add up to 351 (sum of 1 to 26)
s.add( Sum(X) == 351)

# Letters should have a value from 1 to 26
s.add( [ And(X[i] >= 1, X[i] <= 26) for i in range(26) ] )

# Our clue sums should add up
for clue,clueSum in givens:
	sumVars = []
	for v in clue:
		varIndex = ord(v) - ord('A')
		sumVars.append(X[varIndex])
	s.add( Sum(sumVars) == clueSum )

if s.check() == sat:
	m = s.model()
	r = [ m.evaluate(X[i]) for i in range(26) ]
	for i in range(26):
		print chr(i+ord('A')), "=", r[i]
else:
	print "Failed to solve puzzle"
