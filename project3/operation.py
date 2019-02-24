from el import *

def is_value(e):
    assert isinstance(e, Expr)
    return type(e) in (BoolExpr, IdExpr, AbsExpr)

#like much of this program, a better idea shamelessly stolen
def is_reducible(e):
    assert isinstance(e, Expr)
    return not is_value(e)

def size(e):
    assert isinstance(e, Expr)
    if not is_reducible(e):
        return 1
    if type(e) is NotExpr:
        return 1 + size(e.expr)
    if isinstance(e, BinaryExpr):
        return 1 + size(e.lhs) + size(e.rhs)
    assert False

def height(e):
    assert isinstance(e, Expr)
    if not is_reducible(e):
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
        elif type(e1) is NotExpr:
            return same(e1.expr, e2.expr)
        elif type(e1) is AndExpr:
            return same(e1.rhs, e2.rhs) and same(e1.lhs, e2.lhs)
        elif type(e1) is OrExpr:
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

def substitute(e, sub): #sub is {lambda.var: value}, want to replace var in e with value
    if type(e) is IdExpr:
        #I'm not smart enough to figure out what the issue was with yours
        #so 99.99% chance this doesn't fix it
        [(var, value)] = sub.items() 
        #try to check if this id refers to var and can be replaced with value
        #cannot happen until names are resolved otherwise ref = None
        #or if resolved at incorrect time the scope may be inaccurate
        if e.ref is var: 
            return value
        else:
            return e
    if type(e) is AbsExpr:
        return AbsExpr(e.var, substitute(e.expr, sub))
    if type(e) is AppExpr:
        return AppExpr(substitute(e.lhs, sub), substitute(e.rhs, sub))
    assert False

def resolve(e, scope = []):
    if type(e) is AppExpr:
        resolve(e.lhs, scope)
        resolve(e.rhs, scope)
        return
    if type(e) is AbsExpr:
        resolve(e.expr, scope + [e.var])
        return
    if type(e) is IdExpr:
        for var in reversed(scope):
        #in the case of two variables with the same name the
        #lower scoped one should take precedence
            if e.id == var.id:
                e.ref = var
                return
        raise Exception("name lookup error")
    assert False

#still dumb, still might work, even less readable
def step(e):
    assert isinstance(e, Expr)
    if not is_reducible(e):
        return e
    elif type(e) is NotExpr:
        if type(e.expr) is BoolExpr:
            return BoolExpr(not e.expr)
        else:
            return NotExpr(step(e.expr))
    elif type(e) is AndExpr:
        if type(e.lhs) is BoolExpr and type(e.rhs) is BoolExpr:
            return BoolExpr(e.lhs.value and e.rhs.value) 
        elif type(e.lhs) is not BoolExpr:
            return AndExpr(step(e.lhs), e.rhs)
        else:
            return AndExpr(e.lhs, step(e.rhs))
    elif type(e) is OrExpr:
        if type(e.lhs) is BoolExpr and type(e.rhs) is BoolExpr:
            return BoolExpr(e.lhs.value or e.rhs.value) 
        elif type(e.lhs) is not BoolExpr:
            return OrExpr(step(e.lhs), e.rhs)
        else:
            return OrExpr(e.lhs, step(e.rhs))
    elif type(e) is AppExpr:
        if is_reducible(e.lhs):
            return AppExpr(step(e.lhs), e.rhs)
        if type(e.lhs) is not AbsExpr:
            raise Exception("attempted to apply non-lambda")
        if is_reducible(e.rhs):
            return AppExpr(e.lhs, step(e.rhs))
        #lhs is a lambda, rhs is non-reducible
        sub = {e.lhs.var: e.rhs}
        return substitute(e.lhs.expr, sub)
    #no idea if this is what call expresisons are supposed to be or do
    elif type(e) is CallExpr: 
        for expr in e.elist:
            if is_reducible(expr):
                expr = step(expr)
                return CallExpr(e.elist)
        return value(e)
    assert False

def reduce(e):
    assert isinstance(e, Expr)
    if type(e) is AppExpr: #not necessarily the correct place to resolve but the best I can see
        resolve(e)
    while is_reducible(e):
        e = step(e)
        print(e)
    return e
