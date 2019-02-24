from el import *
from operation import *

""" e1 = AndExpr(NotExpr(BoolExpr(True)), BoolExpr(False))
e2 = NotExpr(BoolExpr(False))

print(size(e1))
print(height(e1))
print(same(e1, e2))
print(value(e1))
print(e1)
print(step(e1))
print(reduce(e1)) """

# \x.x
id = AbsExpr("x", IdExpr("x"))

# true = \a.\b.a
t = AbsExpr("a", AbsExpr("b", IdExpr("a")))

# false = \a.\b.b
f = AbsExpr("a", AbsExpr("b", IdExpr("b")))

# and = 
land = \
  AbsExpr("p", 
    AbsExpr("q", 
      AppExpr(
        AppExpr(
          IdExpr("p"), 
          IdExpr("q")),
        IdExpr("p"))))

e1 = AppExpr(AppExpr(land, t), f)

print(t)
print(f)
print(land)
e = e1
reduce(e)
