from el import *
from operation import *
from evaluate import *

listTest = list()
listTest.append(BoolExpr(True))
listTest.append(BoolExpr(False))
dictTest = {"first":BoolExpr(False), "second":BoolExpr(False)}

table = [
  VariantExpr("something", {"not something":BoolExpr(True), "something":BoolExpr(False), "something else":BoolExpr(True)}),
  VariantExpr("something", {"not something":BoolExpr(False), "something":BoolExpr(True), "something else":BoolExpr(False)}),
  TupleExpr(listTest),
  RecordExpr(dictTest)
]

for e in table:
  print(e)
  print(evaluate(e))
