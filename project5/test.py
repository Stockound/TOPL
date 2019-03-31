from el import *
from operation import *
from evaluate import *

listTest = list()
listTest.append(BoolExpr(True))
listTest.append(BoolExpr(False))
dictTest = {"first":BoolExpr(False), "second":BoolExpr(False)}

table = [
  VariantExpr(BoolExpr(True), AndExpr(BoolExpr(True),BoolExpr(False)), OrExpr(BoolExpr(True),BoolExpr(False))),
  VariantExpr(BoolExpr(False), AndExpr(BoolExpr(True),BoolExpr(False)), OrExpr(BoolExpr(True),BoolExpr(False))),
  TupleExpr(listTest),
  RecordExpr(dictTest)
]

for e in table:
  print(e)
  print(evaluate(e))
