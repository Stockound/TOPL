from el import *

def size(e):
    assert isinstance(e, Expr)
    if type(e) is BoolExpr:
        return 1
    if type(e) is NotExpr:
        return 1 + size(e.expr)
    if isinstance(e, BinaryExpr):
        return 1 + size(e.lhs) + size(e.rhs)
    assert False

def height(e):
    assert isinstance(e, Expr)
    if type(e) is BoolExpr:
        return 0
    if type(e) is NotExpr:
        return 1 + height(e.expr)
    if isinstance(e, BinaryExpr):
        return 1 + max(height(e.lhs), height(e.rhs))
    assert False

def same(e1, e2):
    assert isinstance(e1, Expr)
    assert isinstance(e2, Expr)
    if type(e1) == type(e2):
        if type(e1) is BoolExpr:
            return e1.value == e2.value
        if type(e1) is NotExpr:
            return same(e1.expr, e2.expr)
        if type(e1) is AndExpr:
            return same(e1.rhs, e2.rhs) and same(e1.lhs, e2.lhs)
        if type(e1) is OrExpr:
            return same(e1.rhs, e2.rhs) or same(e1.lhs, e2.lhs)
    else:
        return False

def value(e):
    assert isinstance(e, Expr)
    if type(e) is BoolExpr:
        return e.value
    if type(e) is NotExpr:
        return not value(e.expr)
    if type(e) is AndExpr:
        return value(e.lhs) and value(e.rhs)
    if type(e) is OrExpr:
        return value(e.lhs) or value(e.rhs)
    assert False

#a dumb way to do it I'm sure but it probably works
def step(e):
    assert isinstance(e, Expr)
    if type(e) is BoolExpr:
        return e
    if type(e) is NotExpr:
        if type(e.expr) is BoolExpr:
            return BoolExpr(not e.expr)
        else:
            return NotExpr(step(e.expr))
    if type(e) is AndExpr:
        if type(e.lhs) is BoolExpr and type(e.rhs) is BoolExpr:
            return BoolExpr(e.lhs.value and e.rhs.value) 
        elif type(e.lhs) is not BoolExpr:
            return AndExpr(step(e.lhs), e.rhs)
        else:
            return AndExpr(e.lhs, step(e.rhs))
    if type(e) is OrExpr:
        if type(e.lhs) is BoolExpr and type(e.rhs) is BoolExpr:
            return BoolExpr(e.lhs.value or e.rhs.value) 
        elif type(e.lhs) is not BoolExpr:
            return OrExpr(step(e.lhs), e.rhs)
        else:
            return OrExpr(e.lhs, step(e.rhs))
    assert False

#I wasn't sure if you wanted it to actually change the arguement or not so I made it
#not change it.
#I also wasn't sure if you wanted it to reduce to a bool expression or that bool
#expression's value so I made it reduce to the expression (this is not necessarily 
#an issue in reduce() but perhaps step()).
def reduce(e):
    assert isinstance(e, Expr)
    while e != step(e):
        e = step(e)
    return e
