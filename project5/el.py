#types
class Type:
    pass

class BoolType(Type):
    def __str__(self):
        return "bool"

class IntType(Type):
    def __str__(self):
        return "int"

boolType = BoolType()
intType = IntType()


class ArrowType(Type):
    def __init__(self, t1, t2):
        self.parm = t1
        self.ret = t2
    def __str__(self):
        return f"({self.lhs} -> {self.rhs})"

class FnType(Type):
    def __init__(self, parms, ret):
        self.parms = parms
        self.ret = ret

#records and tuples are 2 different types as they prob shouldnt be considered equavalent
class tupleType(Type):
    def __init__(self, vars):
        self.vars = vars

class recordType(Type):
    def __init__(self, vars):
        self.vars = vars

class Expr:
    pass

#Bool Expressions    
class BoolExpr(Expr):
    def __init__(self, val):
        assert val == True or val == False
        self.value = val
    def __str__(self):
        return str(self.value)

class BinaryExpr(Expr):
    def __init__(self, e1, e2):
        self.lhs = expr(e1)
        self.rhs = expr(e2)

class NotExpr(Expr):
    def __init__(self, e):
        self.expr = expr(e)
    def __str__(self):
        return "(not " + str(self.expr) + ")"

class AndExpr(BinaryExpr):
    def __str__(self):
        return "(" + str(self.lhs) + " and " + str(self.rhs) + ")"

class OrExpr(BinaryExpr):
    def __str__(self):
        return "(" + str(self.lhs) + " or " + str(self.rhs) + ")"

class IfExpr(Expr):
    def __init__(self, eif, eth, eel):
        self.eIf = expr(eif)
        self.eTh = expr(eth)
        self.eEl = expr(eel)
    def __str__(self):
        return "if (" + str(self.eIf) + ") then " + str(self.eTh) + " Else " + str(self.eEl)

#Bool Comparison Expressions

class LtExpr(Expr):
    def __init__(self, op1, op2):
        self.lhs = op1
        self.rhs = op2
    def __str__(self):
        return "(" + str(self.lhs) + " < " + str(self.rhs) + ")"

class GtExpr(Expr):
    def __init__(self, op1, op2):
        self.lhs = op1
        self.rhs = op2
    def __str__(self):
        return "(" + str(self.lhs) + " > " + str(self.rhs) + ")"

class LeExpr(Expr):
    def __init__(self, op1, op2):
        self.lhs = op1
        self.rhs = op2
    def __str__(self):
        return "(" + str(self.lhs) + " =< " + str(self.rhs) + ")"

class GeExpr(Expr):
    def __init__(self, op1, op2):
        self.lhs = op1
        self.rhs = op2
    def __str__(self):
        return "(" + str(self.lhs) + " => " + str(self.rhs) + ")"

#Numeric Expressions
class NumExpr(Expr):
    pass

class AddExpr(NumExpr):
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def __str__(self):
        return "(" + str(self.op1) + " + " + str(self.op2) + ")" 

class SubExpr(NumExpr):
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def __str__(self):
        return "(" + str(self.op1) + " - " + str(self.op2) + ")"

class MulExpr(NumExpr):
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def __str__(self):
        return "(" + str(self.op1) + " * " + str(self.op2) + ")"

class DivExpr(NumExpr):
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def __str__(self):
        return "(" + str(self.op1) + " / " + str(self.op2) + ")"

class ModExpr(NumExpr):
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def __str__(self):
        return "(" + str(self.op1) + " % " + str(self.op2) + ")"

class NegExpr(NumExpr):
    def __init__(self, op):
        self.op1 = op
    def __str__(self):
        return "-" + str(self.op1)

#tuples, records, and variants
#didnt know if you wanted them to accept a list of arguements or the arguements 
#as seperate parameters so heres both
#TODO: eval for tuple and Record
class TupleExpr(Expr):
#    def __init__(self, *args):
#        self.vars = list(args)
    def __init__(self, args):
        self.vars = args
    def __str__(self):
        varString = ",".join(str(v) for v in self.vars)
        return f"({varString})"

class RecordExpr(Expr):
#    def __init__(self, **kwargs):
#        self.vars = list(kwargs)
    def __init__(self, args):
        self.vars = args
    def __str__(self):
        varString = ",".join(str("{"+ str(key) + "=" + str(value) +"}") for key, value in (v.items() for v in self.vars))
        return f"({varString})"

#TODO: figure out how i wanna make variants work
class VariantExpr(Expr):
    def __init__(self):
        pass

#Lambda Calculus Support
class IdExpr(Expr):
    def __init__(self, id):
        self.id = id
        self.ref = None
    def __str__(self):
        return self.id

class VarDecl:
    def __init__(self, id, t):
        self.id = id
        self.type = t
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

#Copied from you as mine were wrong
class LambdaExpr(Expr):
    # Represents multi-argument lambda abstractions.
    # Note that '\(x, y, z).e' is syntactic sugar for
    # '\x.\y.\z.e'.
    def __init__(self, vars, e1):
        self.vars = list(map(decl, vars))
        self.expr = expr(e1)

    def __str__(self):
        parms = ",".join(str(v) for v in self.vars)
        return f"\\({parms}).{self.expr}"

class CallExpr(Expr):
    # Represents calls of multi-argument lambda 
    # abstractions.
    def __init__(self, fn, args):
        self.fn = expr(fn)
        self.args = list(map(expr, args))

    def __str__(self):
        args = ",".join(str(a) for a in self.args)
        return f"{self.fn} ({args})"

def expr(x):
    # Turn a Python object into an expression. This is solely
    # used to make simplify the writing expressions.
    if type(x) is bool:
        return BoolExpr(x)
    if type(x) is str:
        return IdExpr(x)
    return x

def decl(x):
    # Turn a python object into a declaration.
    if type(x) is str:
        return VarDecl(x)
    return x

