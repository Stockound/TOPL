from el import *
from operation import *

e1 = AndExpr(NotExpr(BoolExpr(True)), BoolExpr(False))
e2 = NotExpr(BoolExpr(False))

print(size(e1))
print(height(e1))
print(same(e1, e2))
print(value(e1))
print(e1)
print(step(e1))
print(reduce(e1))
