class Expr:
    pass

#Bool Expression Language    
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

#Untyped Lambda Calculus Support
class IdExpr(Expr):
    def __init__(self, id):
        self.id = id
        self.ref = None
    def __str__(self):
        return self.id

class VarDecl:
    def __init__(self, id):
        self.id = id
    def __str__(self):
        return self.id

class AbsExpr(Expr):
    def __init__(self, var, e):
        if type(var) is str:
            self.var = VarDecl(var)
        else:
            self.var = var
        self.expr = e
    def __str__(self):
        return "\\" + str(self.var) + "." + str(self.expr)

class AppExpr(Expr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return "(" + str(self.lhs) + " " + str(self.rhs) + ")"

#Optional Fun; Poorly Done
#Pretty sure this is not what a call expression is
class CallExpr(Expr):
    def __init__(self, elist):
        self.elist = elist

#I'm also pretty confident this is wrong as well
#It's a lambda nested in a lambda for every arguement beyond the first
class MulitAbsExpr(AbsExpr):
    def __init__(self, e, var1, *args):
        abs = AbsExpr(var1, e)
        for var in args:
            abs = AbsExpr(var, abs)
        self = abs
    def __str__(self):
        return "\\" + str(self.var) + "." + str(self.expr)