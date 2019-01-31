class Expr:
    pass
    
class BoolExpr(Expr):
    def __init__(self, val):
        assert val == True or val == False
        self.value = val
    def __str__(self):
        return "Bool(" + str(self.value) + ")"

class BinaryExpr(Expr):
    def __init__(self, e1, e2):
        assert isinstance(e1, Expr)
        assert isinstance(e2, Expr)
        self.lhs = e1
        self.rhs = e2

class NotExpr(Expr):
    def __init__(self, e):
        assert isinstance(e, Expr)
        self.expr = e
    def __str__(self):
        return "(not " + str(self.expr) + ")"

class AndExpr(BinaryExpr):
    def __str__(self):
        return "(" + str(self.lhs) + " and " + str(self.rhs) + ")"

class OrExpr(BinaryExpr):
    def __str__(self):
        return "(" + str(self.lhs) + " or " + str(self.rhs) + ")"
